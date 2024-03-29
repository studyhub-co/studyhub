from rest_framework import serializers

from django.contrib.auth import get_user_model

# from curricula.models import Lesson as LessonC, Module as ModuleC
# from curricula.serializers import LessonSerializer as LessonSerializerC, ModuleSerializer as ModuleSerializerC
# from curricula.services import get_progress_service as get_progress_serviceC

from courses.models import Lesson, Module
from courses.serializers import LessonSerializer, ModuleSerializer
from courses.services import get_progress_service


# from djeddit.models import Thread, Post
from react_comments_django.models import Thread, Post
from profiles.serializers import PublicProfileSerializer
from badges.models import Badge
from badges.serializers import BadgeSerializer

from .models import Notification


class MiniThreadSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        # not so good link
        return "/beta/discussion{}".format(obj.get_absolute_url())

    class Meta:
        fields = ('title', 'url')
        model = Thread


class MiniPostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('uid',)
        model = Post


class BaseObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Post):
            data = MiniPostSerializer(value).data
            data['content_type'] = 'post'
            return data
        if isinstance(value, Thread):
            data = MiniThreadSerializer(value).data
            data['content_type'] = 'thread'
            return data
        if isinstance(value, Badge):
            data = BadgeSerializer(value).data
            data['content_type'] = 'badge'
            return data
        if isinstance(value, Lesson):
            data = LessonSerializer(value).data
            data['content_type'] = 'lesson'
            return data
        if isinstance(value, Module):
            progress_service = get_progress_service(self.context['request'])
            data = ModuleSerializer(value, context={'progress_service': progress_service}).data
            data['content_type'] = 'module'
            return data
        if isinstance(value, get_user_model()):
            data = PublicProfileSerializer(value.profile).data
            data['content_type'] = 'profile'
            return data
        raise Exception('Unexpected type of target object: {}'.format(type(value)))


class NotificationActorRelatedField(BaseObjectRelatedField):
    """
    A custom field to use for the `actor` generic relationship.
    """

    pass


class NotificationActionObjectRelatedField(BaseObjectRelatedField):
    """
    A custom field to use for the `actor` generic relationship.
    """
    pass


class NotificationTargetRelatedField(BaseObjectRelatedField):
    """
    A custom field to use for the `target` generic relationship.
    """
    pass


class NotificationSerializer(serializers.ModelSerializer):
    recipient = PublicProfileSerializer(source='recipient.profile', read_only=True)
    unread = serializers.BooleanField(read_only=True)
    target = NotificationTargetRelatedField(read_only=True)  # thread
    actor = NotificationActorRelatedField(read_only=True)  # sender
    action_object = NotificationActionObjectRelatedField(read_only=True)  # comment

    class Meta:
        # fields = ('recipient', 'slug', 'target', 'actor', 'unread', 'level', 'verb', 'action_object', 'timesince', 'description')
        fields = ('recipient', 'id', 'actor', 'unread', 'level', 'verb', 'action_object', 'timesince', 'description', 'target')
        model = Notification
