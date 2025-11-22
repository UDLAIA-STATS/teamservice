
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.serializers import ValidationError

from torneo.models import Partido, Torneo
from torneo.serializers import TorneoSerializer
from torneo.views import paginate_queryset
from torneo.utils.responses import *
from torneo.utils.format_serializer import format_serializer_errors

class TorneoListCreateView(APIView):
    def post(self, request):
        serializer = TorneoSerializer(data=request.data)
        if not serializer.is_valid():
            errors = format_serializer_errors(serializer.errors)
            raise ValidationError(errors)
        
        torneo = serializer.save()
        return success_response(
            message="Torneo creado correctamente",
            data=TorneoSerializer(torneo).data,
            status=status.HTTP_201_CREATED
        )
        


class TorneoDetailView(APIView):
    def get_object(self, pk):
        return Torneo.objects.filter(pk=pk).first()

    def get(self, request, pk):
        torneo = self.get_object(pk)
        if not torneo:
            return error_response(message="Torneo no encontrado", data=None, status=status.HTTP_404_NOT_FOUND)
        return success_response(message="Torneo encontrado", data=TorneoSerializer(torneo).data, status=status.HTTP_200_OK)


class TorneoAllView(APIView):
    def get(self, request):
        torneos = Torneo.objects.all().order_by("idtorneo")
        paginated_data = paginate_queryset(torneos, TorneoSerializer, request)
        if "error" in paginated_data:
            return error_response(message=paginated_data["error"], data=None, status=status.HTTP_400_BAD_REQUEST)
        return success_response(message="Torneos encontrados", data=paginated_data, status=status.HTTP_200_OK)


class TorneoUpdateView(APIView):
    def patch(self, request, pk):
        try:
            torneo = Torneo.objects.filter(pk=pk).first()
            if not torneo:
                return error_response(message="Torneo no encontrado", data=None, status=status.HTTP_404_NOT_FOUND)

            serializer = TorneoSerializer(torneo, data=request.data, partial=True)
            
            if not serializer.is_valid():
                raise ValidationError(format_serializer_errors(serializer.errors))

            serializer.save()
            return success_response(message="Torneo actualizado correctamente", data=serializer.data, status=status.HTTP_200_OK)
        except ValidationError as ve:
            return error_response(message=str(ve), data=None, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return error_response(message=str(e), data=None, status=status.HTTP_400_BAD_REQUEST)

class TorneoDeleteView(APIView):
    def delete(self, request, pk):
        torneo = Torneo.objects.filter(pk=pk).first()
        if not torneo:
            return error_response(message="Torneo no encontrado", data=None, status=status.HTTP_404_NOT_FOUND)
        
        partidos = Partido.objects.filter(idtorneo=torneo).exists()

        if partidos:
            return error_response(
                message="No se puede eliminar el torneo porque tiene partidos asociados.",
                status=status.HTTP_400_BAD_REQUEST,
                data=None
            )

        torneo.delete()
        return success_response(message="Torneo eliminado correctamente", data=None, status=status.HTTP_200_OK)
