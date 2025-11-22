from rest_framework import serializers
from torneo.models import Torneo, Temporada

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
    
    def validate(self, attrs):
        temporada = None

        if 'idtemporada' in attrs:
            temporada = attrs['idtemporada']
        elif self.instance:
            temporada = self.instance.idtemporada

        if temporada is None:
            raise serializers.ValidationError("El torneo debe estar asociado a una temporada.")
        
        fecha_inicio = attrs.get('fechainiciotorneo', self.instance.fechainiciotorneo if self.instance else None)
        fecha_fin = attrs.get('fechafintorneo', self.instance.fechafintorneo if self.instance else None)

        if fecha_inicio is None or fecha_fin is None:
            raise serializers.ValidationError("Debe especificar fecha de inicio y fin del torneo.")

        if not (temporada.fechainiciotemporada <= fecha_inicio <= temporada.fechafintemporada):
            raise serializers.ValidationError("La fecha de inicio debe estar dentro del rango de la temporada.")
        if not (temporada.fechainiciotemporada <= fecha_fin <= temporada.fechafintemporada):
            raise serializers.ValidationError("La fecha de fin debe estar dentro del rango de la temporada.")

        if fecha_inicio > fecha_fin:
            raise serializers.ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")

        return attrs
