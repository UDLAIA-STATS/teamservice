from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from torneo.models import Torneo, Temporada
from datetime import datetime, timedelta


class TorneoTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.temporada = Temporada.objects.create(
            nombretemporada="Temp T",
            descripciontemporada="Desc",
            tipotemporada="Oficial",
            fechainiciotemporada=datetime.now(),
            fechafintemporada=datetime.now() + timedelta(days=10)
        )

        self.data = {
            "idtemporada": self.temporada.idtemporada,
            "nombretorneo": "Copa Oro",
            "descripciontorneo": "Torneo importante",
            "fechainiciotorneo": datetime.now().isoformat(),
            "fechafintorneo": (datetime.now() + timedelta(days=7)).isoformat(),
            "torneoactivo": True
        }

    def test_crear_torneo(self):
        url = reverse("torneo-list-create")
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_obtener_torneo(self):
        torneo = Torneo.objects.create(
            idtemporada=self.temporada,
            nombretorneo="Liga X",
            descripciontorneo="Desc",
            fechainiciotorneo=datetime.now(),
            fechafintorneo=datetime.now() + timedelta(days=3),
        )
        url = reverse("torneo-detail", args=[torneo.idtorneo])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_actualizar_torneo(self):
        torneo = Torneo.objects.create(
            idtemporada=self.temporada,
            nombretorneo="Actualizar",
            descripciontorneo="Desc",
            fechainiciotorneo=datetime.now(),
            fechafintorneo=datetime.now() + timedelta(days=3),
        )
        url = reverse("torneo-update", args=[torneo.idtorneo])
        response = self.client.patch(url, {"descripciontorneo": "Nueva Desc"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_eliminar_torneo(self):
        torneo = Torneo.objects.create(
            idtemporada=self.temporada,
            nombretorneo="Eliminar",
            descripciontorneo="Desc",
            fechainiciotorneo=datetime.now(),
            fechafintorneo=datetime.now() + timedelta(days=3),
        )
        url = reverse("torneo-delete", args=[torneo.idtorneo])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
