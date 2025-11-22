from django.db import IntegrityError
from rest_framework import serializers
from torneo.models import Institucion

class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = ['idinstitucion', 'nombreinstitucion', 'institucionactiva']

    def validate_nombreinstitucion(self, value):
        if self.instance is None and Institucion.objects.filter(nombreinstitucion=value).exists():
            raise serializers.ValidationError("Ya existe una institución con ese nombre.")
        return value

