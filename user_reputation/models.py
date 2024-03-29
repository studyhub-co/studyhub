from django.db import models
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ReputationManager(models.Manager):
    """
    Custom manager for the "Reputation" model.
    Methods defined here provide shortcuts for modifying and tracking the
    reputation of users.
    """

    def user_reputation(self, user):
        try:
            reputation_object = user.reputation_set.get()
        except ObjectDoesNotExist:
            reputation_object = Reputation(user=user)
            reputation_object.save()
        return reputation_object

    def update_reputation(self, dimension, user, value):
        """
        Updates an "User"s associated "Reputation" object by adding value to
        the user's current reputation.
        if value == 0, then nothing is done.
        """
        if value:
            reputation = self.reputation_for_user(dimension, user)
            reputation.reputation = value
            reputation.save()

    def add_reputation_action(self, user, action_value, target_object, callback=None):
        content_type_object = ContentType.objects.get_for_model(
            target_object.__class__
        )
        object_id = target_object.pk

        try:
            ReputationAction.objects.get(
                user=user,
                content_type=content_type_object,
                object_id=object_id)
        except ReputationAction.MultipleObjectsReturned:
            last = ReputationAction.objects.filter(
                user=user,
                content_type=content_type_object,
                object_id=object_id
            ).last()
            ReputationAction.objects.exclude(pk=last.pk).delete()
        except ReputationAction.DoesNotExist:
            reputation_action = ReputationAction(
                user=user,
                content_type=content_type_object,
                object_id=object_id,
                value=action_value
            )
            reputation_action.save()

            # send notification
            if callback:
                callback(user, action_value, target_object)


class Reputation(TimeStampedModel):
    """
    Model for storing a "User" object's reputation in an IntegerField.
    """
    reputation = models.IntegerField(default=0)
    user = models.ForeignKey(get_user_model(), related_name='reputation_set', on_delete=models.CASCADE)
    dimension = models.CharField(max_length=2, blank=True, null=True)

    objects = ReputationManager()

    def __str__(self):
        return "%s - %s".format(self.user.username, self.reputation)


class ReputationAction(TimeStampedModel):
    """
    Model representing an action a user takes that effects the user's
    reputation.
    """

    user = models.ForeignKey(get_user_model(), related_name='reputation_actions', on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # TODO make it UUID id independent see notifications/models.py for details
    # old_object_id = models.PositiveIntegerField()
    object_id = models.UUIDField(verbose_name=_("object ID"), db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    value = models.IntegerField(default=0)

    def __unicode__(self):
        return u"%s - %d" % (self.user.username, self.value)


@receiver(models.signals.post_save, sender=ReputationAction)
def recalculate_user_reputation(sender, instance, *args, **kwargs):
    """ recalculate user's reputation """
    reputation = Reputation.objects.user_reputation(instance.user)
    # TODO calculate
    reputation.reputation = 20
    reputation.save()
