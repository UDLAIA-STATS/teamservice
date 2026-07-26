from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from torneo.models import Institucion


class InstitucionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {"nombreinstitucion": "Universidad X", "institucionactiva": True}

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
        response = self.client.patch(
            url, {"nombreinstitucion": "Nuevo nombre"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_eliminar_institucion(self):
        inst = Institucion.objects.create(nombreinstitucion="Eliminar X")
        url = reverse("institucion-delete", args=[inst.idinstitucion])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_institucion_nombre_duplicado(self):
        Institucion.objects.create(nombreinstitucion="Universidad X")

        url = reverse("institucion-list-create")
        response = self.client.post(data=self.data, format="json", path=url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_institucion_sin_nombre(self):
        url = reverse("institucion-list-create")
        response = self.client.post(
            url,
            {"institucionactiva": True},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtener_institucion_no_existente(self):
        url = reverse("institucion-detail", args=[9999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_listar_instituciones(self):
        Institucion.objects.create(nombreinstitucion="Inst 1")
        Institucion.objects.create(nombreinstitucion="Inst 2")

        url = reverse("institucion-all")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_actualizar_institucion_no_existente(self):
        url = reverse("institucion-update", args=[9999])
        response = self.client.patch(
            url,
            {"nombreinstitucion": "Nuevo"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_actualizar_institucion_sin_nombre(self):
        inst = Institucion.objects.create(nombreinstitucion="Institucion A")

        url = reverse("institucion-update", args=[inst.idinstitucion])
        response = self.client.patch(
            url,
            {"nombreinstitucion": ""},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deshabilitar_institucion_ya_inactiva(self):
        inst = Institucion.objects.create(
            nombreinstitucion="Institucion X",
            institucionactiva=False,
        )

        url = reverse("institucion-delete", args=[inst.idinstitucion])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_eliminar_institucion_no_existente(self):
        url = reverse("institucion-delete", args=[9999])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_eliminar_institucion_marca_como_inactiva(self):
        inst = Institucion.objects.create(
            nombreinstitucion="Institucion Activa",
            institucionactiva=True,
        )

        url = reverse("institucion-delete", args=[inst.idinstitucion])
        response = self.client.delete(url)

        inst.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(inst.institucionactiva)

    def test_serializer_valida_nombre_duplicado(self):
        Institucion.objects.create(nombreinstitucion="Duplicada")

        from torneo.serializers import InstitucionSerializer

        serializer = InstitucionSerializer(
            data={
                "nombreinstitucion": "Duplicada",
                "institucionactiva": True,
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("nombreinstitucion", serializer.errors)

    def test_serializer_permite_actualizar_mismo_nombre(self):
        from torneo.serializers import InstitucionSerializer

        inst = Institucion.objects.create(nombreinstitucion="Institucion A")

        serializer = InstitucionSerializer(
            inst,
            data={"nombreinstitucion": "Institucion A"},
            partial=True,
        )

        self.assertTrue(serializer.is_valid())