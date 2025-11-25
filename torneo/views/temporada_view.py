from rest_framework.views import APIView
from rest_framework import status
from rest_framework.serializers import ValidationError

from torneo.models import Partido, Temporada, Torneo
from torneo.serializers import TemporadaSerializer
from torneo.utils.format_serializer import format_serializer_errors
from torneo.views import paginate_queryset
from torneo.utils.responses import *

class TemporadaListCreateView(APIView):
    def post(self, request):
        """
        Crea una nueva temporada.
        
        Parameters:
        - request (dict): Contiene la información de la temporada a crear.
        
        Returns:
        - response (dict): Contiene el mensaje de exito y la temporada creada.
        """
        serializer = TemporadaSerializer(data=request.data)
        
        if not serializer.is_valid():
            raise ValidationError(format_serializer_errors(serializer.errors))

        temporada = serializer.save()
        return success_response(
            message="Temporada creada correctamente",
            data=TemporadaSerializer(temporada).data,
            status=status.HTTP_201_CREATED
        )


class TemporadaDetailView(APIView):
    def get_object(self, pk):
        """
        Devuelve el objeto Temporada asociado con el pk.
        
        Parameters:
        - pk (int): Pk de la temporada a buscar.
        
        Returns:
        - temporada (Temporada): Temporada asociado con el pk.
        """
        return Temporada.objects.filter(pk=pk).first()

    def get(self, request, pk):
        """
        Obtiene una temporada por su pk.
        
        Parameters:
        - request (dict): Contiene la información de la petición.
        - pk (int): Pk de la temporada a obtener.
        
        Returns:
        - response (dict): Contiene el mensaje de exito y la temporada obtenida.
        """

        temporada = self.get_object(pk)
        if not temporada:
            return error_response(message="Temporada no encontrada", data=None, status=status.HTTP_404_NOT_FOUND)
        return success_response(message="Temporada encontrada", data=TemporadaSerializer(temporada).data, status=status.HTTP_200_OK)


class TemporadaAllView(APIView):
    def get(self, request):
        """
        Obtiene todas las temporadas.

        Returns:
        - response (dict): Contiene el mensaje de exito y las temporadas encontradas.
        """
        temporadas = Temporada.objects.all().order_by("idtemporada")
        paginated_data = paginate_queryset(temporadas, TemporadaSerializer, request)
        if "error" in paginated_data:
            return error_response(message=paginated_data["error"], data=None, status=status.HTTP_400_BAD_REQUEST)
        return success_response(message="Temporadas encontradas", data=paginated_data, status=status.HTTP_200_OK)


class TemporadaUpdateView(APIView):
    def patch(self, request, pk):
        """
        Actualiza una temporada existente.
        
        Parameters:
        - request (dict): Contiene la información de la petición.
        - pk (int): Pk de la temporada a actualizar.
        
        Returns:
        - response (dict): Contiene el mensaje de exito y la temporada actualizada.
        """
        temporada = Temporada.objects.filter(pk=pk).first()
        if not temporada:
            return Response({"error": "Temporada no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TemporadaSerializer(temporada, data=request.data, partial=True)
        
        if not serializer.is_valid():
            raise ValidationError(format_serializer_errors(serializer.errors))
        
        serializer.save()
        return success_response(message="Temporada actualizada correctamente", data=serializer.data, status=status.HTTP_200_OK)

class TemporadaDeleteView(APIView):
    def delete(self, request, pk):
        """
        Elimina una temporada por su pk.

        Parameters:
        - request (dict): Contiene la información de la petición.
        - pk (int): Pk de la temporada a eliminar.

        Returns:
        - response (dict): Contiene el mensaje de exito y la temporada eliminada.
        """
        temporada = Temporada.objects.filter(pk=pk).first()
        torneos = Torneo.objects.filter(idtemporada=temporada).exists()
        partidos = Partido.objects.filter(idtemporada=temporada).exists()
        if not temporada:
            return error_response(message="Temporada no encontrada", data=None, status=status.HTTP_404_NOT_FOUND)

        if torneos or partidos:
            return error_response(
                message="No se puede eliminar la temporada porque tiene torneos o partidos asociados.",
                data=None,
                status=status.HTTP_400_BAD_REQUEST
            )

        temporada.delete()
        return success_response(message="Temporada eliminada correctamente", data=None, status=status.HTTP_200_OK)
