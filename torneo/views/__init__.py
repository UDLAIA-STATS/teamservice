from .pagination import paginate_queryset
from .equipo_view import EquipoListCreateView, EquipoDetailView, EquipoSearchByNameView, EquipoAllView, EquipoUpdateView, EquipoDeleteView
from .institucion_view import InstitucionListCreateView, InstitucionDetailView, InstitucionAllView, InstitucionUpdateView, InstitucionDeleteView
from .partido_view import PartidoListCreateView, PartidoDetailView, PartidoAllView, PartidoUpdateView, PartidoDeleteView
from .torneo_view import TorneoListCreateView, TorneoDetailView, TorneoAllView, TorneoUpdateView, TorneoDeleteView
from .temporada_view import TemporadaListCreateView, TemporadaDetailView, TemporadaAllView, TemporadaUpdateView, TemporadaDeleteView