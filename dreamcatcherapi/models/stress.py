""" Stress model for dreams """

from django.db import models

class Stress(models.Model):
    """ model representation of a list of Stressful events a user can add to their dream """

    stress_event = models.CharField(max_length=50)
