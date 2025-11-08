import base64
from django.db import IntegrityError
from rest_framework import serializers
from .models import (
    Institucion,
    Equipo,
    Torneo,
    Temporada,
    Partido
)


# ============================================================
# INSTITUCIÓN
# ============================================================
class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = ['idinstitucion', 'nombreinstitucion', 'institucionactiva']

    def validate_nombreinstitucion(self, value):
        if self.instance is None and Institucion.objects.filter(nombreinstitucion=value).exists():
            raise serializers.ValidationError("Ya existe una institución con ese nombre.")
        return value


# ============================================================
# EQUIPO
# ============================================================
class EquipoSerializer(serializers.ModelSerializer):
    institucion_nombre = serializers.StringRelatedField(source='idinstitucion', read_only=True)
    imagenequipo = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Equipo
        fields = ['idequipo', 'nombreequipo', 'imagenequipo', 'equipoactivo', 'idinstitucion', 'institucion_nombre']

    def validate_nombreequipo(self, value):
        if self.instance is None and Equipo.objects.filter(nombreequipo=value).exists():
            raise serializers.ValidationError("Ya existe un equipo con ese nombre.")
        return value

    # def to_internal_value(self, data):
    #     """Permite recibir imagen en base64."""
    #     internal = super().to_internal_value(data)
    #     imagen = data.get('imagenequipo')
    #     if isinstance(imagen, str) and imagen.startswith("data:image"):
    #         try:
    #             _, base64_data = imagen.split(',', 1)
    #             internal['imagenequipo'] = base64.b64decode(base64_data)
    #         except Exception:
    #             raise serializers.ValidationError({"imagenequipo": "Formato Base64 inválido."})
    #     return internal


# ============================================================
# TEMPORADA
# ============================================================
class TemporadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temporada
        fields = [
            'idtemporada',
            'nombretemporada',
            'descripciontemporada',
            'tipotemporada',
            'fechainiciotemporada',
            'fechafintemporada',
            'temporadaactiva'
        ]

    def validate(self, attrs):
        nombre = attrs.get("nombretemporada")
        if self.instance is None and Temporada.objects.filter(nombretemporada=nombre).exists():
            raise serializers.ValidationError("Ya existe una temporada con ese nombre.")
        return attrs


# ============================================================
# TORNEO
# ============================================================
class TorneoSerializer(serializers.ModelSerializer):
    temporada_nombre = serializers.StringRelatedField(source='idtemporada', read_only=True)

    class Meta:
        model = Torneo
        fields = [
            'idtorneo',
            'nombretorneo',
            'descripciontorneo',
            'fechainiciotorneo',
            'fechafintorneo',
            'torneoactivo',
            'idtemporada',
            'temporada_nombre'
        ]

    def validate_nombretorneo(self, value):
        if self.instance is None and Torneo.objects.filter(nombretorneo=value).exists():
            raise serializers.ValidationError("Ya existe un torneo con ese nombre.")
        return value


# ============================================================
# PARTIDO
# ============================================================
class PartidoSerializer(serializers.ModelSerializer):
    equipo_local_nombre = serializers.StringRelatedField(source='idequipolocal', read_only=True)
    equipo_visitante_nombre = serializers.StringRelatedField(source='idequipovisitante', read_only=True)
    torneo_nombre = serializers.StringRelatedField(source='idtorneo', read_only=True)
    temporada_nombre = serializers.StringRelatedField(source='idtemporada', read_only=True)

    class Meta:
        model = Partido
        fields = [
            'idpartido',
            'fechapartido',
            'marcadorequipolocal',
            'marcadorequipovisitante',
            'idequipolocal',
            'idequipovisitante',
            'idtorneo',
            'idtemporada',
            'equipo_local_nombre',
            'equipo_visitante_nombre',
            'torneo_nombre',
            'temporada_nombre'
        ]

    def validate(self, attrs):
        if attrs.get('idequipolocal') == attrs.get('idequipovisitante'):
            raise serializers.ValidationError("Un equipo no puede enfrentarse a sí mismo.")
        return attrs
