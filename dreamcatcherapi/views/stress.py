from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from dreamcatcherapi.models import Stress

class StressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stress
        fields = ('id', 'stress_event')


class StressEvents(ViewSet):
    """ stress events for dreamcatcher """

    def create(self, request):
        """ POST operations for adding a stress event """

        stress = Stress()
        stress.stress_event = request.data['stress_event']
        

        try:
            stress.save()
            serializer = StressSerializer(stress, context={'request': request})

            return Response(serializer.data)

        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """ get a single stress """

        try:
            stress = Stress.objects.get(pk=pk)

            serializer = StressSerializer(stress, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        "GET all stresses"
        stresses = Stress.objects.all()
        
        serializer = StressSerializer(stresses, many=True, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """ update/ edit an existing stress """

        stress = Stress.objects.get(pk=pk)

        stress.stress_event = request.data['stress_event']


        stress.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """ deletes an existing stress """

        try:
            stress = Stress.objects.get(pk=pk)

            stress.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Stress.DoesNotExist as ex:
            return Response({'mesage': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
