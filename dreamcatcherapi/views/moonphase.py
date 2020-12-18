from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from dreamcatcherapi.models import MoonPhase

class MoonPhaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = MoonPhase
        fields = ('id', 'label')


class MoonPhases(ViewSet):
    """ moon phases to be added to dreamcatcher """

    def create(self, request):
        """ POST operations for adding a moon phase """

        moonphase = MoonPhase()
        moonphase.label = request.data['label']
        

        try:
            moonphase.save()
            serializer = MoonPhaseSerializer(moonphase, context={'request': request})

            return Response(serializer.data)

        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """ get a single moon phase """

        try:
            moonphase = MoonPhase.objects.get(pk=pk)

            serializer = MoonPhaseSerializer(moonphase, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        " GET all moon phases "
        moonphases = MoonPhase.objects.all()
        
        serializer = MoonPhaseSerializer(moonphases, many=True, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """ update/ edit an existing moon phase """

        moonphase = MoonPhase.objects.get(pk=pk)

        moonphase.label = request.data['label']

        moonphase.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """ deletes an existing moon phase """

        try:
            moonphase = MoonPhase.objects.get(pk=pk)

            moonphase.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except MoonPhase.DoesNotExist as ex:
            return Response({'mesage': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
