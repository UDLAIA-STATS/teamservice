
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status

from torneo.models import Partido, Torneo
from torneo.serializers import TorneoSerializer
from torneo.views import paginate_queryset
from torneo.utils.responses import *
from torneo.utils.format_serializer import format_serializer_errors

class TorneoListCreateView(APIView):
    def post(self, request):
        """
        Crea un nuevo torneo.
        
        Parameters:
        - request (dict): Contiene la información del torneo a crear.
        
        Returns:
        - response (dict): Contiene el mensaje de exito y el torneo creado.
        """
        try:
            serializer = TorneoSerializer(data=request.data)
            if not serializer.is_valid():
                return error_response(
                    message="Errores de validación",
                    data=format_serializer_errors(serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            torneo = serializer.save()
            return success_response(
                message="Torneo creado correctamente",
                data=TorneoSerializer(torneo).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return error_response(message=str(e), data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TorneoDetailView(APIView):
    def get_object(self, pk):
        """
        Devuelve el objeto Torneo asociado con el pk.
        
        Parameters:
        - pk (int): Identificador del torneo a buscar.
        
        Returns:
        - torneo (Torneo): Torneo asociado con el pk.
        """
        return Torneo.objects.filter(pk=pk).first()

    def get(self, request, pk):
        """
        Obtiene un torneo por su pk.
        
        Parameters:
        - request (dict): Contiene la información de la petición.
        - pk (int): Identificador del torneo a obtener.
        
        Returns:
        - response (dict): Contiene el mensaje de exito y el torneo obtenido.
        """
        try:
            torneo = self.get_object(pk)
            if not torneo:
                raise Exception("Torneo no encontrado")
            return success_response(message="Torneo encontrado", data=TorneoSerializer(torneo).data, status=status.HTTP_200_OK)
        except Exception as e:
            return error_response(message=str(e), data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TorneoAllView(APIView):
    def get(self, request):
        """
        Obtiene todos los torneos.
        
        Returns:
        - response (dict): Contiene el mensaje de exito y los torneos encontrados.
        """
        try:
            torneos = Torneo.objects.all().order_by("idtorneo")
            paginated_data = paginate_queryset(torneos, TorneoSerializer, request)
            return paginated_data
        except Exception as e:
            return error_response(message=str(e), data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TorneoUpdateView(APIView):
    def patch(self, request, pk):
        """
        Actualiza un torneo existente.
        
        Parameters:
        - request (dict): Contiene la información del torneo a actualizar.
        - pk (int): Pk del torneo a actualizar.
        
        Returns:
        - response (dict): Contiene el mensaje de exito y el torneo actualizado.
        """
        try:
            torneo = Torneo.objects.filter(pk=pk).first()
            if not torneo:
                raise Exception("Torneo no encontrado")

            serializer = TorneoSerializer(torneo, data=request.data, partial=True)
            
            if not serializer.is_valid():
                return error_response(
                    message="Errores de validación",
                    data=format_serializer_errors(serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()
            return success_response(message="Torneo actualizado correctamente", data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return error_response(message=str(e), data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TorneoDeleteView(APIView):
    def delete(self, request, pk):
        """
        Elimina un torneo existente.

        Parameters:
        - request (dict): Contiene la información de la petición.
        - pk (int): Identificador del torneo a eliminar.

        Returns:
        - response (dict): Contiene el mensaje de exito y el torneo eliminado.
        """
        try:
            torneo = get_object_or_404(Torneo, pk=pk)

            if not torneo:
                raise Exception("Torneo no encontrado")
            
            if not torneo.torneoactivo:
                raise Exception("El torneo ya está inactivo")
            
            # partidos = Partido.objects.filter(idtorneo=torneo).exists()

            # if partidos:
            #     return error_response(
            #         message="No se puede eliminar el torneo porque tiene partidos asociados.",
            #         status=status.HTTP_400_BAD_REQUEST,
            #         data=None
            #     )

            torneo.torneoactivo = False
            torneo.save(update_fields=['torneoactivo'])

            return success_response(message="Torneo deshabilitado correctamente", data=None, status=status.HTTP_200_OK)
        except Exception as e:
            return error_response(message=str(e), data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)