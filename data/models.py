from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

from pwnlib.commandline.checksec import ELF


class BinaryFile(models.Model):
    """A binary file that we want to test is vulnerable to overflows"""
    data = models.FileField(upload_to='uploads/')
    vulnerable = models.BooleanField(null=True)

    # DB cached 'property', not great but can be re-called a bunch of times in parallel
    def check_vulnerable(self):
        self.vulnerable = not ELF(self.data.name).canary
        return self.vulnerable
