# Reto AI-First Fase 1

Este repositorio contiene el **Reto AI-First · Fase 1** — dos tracks en paralelo con 4 días de ejecución cada uno.

## Estructura del repositorio

```
1-docs/
  1a-guia-ai-first.pdf              # Programa AI-First · Fase 1 — guía del curso completo
  1b-guia-ai-hermes-claude.pdf      # Guía de uso de Hermes + Claude (referencia de herramientas)

2-workshops/
  guia-personal-workshops-1-2.md   # Guía personal — workshops 1 y 2 (Claude Code + Spec Engineering)
  guia-personal-workshops-3-4.md   # Guía personal — workshops 3 y 4 (CLAUDE.md + Plan & Loop + MCP)

3-challenge/
  2a-reto-ai-first-fase1.pdf        # Reto — Track DEV
  2b-reto-ai-first-fase1-qa.pdf     # Reto — Track QA
  gestor-inventario/                # SUT (System Under Test) para el Track QA

4-internal/                         # Acceso restringido (git-crypt)
  reto-ai-first-fase1-evaluacion-interna.pdf
  STEPS.md
  input_*.md
  generate_*.py
```

## Qué es este reto

Ambos tracks tienen ejecución del 26 jun al 6 jul y entregan: repo + `SOUL.md` + demo de 5–7 min el martes 7 de julio.

### Track DEV

Implementar el **Portal de Convocatorias Públicas** con Hermes como orquestador y LLMs de tu elección. Sin código manual.

**Requisitos:**
- Autenticación (registro / login con JWT)
- Backend REST — búsqueda, filtros, bookmarks
- Frontend web funcional
- Base de datos (SQLite o PostgreSQL) — usuarios, bookmarks, búsquedas guardadas
- Integración con **datos.gov.co SECOP** — consulta en vivo de convocatorias públicas colombianas

**Entregables:**

| Archivo | Propósito |
|---------|-----------|
| `SOUL.md` | Log del proceso: scope, tooling, decisiones, blockers |
| App funcionando | Backend + frontend + DB + integración, ejecutable localmente |
| `README.md` | Cómo ejecutar, arquitectura, descripción del caso de uso |

### Track QA

Diseñar y ejecutar una estrategia de pruebas completa sobre `3-challenge/gestor-inventario`. No modificar la app — probarla.

**Entregables:**

| Archivo | Propósito |
|---------|-----------|
| `SOUL.md` | Log del proceso: scope, tooling, decisiones, hallazgos, blockers |
| Plan de pruebas | Estrategia, alcance, riesgos, criterios de aceptación |
| Casos de prueba | Happy path + edge + negativos, documentados |
| Suite API | Contrato + validación de errores — generada con Hermes + LLM, ejecutable con `pytest` |
| Suite E2E _(deseable)_ | Playwright o equivalente contra localhost:8000 — generada con IA si el tiempo lo permite |
| Reporte de defectos | Hallazgos con severidad, pasos de reproducción, evidencia |

## Gestor de Inventario (SUT — Track QA)

`3-challenge/gestor-inventario/` es la aplicación a probar. Incluye:

- Frontend web estático (`static/index.html`)
- Backend Python con FastAPI (`app.py`)
- Base de datos SQLite local (`inventario.db` se genera en el primer arranque)
- Endpoints REST para productos, proveedores, movimientos de stock y alertas
- Servicio de alertas de stock mínimo con simulación de caída (`ALERTS_FAIL=1`)

### Cómo ejecutar

```bash
# Docker (recomendado)
cd 3-challenge/gestor-inventario
docker compose up --build

# Python local
cd 3-challenge/gestor-inventario
pip install -r requirements.txt
uvicorn app:app --port 8000
```

Abre `http://localhost:8000` para el frontend y `http://localhost:8000/docs` para la API interactiva.

### Simular fallo del servicio de alertas

```bash
ALERTS_FAIL=1 uvicorn app:app --port 8000
```

Con esta variable activa, `/api/stock/alerts` y `POST /api/stock/movement` (type=OUT) retornan 503.

### Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/health` | Estado del servicio |
| GET | `/api/suppliers` | Lista de proveedores activos |
| GET | `/api/products` | Lista de productos activos |
| GET | `/api/products/{id}` | Detalle de producto — 404 si no existe |
| POST | `/api/products` | Crear producto (201 / 409 SKU duplicado) |
| POST | `/api/stock/movement` | Registrar movimiento IN o OUT (201 / 503 si ALERTS_FAIL) |
| GET | `/api/stock/alerts` | Productos con stock ≤ mínimo (503 si ALERTS_FAIL) |
| GET | `/api/movements` | Historial de movimientos |

### Aislamiento de base de datos para pruebas

```bash
DB_PATH=test.db uvicorn app:app --port 8001
```

### Dimensiones de cobertura esperadas

- Contrato de API — status codes, campos requeridos, shapes de error
- Funcional — happy path, edge cases, negativos por endpoint
- Integridad de datos — stock se actualiza correctamente tras movimientos
- Fallo de integración — `ALERTS_FAIL=1` → 503 en endpoints afectados
- UI / E2E — flujo de registro de movimientos y consulta de alertas

## Notas

- La app es un **objetivo estable de evaluación** — no se espera modificar su código.
- Usa los documentos del reto en `3-challenge/` para orientar tu estrategia.
- Hermes es el orquestador principal — todo via IA, sin scripts manuales.
