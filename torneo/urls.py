from django.urls import path
import torneo.views as views

urlpatterns = [
    # ================= EQUIPOS =================
    path("equipos/", views.EquipoListCreateView.as_view(), name="equipo-list-create"),
    path("equipos/all/", views.EquipoAllView.as_view(), name="equipo-all"),
    path("equipos/<int:pk>/", views.EquipoDetailView.as_view(), name="equipo-detail"),
    path("equipos/<int:pk>/update/", views.EquipoUpdateView.as_view(), name="equipo-update"),
    path("equipos/<int:pk>/delete/", views.EquipoDeleteView.as_view(), name="equipo-delete"),
    path(
        "equipos/search/<str:name>/",
        views.EquipoSearchByNameView.as_view(),
        name="equipo-search",
    ),
    # ================= PARTIDOS =================
    path("partidos/", views.PartidoListCreateView.as_view(), name="partido-list-create"),
    path("partidos/all/", views.PartidoAllView.as_view(), name="partido-all"),
    path("partidos/<int:pk>/", views.PartidoDetailView.as_view(), name="partido-detail"),
    path(
        "partidos/<int:pk>/update/", views.PartidoUpdateView.as_view(), name="partido-update"
    ),
    path(
        "partidos/<int:pk>/delete/", views.PartidoDeleteView.as_view(), name="partido-delete"
    ),
    # ================= TORNEOS =================
    path("torneos/", views.TorneoListCreateView.as_view(), name="torneo-list-create"),
    path("torneos/all/", views.TorneoAllView.as_view(), name="torneo-all"),
    path("torneos/<int:pk>/", views.TorneoDetailView.as_view(), name="torneo-detail"),
    path("torneos/<int:pk>/update/", views.TorneoUpdateView.as_view(), name="torneo-update"),
    path("torneos/<int:pk>/delete/", views.TorneoDeleteView.as_view(), name="torneo-delete"),
    # ================= TEMPORADAS =================
    path(
        "temporadas/", views.TemporadaListCreateView.as_view(), name="temporada-list-create"
    ),
    path("temporadas/all/", views.TemporadaAllView.as_view(), name="temporada-all"),
    path(
        "temporadas/<int:pk>/", views.TemporadaDetailView.as_view(), name="temporada-detail"
    ),
    path(
        "temporadas/<int:pk>/update/",
        views.TemporadaUpdateView.as_view(),
        name="temporada-update",
    ),
    path(
        "temporadas/<int:pk>/delete/",
        views.TemporadaDeleteView.as_view(),
        name="temporada-delete",
    ),
    # ================= INSTITUCIONES =================
    path(
        "instituciones/",
        views.InstitucionListCreateView.as_view(),
        name="institucion-list-create",
    ),
    path("instituciones/all/", views.InstitucionAllView.as_view(), name="institucion-all"),
    path(
        "instituciones/<int:pk>/",
        views.InstitucionDetailView.as_view(),
        name="institucion-detail",
    ),
    path(
        "instituciones/<int:pk>/update/",
        views.InstitucionUpdateView.as_view(),
        name="institucion-update",
    ),
    path(
        "instituciones/<int:pk>/delete/",
        views.InstitucionDeleteView.as_view(),
        name="institucion-delete",
    ),
]
