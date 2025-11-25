# Team Service - Microservicio de Gestión de Torneos

## Descripción

El **Team Service** es un microservicio desarrollado con Django REST Framework que gestiona toda la información relacionada con torneos deportivos, incluyendo equipos, partidos, temporadas, torneos e instituciones. Este servicio forma parte de una arquitectura de microservicios para la gestión de estadísticas deportivas.

## Funcionalidades

El microservicio proporciona gestión completa de:

- **Equipos**: CRUD de equipos deportivos con imágenes y relación con instituciones
- **Partidos**: Gestión de partidos con marcadores, equipos locales/visitantes, fechas
- **Torneos**: Administración de torneos con fechas de inicio/fin y estado activo
- **Temporadas**: Control de temporadas (Amistosas u Oficiales) con períodos definidos
- **Instituciones**: Gestión de instituciones que agrupan equipos

## Tecnologías

- **Python 3.13**
- **Django 5.0.3**
- **Django REST Framework**
- **PostgreSQL** (base de datos)
- **Docker** (containerización)

## Requisitos Previos

- Docker y Docker Compose (recomendado)
- Python 3.13+ (si se ejecuta localmente)
- PostgreSQL 12+ (si se ejecuta localmente)

## Configuración

### Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto basado en `.env.template`:

```bash
DEBUG=True
SECRET_KEY=tu-secret-key-aqui
POSTGRES_NAME=teamservice_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
API_PORT=8020
ALLOWED_HOSTS=localhost,127.0.0.1
FRONTEND_URL=http://localhost:3000
```

### Instalación con Docker (Recomendado)

#### Imagen de Docker Hub

La imagen oficial del microservicio está disponible en Docker Hub:

🐳 **Docker Hub**: https://hub.docker.com/repository/docker/dase123/udlaia-stats/tags/

```bash
# Descargar la imagen
docker pull dase123/udlaia-stats:latest

# Ejecutar el contenedor
docker run -d \
  -p 8020:8020 \
  --env-file .env \
  --name teamservice \
  dase123/udlaia-stats:latest
```

#### Construcción Local

```bash
# Construir la imagen
docker build -t teamservice .

# Ejecutar el contenedor
docker run -d -p 8020:8020 --env-file .env teamservice
```

### Instalación Local

```bash
# Clonar el repositorio
git clone <repository-url>
cd teamservice

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Ejecutar servidor
python manage.py runserver 8020
```

## API Endpoints

### Base URL
```
http://localhost:8020/api/
```

**Nota**: Este servicio no requiere autenticación. Todos los endpoints son de acceso público.

---

## Endpoints Disponibles

### 📋 Equipos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/equipos/` | Listar equipos (paginado) |
| POST | `/api/equipos/` | Crear nuevo equipo |
| GET | `/api/equipos/all/` | Listar todos los equipos |
| GET | `/api/equipos/<id>/` | Obtener detalle de equipo |
| PUT | `/api/equipos/<id>/update/` | Actualizar equipo |
| DELETE | `/api/equipos/<id>/delete/` | Eliminar equipo |
| GET | `/api/equipos/search/<nombre>/` | Buscar equipo por nombre |

### ⚽ Partidos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/partidos/` | Listar partidos (paginado) |
| POST | `/api/partidos/` | Crear nuevo partido |
| GET | `/api/partidos/all/` | Listar todos los partidos |
| GET | `/api/partidos/<id>/` | Obtener detalle de partido |
| PUT | `/api/partidos/<id>/update/` | Actualizar partido |
| DELETE | `/api/partidos/<id>/delete/` | Eliminar partido |

### 🏆 Torneos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/torneos/` | Listar torneos (paginado) |
| POST | `/api/torneos/` | Crear nuevo torneo |
| GET | `/api/torneos/all/` | Listar todos los torneos |
| GET | `/api/torneos/<id>/` | Obtener detalle de torneo |
| PUT | `/api/torneos/<id>/update/` | Actualizar torneo |
| DELETE | `/api/torneos/<id>/delete/` | Eliminar torneo |

### 📅 Temporadas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/temporadas/` | Listar temporadas (paginado) |
| POST | `/api/temporadas/` | Crear nueva temporada |
| GET | `/api/temporadas/all/` | Listar todas las temporadas |
| GET | `/api/temporadas/<id>/` | Obtener detalle de temporada |
| PUT | `/api/temporadas/<id>/update/` | Actualizar temporada |
| DELETE | `/api/temporadas/<id>/delete/` | Eliminar temporada |

### 🏢 Instituciones

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/instituciones/` | Listar instituciones (paginado) |
| POST | `/api/instituciones/` | Crear nueva institución |
| GET | `/api/instituciones/all/` | Listar todas las instituciones |
| GET | `/api/instituciones/<id>/` | Obtener detalle de institución |
| PUT | `/api/instituciones/<id>/update/` | Actualizar institución |
| DELETE | `/api/instituciones/<id>/delete/` | Eliminar institución |

---

## Ejemplos de Uso con cURL

### 1. Crear una Institución

```bash
curl -X POST http://localhost:8020/api/instituciones/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombreinstitucion": "Universidad de Los Andes",
    "institucionactiva": true
  }'
```

### 2. Crear un Equipo

```bash
curl -X POST http://localhost:8020/api/equipos/ \
  -H "Content-Type: application/json" \
  -d '{
    "idinstitucion": 1,
    "nombreequipo": "Tigres FC",
    "equipoactivo": true
  }'
