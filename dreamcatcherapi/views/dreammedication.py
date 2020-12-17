from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from dreamcatcherapi.models import Dream, Medication, DreamMedication

class MedicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medication
        fields = ('id', 'name')

class DreamMedicationSerializer(serializers.ModelSerializer):
    medication = MedicationSerializer(many=False)

    class Meta:
        model = DreamMedication
        fields = ('id', 'dream_id', 'medication_id', 'medication')
        depth = 1

class DreamMedications(ViewSet):
    """ medications to be added to a dream for dreamcatcher """

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
        "GET all dream medications"
        dreammedications = DreamMedication.objects.all()
        
        serializer = DreamMedicationSerializer(dreammedications, many=True, context={'request': request})

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
