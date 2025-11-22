from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from torneo.models import Temporada
from datetime import datetime, timedelta


class TemporadaTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {
            "nombretemporada": "Temporada 2025",
            "descripciontemporada": "Descripción",
            "tipotemporada": "Oficial",
            "fechainiciotemporada": datetime.now().isoformat(),
            "fechafintemporada": (datetime.now() + timedelta(days=10)).isoformat(),
            "temporadaactiva": True
        }

    def test_crear_temporada(self):
        url = reverse("temporada-list-create")
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_obtener_temporada(self):
        temp = Temporada.objects.create(
            nombretemporada="Temp X",
            descripciontemporada="Desc",
            tipotemporada="Amistosa",
            fechainiciotemporada=datetime.now(),
            fechafintemporada=datetime.now() + timedelta(days=5),
            temporadaactiva=False
        )
        url = reverse("temporada-detail", args=[temp.idtemporada])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_actualizar_temporada(self):
        temp = Temporada.objects.create(
            nombretemporada="Temp Update",
            descripciontemporada="Desc",
            tipotemporada="Amistosa",
            fechainiciotemporada=datetime.now(),
            fechafintemporada=datetime.now() + timedelta(days=5),
        )
        url = reverse("temporada-update", args=[temp.idtemporada])
        response = self.client.patch(url, {"descripciontemporada": "Nueva Desc"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_eliminar_temporada(self):
        temp = Temporada.objects.create(
            nombretemporada="Temp Del",
            descripciontemporada="Desc",
            tipotemporada="Amistosa",
            fechainiciotemporada=datetime.now(),
            fechafintemporada=datetime.now() + timedelta(days=5),
        )
        url = reverse("temporada-delete", args=[temp.idtemporada])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
