from django.db import models

from .institucion import Institucion


class Equipo(models.Model):
    idequipo = models.AutoField(primary_key=True)
    idinstitucion = models.ForeignKey(
        Institucion, on_delete=models.CASCADE, db_column="idinstitucion"
    )
    nombreequipo = models.CharField(max_length=250)
    imagenequipo = models.BinaryField(null=True, blank=True)
    equipoactivo = models.BooleanField(default=True)

    class Meta:
        db_table = "equipo"

    def __str__(self):
        return self.nombreequipo
