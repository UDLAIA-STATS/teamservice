from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import IntegrityError
from .models import Equipo, Partido, Torneo, Temporada, TorneoPartido
from .serializers import (
    EquipoSerializer,
    TorneoSerializer,
    PartidoSerializer,
    TemporadaSerializer,
    TorneoPartidoSerializer
)


# class SoloAutenticados(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.is_authenticated

class EquipoListCreateView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

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
        try:
            return Equipo.objects.get(pk=pk)
        except Partido.DoesNotExist:
            return None

    def get(self, request, pk):
        try:
            equipo = self.get_object(pk)
            if not equipo:
                return Response({"error": "Equipo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            return Response(EquipoSerializer(equipo).data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EquipoSearchByNameView(APIView):

    def get_object(self, name):
        try:
            return Equipo.objects.get(nombreequipo=name)
        except Partido.DoesNotExist:
            return None

    def get(self, request, name):
        try:
            equipo = self.get_object(name)
            if not equipo:
                return Response({"error": "Equipo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            return Response(EquipoSerializer(equipo).data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class EquipoAllView(APIView):
    def get(self, request):
        try:
            equipos = Equipo.objects.all()
            serializer = EquipoSerializer(equipos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PartidoListCreateView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            serializer = PartidoSerializer(data=request.data)
            if serializer.is_valid():
                partido = serializer.save()
                return Response(
                    {
                        "mensaje": "Partido creado correctamente",
                        "partido": PartidoSerializer(partido).data
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PartidoDetailView(APIView):

    def get_object(self, pk):
        try:
            return Partido.objects.get(pk=pk)
        except Partido.DoesNotExist:
            return None

    def get(self, request, pk):
        try:
            partido = self.get_object(pk)
            if not partido:
                return Response({"error": "Partido no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            return Response(PartidoSerializer(partido).data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PartidoAllView(APIView):
    def get(self, request):
        try:
            partidos = Partido.objects.all()
            serializer = PartidoSerializer(partidos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TorneoListCreateView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            serializer = TorneoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                        "mensaje": "Torneo creado correctamente",
                        "torneo": serializer.data
                    },
                    status=status.HTTP_201_CREATED
                    )
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TorneoDetailView(APIView):

    def get_object(self, pk):
        try:
            return Torneo.objects.get(pk=pk)
        except Torneo.DoesNotExist:
            return None

    def get(self, request, pk):
        try:
            torneo = self.get_object(pk)
            if not torneo:
                return Response({"error": "Torneo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            return Response(TorneoSerializer(torneo).data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TorneoAllView(APIView):
    def get(self, request):
        try:
            torneos = Torneo.objects.all()
            serializer = TorneoSerializer(torneos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TemporadaListCreateView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            serializer = TemporadaSerializer(data=request.data)
            if serializer.is_valid():
                temporada = serializer.save()
                return Response({"mensaje": "Temporada creada correctamente", "temporada": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class TemporadaDetailView(APIView):

    def get_object(self, pk):
        try:
            return Temporada.objects.get(pk=pk)
        except Temporada.DoesNotExist:
            return None

    def get(self, request, pk):
        try:
            temporada = self.get_object(pk)
            if not temporada:
                return Response({"error": "Temporada no encontrada"}, status=status.HTTP_404_NOT_FOUND)
            return Response(TemporadaSerializer(temporada).data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TemporadaAllView(APIView):
    def get(self, request):
        try:
            temporadas = Temporada.objects.all()
            serializer = TemporadaSerializer(temporadas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TorneoPartidoListCreateView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            serializer = TorneoPartidoSerializer(data=request.data)
            if serializer.is_valid():
                relacion = serializer.save()
                return Response(
                    {"mensaje": "Partido asignado al torneo correctamente", "relacion": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TorneoPartidoDetailView(APIView):

    def get_object(self, torneo_id, partido_id):
        try:
            return TorneoPartido.objects.get(idTorneo=torneo_id, idPartido=partido_id)
        except TorneoPartido.DoesNotExist:
            return None

    def get(self, request, torneo_id, partido_id):
        try:
            relacion = self.get_object(torneo_id, partido_id)
            if not relacion:
                return Response({"error": "Relación no encontrada"}, status=status.HTTP_404_NOT_FOUND)
            return Response(TorneoPartidoSerializer(relacion).data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TorneoPartidoAllView(APIView):
    def get(self, request):
        try:
            relaciones = TorneoPartido.objects.all()
            serializer = TorneoPartidoSerializer(relaciones, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EquipoUpdateView(APIView):
    def patch(self, request, pk):
        try:
            equipo = Equipo.objects.get(pk=pk)
            if not equipo:
                return Response({"error": "Equipo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            serializer = EquipoSerializer(equipo, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"mensaje": "Equipo actualizado correctamente", "equipo": serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PartidoUpdateView(APIView):
    def patch(self, request, pk):
        try:
            partido = Partido.objects.get(pk=pk)
            if not partido:
                return Response({"error": "Partido no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            serializer = PartidoSerializer(partido, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"mensaje": "Partido actualizado correctamente", "partido": serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TorneoUpdateView(APIView):
    def patch(self, request, pk):
        try:
            torneo = Torneo.objects.get(pk=pk)
            if not torneo:
                return Response({"error": "Torneo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            serializer = TorneoSerializer(torneo, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"mensaje": "Torneo actualizado correctamente", "torneo": serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TemporadaUpdateView(APIView):
    def patch(self, request, pk):
        try:
            temporada = Temporada.objects.get(pk=pk)
            if not temporada:
                return Response({"error": "Temporada no encontrada"}, status=status.HTTP_404_NOT_FOUND)

            serializer = TemporadaSerializer(temporada, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"mensaje": "Temporada actualizada correctamente", "temporada": serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TorneoPartidoUpdateView(APIView):
    def patch(self, request, torneo_id, partido_id):
        try:
            relacion = TorneoPartido.objects.get(idTorneo=torneo_id, idPartido=partido_id)
            serializer = TorneoPartidoSerializer(relacion, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"mensaje": "Relación actualizada correctamente", "relacion": serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TorneoPartido.DoesNotExist:
            return Response({"error": "Relación no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
