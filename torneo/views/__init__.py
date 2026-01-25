from .pagination import paginate_queryset as paginate_queryset
from .equipo_view import (
    EquipoListCreateView as EquipoListCreateView,
    EquipoDetailView as EquipoDetailView,
    EquipoSearchByNameView as EquipoSearchByNameView,
    EquipoAllView as EquipoAllView,
    EquipoUpdateView as EquipoUpdateView,
    EquipoDeleteView as EquipoDeleteView,
)
from .institucion_view import (
    InstitucionListCreateView as InstitucionListCreateView,
    InstitucionDetailView as InstitucionDetailView,
    InstitucionAllView as InstitucionAllView,
    InstitucionUpdateView as InstitucionUpdateView,
    InstitucionDeleteView as InstitucionDeleteView,
)
from .partido_view import (
    PartidoListCreateView as PartidoListCreateView,
    PartidoDetailView as PartidoDetailView,
    PartidoAllView as PartidoAllView,
    PartidoUpdateView as PartidoUpdateView,
    PartidoDeleteView as PartidoDeleteView,
)
from .torneo_view import (
    TorneoListCreateView as TorneoListCreateView,
    TorneoDetailView as TorneoDetailView,
    TorneoAllView as TorneoAllView,
    TorneoUpdateView as TorneoUpdateView,
    TorneoDeleteView as TorneoDeleteView,
)
from .temporada_view import (
    TemporadaListCreateView as TemporadaListCreateView,
    TemporadaDetailView as TemporadaDetailView,
    TemporadaAllView as TemporadaAllView,
    TemporadaUpdateView as TemporadaUpdateView,
    TemporadaDeleteView as TemporadaDeleteView,
)
