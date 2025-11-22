from rest_framework import serializers
from torneo.models import Partido, equipo

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
        
        torneo = self.instance.idtorneo if self.instance else attrs.get('idtorneo')
        temporada = self.instance.idtemporada if self.instance else attrs.get('idtemporada')
        fecha_partido = attrs.get('fechapartido', self.instance.fechapartido if self.instance else None)
        if torneo and fecha_partido:
            if not (torneo.fechainiciotorneo <= fecha_partido <= temporada.fechafintorneo):
                raise serializers.ValidationError("La fecha del partido debe estar dentro del rango del torneo.")

        equipo_local = attrs.get('idequipolocal', self.instance.idequipolocal if self.instance else None)
        equipo_visitante = attrs.get('idequipovisitante', self.instance.idequipovisitante if self.instance else None)

        if not equipo_local and not equipo_visitante:
            raise serializers.ValidationError("Debe especificar al menos un equipo (local o visitante).")
        
        if equipo_local == equipo_visitante:
            raise serializers.ValidationError("Un equipo no puede enfrentarse a sí mismo.")

        return attrs
