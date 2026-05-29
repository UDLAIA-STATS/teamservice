from django.db import models

from .temporada import Temporada


class Torneo(models.Model):
    idtorneo = models.AutoField(primary_key=True)
    idtemporada = models.ForeignKey(
        Temporada, on_delete=models.CASCADE, db_column="idtemporada"
    )
    nombretorneo = models.CharField(max_length=250, unique=True)
    descripciontorneo = models.CharField(max_length=250)
    fechainiciotorneo = models.DateTimeField()
    fechafintorneo = models.DateTimeField()
    torneoactivo = models.BooleanField(default=False)

    class Meta:
        db_table = "torneo"

    def __str__(self):
        return self.nombretorneo
