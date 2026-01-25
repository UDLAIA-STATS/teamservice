from rest_framework import serializers
from torneo.models import Temporada


class TemporadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temporada
        fields = [
            "idtemporada",
            "nombretemporada",
            "descripciontemporada",
            "tipotemporada",
            "fechainiciotemporada",
            "fechafintemporada",
            "temporadaactiva",
        ]

    def validate(self, attrs):
        """
        Valida que no existe una temporada con el nombre especificado.
        Levanta una excepcion si ya existe una temporada con ese nombre.
        """
        nombre = attrs.get("nombretemporada")
        if (
            self.instance is None
            and Temporada.objects.filter(nombretemporada=nombre).exists()
        ):
            raise serializers.ValidationError("Ya existe una temporada con ese nombre.")
        return attrs
