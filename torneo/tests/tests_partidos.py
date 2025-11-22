from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from torneo.models import Partido, Equipo, Institucion, Temporada, Torneo
from datetime import datetime, timedelta


class PartidoTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.institucion = Institucion.objects.create(nombreinstitucion="Inst X")
        self.temp = Temporada.objects.create(
            nombretemporada="Temp P",
            descripciontemporada="Desc",
            tipotemporada="Oficial",
            fechainiciotemporada=datetime.now() - timedelta(days=5),
            fechafintemporada=datetime.now() + timedelta(days=10)
        )

        self.torneo = Torneo.objects.create(
            idtemporada=self.temp,
            nombretorneo="Torneo P",
            descripciontorneo="Desc",
            fechainiciotorneo=datetime.now() - timedelta(days=2),
            fechafintorneo=datetime.now() + timedelta(days=4),
        )
        self.equipo1 = Equipo.objects.create(
            idinstitucion=self.institucion,
            nombreequipo="Equipo A"
        )
        self.equipo2 = Equipo.objects.create(
            idinstitucion=self.institucion,
            nombreequipo="Equipo B"
        )

        self.data = {
            "fechapartido": datetime.now(),
            "idequipolocal": self.equipo1.idequipo,
            "idequipovisitante": self.equipo2.idequipo,
            "idtorneo": self.torneo.idtorneo,
            "idtemporada": self.temp.idtemporada,
        }

    def test_crear_partido(self):
        url = reverse("partido-list-create")
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_obtener_partido(self):
        partido = Partido.objects.create(
            fechapartido=datetime.now(),
            idequipolocal=self.equipo1,
            idequipovisitante=self.equipo2,
            idtorneo=self.torneo,
            idtemporada=self.temp,
        )
        url = reverse("partido-detail", args=[partido.idpartido])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_actualizar_partido(self):
        partido = Partido.objects.create(
            fechapartido=datetime.now(),
            idequipolocal=self.equipo1,
            idequipovisitante=self.equipo2,
            idtorneo=self.torneo,
            idtemporada=self.temp,
        )
        url = reverse("partido-update", args=[partido.idpartido])
        response = self.client.patch(url, {
            "marcadorequipolocal": 4,
            "marcadorequipovisitante": 2,
            "fechapartido": datetime.now(),
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
    def test_eliminar_partido(self):
        partido = Partido.objects.create(
            fechapartido=datetime.now(),
            idequipolocal=self.equipo1,
            idequipovisitante=self.equipo2,
            idtorneo=self.torneo,
            idtemporada=self.temp,
        )
        url = reverse("partido-delete", args=[partido.idpartido])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
