from django.db import models


class Temporada(models.Model):
    idtemporada = models.AutoField(primary_key=True)
    nombretemporada = models.CharField(max_length=250, unique=True)
    descripciontemporada = models.CharField(max_length=250)
    tipotemporada = models.CharField(
        max_length=250, choices=[("Amistosa", "Amistosa"), ("Oficial", "Oficial")]
    )
    fechainiciotemporada = models.DateTimeField()
    fechafintemporada = models.DateTimeField()
    temporadaactiva = models.BooleanField(default=False)

    class Meta:
        db_table = "temporada"

    def __str__(self):
        return self.nombretemporada
