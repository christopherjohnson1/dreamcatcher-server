""" Dream Medication join table model for dreams """

from django.db import models

class DreamMedication(models.Model):
    """ model representation of the join table for medications to be added to a dream story """

    dream = models.ForeignKey("Dream", on_delete=models.CASCADE)
    medication = models.ForeignKey("Medication", on_delete=models.CASCADE)
