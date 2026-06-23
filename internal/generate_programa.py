"""Generate 1-programa-ai-first-fase1.pdf using ReportLab + DejaVu Sans."""
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
    TableStyle,
)

FONT_DIR = "/Users/dorothy/Library/Fonts"
pdfmetrics.registerFont(TTFont("DejaVu", f"{FONT_DIR}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", f"{FONT_DIR}/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Italic", f"{FONT_DIR}/DejaVuSans-Oblique.ttf"))

TEAL = colors.HexColor("#006A71")
TEAL_LIGHT = colors.HexColor("#E0F2F3")
TEAL_MID = colors.HexColor("#B2DFDB")
WHITE = colors.white
GREY_ROW = colors.HexColor("#EEEEEE")

def styles():
    base = dict(fontName="DejaVu", fontSize=9.5, leading=16, alignment=TA_JUSTIFY,
                spaceAfter=6)
    return {
        "title": ParagraphStyle("title", fontName="DejaVu-Bold", fontSize=22,
                                textColor=TEAL, alignment=TA_CENTER, spaceAfter=14),
        "subtitle": ParagraphStyle("subtitle", fontName="DejaVu", fontSize=11,
                                   textColor=colors.HexColor("#444444"),
                                   alignment=TA_CENTER, spaceAfter=6),
        # h1 inner: white bold text inside the teal Table cell
        "h1": ParagraphStyle("h1", fontName="DejaVu-Bold", fontSize=14,
                              textColor=WHITE, alignment=TA_LEFT, leading=20),
        "h2": ParagraphStyle("h2", fontName="DejaVu-Bold", fontSize=11,
                              textColor=TEAL, spaceBefore=16, spaceAfter=6),
        "h3": ParagraphStyle("h3", fontName="DejaVu-Bold", fontSize=9.5,
                              textColor=colors.HexColor("#333333"),
                              spaceBefore=12, spaceAfter=5),
        "body": ParagraphStyle("body", **base),
        "bullet": ParagraphStyle("bullet", **{**base, "leftIndent": 14,
                                              "bulletIndent": 4, "spaceAfter": 5}),
        "note": ParagraphStyle("note", fontName="DejaVu-Italic", fontSize=8.5,
                               textColor=colors.HexColor("#555555"),
                               alignment=TA_JUSTIFY, spaceAfter=6, leading=13),
        "box": ParagraphStyle("box", fontName="DejaVu", fontSize=9.5,
                              backColor=TEAL_LIGHT, borderColor=TEAL, borderWidth=1,
                              borderPad=10, leading=16, alignment=TA_JUSTIFY,
                              spaceAfter=10),
    }

LLM_NOTE = ("Hermes como agente principal y uno o varios LLMs de su preferencia "
            "para codificar o implementar (ej: Claude Sonnet, Haiku, Opus, Codex, "
            "DeepSeek, Kimi K2, etc.)")

def tbl_style(header_bg=TEAL, alt=GREY_ROW):
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "DejaVu-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("FONTNAME", (0, 1), (-1, -1), "DejaVu"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, alt]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BBBBBB")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ])

