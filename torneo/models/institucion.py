from django.db import models


class Institucion(models.Model):
    idinstitucion = models.AutoField(primary_key=True)
    nombreinstitucion = models.CharField(max_length=250)
    institucionactiva = models.BooleanField(default=True)

    class Meta:
        db_table = "institucion"

    def __str__(self):
        return self.nombreinstitucion
