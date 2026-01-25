from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from torneo.models import Torneo, Temporada
from datetime import datetime, timedelta

from torneo.tests.helpers import parse_response


class TorneoTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.temporada = Temporada.objects.create(
            nombretemporada="Temp T",
            descripciontemporada="Desc",
            tipotemporada="Oficial",
            fechainiciotemporada=datetime.now(),
            fechafintemporada=datetime.now() + timedelta(days=10),
        )

        self.data = {
            "idtemporada": self.temporada.idtemporada,
            "nombretorneo": "Copa Oro",
            "descripciontorneo": "Torneo importante",
            "fechainiciotorneo": datetime.now().isoformat(),
            "fechafintorneo": (datetime.now() + timedelta(days=7)).isoformat(),
            "torneoactivo": True,
        }

        # crear torneos para búsqueda/paginación
        self.torneos = []
        for i in range(3):
            t = Torneo.objects.create(
                idtemporada=self.temporada,
                nombretorneo=f"Torneo {i}",
                descripciontorneo="Desc",
                fechainiciotorneo=datetime.now(),
                fechafintorneo=datetime.now() + timedelta(days=3),
                torneoactivo=True,
            )
            self.torneos.append(t)

    def test_crear_torneo(self):
        url = reverse("torneo-list-create")
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_crear_torneo_sin_temporada(self):
        url = reverse("torneo-list-create")
        invalid = self.data.copy()
        invalid.pop("idtemporada")
        response = self.client.post(url, invalid, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtener_torneo(self):
        torneo = self.torneos[0]
        url = reverse("torneo-detail", args=[torneo.idtorneo])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_actualizar_torneo(self):
        torneo = self.torneos[1]
        url = reverse("torneo-update", args=[torneo.idtorneo])
        response = self.client.patch(
            url, {"descripciontorneo": "Nueva Desc"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_eliminar_torneo(self):
        torneo = self.torneos[2]
        url = reverse("torneo-delete", kwargs={"pk": torneo.idtorneo})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_buscar_torneo_parcial(self):
        url = reverse("torneo-all") + "?page=1&offset=10"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = parse_response(response)
        self.assertIn("results", data)
