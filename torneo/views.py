from django.db import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from math import ceil

from .models import Equipo, Partido, Torneo, Temporada
from .serializers import (
    EquipoSerializer,
    PartidoSerializer,
    TorneoSerializer,
    TemporadaSerializer,
)


# ============================================
# Función auxiliar de paginación
# ============================================
def paginate_queryset(queryset, serializer_class, request):
    """Aplica paginación con parámetros opcionales: ?page=N&offset=M"""
    try:
        page = int(request.query_params.get("page", 1))
        offset = int(request.query_params.get("offset", 10))
    except ValueError:
        return {"error": "Los parámetros 'page' y 'offset' deben ser números enteros."}

    total = queryset.count()
    start = (page - 1) * offset
    end = start + offset
    paginated = queryset[start:end]

    serializer = serializer_class(paginated, many=True)
    return {
        "count": total,
        "page": page,
        "offset": offset,
        "pages": ceil(total / offset) if offset else 1,
        "results": serializer.data,
    }


# ================================
# EQUIPO VIEWS
# ================================
class EquipoListCreateView(APIView):
    def post(self, request):
        serializer = EquipoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                equipo = serializer.save()
                return Response(
                    {"mensaje": "Equipo creado correctamente", "equipo": EquipoSerializer(equipo).data},
                    status=status.HTTP_201_CREATED
                )
            except IntegrityError:
                return Response({"error": "Ya existe un equipo con ese nombre"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EquipoDetailView(APIView):
    def get_object(self, pk):
        return Equipo.objects.filter(pk=pk).first()

    def get(self, request, pk):
        equipo = self.get_object(pk)
        if not equipo:
            return Response({"error": "Equipo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(EquipoSerializer(equipo).data)


class EquipoSearchByNameView(APIView):
    def get(self, request, name):
        equipo = Equipo.objects.filter(nombreequipo=name).first()
        if not equipo:
            return Response({"error": "Equipo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(EquipoSerializer(equipo).data)


class EquipoAllView(APIView):
    def get(self, request):
        equipos = Equipo.objects.all().order_by("idequipo")
        paginated_data = paginate_queryset(equipos, EquipoSerializer, request)
        if "error" in paginated_data:
            return Response(paginated_data, status=status.HTTP_400_BAD_REQUEST)
        return Response(paginated_data, status=status.HTTP_200_OK)


class EquipoUpdateView(APIView):
    def patch(self, request, pk):
        equipo = Equipo.objects.filter(pk=pk).first()
        if not equipo:
            return Response({"error": "Equipo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EquipoSerializer(equipo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Equipo actualizado correctamente", "equipo": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EquipoDeleteView(APIView):
    def delete(self, request, pk):
        equipo = Equipo.objects.filter(pk=pk).first()
        if not equipo:
            return Response({"error": "Equipo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if Partido.objects.filter(idequipolocal=equipo).exists() or Partido.objects.filter(idequipovisitante=equipo).exists():
            return Response(
                {"error": "No se puede eliminar el equipo porque está relacionado con uno o más partidos."},
                status=status.HTTP_400_BAD_REQUEST
            )

        equipo.delete()
        return Response({"mensaje": "Equipo eliminado correctamente"}, status=status.HTTP_200_OK)


# ================================
# PARTIDO VIEWS
# ================================
class PartidoListCreateView(APIView):
    def post(self, request):
        serializer = PartidoSerializer(data=request.data)
        if serializer.is_valid():
            partido = serializer.save()
            return Response(
                {"mensaje": "Partido creado correctamente", "partido": PartidoSerializer(partido).data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartidoDetailView(APIView):
    def get_object(self, pk):
        return Partido.objects.filter(pk=pk).first()

    def get(self, request, pk):
        partido = self.get_object(pk)
        if not partido:
            return Response({"error": "Partido no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(PartidoSerializer(partido).data)


class PartidoAllView(APIView):
    def get(self, request):
        partidos = Partido.objects.all().order_by("idpartido")
        paginated_data = paginate_queryset(partidos, PartidoSerializer, request)
        if "error" in paginated_data:
            return Response(paginated_data, status=status.HTTP_400_BAD_REQUEST)
        return Response(paginated_data, status=status.HTTP_200_OK)


class PartidoUpdateView(APIView):
    def patch(self, request, pk):
        partido = Partido.objects.filter(pk=pk).first()
        if not partido:
            return Response({"error": "Partido no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PartidoSerializer(partido, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Partido actualizado correctamente", "partido": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartidoDeleteView(APIView):
    def delete(self, request, pk):
        partido = Partido.objects.filter(pk=pk).first()
        if not partido:
            return Response({"error": "Partido no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        partido.delete()
        return Response({"mensaje": "Partido eliminado correctamente"}, status=status.HTTP_200_OK)


# ================================
# TORNEO VIEWS
# ================================
class TorneoListCreateView(APIView):
    def post(self, request):
        serializer = TorneoSerializer(data=request.data)
        if serializer.is_valid():
            torneo = serializer.save()
            return Response(
                {"mensaje": "Torneo creado correctamente", "torneo": TorneoSerializer(torneo).data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TorneoDetailView(APIView):
    def get_object(self, pk):
        return Torneo.objects.filter(pk=pk).first()

    def get(self, request, pk):
        torneo = self.get_object(pk)
        if not torneo:
            return Response({"error": "Torneo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(TorneoSerializer(torneo).data)


class TorneoAllView(APIView):
    def get(self, request):
        torneos = Torneo.objects.all().order_by("idtorneo")
        paginated_data = paginate_queryset(torneos, TorneoSerializer, request)
        if "error" in paginated_data:
            return Response(paginated_data, status=status.HTTP_400_BAD_REQUEST)
        return Response(paginated_data, status=status.HTTP_200_OK)


class TorneoUpdateView(APIView):
    def patch(self, request, pk):
        torneo = Torneo.objects.filter(pk=pk).first()
        if not torneo:
            return Response({"error": "Torneo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TorneoSerializer(torneo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Torneo actualizado correctamente", "torneo": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TorneoDeleteView(APIView):
    def delete(self, request, pk):
        torneo = Torneo.objects.filter(pk=pk).first()
        if not torneo:
            return Response({"error": "Torneo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if Temporada.objects.filter(idtorneo=torneo).exists():
            return Response(
                {"error": "No se puede eliminar el torneo porque tiene temporadas asociadas."},
                status=status.HTTP_400_BAD_REQUEST
            )

        torneo.delete()
        return Response({"mensaje": "Torneo eliminado correctamente"}, status=status.HTTP_200_OK)


# ================================
# TEMPORADA VIEWS
# ================================
class TemporadaListCreateView(APIView):
    def post(self, request):
        serializer = TemporadaSerializer(data=request.data)
        if serializer.is_valid():
            temporada = serializer.save()
            return Response(
                {"mensaje": "Temporada creada correctamente", "temporada": TemporadaSerializer(temporada).data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemporadaDetailView(APIView):
    def get_object(self, pk):
        return Temporada.objects.filter(pk=pk).first()

    def get(self, request, pk):
        temporada = self.get_object(pk)
        if not temporada:
            return Response({"error": "Temporada no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        return Response(TemporadaSerializer(temporada).data)


class TemporadaAllView(APIView):
    def get(self, request):
        temporadas = Temporada.objects.all().order_by("idtemporada")
        paginated_data = paginate_queryset(temporadas, TemporadaSerializer, request)
        if "error" in paginated_data:
            return Response(paginated_data, status=status.HTTP_400_BAD_REQUEST)
        return Response(paginated_data, status=status.HTTP_200_OK)


class TemporadaUpdateView(APIView):
    def patch(self, request, pk):
        temporada = Temporada.objects.filter(pk=pk).first()
        if not temporada:
            return Response({"error": "Temporada no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TemporadaSerializer(temporada, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Temporada actualizada correctamente", "temporada": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemporadaDeleteView(APIView):
    def delete(self, request, pk):
        temporada = Temporada.objects.filter(pk=pk).first()
        if not temporada:
            return Response({"error": "Temporada no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        temporada.delete()
        return Response({"mensaje": "Temporada eliminada correctamente"}, status=status.HTTP_200_OK)
