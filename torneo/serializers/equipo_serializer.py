import base64
from rest_framework import serializers
from torneo.models import Equipo


class EquipoSerializer(serializers.ModelSerializer):
    institucion_nombre = serializers.StringRelatedField(
        source="idinstitucion", read_only=True
    )

    class Meta:
        model = Equipo
        fields = [
            "idequipo",
            "nombreequipo",
            "imagenequipo",
            "equipoactivo",
            "idinstitucion",
            "institucion_nombre",
        ]

    def validate_nombreequipo(self, value):
        """
        Valida que un equipo con el nombre especificado ya existe.
        """
        if self.instance is None and Equipo.objects.filter(nombreequipo=value).exists():
            raise serializers.ValidationError("Ya existe un equipo con ese nombre.")
        return value

    def to_internal_value(self, data):
        """
        Convierte el valor de 'imagenequipo' en base64 a bytes.
        Si el valor es None o una cadena vacía, se deja como None.
        Si el valor es una cadena que comienza con "data:image", se intenta
        convertir a bytes. Si no se puede parsear, se devuelve un
        ValidationError con el mensaje "Formato Base64 inválido.".
        """
        internal = super().to_internal_value(data)
        imagen = data.get("imagenequipo")

        if not imagen:
            return internal

        # Si viene como base64, la convertimos a bytes
        if isinstance(imagen, str) and imagen.startswith("data:image"):
            try:
                _, base64_data = imagen.split(",", 1)
                internal["imagenequipo"] = base64.b64decode(base64_data)
            except Exception:
                raise serializers.ValidationError(
                    {"imagenequipo": "Formato Base64 inválido."}
                )
        elif imagen is None or imagen == "":
            internal["imagenequipo"] = None

        return internal

    def to_representation(self, instance):
        """
        Convierte una instancia de Equipo en un objeto JSON.
        Se convierte el campo 'imagenequipo' de bytes a base64
        para enviar al frontend. Si el campo es None o una cadena
        vacía, se deja como None.
        """
        rep = super().to_representation(instance)
        # Convertimos los bytes a base64 para enviar al frontend
        if instance.imagenequipo:
            rep["imagenequipo"] = (
                f"data:image/png;base64,{base64.b64encode(instance.imagenequipo).decode('utf-8')}"
            )
        else:
            rep["imagenequipo"] = None
        return rep