def build():
    S = styles()
    W = A4[0] - 4 * cm

    def h1(text):
        t = Table([[Paragraph(text, S["h1"])]], colWidths=[W])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), TEAL),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ]))
        return t
    def h2(text): return Paragraph(text, S["h2"])
    def h3(text): return Paragraph(text, S["h3"])
    def p(text):  return Paragraph(text, S["body"])
    def b(text):  return Paragraph(f"• {text}", S["bullet"])
    def note(text): return Paragraph(text, S["note"])
    def sp(h=0.4): return Spacer(1, h * cm)
    def hr(): return HRFlowable(width="100%", thickness=0.5,
                                color=colors.HexColor("#CCCCCC"), spaceAfter=4)

    story = []

    # ── Title block ──────────────────────────────────────────────────────────
    story += [
        sp(1.0),
        Paragraph("Programa AI-First · Fase 1", S["title"]),
        Paragraph("Jikkosoft — Preparación y Reto", S["subtitle"]),
        Paragraph("Preparado por Diego Trujillo · diego.trujillo@jikkosoft.com", S["subtitle"]),
        sp(0.8),
        hr(),
        sp(0.8),
    ]

    # ── Principio fundacional ────────────────────────────────────────────────
    story += [
        h1("Principio fundacional"),
        sp(0.4),
        Paragraph(
            "Todo proyecto AI empieza con <b>/init</b>. "
            "Antes de escribir una sola spec, antes de tocar código, antes de todo: "
            "ejecuta <b>claude /init</b> en el repositorio. Esto genera el CLAUDE.md "
            "base y establece el contrato AI del proyecto. Sin este paso, la IA "
            "trabaja sin contexto y los resultados son impredecibles.",
            S["box"],
        ),
        sp(0.6),
    ]

    # ── Estructura general ───────────────────────────────────────────────────
    story += [h1("Estructura general"), sp(0.4)]
    tbl_struct = Table(
        [
            ["Semana", "Tema", "Workshops"],
            ["1", "Claude CLI + Spec Engineering", "2"],
            ["2", "CLAUDE.md", "2"],
            ["3", "Plan & Loop · MCP Servers · Subagentes · Git", "2"],
            ["4", "Reto Fase 1 (DEV + QA en paralelo)", "—"],
        ],
        colWidths=[1.8 * cm, W - 4.8 * cm, 3 * cm],
    )
    tbl_struct.setStyle(tbl_style())
    story += [tbl_struct, sp(0.2),
              note("6 workshops en total · 1–2 por semana · evaluación el viernes de la semana 4."),
              sp(0.3)]

    # ── Semana 1 ─────────────────────────────────────────────────────────────
    story += [PageBreak(), h1("Semana 1 — Claude CLI"), sp(0.2),
              h2("Workshop 1 — Apertura + Claude CLI"),
              h3("Lunes"),
              b("Apertura del programa: contexto del “momento cero” y el nuevo modelo operativo AI-first."),
              b("Instalación y configuración: Claude Code + modelo conectado a Hermes."),
              b("El ritual /init en vivo sobre un repo vacío: qué genera, por qué importa."),
              b("Navegación básica: slash commands, permisos, modo interactivo vs. autónomo."),
              b(f"Hermes como intermediario obligatorio: toda interacción con modelos pasa por aquí. "
                f"Libertad de elegir uno o varios LLMs para codificar o implementar "
                f"(ej: Claude Sonnet, Haiku, Opus, Codex, DeepSeek, Kimi K2, etc.)."),
              sp(0.3),
              h2("Workshop 2 — Spec Engineering"),
              h3("Jueves o viernes"),
              b("Por qué la calidad de la spec supera la elección del modelo."),
              b("La matriz real: 3 niveles de spec × 7 modelos — caso de estudio extraído del "
                "experimento interno de Diego (<i>hermes-exploratory</i>)."),
              b("Hallazgo clave: Haiku + Spec C (88 pts) &gt; Opus + Spec A (72 pts). "
                "Spec B + Sonnet es el punto de equilibrio costo/calidad."),
              b("Ejercicio práctico: cada participante escribe 3 versiones de spec para algo de "
                "su contexto y compara outputs."),
              sp(0.2),
              note("Días sin workshop: adaptación libre + punto de control "
                   "(3 líneas de avance + bloqueos vía Hermes)."),
              sp(0.3)]

    # ── Semana 2 ─────────────────────────────────────────────────────────────
    story += [PageBreak(), h1("Semana 2 — CLAUDE.md"), sp(0.2),
              h2("Workshop 3 — Anatomía del CLAUDE.md"),
              h3("Lunes"),
              b("El /init genera el esqueleto; tú lo conviertes en un contrato AI preciso."),
              b("Componentes esenciales: authority hierarchy, safe/unsafe zones, naming conventions, "
                "model selection table."),
              b("Revisión en vivo de un CLAUDE.md real de producción (21 KB, API de SILIN)."),
              b("Diferencia entre un README y un AI operating contract."),
              sp(0.3),
              h2("Workshop 4 — CLAUDE.md hands-on"),
              h3("Jueves o viernes"),
              b("Cada participante toma su repo actual (SILIN / integraciones) y escribe "
                "su propio CLAUDE.md desde cero."),
              b("Track DEV: orientado a construcción (safe zones para schema, API, FE)."),
              b("Track QA: orientado a pruebas (qué no modificar del SUT, cómo describir "
                "el alcance de cobertura)."),
              b("Revisión cruzada en pares."),
              sp(0.3)]

    # ── Semana 3 ─────────────────────────────────────────────────────────────
    story += [PageBreak(),
              h1("Semana 3 — Plan & Loop · MCP Servers · Subagentes · Git"),
              sp(0.2),
              h2("Workshop 5 — Plan Mode + Loop + Skills"),
              h3("Lunes"),
              b("/plan antes de cualquier tarea compleja: cómo estructurar el trabajo antes "
                "de generar código."),
              b("Loop modes para tareas iterativas."),
              b("Sistema everything-claude-code: el skill correcto para cada tipo de tarea.")]

    tbl5 = Table(
        [
            ["Skill", "Uso"],
            [":tdd-workflow", "Desarrollo guiado por pruebas"],
            [":backend-patterns", "APIs y servicios"],
            [":security-review", "Revisión de seguridad"],
            [":database-reviewer", "Schema y queries"],
        ],
        colWidths=[4 * cm, W - 4 * cm],
    )
    tbl5.setStyle(tbl_style(header_bg=colors.HexColor("#00838F"), alt=TEAL_LIGHT))
    story += [sp(0.1), tbl5, sp(0.2),
              b("Demostración completa: /init → /plan → build con skills apropiados."),
              sp(0.3),
              h2("Workshop 6 — MCP Servers + Subagentes + Git + Cierre"),
              h3("Jueves o viernes"),
              b("MCP Servers: Figma como fuente de diseño leíble por IA · Azure DevOps WI como PRD "
                "· claude-mem para memoria persistente entre sesiones."),
              b("Subagentes paralelos: el patrón LLM-as-judge (un modelo evalúa el output de otro). "
                "Caso real: job_hermes_gate en GitLab CI."),
              b("Git con AI: commits semánticos, PRs, ai-dev-log para trazabilidad de sesiones."),
              b("Cierre del curso y lanzamiento oficial de los Retos Fase 1."),
              sp(0.3)]

    # ── Semana 4 ─────────────────────────────────────────────────────────────
    story += [PageBreak(), h1("Semana 4 — Reto Fase 1"), sp(0.2),
              h2("Dos tracks en paralelo"), sp(0.1)]

    # Track DEV
    story += [
        h2("Track DEV — Implementa una app similar a mini-tienda-base"),
        p(f"<b>Misión:</b> En 4 días, implementar una app con la misma estructura que "
          f"<i>mini-tienda-base</i> — frontend, backend, base de datos e integración — "
          f"sobre un caso de uso comercial distinto a SILIN, sin escribir código a mano. "
          f"Todo se genera y se itera a través de {LLM_NOTE}."),
        sp(0.15),
        h3("Componentes obligatorios (misma estructura que mini-tienda-base):"),
    ]
    tbl_dev = Table(
        [
            ["Componente", "Requisito"],
            ["Backend", "Servicio con lógica de negocio y API REST"],
            ["Frontend", "Interfaz web funcional (equivalente a static/index.html)"],
            ["Base de datos", "PostgreSQL, SQLite, MongoDB o la de tu preferencia"],
            ["Integración", "Al menos una integración externa o entre módulos propios"],
        ],
        colWidths=[4 * cm, W - 4 * cm],
    )
    tbl_dev.setStyle(tbl_style())
    story += [tbl_dev, sp(0.2), h3("Reglas:")]
    for i, r in enumerate([
        "Cero código manual — solo especificas, diriges, revisas e iteras.",
        f"{LLM_NOTE} — obligatorio e innegociable.",
        "Caso de uso libre — distinto a SILIN y distinto a mini-tienda.",
        "Repositorio público (GitHub o GitLab).",
    ], 1):
        story.append(Paragraph(f"{i}. {r}", S["bullet"]))
    story.append(sp(0.3))

    # Track QA
    story += [
        h2("Track QA — Diseña y ejecuta una estrategia de pruebas"),
        p(f"<b>Misión:</b> En 4 días, diseñar, automatizar y ejecutar una estrategia de pruebas "
          f"E2E sobre la aplicación base provista (<i>mini-tienda-base</i>), sin escribir "
          f"scripts a mano. Se usa {LLM_NOTE}."),
        sp(0.15),
        h3("Requisitos mínimos de entrega:"),
    ]
    tbl_qa = Table(
        [
            ["Componente", "Requisito"],
            ["Plan de pruebas", "Estrategia, alcance, riesgos y criterios de aceptación"],
            ["Pruebas funcionales", "Casos: happy path, borde y negativos"],
            ["Automatización UI / E2E", "Suite automatizada sobre el frontend"],
            ["Pruebas de API", "Contratos, estados HTTP, errores"],
            ["Pruebas de datos e integración",
             "Validación de BD y de la integración de precios"],
            ["Reporte de defectos",
             "Hallazgos con severidad, pasos de reproducción y evidencia"],
        ],
        colWidths=[5.5 * cm, W - 5.5 * cm],
    )
    tbl_qa.setStyle(tbl_style())
    story += [tbl_qa, sp(0.2), h3("Reglas:")]
    for i, r in enumerate([
        "Cero scripts manuales — la IA los genera, tú especificas y revisas.",
        f"{LLM_NOTE} — obligatorio como agente principal.",
        "No modificar el código de producción del SUT.",
        "Repositorio público (GitHub o GitLab).",
    ], 1):
        story.append(Paragraph(f"{i}. {r}", S["bullet"]))
    story.append(sp(0.3))

    # ── Cronograma ───────────────────────────────────────────────────────────
    story += [PageBreak(), h1("Cronograma — Semana 4"), sp(0.2)]
    tc_hdr = ParagraphStyle("tc_hdr", fontName="DejaVu-Bold", fontSize=9,
                            textColor=WHITE, leading=13)
    tc_body = ParagraphStyle("tc_body", fontName="DejaVu", fontSize=8.5, leading=13,
                             alignment=TA_LEFT)
    def tc(text, hdr=False):
        return Paragraph(text, tc_hdr if hdr else tc_body)
    dia_w = 2.2 * cm
    col_w = (W - dia_w) / 2
    tbl_cron = Table(
        [
            [tc("Día", hdr=True), tc("DEV", hdr=True), tc("QA", hdr=True)],
            [tc("Lunes"),
             tc("/init → CLAUDE.md → primera spec → inicio de construcción"),
             tc("/init → plan de pruebas → setup Playwright / pytest")],
            [tc("Martes–\nJueves"),
             tc("Backend + Frontend + DB + Integración · punto de control diario (3 líneas vía Hermes)"),
             tc("E2E + API + datos + escenario PRICING_FAIL=1 · punto de control diario")],
            [tc("Viernes AM"),
             tc("Repo final + HERMES_CONTEXT.md"),
             tc("Repo final + HERMES_CONTEXT.md")],
            [tc("Viernes PM"),
             tc("Demo 5–7 min (viernes de la semana del reto) + cata por grupos"),
             tc("Demo 5–7 min (viernes de la semana del reto) + cata por grupos")],
        ],
        colWidths=[dia_w, col_w, col_w],
    )
    tbl_cron.setStyle(tbl_style())
    story += [tbl_cron, sp(0.3)]

    # ── Entregables ──────────────────────────────────────────────────────────
    story += [h1("Entregables de ambos tracks"), sp(0.2),
              b("<b>HERMES_CONTEXT.md</b> (obligatorio, tan importante como el código)"),
              sp(0.15), h3("Track DEV:")]
    for item in [
        "Qué construiste y qué problema resuelve",
        "Stack y arquitectura: componentes y cómo se conectan",
        "Cómo usaste Hermes y los LLMs: skills, specs y prompts que mejor funcionaron",
        "Decisiones y trade-offs",
        "Bloqueos y cómo los resolviste",
        "Qué mejorarías o pedirías",
        "Enlace al repositorio",
    ]:
        story.append(b(item))
    story += [sp(0.2), h3("Track QA:")]
    for item in [
        "Alcance: qué probaste y bajo qué estrategia",
        "Enfoque y herramientas: tipos de prueba y stack usado",
        "Cómo usaste Hermes y los LLMs: skills, specs e iteraciones",
        "Decisiones y trade-offs: qué priorizaste y por qué",
        "Bloqueos y cómo los resolviste",
        "Hallazgos principales / riesgos detectados",
        "Enlace al repositorio",
    ]:
        story.append(b(item))
    story.append(sp(0.3))

    # ── Criterios ────────────────────────────────────────────────────────────
    story += [PageBreak(), h1("Criterios de evaluación"), sp(0.2)]
    tbl_crit = Table(
        [
            ["Dimensión", "Peso"],
            ["Calidad del HERMES_CONTEXT.md y trazabilidad del proceso", "25%"],
            ["Autonomía: investigó y desbloqueó por cuenta propia", "25%"],
            ["Orquestación de IA: claridad de specs, iteración, manejo de contexto", "18%"],
            ["Funcionalidad E2E (DEV) / Cobertura y profundidad (QA)", "14%"],
            ["Previsión y comunicación a tiempo", "10%"],
            ["Criterio técnico (DEV) / Criterio de QA (QA)", "8%"],
        ],
        colWidths=[W - 2 * cm, 2 * cm],
    )
    tbl_crit.setStyle(tbl_style())
    story += [tbl_crit, sp(0.2),
              note("Se busca criterio y adaptación, no el proyecto más grande ni la suite más extensa."),
              sp(0.3)]

    # ── Créditos y costos ────────────────────────────────────────────────────
    story += [
        h1("Sobre créditos y costos"),
        sp(0.2),
        p("Los modelos tienen costo y las capas gratuitas se agotan. "
          "Prever esto es parte del reto."),
        sp(0.1),
        p("Si necesitas acceso a un modelo corporativo o te vas a quedar corto de créditos, "
          "levanta la mano a tiempo — no el último día. Anticiparte y comunicar a tiempo "
          "es una de las capacidades que se están evaluando."),
        sp(0.2),
        note("Dudas durante el programa: canalízalas a Diego Trujillo — diego.trujillo@jikkosoft.com o Google Chat."),
    ]

    out = "/Users/dorothy/Stuff/Jikkosoft/Code/ai/lab/reto-ai-first-fase1/1-programa-ai-first-fase1.pdf"
    doc = SimpleDocTemplate(
        out, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
    )
    doc.build(story)
    print(f"Generated: {out}")

if __name__ == "__main__":
    build()
