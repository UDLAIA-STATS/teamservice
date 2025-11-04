from django import db
from django.db import models

class Equipo(models.Model):
    
    idequipo = models.AutoField(primary_key=True)
    nombreequipo = models.CharField(max_length=100, unique=True)
    logoequipo = models.ImageField(upload_to='logos/', null=True, blank=True)

    def __str__(self):
        return self.nombreequipo
    
    class Meta:
        db_table='Equipo'


class Partido(models.Model):
    idpartido = models.AutoField(primary_key=True)
    marcadorequipolocal = models.IntegerField(null=True, blank=True)
    marcadorequipovisitante = models.IntegerField(null=True, blank=True)
    fechapartido = models.DateTimeField(unique=True)
    tipopartido = models.BooleanField()  # True = oficial, False = amistoso
    idequipolocal = models.ForeignKey(
        Equipo, related_name='partidos_local', on_delete=models.CASCADE)
    idequipovisitante = models.ForeignKey(
        Equipo, related_name='partidos_visitante', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.idequipolocal} vs {self.idequipovisitante} ({self.fechapartido})"

    class Meta:
        db_table='Partido'


class Torneo(models.Model):
    idtorneo = models.AutoField(primary_key=True)
    nombretorneo = models.CharField(max_length=100, unique=True)
    descripciontorneo = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.nombretorneo

    class Meta:
        db_table='Torneo'


class TorneoPartido(models.Model):
    idtorneo = models.ForeignKey(Torneo, on_delete=models.CASCADE)
    idpartido = models.ForeignKey(Partido, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('idtorneo', 'idpartido')
        db_table='TorneoPartido'

    def __str__(self):
        return f"{self.idtorneo.nombretorneo} - Partido {self.idpartido.idpartido}"


class Temporada(models.Model):
    idtemporada = models.AutoField(primary_key=True)
    nombretemporada = models.CharField(max_length=100)
    tipotemporada = models.BooleanField()  # True = Apertura / False = Clausura
    idtorneo = models.ForeignKey(Torneo, on_delete=models.CASCADE)

    class Meta:
        db_table='Temporada'

    def __str__(self):
        return f"{self.nombretemporada} ({self.idtorneo.nombretorneo})"
