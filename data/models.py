from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.
class FileUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.FileField(upload_to='uploads/')
    word_count = models.BigIntegerField(null=True)


@receiver(pre_save, sender=FileUpload)
def FileUploadPreSave(instance, **kwargs):
    try:
        with open(instance.data.name) as fp:
            data = fp.read().strip()
            instance.word_count = len(data.strip().replace('\n', ' ').split(' '))
    except Exception as e:
        pass
    return
