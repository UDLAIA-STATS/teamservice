from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from torneo.models import Institucion


class InstitucionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {
            "nombreinstitucion": "Universidad X",
            "institucionactiva": True
        }

    def test_crear_institucion(self):
        url = reverse("institucion-list-create")
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_obtener_institucion(self):
        inst = Institucion.objects.create(nombreinstitucion="ABC")
        url = reverse("institucion-detail", args=[inst.idinstitucion])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_actualizar_institucion(self):
        inst = Institucion.objects.create(nombreinstitucion="Institucion Y")
        url = reverse("institucion-update", args=[inst.idinstitucion])
        response = self.client.patch(url, {"nombreinstitucion": "Nuevo nombre"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_eliminar_institucion(self):
        inst = Institucion.objects.create(nombreinstitucion="Eliminar X")
        url = reverse("institucion-delete", args=[inst.idinstitucion])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
