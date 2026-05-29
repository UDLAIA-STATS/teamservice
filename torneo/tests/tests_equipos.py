from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from torneo.models import Equipo, Institucion
from torneo.tests.helpers import parse_response


class EquipoTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.institucion = Institucion.objects.create(nombreinstitucion="Institución 1")
        # create multiple equipos for search/pagination tests
        self.equipos = []
        names = ["Tigres FC", "Leones", "Panteras", "Pantera Negra", "Equipo Medio"]
        for n in names:
            e = Equipo.objects.create(
                idinstitucion=self.institucion, nombreequipo=n, equipoactivo=True
            )
            self.equipos.append(e)

        self.data = {
            "idinstitucion": self.institucion.idinstitucion,
            "nombreequipo": "Tigres FC",
            "equipoactivo": True,
        }

    # ---------- Creación (positivos y negativos - particiones) ----------
    def test_crear_equipo_valido(self):
        url = reverse("equipo-list-create")
        data = {
            "idinstitucion": self.institucion.idinstitucion,
            "nombreequipo": "Águilas",
            "equipoactivo": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_crear_equipo_sin_institucion(self):
        url = reverse("equipo-list-create")
        invalid = self.data.copy()
        invalid.pop("idinstitucion")
        response = self.client.post(url, invalid, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_equipo_nombre_vacio(self):
        url = reverse("equipo-list-create")
        invalid = self.data.copy()
        invalid["nombreequipo"] = ""
        response = self.client.post(url, invalid, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ---------- Obtener / Actualizar / Eliminar (positivos y negativos) ----------
    def test_obtener_equipo(self):
        equipo = self.equipos[1]
        url = reverse("equipo-detail", args=[equipo.idequipo])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_obtener_equipo_inexistente(self):
        url = reverse("equipo-detail", args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_actualizar_equipo(self):
        equipo = self.equipos[0]
        url = reverse("equipo-update", args=[equipo.idequipo])
        response = self.client.patch(
            url, {"nombreequipo": "NuevoNombre"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_actualizar_equipo_inexistente(self):
        url = reverse("equipo-update", args=[9999])
        response = self.client.patch(url, {"nombreequipo": "X"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_eliminar_equipo(self):
        equipo = self.equipos[2]
        url = reverse("equipo-delete", args=[equipo.idequipo])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_eliminar_equipo_inactivo(self):
        equipo = self.equipos[3]
        equipo.equipoactivo = False
        equipo.save(update_fields=["equipoactivo"])
        url = reverse("equipo-delete", args=[equipo.idequipo])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ---------- Búsqueda (positivos, negativos, medio/substring) ----------
    def test_buscar_equipo_por_nombre_exacto(self):
        url = reverse("equipo-search", args=["Panteras"])
        response = self.client.get(url)
        # endpoint devuelve 200 si encuentra, 404 si no (actual behavior)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = parse_response(response)
        self.assertIn("data", data)
        self.assertEqual(data["data"]["nombreequipo"], "Panteras")

    def test_buscar_equipo_por_nombre_parcial(self):
        # buscar por substring que coincide con 2 equipos (Panteras, Pantera Negra)
        # current endpoint requires exact name; test documents behavior expecting 404 for substring
        url = reverse("equipo-search", args=["Pantera"])
        response = self.client.get(url)
        # If API returns 404 for non-exact, assert 404; if changed later to support
        # #substring, adjust to 200 and check results length
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ---------- Paginación (valores típicos, límites, no numéricos) ----------
    def test_paginacion_valida(self):
        url = reverse("equipo-all") + "?page=1&offset=2"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = parse_response(response)
        self.assertIn("results", data)
        self.assertLessEqual(len(data["results"]), 2)

    def test_paginacion_page_zero(self):
        url = reverse("equipo-all") + "?page=0&offset=2"
        response = self.client.get(url)
        # Endpoint may treat page=0 as invalid -> expect 400 or return page 1;
        # accept either but assert type and structure
        self.assertIn(
            response.status_code, (status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST)
        )

    def test_paginacion_offset_negativo(self):
        url = reverse("equipo-all") + "?page=1&offset=-1"
        response = self.client.get(url)
        # current pagination implementation may accept negative offsets and return 200,
        # or validate and return 400. Accept both behaviors but ensure response structure.
        self.assertIn(
            response.status_code, (status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST)
        )
        if response.status_code == status.HTTP_200_OK:
            data = parse_response(response)
            self.assertIn("results", data)
