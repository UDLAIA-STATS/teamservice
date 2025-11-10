from django.db import models


class Temporada(models.Model):
    idtemporada = models.AutoField(primary_key=True)
    nombretemporada = models.CharField(max_length=250, unique=True)
    descripciontemporada = models.CharField(max_length=250)
    tipotemporada = models.CharField(
        max_length=250,
        choices=[('Amistosa', 'Amistosa'), ('Oficial', 'Oficial')]
    )
    fechainiciotemporada = models.DateTimeField()
    fechafintemporada = models.DateTimeField()
    temporadaactiva = models.BooleanField(default=False)

    class Meta:
        db_table = 'temporada'

    def __str__(self):
        return self.nombretemporada


class Torneo(models.Model):
    idtorneo = models.AutoField(primary_key=True)
    idtemporada = models.ForeignKey(
        Temporada, on_delete=models.CASCADE, db_column='idtemporada')
    nombretorneo = models.CharField(max_length=250, unique=True)
    descripciontorneo = models.CharField(max_length=250)
    fechainiciotorneo = models.DateTimeField()
    fechafintorneo = models.DateTimeField()
    torneoactivo = models.BooleanField(default=False)

    class Meta:
        db_table = 'torneo'

    def __str__(self):
        return self.nombretorneo


class Institucion(models.Model):
    idinstitucion = models.AutoField(primary_key=True)
    nombreinstitucion = models.CharField(max_length=250)
    institucionactiva = models.BooleanField(default=True)

    class Meta:
        db_table = 'institucion'

    def __str__(self):
        return self.nombreinstitucion


class Equipo(models.Model):
    idequipo = models.AutoField(primary_key=True)
    idinstitucion = models.ForeignKey(
        Institucion, on_delete=models.CASCADE, db_column='idinstitucion')
    nombreequipo = models.CharField(max_length=250)
    imagenequipo = models.ImageField(upload_to='equipos/', null=True, blank=True)
    equipoactivo = models.BooleanField(default=True)

    class Meta:
        db_table = 'equipo'

    def __str__(self):
        return self.nombreequipo


class Partido(models.Model):
    idpartido = models.AutoField(primary_key=True)
    fechapartido = models.DateTimeField()
    marcadorequipolocal = models.IntegerField(null=True, blank=True)
    marcadorequipovisitante = models.IntegerField(null=True, blank=True)

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
