from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from dreamcatcherapi.models import DreamcatcherUser

class Profiles(ViewSet):
    """ dreamcatcher user types """
    
    def list(self, request):
        """ Handle GET request for single user profile """

        user = DreamcatcherUser.objects.get(user=request.auth.user)
        serializer = DreamcatcherUserSerializer(user, context={'request': request})


        # profile = User.objects.get(pk=pk)
        # serializer = ProfileSerializer(profile, context={'request': request})

        return Response(serializer.data)

        # except Exception as ex:
        #     return HttpResponseServerError(ex)


class ProfileSerializer(serializers.ModelSerializer):
    """ JSON Serializer for profile types

    Arguments:
        serializers
    """

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')

class DreamcatcherUserSerializer(serializers.ModelSerializer):
    """ JSON Serializer for user 
    Arguments: 
        serializers
    """
    user = ProfileSerializer(serializers.ModelSerializer)
    class Meta:
        model = DreamcatcherUser
        fields = ('id', 'user', 'bio', 'profile_photo')