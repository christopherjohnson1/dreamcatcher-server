""" Moon phase model for dreams """

from django.db import models

class MoonPhase(models.Model):
    """ model representation of a list of moon phases a user can add to their dream """

    label = models.CharField(max_length=25)
