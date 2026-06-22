# Reto AI-First Fase 1

Este repositorio contiene el **Reto AI-First · Fase 1**, que comprende dos tracks paralelos:

- **Track DEV** — construir un producto full-stack (backend + frontend + DB + integración) sobre cualquier caso de uso comercial distinto a SILIN, sin escribir código manualmente, usando Hermes como agente principal y uno o varios LLMs de su preferencia para codificar o implementar (ej: Claude Sonnet, Haiku, Opus, Codex, DeepSeek, Kimi K2, etc.).
- **Track QA** — diseñar y ejecutar una estrategia de pruebas completa sobre la **mini tienda full-stack** incluida en este repo, sin modificar la aplicación, usando Hermes como agente principal y uno o varios LLMs de su preferencia para codificar o implementar (ej: Claude Sonnet, Haiku, Opus, Codex, DeepSeek, Kimi K2, etc.).

## Contenido del repositorio

- `1-programa-ai-first-fase1.pdf`: **programa completo** — curso de 4 semanas + Reto Fase 1 (DEV y QA).
- `mini-tienda-base/`: aplicación base mínima y autocontenida que sirve como **Sistema Bajo Prueba (SUT)** para el Track QA.
- `2a-reto-ai-first-fase1-brief.pdf`: brief del Reto Fase 1 — Track DEV.
- `2b-reto-ai-first-fase1-qa-brief.pdf`: brief del Reto Fase 1 — Track QA.
- `docs/reto-ai-first-fase1-evaluacion-interna.pdf`: documento de evaluación interna (acceso restringido).

## Qué es este reto

Ambos tracks tienen 4 días de ejecución y entregan: repo + `HERMES_CONTEXT.md` + demo de 5–7 min el viernes de la semana del reto.

### Track DEV

Construir un producto full-stack end-to-end sobre **cualquier caso de uso comercial** (distinto a SILIN), sin escribir código manualmente. Se espera:

- Backend + frontend + base de datos + integración externa.
- 100% generado mediante Hermes (agente AI).
- Idea libre; el criterio es coherencia y funcionamiento real del producto.

### Track QA

El foco es **probar** la mini tienda incluida en este repo, no modificarla. Se espera diseñar y ejecutar una estrategia de pruebas que cubra:

- Casos funcionales del frontend y backend.
- Contratos de API y validación de respuestas.
- Verificación de datos en la base SQLite.
- Comportamiento de la integración de precios/impuestos.
- Escenarios negativos y de borde.
- Automatización UI/E2E.
- Manejo de fallos en integración (simulación de caídas).

## MiniTienda Base App

`mini-tienda-base/` es la aplicación de referencia que debes usar como base para el reto. Incluye:

- Frontend web estático (`static/index.html`).
- Backend Python con FastAPI (`app.py`).
- Base de datos SQLite local (`minitienda.db` se genera en el primer arranque).
- Endpoints REST para productos, órdenes, estado de salud y cotización de precios.

### Endpoints principales

| Método | Ruta                 | Descripción                          |
| ------ | -------------------- | ------------------------------------ |
| GET    | `/api/health`        | Verifica disponibilidad del servicio |
| GET    | `/api/products`      | Lista de productos                   |
| GET    | `/api/products/{id}` | Detalle de producto                  |
| GET    | `/api/pricing/quote` | Cotiza impuestos y total según país  |
| POST   | `/api/orders`        | Crea una orden                       |
| GET    | `/api/orders/{id}`   | Detalle de orden                     |

### Requisitos de negocio clave

- Montos en **centavos** (`price_cents`, `total_cents`, etc.).
- Impuesto por país:
  - `CO`: 19%
  - `US`: 0%
  - otro: 10%
- Crear orden reduce stock del producto asociado.
- Validar códigos de país, cantidades y existencia de producto.

## Cómo ejecutar la app

### Opción A — Docker (recomendada)

```bash
cd mini-tienda-base
docker compose up --build
```

### Opción B — Python local

```bash
cd mini-tienda-base
pip install -r requirements.txt
uvicorn app:app --port 8000
```

Luego abre:

- `http://localhost:8000` para el frontend
- `http://localhost:8000/docs` para la documentación interactiva de la API

## Simular fallo del servicio de precios

Para probar el comportamiento bajo falla de integración:

```bash
PRICING_FAIL=1 uvicorn app:app --port 8000
```

## Estrategia de pruebas recomendada

Se recomienda cubrir estos ámbitos:

- Pruebas de integración de API: flujo completo de creación de órdenes y consulta de datos.
- Pruebas de contrato: respuestas correctas, códigos HTTP, campos obligatorios.
- Pruebas de datos: consistencia entre orden, producto y stock.
- Pruebas de UI/E2E: interacción de compra y confirmación de orden.
- Pruebas de fallos: servicio de precios caído, producto inexistente, stock insuficiente.

## Cómo contribuir

1. Crear una rama de trabajo para tu solución.
2. Mantener el foco en pruebas, no en cambios funcionales de la app.
3. Documentar tus casos de prueba, resultados y evidencias.
4. Evitar agregar credenciales o datos sensibles.

## Notas adicionales

- La aplicación base está diseñada para ser un **objetivo estable de evaluación**.
- No se espera reescribir el core de `mini-tienda-base`; se espera probarlo.
- Usa los documentos del reto (`brief`, `qa-brief`, `evaluacion-interna`) para orientar tu estrategia.
