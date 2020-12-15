""" Medication model for dreams """

from django.db import models

class Medication(models.Model):
    """ model representation of a list of medications a user can add to their dream """

    name = models.CharField(max_length=75)
