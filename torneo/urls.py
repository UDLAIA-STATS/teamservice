from django.urls import path
from .views import (
    EquipoDetailView,
    EquipoListCreateView,
    EquipoAllView,
    PartidoDetailView,
    PartidoListCreateView,
    PartidoAllView,
    TorneoDetailView,
    TorneoListCreateView,
    TorneoAllView,
    TemporadaDetailView,
    TemporadaListCreateView,
    TemporadaAllView,
    TorneoPartidoListCreateView,
    TorneoPartidoDetailView,
    TorneoPartidoAllView,
    EquipoUpdateView,
    TorneoUpdateView,
    PartidoUpdateView,
    TemporadaUpdateView
)

urlpatterns = [
    path('equipos/', EquipoListCreateView.as_view(), name='equipo-list-create'),
    path('equipos/<int:pk>/', EquipoDetailView.as_view(), name='equipo-detail'),
    path('equipos/all/', EquipoAllView.as_view(), name='equipo-all'),
    path('equipos/<int:pk>/update/', EquipoUpdateView.as_view(), name='equipo-update'),

    path('partidos/', PartidoListCreateView.as_view(), name='partido-list-create'),
    path('partidos/<int:pk>/', PartidoDetailView.as_view(), name='partido-detail'),
    path('partidos/all/', PartidoAllView.as_view(), name='partido-all'),
    path('partidos/<int:pk>/update/', PartidoUpdateView.as_view(), name='partido-update'),

    path('torneos/', TorneoListCreateView.as_view(), name='torneo-list-create'),
    path('torneos/<int:pk>/', TorneoDetailView.as_view(), name='torneo-detail'),
    path('torneos/all/', TorneoAllView.as_view(), name='torneo-all'),
    path('torneos/<int:pk>/update/', TorneoUpdateView.as_view(), name='torneo-update'),

    path('temporadas/', TemporadaListCreateView.as_view(), name='temporada-list-create'),
    path('temporadas/<int:pk>/', TemporadaDetailView.as_view(), name='temporada-detail'),
    path('temporadas/all/', TemporadaAllView.as_view(), name='temporada-all'),
    path('temporadas/<int:pk>/update/', TemporadaUpdateView.as_view(), name='temporada-update'),

    path('torneo-partidos/', TorneoPartidoListCreateView.as_view(), name='torneo-partido-list-create'),
    path(
        'torneo-partidos/<int:torneo_id>/<int:partido_id>/',
        TorneoPartidoDetailView.as_view(),
        name='torneo-partido-detail'
    ),
    path('torneo-partidos/all/', TorneoPartidoAllView.as_view(), name='torneo-partido-all'),
]
