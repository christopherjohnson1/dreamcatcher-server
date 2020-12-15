""" Dream Model  """

from django.db import models

class Dream(models.Model):
    """ Model representation of a dreamcatcher user account that can be created """

    user = models.ForeignKey("DreamcatcherUser", on_delete=models.CASCADE)
    title = models.CharField(max_length=45)
    dream_story = models.CharField(max_length=3000)
    date = models.DateField(auto_now_add=True, auto_now=False)
    private = models.BooleanField(default=False)
    dream_type = models.ForeignKey("DreamType", on_delete=models.CASCADE)
    exercise = models.ForeignKey("Exercise", on_delete=models.CASCADE)
    stress = models.ForeignKey("Stress", on_delete=models.CASCADE)
    moon_phase = models.ForeignKey("MoonPhase", on_delete=models.CASCADE)
    