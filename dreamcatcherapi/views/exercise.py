from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from dreamcatcherapi.models import Exercise

class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = ('id', 'exercise_type', 'duration')


class Exercises(ViewSet):
    """ exercises to be added to a dream for dreamcatcher """

    def create(self, request):
        """ POST operations for adding a medication to a dream """

        exercise = Exercise()
        exercise.exercise_type = request.data['exercise_type']
        exercise.duration = request.data['duration']
        

        try:
            exercise.save()
            serializer = ExerciseSerializer(exercise, context={'request': request})

            return Response(serializer.data)

        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """ get a single exercise """

        try:
            exercise = Exercise.objects.get(pk=pk)

            serializer = ExerciseSerializer(exercise, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        "GET all exercises"
        exercises = Exercise.objects.all()
        
        serializer = ExerciseSerializer(exercises, many=True, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """ update/ edit an existing exercise """

        exercise = Exercise.objects.get(pk=pk)

        exercise.exercise_type = request.data['exercise_type']
        exercise.duration = request.data['duration']

        exercise.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """ deletes an existing exercise """

        try:
            exercise = Exercise.objects.get(pk=pk)

            exercise.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Exercise.DoesNotExist as ex:
            return Response({'mesage': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
