from django.urls import path
from .views import (
    # EQUIPO
    EquipoListCreateView,
    EquipoDetailView,
    EquipoAllView,
    EquipoSearchByNameView,
    EquipoUpdateView,
    EquipoDeleteView,

    # INSTITUCIÓN
    InstitucionListCreateView,
    InstitucionDetailView,
    InstitucionAllView,
    InstitucionUpdateView,
    InstitucionDeleteView,

    # PARTIDO
    PartidoListCreateView,
    PartidoDetailView,
    PartidoAllView,
    PartidoUpdateView,
    PartidoDeleteView,

    # TORNEO
    TorneoListCreateView,
    TorneoDetailView,
    TorneoAllView,
    TorneoUpdateView,
    TorneoDeleteView,

    # TEMPORADA
    TemporadaListCreateView,
    TemporadaDetailView,
    TemporadaAllView,
    TemporadaUpdateView,
    TemporadaDeleteView,
)

urlpatterns = [
    # ================= EQUIPOS =================
    path('equipos/', EquipoListCreateView.as_view(), name='equipo-list-create'),
    path('equipos/all/', EquipoAllView.as_view(), name='equipo-all'),
    path('equipos/<int:pk>/', EquipoDetailView.as_view(), name='equipo-detail'),
    path('equipos/<int:pk>/update/', EquipoUpdateView.as_view(), name='equipo-update'),
    path('equipos/<int:pk>/delete/', EquipoDeleteView.as_view(), name='equipo-delete'),
    path('equipos/search/<str:name>/', EquipoSearchByNameView.as_view(), name='equipo-search'),

    # ================= PARTIDOS =================
    path('partidos/', PartidoListCreateView.as_view(), name='partido-list-create'),
    path('partidos/all/', PartidoAllView.as_view(), name='partido-all'),
    path('partidos/<int:pk>/', PartidoDetailView.as_view(), name='partido-detail'),
    path('partidos/<int:pk>/update/', PartidoUpdateView.as_view(), name='partido-update'),
    path('partidos/<int:pk>/delete/', PartidoDeleteView.as_view(), name='partido-delete'),

    # ================= TORNEOS =================
    path('torneos/', TorneoListCreateView.as_view(), name='torneo-list-create'),
    path('torneos/all/', TorneoAllView.as_view(), name='torneo-all'),
    path('torneos/<int:pk>/', TorneoDetailView.as_view(), name='torneo-detail'),
    path('torneos/<int:pk>/update/', TorneoUpdateView.as_view(), name='torneo-update'),
    path('torneos/<int:pk>/delete/', TorneoDeleteView.as_view(), name='torneo-delete'),

    # ================= TEMPORADAS =================
    path('temporadas/', TemporadaListCreateView.as_view(), name='temporada-list-create'),
    path('temporadas/all/', TemporadaAllView.as_view(), name='temporada-all'),
    path('temporadas/<int:pk>/', TemporadaDetailView.as_view(), name='temporada-detail'),
    path('temporadas/<int:pk>/update/', TemporadaUpdateView.as_view(), name='temporada-update'),
    path('temporadas/<int:pk>/delete/', TemporadaDeleteView.as_view(), name='temporada-delete'),

    # ================= INSTITUCIONES =================
    path('instituciones/', InstitucionListCreateView.as_view(), name='institucion-list-create'),
    path('instituciones/all/', InstitucionAllView.as_view(), name='institucion-all'),
    path('instituciones/<int:pk>/', InstitucionDetailView.as_view(), name='institucion-detail'),
    path('instituciones/<int:pk>/update/', InstitucionUpdateView.as_view(), name='institucion-update'),
    path('instituciones/<int:pk>/delete/', InstitucionDeleteView.as_view(), name='institucion-delete'),
]
