from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.serializers import ValidationError

from torneo.models import Equipo, Partido
from torneo.serializers import EquipoSerializer
from torneo.utils.format_serializer import format_serializer_errors
from torneo.views import paginate_queryset
from torneo.utils.responses import *


class EquipoListCreateView(APIView):
    def post(self, request):
        """
        Crea un nuevo equipo.
        
        Parameters:
        - request (dict): Contiene la informacion del equipo a crear.
        
        Returns:
        - response (dict): Contiene el mensaje de exito y el equipo creado.
        """
        try:
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
        except ValidationError as ve:
            return error_response(message=str(ve), data=ve.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return error_response(message=str(e), data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EquipoDetailView(APIView):
    def get_object(self, pk):
        """
        Devuelve el objeto Equipo asociado con el pk.
        
        Parameters:
        - pk (int): Identificador del equipo a buscar.
        
        Returns:
        - equipo (Equipo): Equipo asociado con el pk.
        """
        return Equipo.objects.filter(pk=pk).first()

    def get(self, request, pk):
        try:
            equipo = self.get_object(pk)
            if not equipo:
                raise Exception("Equipo no encontrado")
            return success_response(message="Equipo encontrado", data=EquipoSerializer(equipo).data, status=status.HTTP_200_OK)
        except Exception as e:
            return error_response(message=str(e), data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EquipoSearchByNameView(APIView):
    def get(self, request, name):
        
        """
        Busca un equipo por su nombre.
        
        Parameters:
        - request (dict): Contiene la informacion del equipo a buscar.
        - name (str): Nombre del equipo a buscar.
        
        Returns:
        - response (dict): Contiene el mensaje de exito y el equipo encontrado.
        """
        try:
            equipo = Equipo.objects.filter(nombreequipo=name).first()
            if not equipo:
                raise Exception("Equipo no encontrado")
            return success_response(message="Equipo encontrado", data=EquipoSerializer(equipo).data, status=status.HTTP_200_OK)
        except Exception as e:
            return error_response(message=str(e), data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EquipoAllView(APIView):
    def get(self, request):
        """
        Obtiene todos los equipos.

        Returns:
            - response (dict): Contiene el mensaje de exito y los equipos encontrados.
        """
        try:
            equipos = Equipo.objects.all().order_by("idequipo")
            paginated_data = paginate_queryset(equipos, EquipoSerializer, request)
            if "error" in paginated_data:
                raise Exception(paginated_data["error"])
            return paginated_data
        except Exception as e:
            return error_response(message=str(e), data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EquipoUpdateView(APIView):
    def patch(self, request, pk):
        """
        Actualiza un equipo existente.
        
        Parameters:
        - request (dict): Contiene la informacion del equipo a actualizar.
        - pk (int): Identificador del equipo a actualizar.
        
        Returns:
        - response (dict): Contiene el mensaje de exito y el equipo actualizado.
        """
        try:
            equipo = Equipo.objects.filter(pk=pk).first()
            if not equipo:
                raise Exception("Equipo no encontrado")

            serializer = EquipoSerializer(equipo, data=request.data, partial=True, context={'request': request})
            
            if not serializer.is_valid():
                raise ValidationError(format_serializer_errors(serializer.errors))
            
            serializer.save()
            return success_response(message="Equipo actualizado correctamente", data=serializer.data, status=status.HTTP_200_OK)
        except ValidationError as ve:
            return error_response(message=str(ve), data=None, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return error_response(message=str(e), data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EquipoDeleteView(APIView):
    def delete(self, request, pk):
        """
        Elimina un equipo existente.
        
        Parameters:
        - request (dict): Contiene la informacion del equipo a eliminar.
        - pk (int): Identificador del equipo a eliminar.
        
        Returns:
        - response (dict): Contiene el mensaje de exito y el equipo eliminado.
        """
        try:
            equipo = get_object_or_404(Equipo, pk=pk)

            if not equipo.equipoactivo:
                raise Exception("El equipo ya está inactivo")

            # if Partido.objects.filter(idequipolocal=equipo).exists() or Partido.objects.filter(idequipovisitante=equipo).exists():
            #     raise Exception("No se puede eliminar el equipo porque está relacionado con uno o más partidos.")

            equipo.equipoactivo = False
            equipo.save(update_fields=['equipoactivo'])
            return success_response(message="Equipo deshabilitado correctamente", data=None, status=status.HTTP_200_OK)
        except ValidationError as ve:
            return error_response(message=str(ve), data=None, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return error_response(message=str(e), data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
