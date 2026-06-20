# MiniTienda — aplicación base para pruebas

App full-stack mínima y autocontenida que sirve como **sistema bajo prueba (SUT)** para el Reto AI-First · Track QA. Tu trabajo **no es modificar esta app**, sino **cubrirla con pruebas** (funcionales, API, datos, integración y automatización UI/E2E).

> Consulta el README principal del reto en `../README.md` para el contexto completo del proyecto, los documentos de evaluación y la estrategia recomendada.

## Cómo ejecutarla

**Opción A — Docker (recomendada, un comando):**
```bash
docker compose up --build
```

**Opción B — Python (3.10+):**
```bash
pip install -r requirements.txt
uvicorn app:app --port 8000
```

Luego abre **http://localhost:8000** (frontend) y **http://localhost:8000/docs** (documentación interactiva de la API).

La base de datos SQLite (`minitienda.db`) se crea y se siembra sola en el primer arranque. Para reiniciar el estado, borra ese archivo.

## Componentes (todas las capas que debes probar)

| Capa | Dónde |
|---|---|
| Frontend | Página en `/` (lista productos, crea órdenes) |
| Backend / API | Rutas bajo `/api` |
| Base de datos | SQLite local (`minitienda.db`) |
| Web service | Endpoints REST (ver abajo) |
| Integración | Servicio de precios/impuestos `/api/pricing/quote` |

## Contrato de la API

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/health` | Estado del servicio |
| GET | `/api/products` | Lista de productos |
| GET | `/api/products/{id}` | Detalle de producto (404 si no existe) |
| GET | `/api/pricing/quote?subtotal_cents=&country=` | Cotización de impuesto/total |
| POST | `/api/orders` | Crea una orden |
| GET | `/api/orders/{id}` | Detalle de una orden (404 si no existe) |

**Crear orden** — cuerpo:
```json
{ "country": "CO", "items": [ { "product_id": 1, "qty": 2 } ] }
```

Notas de negocio:
- Los montos están en **centavos** (`price_cents`, `total_cents`, etc.).
- Impuesto por país: `CO` = 19%, `US` = 0%, cualquier otro = 10% por defecto.
- Al crear una orden, el stock del producto se descuenta.

## Simular una caída de la integración

Para probar el comportamiento ante un fallo del servicio de precios, arranca con:
```bash
PRICING_FAIL=1 uvicorn app:app --port 8000      # o la variable en docker-compose
```

## Qué se espera de ti

Diseña y ejecuta una estrategia de pruebas que cubra las capas anteriores: casos funcionales (happy path, borde y negativos), validación de la API y sus contratos, verificación de datos en la BD, comportamiento de la integración (incluida su caída) y automatización UI/E2E. Recuerda: **todo se construye orquestando IA a través de Hermes**, no escribiendo scripts a mano.

Reporta los defectos que encuentres con severidad, pasos de reproducción y evidencia.
