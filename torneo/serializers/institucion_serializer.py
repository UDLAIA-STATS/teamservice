from rest_framework import serializers
from torneo.models import Institucion


class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = ["idinstitucion", "nombreinstitucion", "institucionactiva"]

    def validate_nombreinstitucion(self, value):
        """
        Valida que una institución con el nombre especificado ya existe.
        """

        if (
            self.instance is None
            and Institucion.objects.filter(nombreinstitucion=value).exists()
        ):
            raise serializers.ValidationError(
                "Ya existe una institución con ese nombre."
            )
        return value
