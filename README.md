# Kraken Rolls — Backend (FastAPI)

Sistema backend para administrar un restaurante de sushi: productos, platillos, trabajadores e inventario, con una API REST completa (CRUD) construida con **FastAPI** y una base de datos relacional (**SQLite**, vía **SQLAlchemy**).

## Caso de uso

Restaurante de sushi con reparto a domicilio. Se administran:
- **Productos**: ingredientes/insumos base (ej. salmón, camarón, alga nori).
- **Platillos**: rolls/preparaciones que se venden, hechos a partir de un producto y, opcionalmente, registrados por un trabajador.
- **Trabajadores**: personal del restaurante (sushiman, repartidor, cajero, etc.).
- **Inventario**: existencias disponibles de cada producto.

## Diseño de la base de datos

| Tabla | Clave primaria | Claves foráneas | Relación |
|---|---|---|---|
| `productos` | `id_prod` | — | — |
| `trabajadores` | `id` | — | — |
| `platillos` | `id_plat` | `id_prod` → productos, `id_trabajador` → trabajadores | Un platillo pertenece a un producto; opcionalmente lo registra un trabajador |
| `inventario` | `id` | `id_prod` → productos | Cada registro de inventario controla existencias de un producto |

El script `schema.sql` en la raíz del proyecto contiene las sentencias `CREATE TABLE` con tipos de datos, llaves primarias y foráneas, además de datos de ejemplo. La aplicación también las crea automáticamente al arrancar (no es necesario correr el script a mano para usar la API).

## Estructura del proyecto

```
app_reparto/
├── requirements.txt
├── schema.sql               ← script SQL de la base de datos
├── reparto.db                ← se genera sola al correr la app (SQLite)
└── app/
    ├── main.py               ← arranca la API, monta rutas y el panel visual
    ├── database.py           ← conexión a la base de datos
    ├── models.py             ← las 4 tablas (SQLAlchemy)
    ├── schemas.py             ← validación de datos (Pydantic)
    ├── crud.py                ← funciones Create/Read/Update/Delete
    ├── static/                ← panel visual (HTML/CSS/JS) en /ui
    └── routers/
        ├── productos.py
        ├── platillos.py
        ├── trabajadores.py
        └── inventario.py
```

## Instalación y configuración

**Requisitos:** Python 3.10+ y VS Code (o cualquier editor).

1. Clona o descarga el proyecto y ábrelo en VS Code.
2. Crea un entorno virtual:
   ```bash
   python -m venv .venv
   ```
3. Actívalo:
   - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
   - Mac/Linux: `source .venv/bin/activate`
4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

No se requiere configurar nada más: la base de datos es SQLite y se crea sola (archivo `reparto.db`) la primera vez que arranca la aplicación.

## Ejecución

```bash
uvicorn app.main:app --reload
```

Esto levanta el servidor en `http://127.0.0.1:8000`.

- **Panel visual:** `http://127.0.0.1:8000/ui`
- **Documentación interactiva (Swagger):** `http://127.0.0.1:8000/docs`

## Endpoints disponibles

Cada una de las 4 tablas implementa el CRUD completo:

| Método | Ruta | Operación |
|---|---|---|
| GET | `/productos/` | Consultar todos |
| GET | `/productos/{id_prod}` | Consultar por ID |
| POST | `/productos/` | Crear |
| PUT | `/productos/{id_prod}` | Actualizar |
| DELETE | `/productos/{id_prod}` | Eliminar |

Igual para `/trabajadores/{id}`, `/platillos/{id_plat}` e `/inventario/{id}`.

## Pruebas (Swagger UI)

1. Abre `http://127.0.0.1:8000/docs`.
2. Prueba en este orden (por las relaciones entre tablas):
   - `POST /productos/` → crea un producto, anota el `id_prod` devuelto.
   - `POST /trabajadores/` → crea un trabajador (opcional).
   - `POST /platillos/` → usa el `id_prod` (y opcionalmente `id_trabajador`) del paso anterior.
   - `POST /inventario/` → usa el mismo `id_prod` para registrar existencias.
3. Prueba `GET` (lista y por ID), `PUT` (actualizar) y `DELETE` en cada tabla.
4. **Casos de error que ya maneja la API:**
   - `GET /productos/999` con un ID que no existe → `404 Not Found`.
   - `POST /platillos/` con un `id_prod` que no existe → `400 Bad Request` ("id_prod no existe en productos").
   - `POST /productos/` sin `nombre` o con `precio` como texto → `422 Unprocessable Entity` (validación de Pydantic).
   - `DELETE` sobre un registro que ya no existe → `404 Not Found`.

## Panel visual

Además de Swagger, el proyecto incluye una interfaz simple (`/ui`) con pestañas para cada tabla, tablas de datos y formularios para crear/editar/eliminar sin necesidad de usar `/docs`.

## Siguientes pasos sugeridos

- Agregar una tabla de **Pedidos** (qué platillos pidió un cliente y a qué trabajador se le asigna la entrega).
- Autenticación de trabajadores (login).
- Desplegar la API en un servicio en la nube.
