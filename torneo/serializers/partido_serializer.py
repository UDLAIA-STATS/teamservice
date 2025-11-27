from rest_framework import serializers
from django.db.models import Q
from torneo.models import Partido

class PartidoSerializer(serializers.ModelSerializer):
    equipo_local_nombre = serializers.StringRelatedField(source='idequipolocal', read_only=True)
    equipo_visitante_nombre = serializers.StringRelatedField(source='idequipovisitante', read_only=True)
    torneo_nombre = serializers.StringRelatedField(source='idtorneo', read_only=True)
    temporada_nombre = serializers.StringRelatedField(source='idtemporada', read_only=True)
    partidosubido = serializers.BooleanField(default=False)

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
            'temporada_nombre',
            'partidosubido'
        ]

    def validate(self, attrs):
        """
        Validates the given attributes for a partido.

        Checks that the local and visitant team are not the same, and that the date of the party is within the range of the tournament.

        Also checks that at least one of the two teams is specified.

        Raises a ValidationError if any of the checks fail.

        :param attrs: The attributes to validate.
        :return: The validated attributes.
        :raises: ValidationError
        """
        # Equipos
        equipo_local = attrs.get('idequipolocal', self.instance.idequipolocal if self.instance else None)
        equipo_visitante = attrs.get('idequipovisitante', self.instance.idequipovisitante if self.instance else None)

        if equipo_local == equipo_visitante:
            raise serializers.ValidationError("Un equipo no puede enfrentarse a sí mismo.")

        # Torneo y fecha
        torneo = self.instance.idtorneo if self.instance else attrs.get('idtorneo')
        fecha_partido = attrs.get('fechapartido', self.instance.fechapartido if self.instance else None)
        
        if torneo and fecha_partido:
            if not (torneo.fechainiciotorneo <= fecha_partido <= torneo.fechafintorneo):
                raise serializers.ValidationError("La fecha del partido debe estar dentro del rango del torneo.")
            conflicting_partidos = Partido.objects.filter(
                Q(fechapartido=fecha_partido) & (
                    Q(idequipolocal=equipo_local) | Q(idequipovisitante=equipo_local) |
                    Q(idequipolocal=equipo_visitante) | Q(idequipovisitante=equipo_visitante)
                )
            )
            if self.instance:
                conflicting_partidos = conflicting_partidos.exclude(idpartido=self.instance.idpartido)
            if conflicting_partidos.exists():
                raise serializers.ValidationError("Un equipo no puede tener más de un partido en la misma fecha.")

        if not equipo_local and not equipo_visitante:
            raise serializers.ValidationError("Debe especificar al menos un equipo (local o visitante).")
        


        return attrs