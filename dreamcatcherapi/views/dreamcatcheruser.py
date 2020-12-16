from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from dreamcatcherapi.models import Dream, DreamcatcherUser, DreamType, Exercise, Stress, MoonPhase

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'is_staff', 'username', 'email')

class DreamCatcherUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = DreamcatcherUser
        fields = ('id', 'user', 'birthday', 'profile_photo', 'bio')
        depth = 1

class DreamCatcherUsers(ViewSet):
    """ comments for dreamcatcher """

    def retrieve(self, request, pk=None):
        """ get a single dreamcatcheruser """

        try:
            dreamcatcheruser = DreamcatcherUser.objects.get(pk=pk)

            serializer = DreamCatcherUserSerializer(dreamcatcheruser, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        "GET all dreamcatcherusers"
        dreamcatcheruser = DreamcatcherUser.objects.all()
        
        serializer = DreamCatcherUserSerializer(dreamcatcheruser, many=True, context={'request': request})

        return Response(serializer.data)
