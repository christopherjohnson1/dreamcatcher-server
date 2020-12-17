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
        """ POST operations for adding a medication to a dream """

        dreammedication = DreamMedication()
        dreammedication.dream = Dream.objects.get(pk=request.data['dream_id'])
        dreammedication.medication = Medication.objects.get(pk=request.data['medication_id'])
        

        try:
            dreammedication.save()
            serializer = DreamMedicationSerializer(dreammedication, context={'request': request})

            return Response(serializer.data)

        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """ get a single dream medication """

        try:
            dreammedication = DreamMedication.objects.get(pk=pk)

            serializer = DreamMedicationSerializer(dreammedication, context={'request': request})
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

        dreammedication = DreamMedication.objects.get(pk=pk)

        dreammedication.dream = Dream.objects.get(pk=request.data['dream_id'])
        dreammedication.medication = Medication.objects.get(pk=request.data['medication_id'])

        dreammedication.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """ deletes an existing dream """

        try:
            dreammedication = DreamMedication.objects.get(pk=pk)

            dreammedication.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except DreamMedication.DoesNotExist as ex:
            return Response({'mesage': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
