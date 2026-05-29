from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from torneo.models import Temporada
from torneo.serializers import TemporadaSerializer
from torneo.utils.format_serializer import format_serializer_errors
from torneo.views import paginate_queryset
from torneo.utils.responses import error_response, success_response


class TemporadaListCreateView(APIView):
    def post(self, request):
        """
        Crea una nueva temporada.

        Parameters:
        - request (dict): Contiene la información de la temporada a crear.

        Returns:
        - response (dict): Contiene el mensaje de exito y la temporada creada.
        """
        try:
            serializer = TemporadaSerializer(data=request.data)

            if not serializer.is_valid():
                return error_response(
                    message="Errores de validación",
                    data=format_serializer_errors(serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            temporada = serializer.save()
            return success_response(
                message="Temporada creada correctamente",
                data=TemporadaSerializer(temporada).data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return error_response(
                message=str(e), data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TemporadaDetailView(APIView):
    def get(self, request, pk):
        """
        Obtiene una temporada por su pk.

        Parameters:
        - request (dict): Contiene la información de la petición.
        - pk (int): Pk de la temporada a obtener.

        Returns:
        - response (dict): Contiene el mensaje de exito y la temporada obtenida.
        """
        try:
            temporada = get_object_or_404(Temporada, pk=pk)
            return success_response(
                message="Temporada encontrada",
                data=TemporadaSerializer(temporada).data,
                status=status.HTTP_200_OK,
            )
        except Http404:
            return error_response(
                message="Temporada no encontrada",
                data=None,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return error_response(
                message=str(e), data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TemporadaAllView(APIView):
    def get(self, request):
        """
        Obtiene todas las temporadas.

        Returns:
        - response (dict): Contiene el mensaje de exito y las temporadas encontradas.
        """
        try:
            temporadas = Temporada.objects.all().order_by("idtemporada")
            paginated_data = paginate_queryset(temporadas, TemporadaSerializer, request)
            if "error" in paginated_data:
                raise Exception(paginated_data["error"])
            return paginated_data
        except Exception as e:
            return error_response(
                message=str(e), data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
        try:
            temporada = get_object_or_404(Temporada, pk=pk)
            serializer = TemporadaSerializer(temporada, data=request.data, partial=True)

            if not serializer.is_valid():
                return error_response(
                    message="Errores de validación",
                    data=format_serializer_errors(serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            return success_response(
                message="Temporada actualizada correctamente",
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        except Http404:
            return error_response(
                message="Temporada no encontrada",
                data=None,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return error_response(
                message=str(e), data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
        try:
            temporada = get_object_or_404(Temporada, pk=pk)
            if not temporada:
                return error_response(
                    message="Temporada no encontrada",
                    data=None,
                    status=status.HTTP_404_NOT_FOUND,
                )

            if not temporada.temporadaactiva:
                return error_response(
                    message="La temporada ya está inactiva.",
                    data=None,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            temporada.temporadaactiva = False
            temporada.save(update_fields=["temporadaactiva"])

            return success_response(
                message="Temporada deshabilitada correctamente",
                data=None,
                status=status.HTTP_200_OK,
            )
        except Http404:
            return error_response(
                message="Temporada no encontrada",
                data=None,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return error_response(
                message=str(e), data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
