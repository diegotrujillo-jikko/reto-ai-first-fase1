# Reto AI-First Fase 1

Este repositorio contiene el **Reto AI-First · Fase 1**, que comprende dos tracks paralelos:

- **Track DEV** — implementar una app con la misma estructura que `3-challenge/mini-tienda-base` (frontend + backend + DB + integración) sobre un caso de uso comercial distinto a SILIN, sin escribir código manualmente, usando Hermes como agente principal y uno o varios LLMs de su preferencia para codificar o implementar (ej: Claude Sonnet, Haiku, Opus, Codex, DeepSeek, Kimi K2, etc.).
- **Track QA** — diseñar y ejecutar una estrategia de pruebas completa sobre la **mini tienda full-stack** en `3-challenge/mini-tienda-base`, sin modificar la aplicación, usando Hermes como agente principal y uno o varios LLMs de su preferencia para codificar o implementar (ej: Claude Sonnet, Haiku, Opus, Codex, DeepSeek, Kimi K2, etc.).

## Estructura del repositorio

```
1-docs/
  1a-guia-ai-first.pdf              # Programa AI-First · Fase 1 — guía del curso completo
  1b-guia-ai-hermes-claude.pdf      # Guía de uso de Hermes + Claude (referencia de herramientas)

2-workshops/
  guia-personal-workshops-1-2.md   # Guía personal — workshops 1 y 2 (Claude Code + Spec Engineering)
  guia-personal-workshops-3-4.md   # Guía personal — workshops 3 y 4 (CLAUDE.md + Plan & Loop + MCP)

3-challenge/
  2a-reto-ai-first-fase1.pdf        # Brief del Reto — Track DEV
  2b-reto-ai-first-fase1-qa.pdf     # Brief del Reto — Track QA
  mini-tienda-base/                 # SUT (System Under Test) para el Track QA

4-internal/                         # Acceso restringido (git-crypt)
  reto-ai-first-fase1-evaluacion-interna.pdf
  STEPS.md
  input_*.md
  generate_*.py
```

## Qué es este reto

> **⚠️ Reto en construcción.** El brief completo, instrucciones detalladas y carpetas de entrega para ambos tracks estarán disponibles en esta sección y en `3-challenge/` a partir del **viernes 26 de junio**.

Ambos tracks tienen 4 días de ejecución y entregan: repo + `HERMES_CONTEXT.md` + demo de 5–7 min el viernes de la semana del reto.

### Track DEV

> **⚠️ Instrucciones completas disponibles el 26 de junio.**

Implementar una app con la **misma estructura que `3-challenge/mini-tienda-base`** — frontend, backend, base de datos e integración — sobre un caso de uso comercial distinto a SILIN, sin escribir código manualmente. Se espera:

- Misma arquitectura de referencia: frontend web + backend con API + DB + al menos una integración.
- Caso de uso libre (e-commerce, reservas, inventario, etc.) — distinto a SILIN y distinto a mini-tienda.
- 100% generado con Hermes + LLMs; sin código manual.

### Track QA

> **⚠️ Instrucciones completas disponibles el 26 de junio.**

El foco es **probar** la mini tienda incluida en este repo, no modificarla. Se espera diseñar y ejecutar una estrategia de pruebas que cubra:

- Casos funcionales del frontend y backend.
- Contratos de API y validación de respuestas.
- Verificación de datos en la base SQLite.
- Comportamiento de la integración de precios/impuestos.
- Escenarios negativos y de borde.
- Automatización UI/E2E.
- Manejo de fallos en integración (simulación de caídas).

## MiniTienda Base App

> **ℹ️ La mini tienda actual es una versión preliminar.** El reto definitivo incluirá ajustes y casos de prueba adicionales que se publicarán el **26 de junio**.

`3-challenge/mini-tienda-base/` es la aplicación de referencia que debes usar como base para el reto. Incluye:

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
cd 3-challenge/mini-tienda-base
docker compose up --build
```

### Opción B — Python local

```bash
cd 3-challenge/mini-tienda-base
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
- No se espera reescribir el core de `3-challenge/mini-tienda-base`; se espera probarlo.
- Usa los documentos del reto en `3-challenge/` y `4-internal/` para orientar tu estrategia.
