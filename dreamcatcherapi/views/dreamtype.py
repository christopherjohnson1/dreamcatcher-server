from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from dreamcatcherapi.models import DreamType

class DreamTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DreamType
        fields = ('id', 'label')


class DreamTypes(ViewSet):
    """ dream types to be added to a dream for dreamcatcher """

    def create(self, request):
        """ POST operations for adding a medication to a dream """

        dreamtype = DreamType()
        dreamtype.label = request.data['label']
        

        try:
            dreamtype.save()
            serializer = DreamTypeSerializer(dreamtype, context={'request': request})

            return Response(serializer.data)

        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """ get a single dream type """

        try:
            dreamtype = DreamType.objects.get(pk=pk)

            serializer = DreamTypeSerializer(dreamtype, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        "GET all dream types"
        dreamtypes = DreamType.objects.all()
        
        serializer = DreamTypeSerializer(dreamtypes, many=True, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """ update/ edit an existing dream type """

        dreamtype = DreamType.objects.get(pk=pk)

        dreamtype.label = request.data['label']

        dreamtype.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """ deletes an existing dream """

        try:
            dreamtype = DreamType.objects.get(pk=pk)

            dreamtype.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except DreamType.DoesNotExist as ex:
            return Response({'mesage': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
