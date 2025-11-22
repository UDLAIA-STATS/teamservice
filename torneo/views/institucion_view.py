from torneo.models import Institucion
from torneo.serializers import InstitucionSerializer
from rest_framework.views import APIView
from django.db import IntegrityError
from rest_framework.serializers import ValidationError
from rest_framework import status

from torneo.views import paginate_queryset
from torneo.utils.format_serializer import format_serializer_errors
from torneo.utils.responses import *

class InstitucionListCreateView(APIView):
    def post(self, request):
        serializer = InstitucionSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(format_serializer_errors(serializer.errors))

        try:
            institucion = serializer.save()
            return success_response(
                message="Institución creada correctamente",
                status=status.HTTP_201_CREATED,
                data=InstitucionSerializer(institucion).data
            )
        except IntegrityError:
            return error_response(
                message="Ya existe una institución con ese nombre",
                data=None,
                status=status.HTTP_400_BAD_REQUEST
            )


class InstitucionDetailView(APIView):
    def get(self, request, pk):
        institucion = Institucion.objects.filter(pk=pk).first()
        if not institucion:
            return error_response(message="Institución no encontrada", data=None, status=status.HTTP_404_NOT_FOUND)
        return success_response(message="Institución encontrada", data=InstitucionSerializer(institucion).data, status=status.HTTP_200_OK)


class InstitucionAllView(APIView):
    def get(self, request):
        instituciones = Institucion.objects.all().order_by("idinstitucion")
        paginated_data = paginate_queryset(instituciones, InstitucionSerializer, request)
        if "error" in paginated_data:
            return error_response(message=paginated_data["error"], data=None, status=status.HTTP_400_BAD_REQUEST)
        return success_response(message="Instituciones encontradas", data=paginated_data, status=status.HTTP_200_OK)


class InstitucionUpdateView(APIView):
    def patch(self, request, pk):
        institucion = Institucion.objects.filter(pk=pk).first()
        if not institucion:
            return error_response(message="Institución no encontrada", data=None, status=status.HTTP_404_NOT_FOUND)

        serializer = InstitucionSerializer(institucion, data=request.data, partial=True)
        
        if not serializer.is_valid():
            raise ValidationError(format_serializer_errors(serializer.errors))

        serializer.save()
        return success_response(message="Institución actualizada correctamente", data=serializer.data, status=status.HTTP_200_OK)

class InstitucionDeleteView(APIView):
    def delete(self, request, pk):
        institucion = Institucion.objects.filter(pk=pk).first()
        if not institucion:
            return error_response(message="Institución no encontrada", data=None, status=status.HTTP_404_NOT_FOUND)

        institucion.delete()
        return success_response(message="Institución eliminada correctamente", data=None, status=status.HTTP_200_OK)