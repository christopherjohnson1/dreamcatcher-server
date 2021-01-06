from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from dreamcatcherapi.models import Dream, DreamcatcherUser, DreamType, Exercise, Stress, MoonPhase
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """ JSON serializer for user """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')

class DreamcatcherUserSerializer(serializers.ModelSerializer):
    """ JSON Serializer for user """
    user = UserSerializer(serializers.ModelSerializer)
    class Meta:
        model = DreamcatcherUser
        fields = ('id', 'user', 'full_name', 'profile_photo')

class DreamTypeSerializer(serializers.ModelSerializer):
    """ JSON Serializer for dream type """
    class Meta:
        model = DreamType
        fields = ('id', 'label')

class ExerciseSerializer(serializers.ModelSerializer):
    """ JSON Serializer for exercise type """
    class Meta:
        model = Exercise
        fields = ('id', 'exercise_type')

class StressSerializer(serializers.ModelSerializer):
    """ JSON Serializer for Stress type """
    class Meta:
        model = Stress
        fields = ('id', 'stress_event')
class MoonPhaseSerializer(serializers.ModelSerializer):
    """ JSON Serializer for moon phase """
    class Meta:
        model = MoonPhase
        fields = ('id', 'label')
class DreamSerializer(serializers.ModelSerializer):
    """ JSON Serializer for dreams """
    user = DreamcatcherUserSerializer(many=False)
    dream_type = DreamTypeSerializer
    exercise = ExerciseSerializer
    stress = StressSerializer
    moon_phase = MoonPhaseSerializer

    class Meta:
        model = Dream
        fields = ('id', 'user', 'user_id', 'title', 'dream_story', 'date', 'private', 'dream_type_id', 'exercise_id', 'stress_id', 'moon_phase_id', 'dream_type', 'exercise', 'stress', 'moon_phase')
        depth = 1

class Dreams(ViewSet):
    """ comments for dreamcatcher """

    def create(self, request):
        """ POST operations for adding a dream """

        dream = Dream()
        dream.user = DreamcatcherUser.objects.get(user=request.auth.user)
        dream.title = request.data['title']
        dream.dream_story = request.data['dream_story']
        dream.private = request.data['private']
        dream.dream_type = DreamType.objects.get(pk=request.data['dream_type_id'])
        dream.exercise = Exercise.objects.get(pk=request.data['exercise_id'])
        dream.stress = Stress.objects.get(pk=request.data['stress_id'])
        dream.moon_phase = MoonPhase.objects.get(pk=request.data['moon_phase_id'])

        try:
            dream.save()
            serializer = DreamSerializer(dream, context={'request': request})

            return Response(serializer.data)

        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """ get a single dream """

        try:
            dream = Dream.objects.get(pk=pk)

            serializer = DreamSerializer(dream, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        "GET all dreams"
        dreams = Dream.objects.all()

        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            dreams = dreams.filter(user_id=user_id)
        
        serializer = DreamSerializer(dreams, many=True, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """ update/ edit an existing dream """

        dream = Dream.objects.get(pk=pk)

        dream.user = DreamcatcherUser.objects.get(user=request.auth.user)
        dream.title = request.data['title']
        dream.dream_story = request.data['dream_story']
        dream.private = request.data['private']
        dream.dream_type = DreamType.objects.get(pk=request.data['dream_type_id'])
        dream.exercise = Exercise.objects.get(pk=request.data['exercise_id'])
        dream.stress = Stress.objects.get(pk=request.data['stress_id'])
        dream.moon_phase = MoonPhase.objects.get(pk=request.data['moon_phase_id'])

        dream.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """ deletes an existing dream """

        try:
            dream = Dream.objects.get(pk=pk)

            dream.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Dream.DoesNotExist as ex:
            return Response({'mesage': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