```

### 3. Listar Todos los Equipos

```bash
curl -X GET http://localhost:8020/api/equipos/all/
```

### 4. Obtener Detalle de un Equipo

```bash
curl -X GET http://localhost:8020/api/equipos/1/
```

### 5. Buscar Equipo por Nombre

```bash
curl -X GET http://localhost:8020/api/equipos/search/Tigres/
```

### 6. Crear una Temporada

```bash
curl -X POST http://localhost:8020/api/temporadas/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombretemporada": "Temporada 2024",
    "descripciontemporada": "Temporada regular 2024",
    "tipotemporada": "Oficial",
    "fechainiciotemporada": "2024-01-01T00:00:00Z",
    "fechafintemporada": "2024-12-31T23:59:59Z",
    "temporadaactiva": true
  }'
```

### 7. Crear un Torneo

```bash
curl -X POST http://localhost:8020/api/torneos/ \
  -H "Content-Type: application/json" \
  -d '{
    "idtemporada": 1,
    "nombretorneo": "Copa Universitaria 2024",
    "descripciontorneo": "Torneo anual de fútbol universitario",
    "fechainiciotorneo": "2024-03-01T00:00:00Z",
    "fechafintorneo": "2024-06-30T23:59:59Z",
    "torneoactivo": true
  }'
```

### 8. Crear un Partido

```bash
curl -X POST http://localhost:8020/api/partidos/ \
  -H "Content-Type: application/json" \
  -d '{
    "fechapartido": "2024-04-15T18:00:00Z",
    "idequipolocal": 1,
    "idequipovisitante": 2,
    "idtorneo": 1,
    "idtemporada": 1,
    "marcadorequipolocal": 3,
    "marcadorequipovisitante": 2
  }'
```

### 9. Actualizar un Partido

```bash
curl -X PUT http://localhost:8020/api/partidos/1/update/ \
  -H "Content-Type: application/json" \
  -d '{
    "marcadorequipolocal": 4,
    "marcadorequipovisitante": 2
  }'
```

### 10. Eliminar un Equipo

```bash
curl -X DELETE http://localhost:8020/api/equipos/1/delete/
```

### 11. Listar con Paginación

```bash
curl -X GET "http://localhost:8020/api/equipos/?page=1&page_size=10"
```

---

## Modelos de Datos

### Equipo
```python
{
  "idequipo": int,
  "idinstitucion": int,
  "nombreequipo": string,
  "imagenequipo": binary (opcional),
  "equipoactivo": boolean
}
```

### Partido
```python
{
  "idpartido": int,
  "fechapartido": datetime,
  "marcadorequipolocal": int (opcional),
  "marcadorequipovisitante": int (opcional),
  "idequipolocal": int,
  "idequipovisitante": int,
  "idtorneo": int,
  "idtemporada": int
}
```

### Torneo
```python
{
  "idtorneo": int,
  "idtemporada": int,
  "nombretorneo": string (único),
  "descripciontorneo": string,
  "fechainiciotorneo": datetime,
  "fechafintorneo": datetime,
  "torneoactivo": boolean
}
```

### Temporada
```python
{
  "idtemporada": int,
  "nombretemporada": string (único),
  "descripciontemporada": string,
  "tipotemporada": "Amistosa" | "Oficial",
  "fechainiciotemporada": datetime,
  "fechafintemporada": datetime,
  "temporadaactiva": boolean
}
```

### Institución
```python
{
  "idinstitucion": int,
  "nombreinstitucion": string,
  "institucionactiva": boolean
}
```

---

## Estructura del Proyecto

```
teamservice/
├── teamservice/          # Configuración del proyecto Django
│   ├── settings.py       # Configuración principal
│   ├── urls.py           # URLs principales
│   └── wsgi.py           # WSGI config
├── torneo/               # Aplicación principal
│   ├── models/           # Modelos de datos
│   ├── views/            # Vistas API
│   ├── serializers/      # Serializadores DRF
│   ├── urls.py           # URLs de la API
│   └── tests/            # Tests unitarios
├── docker/               # Configuración Docker
├── Dockerfile            # Imagen Docker
├── requirements.txt      # Dependencias Python
└── manage.py             # CLI de Django
```

---

## Testing

Ejecutar los tests:

```bash
# Todos los tests
python manage.py test

# Tests específicos
python manage.py test torneo.tests.tests_equipos
python manage.py test torneo.tests.tests_partidos
python manage.py test torneo.tests.tests_torneos
python manage.py test torneo.tests.tests_temporadas
python manage.py test torneo.tests.tests_instituciones
```

---

## Desarrollo

### Migraciones

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ver estado de migraciones
python manage.py showmigrations
```

### Admin de Django

Crear superusuario para acceder al panel de administración:

```bash
python manage.py createsuperuser
```

Acceder al admin en: http://localhost:8020/admin/

---

## Troubleshooting

### Puerto ya en uso
Si el puerto 8020 está ocupado, cambia la variable `API_PORT` en el archivo `.env`.

### Error de conexión a base de datos
Verifica que PostgreSQL esté ejecutándose y las credenciales en `.env` sean correctas.

---

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## Licencia

Este proyecto es parte del sistema UDLAIA Stats para la gestión de estadísticas deportivas.

---

## Soporte

Para reportar bugs o solicitar features, por favor abre un issue en el repositorio.

---

## Docker Hub

🐳 **Imagen oficial**: https://hub.docker.com/repository/docker/dase123/udlaia-stats/tags/

```bash
docker pull dase123/udlaia-stats:latest
```
