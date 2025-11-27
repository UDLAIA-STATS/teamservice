from django.db import models
from .temporada import *
from .equipo import *
from .institucion import *
from .torneo import *

class Partido(models.Model):
    idpartido = models.AutoField(primary_key=True)
    fechapartido = models.DateTimeField()
    marcadorequipolocal = models.IntegerField(null=True, blank=True)
    marcadorequipovisitante = models.IntegerField(null=True, blank=True)
    partidosubido = models.BooleanField(default=False)

    idequipolocal = models.ForeignKey(
        Equipo, related_name='partidoslocal', on_delete=models.CASCADE, db_column='idequipolocal')
    idequipovisitante = models.ForeignKey(
        Equipo, related_name='partidosvisitante', on_delete=models.CASCADE, db_column='idequipovisitante')
    idtorneo = models.ForeignKey(
        Torneo, on_delete=models.CASCADE, db_column='idtorneo')
    idtemporada = models.ForeignKey(
        Temporada, on_delete=models.CASCADE, db_column='idtemporada')

    class Meta:
        db_table = 'partido'

    def __str__(self):
        return f"{self.idequipolocal} vs {self.idequipovisitante} ({self.fechapartido.date()})"
