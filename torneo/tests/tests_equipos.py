from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from torneo.models import Equipo, Institucion


class EquipoTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.institucion = Institucion.objects.create(
            nombreinstitucion="Institución 1"
        )
        self.data = {
            "idinstitucion": self.institucion.idinstitucion,
            "nombreequipo": "Tigres FC",
            "equipoactivo": True
        }

    def test_crear_equipo(self):
        url = reverse("equipo-list-create")
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_obtener_equipo(self):
        equipo = Equipo.objects.create(
            idinstitucion=self.institucion,
            nombreequipo="Leones"
        )
        url = reverse("equipo-detail", args=[equipo.idequipo])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_buscar_equipo_por_nombre(self):
        Equipo.objects.create(idinstitucion=self.institucion, nombreequipo="Panteras")
        url = reverse("equipo-search", args=["Panteras"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_actualizar_equipo(self):
        equipo = Equipo.objects.create(
            idinstitucion=self.institucion,
            nombreequipo="ViejoNombre"
        )
        url = reverse("equipo-update", args=[equipo.idequipo])
        response = self.client.patch(url, {"nombreequipo": "NuevoNombre"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_eliminar_equipo(self):
        equipo = Equipo.objects.create(
            idinstitucion=self.institucion,
            nombreequipo="BorrarFC"
        )
        url = reverse("equipo-delete", args=[equipo.idequipo])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
