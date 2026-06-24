"""Generate workshops/guia-personal-workshops-1-2.pdf using ReportLab + DejaVu Sans."""
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable, KeepTogether, PageBreak, Paragraph,
    SimpleDocTemplate, Spacer, Table, TableStyle,
)
import os

FONT_DIR = "/Users/dorothy/Library/Fonts"
pdfmetrics.registerFont(TTFont("DejaVu",        f"{FONT_DIR}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold",   f"{FONT_DIR}/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Italic", f"{FONT_DIR}/DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Mono",   f"{FONT_DIR}/DejaVuSansMono.ttf"))

TEAL       = colors.HexColor("#006A71")
TEAL_LIGHT = colors.HexColor("#E0F2F3")
AMBER      = colors.HexColor("#FFF8E1")
AMBER_BDR  = colors.HexColor("#F9A825")
CODE_BG    = colors.HexColor("#F5F5F5")
CODE_BDR   = colors.HexColor("#BDBDBD")
WHITE      = colors.white
GREY_ROW   = colors.HexColor("#EEEEEE")


def build():
    OUT = os.path.join(os.path.dirname(__file__), "guia-personal-workshops-1-2.pdf")
    doc = SimpleDocTemplate(
        OUT, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
    )
    W = A4[0] - 4 * cm

    S = {
        "title":   ParagraphStyle("title",   fontName="DejaVu-Bold",   fontSize=22,
                                  textColor=TEAL, alignment=TA_CENTER, spaceAfter=10),
        "subtitle":ParagraphStyle("subtitle", fontName="DejaVu",        fontSize=11,
                                  textColor=colors.HexColor("#444444"),
                                  alignment=TA_CENTER, spaceAfter=4),
        "author":  ParagraphStyle("author",  fontName="DejaVu-Italic",  fontSize=9.5,
                                  textColor=colors.HexColor("#666666"),
                                  alignment=TA_CENTER, spaceAfter=4),
        "h2":      ParagraphStyle("h2",      fontName="DejaVu-Bold",    fontSize=11,
                                  textColor=TEAL, spaceBefore=14, spaceAfter=6),
        "body":    ParagraphStyle("body",    fontName="DejaVu",         fontSize=9.5,
                                  leading=16, alignment=TA_JUSTIFY, spaceAfter=6),
        "bullet":  ParagraphStyle("bullet",  fontName="DejaVu",         fontSize=9.5,
                                  leading=16, leftIndent=14, bulletIndent=4, spaceAfter=5),
        "num":     ParagraphStyle("num",     fontName="DejaVu",         fontSize=9.5,
                                  leading=16, leftIndent=18, spaceAfter=5),
        "code":    ParagraphStyle("code",    fontName="DejaVu-Mono",    fontSize=8.5,
                                  backColor=CODE_BG, borderColor=CODE_BDR, borderWidth=0.5,
                                  borderPad=8, leading=14, spaceAfter=8, alignment=TA_LEFT),
        "callout": ParagraphStyle("callout", fontName="DejaVu-Italic",  fontSize=9.5,
                                  backColor=AMBER, borderColor=AMBER_BDR, borderWidth=1,
                                  borderPad=10, leading=16, alignment=TA_JUSTIFY, spaceAfter=8),
        "box":     ParagraphStyle("box",     fontName="DejaVu",         fontSize=9.5,
                                  backColor=TEAL_LIGHT, borderColor=TEAL, borderWidth=1,
                                  borderPad=10, leading=16, alignment=TA_JUSTIFY, spaceAfter=8),
        "link":    ParagraphStyle("link",    fontName="DejaVu",         fontSize=9.5,
                                  leading=16, spaceAfter=4),
        "h1_inner":ParagraphStyle("h1i",     fontName="DejaVu-Bold",    fontSize=14,
                                  textColor=WHITE, alignment=TA_LEFT, leading=20),
        "footer":  ParagraphStyle("footer",  fontName="DejaVu-Italic",  fontSize=8.5,
                                  textColor=colors.HexColor("#777777"),
                                  alignment=TA_CENTER, spaceAfter=4),
    }

    def h1(text):
        t = Table([[Paragraph(text, S["h1_inner"])]], colWidths=[W])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), TEAL),
            ("TOPPADDING",    (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING",   (0, 0), (-1, -1), 12),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ]))
        return t

    def h2(text):    return Paragraph(text, S["h2"])
    def p(text):     return Paragraph(text, S["body"])
    def b(text):     return Paragraph(f"• {text}", S["bullet"])
    def sp(h=0.4):   return Spacer(1, h * cm)
    def hr():        return HRFlowable(width="100%", thickness=0.5,
                                       color=colors.HexColor("#CCCCCC"), spaceAfter=4)
    def code(text):  return Paragraph(text.replace("\n", "<br/>"), S["code"])
    def callout(t):  return Paragraph(t, S["callout"])
    def box(t):      return Paragraph(t, S["box"])
    def lnk(label, url):
        return Paragraph(
            f'• <a href="{url}" color="#0066CC"><u>{label}</u></a>', S["link"]
        )

    def tbl_style(header_bg=TEAL, alt=GREY_ROW):
        return TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0),  header_bg),
            ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
            ("FONTNAME",      (0, 0), (-1, 0),  "DejaVu-Bold"),
            ("FONTNAME",      (0, 1), (-1, -1), "DejaVu"),
            ("FONTSIZE",      (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, alt]),
            ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#BBBBBB")),
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING",    (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ])

    _th = ParagraphStyle("_th", fontName="DejaVu-Bold", fontSize=9, textColor=WHITE, leading=13)
    _tb = ParagraphStyle("_tb", fontName="DejaVu", fontSize=9, leading=14)
    def tc(t, hdr=False): return Paragraph(t, _th if hdr else _tb)

    story = []

    # ── Title ────────────────────────────────────────────────────────────────
    story += [
        sp(2.0),
        Paragraph("Mi experiencia: Claude Code + Spec Engineering", S["title"]),
        sp(0.4),
        Paragraph("Guía rápida para el equipo dev — Jikkosoft AI-First", S["subtitle"]),
        sp(0.1),
        Paragraph("Diego Trujillo · Etapa 1 · Miércoles 24 jun 2026", S["author"]),
        sp(1.0),
        hr(),
        sp(0.8),
    ]

    # ── Cambio de paradigma ──────────────────────────────────────────────────
    story += [
        box('Antes de esto pensaba en IA como “autocompletado avanzado”. '
            "Lo que cambió: el modelo no es el protagonista, <b>la spec sí lo es</b>. "
            "El mejor modelo con una spec mala produce basura. "
            "El modelo más barato con una spec bien escrita produce output de producción. "
            "Eso lo confirma el experimento interno <i>hermes-exploratory</i>."),
        sp(0.4),
    ]

    # ── Workshop 1 ───────────────────────────────────────────────────────────
    story += [h1("Workshop 1 — Claude Code + Hermes · Miércoles 24 jun (1–1.5 hrs)"), sp(0.4)]

    story += [h2("Las herramientas"), sp(0.1)]
    tbl_tools = Table(
        [
            [tc("Herramienta", hdr=True), tc("Rol", hdr=True)],
            [tc("Claude Code (Anthropic)"),
             tc("Agente de código en terminal — ejecuta, edita, "
                "crea archivos, razona sobre el código")],
            [tc("Hermes (NousResearch)"),
             tc("Capa de orquestación: selecciona el modelo y administra el contexto")],
        ],
        colWidths=[4.5 * cm, W - 4.5 * cm],
    )
    tbl_tools.setStyle(tbl_style(header_bg=colors.HexColor("#00838F"), alt=TEAL_LIGHT))
    story += [tbl_tools, sp(0.2),
              p("<b>Regla del programa:</b> toda interacción con LLMs pasa por Hermes. "
                "Claude Code es el ejecutor — Hermes elige el modelo correcto para cada tarea."),
              sp(0.3)]

    story += [
        h2("Instalación en 2 pasos"), sp(0.1),
        code("# 1. Claude Code\n"
             "# Descargar desde https://claude.ai/code\n"
             "claude --version   # verifica instalación\n\n"
             "# 2. Hermes\n"
             "curl -fsSL https://raw.githubusercontent.com/NousResearch/"
             "hermes-agent/main/scripts/install.sh | bash\n"
             "hermes doctor      # verifica conexión a proveedores\n"
             "hermes setup       # conecta Anthropic / DeepSeek / Moonshot"),
        sp(0.2),
    ]

    story += [KeepTogether([
        h2("El ritual /init — por qué importa"),
        sp(0.1),
        code("# En cualquier repo vacío o existente:\nclaude /init"),
        p("Genera el <b>CLAUDE.md</b> base: el contrato AI del proyecto. "
          "Sin este archivo, el modelo trabaja sin contexto y alucina convenciones, "
          "nombres de columnas, rutas. Con él, cualquier modelo (incluso Haiku) "
          "respeta las reglas del proyecto."),
        sp(0.1),
        b("Authority hierarchy (qué puede y qué no puede hacer la IA)"),
        b("Naming conventions del proyecto"),
        b("Safe/unsafe zones (qué archivos nunca tocar)"),
        b("Stack y arquitectura"),
        sp(0.2),
        callout("Mi experiencia: la primera vez que lo corrí en el repo de SILIN "
                "generó un CLAUDE.md de 4 KB que luego expandí a 21 KB. "
                "Desde entonces el modelo no volvió a inventar nombres de tablas."),
    ])]
    story += [sp(0.3)]

    story += [
        h2("Navegación básica en Hermes"), sp(0.1),
        code("hermes model                          # selector visual de modelo\n"
             "/model anthropic:claude-sonnet-4-6   # cambiar modelo sin salir\n"
             "/new                                  # conversación fresca — evita memory bleed\n"
             "hermes config list                    # ver claves de configuración"),
        b("<b>Interactivo</b> (<i>hermes</i>): el agente pide confirmación antes de ejecutar"),
        b("<b>Autónomo</b> (<i>hermes --auto</i>): ejecuta sin confirmar "
          "— usar solo en ramas desechables"),
        sp(0.3),
    ]

    story += [
        h2("Videos y recursos"), sp(0.1),
        lnk("Anthropic YouTube — tutoriales y demos de Claude Code",
            "https://www.youtube.com/@Anthropic"),
        lnk("Claude Code docs — quickstart oficial",
            "https://code.claude.com/docs/en/overview"),
        lnk("Repositorio Hermes (NousResearch)",
            "https://github.com/NousResearch/hermes-agent"),
        sp(0.5),
    ]

    # ── Workshop 2 ───────────────────────────────────────────────────────────
    story += [h1("Workshop 2 — Spec Engineering · Miércoles 24 jun, tarde (1–1.5 hrs)"), sp(0.4)]

    story += [KeepTogether([
        h2("El hallazgo que lo cambia todo"),
        sp(0.1),
        code("Spec A (~150 palabras) + Opus 4.8   → 72 pts\n"
             "Spec C (~480 palabras) + Haiku 4.5  → 88 pts"),
        callout("<b>Conclusión:</b> mejorar la spec es 3× más barato y efectivo "
                "que subir de modelo. "
                "El punto de equilibrio costo/calidad: <b>Spec B + Sonnet</b>."),
    ])]
    story += [sp(0.3)]

    story += [h2("Los 3 niveles de spec"), sp(0.1)]
    tbl_spec = Table(
        [
            [tc("Nivel", hdr=True), tc("Tamaño aprox.", hdr=True), tc("Resultado típico", hdr=True)],
            [tc("Spec A — básica"),     tc("&lt; 150 palabras"),
             tc("Modelo alucina tablas, ignora constraints")],
            [tc("Spec B — equilibrio"), tc("300–500 palabras"),
             tc("Punto de equilibrio costo/calidad ✓")],
            [tc("Spec C — detallada"),  tc("500+ palabras"),
             tc("Máxima calidad, mejor con tareas complejas")],
        ],
        colWidths=[4 * cm, 3.5 * cm, W - 7.5 * cm],
    )
    tbl_spec.setStyle(tbl_style(header_bg=colors.HexColor("#00838F"), alt=TEAL_LIGHT))
    story += [tbl_spec, sp(0.3)]

    story += [h2("Checklist de una Spec B efectiva"), sp(0.1)]
    for i, item in enumerate([
        "<b>Dominio</b> — qué representa en 2–3 oraciones",
        "<b>Scope</b> — lista de entidades/tablas con columnas clave",
        "<b>Tech stack</b> — versión de DB, IDs, formato de timestamps",
        "<b>Convenciones</b> — naming, columnas de estado, tipo de moneda (ej: centavos)",
        "<b>Reglas de integridad</b> — soft delete, ON DELETE, UNIQUE, CHECK constraints",
        "<b>Reglas de safe-change</b> — columnas nullable, sin renombrados, índices en FKs",
        "<b>Fuera de scope</b> — qué NO generar (evita tablas alucinadas)",
        "<b>Entregable esperado</b> — formato exacto (solo SQL, sin prosa, sin fences)",
    ], 1):
        story.append(Paragraph(f"{i}. {item}", S["num"]))
    story += [sp(0.3)]

    story += [
        h2("El ejercicio práctico que más me sirvió"), sp(0.1),
        code('Spec A: "Crea una tabla de órdenes con sus productos y precios."\n'
             '          → el modelo inventa nombres, olvida FKs, ignora soft delete\n\n'
             'Spec B: "Tabla `orders` con `id UUID PK`, `status VARCHAR CHECK(...)`,\n'
             '          `created_at TIMESTAMPTZ DEFAULT NOW()`, FK a `customers(id)`.\n'
             '          Soft delete: columna `deleted_at`. Montos en centavos (INTEGER).\n'
             '          Fuera de scope: pagos, envíos."\n'
             '          → output limpio, constraints correctos\n\n'
             'Spec C: Spec B + queries que deben funcionar + casos de borde\n'
             '          → output de producción directamente usable'),
        p("Comparar los tres outputs. El ejercicio dura 20 minutos y convence mejor "
          "que cualquier presentación."),
        sp(0.3),
    ]

    story += [KeepTogether([
        h2("Regla práctica"),
        sp(0.1),
        box("<b>score &lt; 80 → la spec necesita más detalle, no un modelo más caro.</b><br/><br/>"
            "Si el output no es lo que esperabas, antes de cambiar de modelo: agrega "
            "el punto del checklist que falta. Casi siempre es el 4, 5 o 7."),
    ])]
    story += [sp(0.3)]

    story += [
        h2("Videos y recursos"), sp(0.1),
        lnk("Prompt engineering guide (Anthropic)",
            "https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview"),
        lnk("Tutorial interactivo — Jupyter notebooks",
            "https://github.com/anthropics/prompt-eng-interactive-tutorial"),
        lnk("Experimento interno hermes-exploratory (acceso interno)",
            "https://github.com/diegotrujillo-jikko/hermes-exploratory"),
        sp(0.5),
    ]

    # ── TL;DR ────────────────────────────────────────────────────────────────
    story += [
        h1("TL;DR para el equipo"), sp(0.3),
        code("1. Instala: Claude Code + Hermes\n"
             "2. En cada repo nuevo: claude /init  →  expande el CLAUDE.md generado\n"
             "3. Antes de pedir cualquier cosa al modelo: escribe la spec (mínimo Spec B)\n"
             "4. Si el output es malo: mejora la spec, no cambies el modelo\n"
             "5. Usa Hermes como entrada única — él elige el modelo correcto"),
        sp(0.8),
        hr(),
        sp(0.3),
        Paragraph("Preguntas → Diego Trujillo · diego.trujillo@jikkosoft.com", S["footer"]),
    ]

    doc.build(story)
    print(f"Generated: {OUT}")


if __name__ == "__main__":
    build()
