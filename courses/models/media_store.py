import os
# from io import BytesIO

# from PIL import Image

from django.db import models
# from django.db.models.signals import pre_save
from django.dispatch import receiver
# from django.core.files.uploadedfile import InMemoryUploadedFile

from . import BaseItemModel, Material


def uuid_as_name(instance, filename):
    try:
        file_extension = os.path.splitext(filename)[1]
    except IndexError:
        file_extension = '.png'
    return 'materials_data/images/{0}{1}'.format(instance.pk, file_extension)


class JsonDataImage(BaseItemModel):
    """
    Images of materials JSON data
    """
    # NOTE due JSON data of different materials can contain the same images paths
    # - we no need store ForeignKey to material, we assume that medias_store - this is separate
    # media data storage (which it can be in the future)
    # material = models.ForeignKey(Material, related_name='data_images', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to=uuid_as_name)  # storage=OverwriteStorage(),

    def __str__(self):
        return '{}'.format(self.name)


# TODO add video, files...


# remove old file on delete, we suppose that JsonDataImage not re-save: only create/delete mode
@receiver(models.signals.post_delete, sender=JsonDataImage)
def remove_file(sender, instance, using, **kwargs):
    if not JsonDataImage.objects.filter(name=instance.image.name).exists():
        # NOTE: we can remove file because we delete JsonDataImage directly (e.g. from admin):
        # without on_delete=models.CASCADE, so if one material will be deleted -
        # JsonDataImage will be exist until we run remove_unused_media_storage_files manage.py script
        instance.image.delete(save=False)

# FIXME not sure that we need to resize. Or change it to a greater size?
# @receiver(pre_save, sender=JsonDataImage)
# def resize_img(sender, instance, **kwargs):
#     output_size = (300, 300)
#
#     if instance.image:
#         image = Image.open(instance.image.file.file)
#
#         # do not resize if already resized
#         if image.height > output_size[0] or image.width > output_size[1]:
#             image.thumbnail(size=output_size)
#             image_file = BytesIO()
#             image.save(image_file, image.format)
#
#             instance.image.save(
#                 instance.image.name,
#                 InMemoryUploadedFile(
#                     image_file,
#                     None, '',
#                     instance.image.file.content_type,
#                     image.size,
#                     instance.image.file.charset,
#                 ),
#                 save=False
#             )
