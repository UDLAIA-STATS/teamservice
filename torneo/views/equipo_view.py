from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError

from torneo.models import Equipo, Partido
from torneo.serializers import EquipoSerializer
from torneo.utils.format_serializer import format_serializer_errors
from torneo.views import paginate_queryset
from torneo.utils.responses import *


class EquipoListCreateView(APIView):
    def post(self, request):
        serializer = EquipoSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            errors = format_serializer_errors(serializer.errors)
            raise ValidationError(errors)
        
        equipo = serializer.save()
        return success_response(
            message="Equipo creado correctamente",
            status=status.HTTP_201_CREATED,
            data=EquipoSerializer(equipo, context={'request': request}).data
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EquipoDetailView(APIView):
    def get_object(self, pk):
        return Equipo.objects.filter(pk=pk).first()

    def get(self, request, pk):
        equipo = self.get_object(pk)
        if not equipo:
            return error_response(message="Equipo no encontrado", data=None, status=status.HTTP_404_NOT_FOUND)
        return success_response(message="Equipo encontrado", data=EquipoSerializer(equipo).data, status=status.HTTP_200_OK)


class EquipoSearchByNameView(APIView):
    def get(self, request, name):
        equipo = Equipo.objects.filter(nombreequipo=name).first()
        if not equipo:
            return error_response(message="Equipo no encontrado", data=None, status=status.HTTP_404_NOT_FOUND)
        return success_response(message="Equipo encontrado", data=EquipoSerializer(equipo).data, status=status.HTTP_200_OK)


class EquipoAllView(APIView):
    def get(self, request):
        equipos = Equipo.objects.all().order_by("idequipo")
        paginated_data = paginate_queryset(equipos, EquipoSerializer, request)
        if "error" in paginated_data:
            return error_response(message=paginated_data["error"], data=None, status=status.HTTP_400_BAD_REQUEST)
        return success_response(message="Equipos encontrados", data=paginated_data, status=status.HTTP_200_OK)


class EquipoUpdateView(APIView):
    def patch(self, request, pk):
        equipo = Equipo.objects.filter(pk=pk).first()
        if not equipo:
            return error_response(message="Equipo no encontrado", data=None, status=status.HTTP_404_NOT_FOUND)

        serializer = EquipoSerializer(equipo, data=request.data, partial=True, context={'request': request})
        
        if not serializer.is_valid():
            raise ValidationError(format_serializer_errors(serializer.errors))
        
        serializer.save()
        return success_response(message="Equipo actualizado correctamente", data=serializer.data, status=status.HTTP_200_OK)


class EquipoDeleteView(APIView):
    def delete(self, request, pk):
        equipo = Equipo.objects.filter(pk=pk).first()
        if not equipo:
            return error_response(message="Equipo no encontrado", data=None, status=status.HTTP_404_NOT_FOUND)

        if Partido.objects.filter(idequipolocal=equipo).exists() or Partido.objects.filter(idequipovisitante=equipo).exists():
            return error_response(
                message="No se puede eliminar el equipo porque está relacionado con uno o más partidos.",
                data=None,
                status=status.HTTP_400_BAD_REQUEST
            )

        equipo.delete()
        return success_response(message="Equipo eliminado correctamente", data=None, status=status.HTTP_200_OK)
