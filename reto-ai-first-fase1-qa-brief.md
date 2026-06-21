# Reto AI-First · Fase 1 — Track QA
**Diseña y ejecuta una estrategia de pruebas end-to-end orquestando IA — sin escribir scripts manualmente**

> Borrador v0.1 — preparado por Diego Trujillo · pendiente de validación con Juan David y Javier

---

## 1. Por qué hacemos esto

Jikkosoft está dando un paso hacia un modelo de trabajo **AI-first**: el rol de QA deja de ser *escribir y ejecutar pruebas a mano* y pasa a ser *especificar, orquestar y validar* la calidad con asistencia de IA.

Este reto es tu espacio para experimentar ese cambio de chip mental en un entorno seguro, con acompañamiento y una ruta de aprendizaje. No se trata de saberlo todo desde el día uno: se trata de **adaptarte, investigar y construir**.

## 2. El reto en una frase

En **4 días**, diseña, automatiza y ejecuta una estrategia de pruebas **end-to-end** sobre una aplicación base, **sin escribir scripts a mano**: todo se genera y se itera a través de **Hermes**.

## 3. Qué debes construir

Trabajarás sobre una **aplicación base** que te entregaremos (incluye backend, frontend, base de datos, web service e integración). Tu misión es **cubrirla con pruebas** y dejar evidencia de su calidad.

Tu entrega **debe incluir obligatoriamente**:

| Componente | Requisito mínimo |
|---|---|
| Plan de pruebas | Estrategia, alcance, riesgos y criterios de aceptación (qué es "done") |
| Pruebas funcionales | Casos documentados: happy path, borde y negativos |
| Automatización UI / E2E | Suite automatizada sobre el frontend |
| Pruebas de API / web service | Validación de endpoints (contratos, estados, errores) |
| Pruebas de datos e integración | Validación de la BD y de la(s) integración(es) |
| Reporte de defectos y resultados | Hallazgos con severidad, pasos de reproducción y evidencia |

## 4. Reglas del juego

1. **Cero scripts manuales.** No escribes el código de prueba tú; lo genera la IA. Tu trabajo es especificar, dirigir, revisar e iterar.
2. **Hermes es obligatorio e innegociable.** Toda interacción con modelos (generación, consulta, refactor) pasa **a través de Hermes**. Nada de consultas sueltas por fuera.
3. **Trabaja sobre la app base.** No modifiques su código de producción salvo lo mínimo para habilitar las pruebas.
4. **Tu repo, tu casa.** Sube tus artefactos de prueba a **GitHub público** o **GitLab**, donde prefieras.
5. **Provee tu acceso a modelos.** Necesitarás un proveedor LLM conectado a Hermes (OpenAI, Anthropic, etc.). Ver punto 7 sobre créditos.

## 5. Qué debes entregar

1. **Repositorio** (GitHub público o GitLab) con los artefactos de prueba: plan, casos, suites automatizadas y reporte.
2. **Contexto de Hermes en un archivo `.md`** — el resumen contextual de tu trabajo con Hermes (plantilla abajo). Este archivo es tan importante como las pruebas: es la evidencia de *cómo* trabajaste.
3. **Demo corta** (5–7 min) el día de evaluación: recorrido por la estrategia, la automatización corriendo y los hallazgos.

### Plantilla del entregable `HERMES_CONTEXT.md`
- **Alcance:** qué probaste y bajo qué estrategia
- **Enfoque y herramientas:** tipos de prueba y stack usado
- **Cómo usaste Hermes:** skills/instrucciones clave, specs o prompts que mejor funcionaron, iteraciones
- **Decisiones y trade-offs:** qué priorizaste cubrir y por qué
- **Bloqueos y cómo los resolviste**
- **Hallazgos principales / riesgos detectados**
- **Qué mejorarías o pedirías**
- **Enlace al repositorio**

## 6. Cronograma (tentativo)

| Día | Fecha | Foco |
|---|---|---|
| Apertura | Lun 22 jun | Lanzamiento del reto, entrega de la app base, ruta de aprendizaje |
| Días 1–4 | Lun–Jue | Diseño + automatización + ejecución + puntos de control diarios |
| Evaluación | Vie 26 jun | Demos y revisión por grupos |

**Punto de control diario:** un reporte breve (3 líneas) de avance + bloqueos, vía Hermes/Drive. Sirve para acompañarte, no para vigilarte.

## 7. Sobre créditos y costos — léelo

Los modelos cuestan y las capas gratuitas se agotan. **Prever esto es parte del reto.**

Si ves que te vas a quedar corto de créditos o necesitas acceso a un modelo corporativo, **levanta la mano a tiempo** (no el último día). Anticiparte y comunicar a tiempo es justamente una de las capacidades que estamos observando.

## 8. Ruta de aprendizaje sugerida

No estás solo. Te sugerimos recursos para arrancar (no son obligatorios ni exhaustivos — explóralos y trae los tuyos). Sea cual sea la herramienta que elijas, recuerda que debe conectarse **a través de Hermes**.

**Fundamentos de orquestación de IA y agentes**

- Anthropic — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Anthropic Academy — [Build with Claude](https://www.anthropic.com/learn/build-with-claude)

**Escritura de specs / prompting efectivo**

- [Guía de prompt engineering (Claude Docs)](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Tutorial interactivo de prompting (Anthropic)](https://github.com/anthropics/prompt-eng-interactive-tutorial)

**QA y automatización de pruebas** (elige según el stack de la app base)

- [Playwright — automatización E2E](https://playwright.dev/docs/intro)
- [Postman Learning Center — pruebas de API](https://learning.postman.com/)

**Herramientas de desarrollo asistido por IA**

- [Documentación de Claude Code](https://code.claude.com/docs/en/overview)

**Uso de Hermes (obligatorio)**

- Hermes Agent (Nous Research) — [repositorio y documentación oficial](https://github.com/NousResearch/hermes-agent)

**Manejo de repositorios (GitHub / GitLab)**

- [GitHub — primeros pasos](https://docs.github.com/get-started)
- [GitLab Docs](https://docs.gitlab.com/)

## 9. Cómo te vamos a evaluar (visión general)

No buscamos la suite más grande, buscamos **criterio y adaptación**. Valoramos especialmente:

- La **calidad de tu `HERMES_CONTEXT.md`** y la trazabilidad de tu proceso
- Tu **autonomía**: cómo investigaste y resolviste bloqueos por tu cuenta
- Qué tan bien **orquestaste la IA** (claridad de tus specs, iteración, contexto)
- La **cobertura y profundidad** de tus pruebas (funcional, datos, integración, automatización)
- Tu **previsión y comunicación** a tiempo

---

_Dudas durante el reto: canalízalas a Diego Trujillo por Google Chat._
