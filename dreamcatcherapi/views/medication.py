from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from dreamcatcherapi.models import Medication

class MedicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medication
        fields = ('id', 'name')


class Medications(ViewSet):
    """ medications for dreamcatcher """

    def create(self, request):
        """ POST operations for adding a medication """

        medication = Medication()
        medication.name = request.data['name']
        

        try:
            medication.save()
            serializer = MedicationSerializer(medication, context={'request': request})

            return Response(serializer.data)

        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """ get a single medication """

        try:
            medication = Medication.objects.get(pk=pk)

            serializer = MedicationSerializer(medication, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        "GET all medications"
        medications = Medication.objects.all()
        
        serializer = MedicationSerializer(medications, many=True, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """ update/ edit an existing medication """

        medication = Medication.objects.get(pk=pk)

        medication.name = request.data['name']


        medication.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """ deletes an existing medication """

        try:
            medication = Medication.objects.get(pk=pk)

            medication.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Medication.DoesNotExist as ex:
            return Response({'mesage': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
