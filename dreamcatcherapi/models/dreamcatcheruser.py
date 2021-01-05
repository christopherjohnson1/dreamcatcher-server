""" Dreamcatcher User Model  """

from django.db import models
from django.conf import settings

class DreamcatcherUser(models.Model):
    """ Model representation of a dreamcatcher user account that can be created """

    birthday = models.DateField()
    profile_photo = models.URLField()
    bio = models.CharField(max_length=250)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def full_name(self):
        """Provides full name for a user

        Returns:
            string: Full name of user
        """
        return f"{self.user.first_name} {self.user.last_name}"
    