import base64
from django.db import IntegrityError
from rest_framework import serializers
from .models import Equipo, Partido, Torneo, TorneoPartido, Temporada


import base64
from django.db import IntegrityError
from rest_framework import serializers
from .models import Equipo

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = ['idequipo', 'nombreequipo', 'logoequipo']

    def validate(self, attrs):
        # Evitar duplicados en la creación
        nombre = attrs.get("nombreequipo")
        if self.instance is None and Equipo.objects.filter(nombreequipo=nombre).exists():
            raise serializers.ValidationError("Ya existe un equipo con ese nombre.")
        return attrs

    def create(self, validated_data):
        try:
            # Decodificar imagen si viene en base64
            logoequipo = validated_data.get('logoequipo')
            if isinstance(logoequipo, str) and logoequipo.startswith("data:image"):
                header, base64_data = logoequipo.split(',', 1)
                validated_data['logoequipo'] = base64.b64decode(base64_data)

            equipo = Equipo.objects.create(**validated_data)
            return equipo
        except IntegrityError:
            raise serializers.ValidationError({
                "error": f"Ya existe un equipo con el nombre: {validated_data.get('nombreequipo')}"
            })
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

    def update(self, instance, validated_data):
        try:
            if 'nombreequipo' in validated_data:
                instance.nombreequipo = validated_data['nombreequipo']

            logoequipo = validated_data.get('logoequipo')
            if isinstance(logoequipo, str) and logoequipo.startswith("data:image"):
                try:
                    _, base64_data = logoequipo.split(',', 1)
                    instance.logoequipo = base64.b64decode(base64_data)
                except Exception as e:
                    raise serializers.ValidationError({"error": f"Formato Base64 inválido: {e}"})
            elif logoequipo is not None:
                instance.logoequipo = logoequipo

            instance.save()
            return instance
        except IntegrityError:
            raise serializers.ValidationError({
                "error": f"El equipo con el nombre {instance.nombreequipo} no pudo ser actualizado."
            })
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})


class PartidoSerializer(serializers.ModelSerializer): # type: ignore
    equipo_local = serializers.StringRelatedField(source='idequipolocal', read_only=True)
    equipo_visitante = serializers.StringRelatedField(source='idequipovisitante', read_only=True)

    class Meta:
        model = Partido
        fields = [
            'idpartido',
            'marcadorequipolocal',
            'marcadorequipovisitante',
            'fechapartido',
            'tipopartido',
            'idequipolocal',
            'idequipovisitante',
            'equipo_local',
            'equipo_visitante'
        ]

    def validate(self, attrs):
        # Evita que el mismo equipo sea local y visitante
        if attrs.get('idequipolocal') == attrs.get('idequipovisitante'):
            raise serializers.ValidationError("Un equipo no puede jugar contra sí mismo.") # type: ignore
        return attrs
    
    def create(self, validated_data):
        try:
            partido = Partido.objects.create(
                marcadorequipolocal=validated_data.get('marcadorequipolocal'),
                marcadorequipovisitante=validated_data.get('marcadorequipovisitante'),
                fechapartido=validated_data.get('fechapartido'),
                tipopartido=validated_data.get('tipopartido'),
                idequipolocal=validated_data.get('idequipolocal'),
                idequipovisitante=validated_data.get('idequipovisitante')
            )
            return partido
        except ValueError as e:
            raise serializers.ValidationError({"error": str(e)})
        except IntegrityError as e:
            raise serializers.ValidationError({"error": "No se pudo crear el partido debido a un conflicto de integridad."})

    def update(self, instance, validated_data):
        try:
            instance.marcadorequipolocal = validated_data.get('marcadorequipolocal', instance.marcadorequipolocal)
            instance.marcadorequipovisitante = validated_data.get('marcadorequipovisitante', instance.marcadorequipovisitante)
            instance.fechapartido = validated_data.get('fechapartido', instance.fechapartido)
            instance.tipopartido = validated_data.get('tipopartido', instance.tipopartido)
            instance.idequipolocal = validated_data.get('idequipolocal', instance.idequipolocal)
            instance.idequipovisitante = validated_data.get('idequipovisitante', instance.idequipovisitante)
            instance.save()
            return instance
        except ValueError as e:
            raise serializers.ValidationError({"error": str(e)})
        except IntegrityError as e:
            raise serializers.ValidationError({"error": "No se pudo actualizar el partido debido a un conflicto de integridad."})


class TorneoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Torneo
        fields = ['idtorneo', 'nombretorneo', 'descripciontorneo']

    def validate(self, attrs):
        if self.instance is None and Torneo.objects.filter(nombretorneo=attrs).exists():
            raise serializers.ValidationError("Ya existe un torneo con ese nombre.")
        return attrs
    
    def create(self, validated_data):
        try:
            torneo = Torneo.objects.create(
                nombretorneo=validated_data.get('nombretorneo'),
                descripciontorneo=validated_data.get('descripciontorneo')
            )
            return torneo
        except ValueError as e:
            raise serializers.ValidationError({"error": str(e)})
        except IntegrityError as e:
            raise serializers.ValidationError({"error": f"Ya existe un torneo con el nombre: {validated_data.get('nombretorneo')}"})
        
    def update(self, instance, validated_data):
        try:
            instance.nombretorneo = validated_data.get('nombretorneo', instance.nombretorneo)
            instance.descripciontorneo = validated_data.get('descripciontorneo', instance.descripciontorneo)
            instance.save()
            return instance
        except ValueError as e:
            raise serializers.ValidationError({"error": str(e)})
        except IntegrityError as e:
            raise serializers.ValidationError({"error": f"El torneo con el nombre {instance.nombretorneo} no pudo ser actualizado."})


class TemporadaSerializer(serializers.ModelSerializer):
    torneo_nombre = serializers.StringRelatedField(source='idtorneo', read_only=True)

    class Meta:
        model = Temporada
        fields = ['idtemporada', 'nombretemporada', 'tipotemporada', 'idtorneo', 'torneo_nombre']

    def validate(self, attrs):
        # Evita duplicar nombre dentro del mismo torneo
        torneo = attrs.get('idtorneo')
        nombre = attrs.get('nombretemporada')
        if self.instance is None and Temporada.objects.filter(nombretemporada=nombre, idtorneo=torneo).exists():
            raise serializers.ValidationError("Ya existe una temporada con ese nombre en el torneo seleccionado.")
        return attrs
    
    def create(self, validated_data):
        try:
            temporada = Temporada.objects.create(
                nombretemporada=validated_data.get('nombretemporada'),
                tipotemporada=validated_data.get('tipotemporada'),
                idtorneo=validated_data.get('idtorneo')
            )
            return temporada
        except ValueError as e:
            raise serializers.ValidationError({"error": str(e)})
        except IntegrityError as e:
            raise serializers.ValidationError({"error": "No se pudo crear la temporada debido a un conflicto de integridad."})


class TorneoPartidoSerializer(serializers.ModelSerializer):
    torneo = serializers.StringRelatedField(source='idtorneo', read_only=True)
    partido = serializers.StringRelatedField(source='idpartido', read_only=True)

    class Meta:
        model = TorneoPartido
        fields = ['idtorneo', 'idpartido', 'torneo', 'partido']

    def validate(self, attrs):
        # Evita registrar un partido dos veces en el mismo torneo
        if TorneoPartido.objects.filter(
            idtorneo=attrs['idtorneo'],
            idpartido=attrs['idpartido']
        ).exists():
            raise serializers.ValidationError("Ese partido ya está asignado a este torneo.")
        return attrs
    
    def create(self, validated_data):
        try:
            torneo_partido = TorneoPartido.objects.create(
                idtorneo=validated_data.get('idtorneo'),
                idpartido=validated_data.get('idpartido')
            )
            return torneo_partido
        except ValueError as e:
            raise serializers.ValidationError({"error": str(e)})
        except IntegrityError as e:
            raise serializers.ValidationError({"error": "No se pudo asignar el partido al torneo debido a un conflicto de integridad."})
        
    def update(self, instance, validated_data):
        try:
            instance.idtorneo = validated_data.get('idtorneo', instance.idtorneo)
            instance.idpartido = validated_data.get('idpartido', instance.idpartido)
            instance.save()
            return instance
        except ValueError as e:
            raise serializers.ValidationError({"error": str(e)})
        except IntegrityError as e:
            raise serializers.ValidationError({"error": "No se pudo actualizar la asignación debido a un conflicto de integridad."})
