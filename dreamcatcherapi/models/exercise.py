""" Exercise model for dreams """

from django.db import models

class Exercise(models.Model):
    """ model representation of a list of Exercises a user can add to their dream """

    exercise_type = models.CharField(max_length=500)
    duration = models.IntegerField()
