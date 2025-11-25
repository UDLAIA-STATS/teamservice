from rest_framework.views import APIView
from rest_framework import status
from rest_framework.serializers import ValidationError

from torneo.models import Partido
from torneo.serializers import PartidoSerializer
from torneo.views import paginate_queryset
from torneo.utils.responses import *
from torneo.utils.format_serializer import format_serializer_errors

class PartidoListCreateView(APIView):
    def post(self, request):
        """
        Crea un nuevo partido.

        Parameters:
        - request (dict): Contiene la informacion del partido a crear.

        Returns:
        - response (dict): Contiene el mensaje de exito y el partido creado.
        """
        serializer = PartidoSerializer(data=request.data)
        
        if not serializer.is_valid():
            raise ValidationError(format_serializer_errors(serializer.errors))

        partido = serializer.save()
        return success_response(
            message="Partido creado correctamente",
            status=status.HTTP_201_CREATED,
            data=PartidoSerializer(partido).data
        )

class PartidoDetailView(APIView):
    def get_object(self, pk):
        """
        Devuelve el objeto Partido asociado con el pk.

        Parameters:
        - pk (int): Identificador del partido a buscar.

        Returns:
        - partido (Partido): Partido asociado con el pk.
        """
        return Partido.objects.filter(pk=pk).first()

    def get(self, request, pk):
        partido = self.get_object(pk)
        if not partido:
            return error_response(message="Partido no encontrado", data=None, status=status.HTTP_404_NOT_FOUND)
        return success_response(message="Partido encontrado", data=PartidoSerializer(partido).data, status=status.HTTP_200_OK)

class PartidoAllView(APIView):
    def get(self, request):
        """
        Obtiene todos los partidos.

        Returns:
        - response (dict): Contiene el mensaje de exito y los partidos encontrados.
        """
        partidos = Partido.objects.all().order_by("idpartido")
        paginated_data = paginate_queryset(partidos, PartidoSerializer, request)
        if "error" in paginated_data:
            return error_response(message=paginated_data["error"], data=None, status=status.HTTP_400_BAD_REQUEST)
        return success_response(message="Partidos encontrados", data=paginated_data, status=status.HTTP_200_OK)


class PartidoUpdateView(APIView):
    def patch(self, request, pk):
        """
        Actualiza un partido existente.

        Parameters:
        - request (dict): Contiene la informacion del partido a actualizar.
        - pk (int): Pk del partido a actualizar.

        Returns:
        - response (dict): Contiene el mensaje de exito y el partido actualizado.
        """
        partido = Partido.objects.filter(pk=pk).first()
        if not partido:
            return error_response(message="Partido no encontrado", data=None, status=status.HTTP_404_NOT_FOUND)

        serializer = PartidoSerializer(partido, data=request.data, partial=True)
        if not serializer.is_valid():
            raise ValidationError(format_serializer_errors(serializer.errors))

        serializer.save()
        return success_response(message="Partido actualizado correctamente", data=serializer.data, status=status.HTTP_200_OK)

class PartidoDeleteView(APIView):
    def delete(self, request, pk):
        """
        Elimina un partido existente.

        Parameters:
        - request (dict): Contiene la informacion del partido a eliminar.
        - pk (int): Identificador del partido a eliminar.

        Returns:
        - response (dict): Contiene el mensaje de exito y el partido eliminado.
        """
        partido = Partido.objects.filter(pk=pk).first()
        if not partido:
            return error_response(message="Partido no encontrado", data=None, status=status.HTTP_404_NOT_FOUND)

        partido.delete()
        return success_response(message="Partido eliminado correctamente", data=None, status=status.HTTP_200_OK)