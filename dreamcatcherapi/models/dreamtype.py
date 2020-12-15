""" Dream type model for dreams """

from django.db import models

class DreamType(models.Model):
    """ model representation of a list of dream types a user can add to their dream """

    label = models.CharField(max_length=33)
