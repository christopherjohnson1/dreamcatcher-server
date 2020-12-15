""" Comment model for dreams """

from django.db import models

class Comment(models.Model):
    """ model representation of a list of Comments a user can add to their dream """

    dream = models.ForeignKey("Dream", on_delete=models.CASCADE)
    user = models.ForeignKey("DreamcatcherUser", on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False)
