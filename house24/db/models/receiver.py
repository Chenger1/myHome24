from django.db import models
from django.dispatch import receiver

import os


def delete_image_path(path):
    if os.path.isfile(path):
        os.remove(path)


@receiver(models.signals.pre_save)
def delete_old_image_after_model_update(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_images = sender.objects.get(pk=instance.pk).get_images()
    except models.ObjectDoesNotExist:
        return False
    except AttributeError:
        return False

    if old_images:
        new_images = instance.get_images()
        if new_images:
            for new, old in zip(new_images, old_images):
                if old != new:
                    delete_image_path(old.path)


@receiver(models.signals.pre_delete)
def delete_image_with_deleting_instance(sender, instance, **kwargs):
    try:
        images = instance.get_images()
        if images:
            for image in images:
                delete_image_path(image)
    except AttributeError:
        return False
