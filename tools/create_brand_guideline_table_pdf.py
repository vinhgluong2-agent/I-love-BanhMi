from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "documents" / "ilovebanhmi_brand_guideline_table.pdf"
LOGO = ROOT / "logo.png"


def hex_color(value: str) -> colors.HexColor:
    return colors.HexColor(value)


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def swatch(name: str, hex_value: str, usage: str, note: str, body: ParagraphStyle):
    fill = hex_color(hex_value)
    text_color = colors.white if hex_value.upper() in {"#111111", "#000000", "#E31837"} else colors.black
    return [
        Table(
            [[Paragraph(hex_value, ParagraphStyle("swatchText", parent=body, alignment=TA_CENTER, textColor=text_color, fontSize=8))]],
            colWidths=[28 * mm],
            rowHeights=[13 * mm],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), fill),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D7C9B5")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            ),
        ),
        p(f"<b>{name}</b>", body),
        p(usage, body),
        p(note, body),
    ]


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=landscape(A4),
        rightMargin=12 * mm,
        leftMargin=12 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm,
        title="I Love BanhMi Brand Guideline Table",
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=25,
        textColor=colors.HexColor("#111111"),
        alignment=TA_LEFT,
        spaceAfter=2 * mm,
    )
    subtitle = ParagraphStyle(
        "SubtitleCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#5F5B53"),
        alignment=TA_LEFT,
    )
    section = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=14,
        textColor=colors.HexColor("#111111"),
        spaceBefore=5 * mm,
        spaceAfter=2 * mm,
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=10.5,
        textColor=colors.HexColor("#27231F"),
    )
    small = ParagraphStyle(
        "Small",
        parent=body,
        fontSize=7.3,
        leading=9.2,
        textColor=colors.HexColor("#5F5B53"),
    )
    th = ParagraphStyle(
        "TableHeader",
        parent=body,
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=10,
        textColor=colors.white,
        alignment=TA_CENTER,
    )

    story = []

    logo = Image(str(LOGO), width=43 * mm, height=29 * mm)
    header = Table(
        [
            [
                logo,
                [
                    p("I Love BanhMi Brand Guideline", title),
                    p("Quick compliance table for vendors, printers, packaging suppliers, signage fabricators, and internal review.", subtitle),
                    p("Reference: I Love BanhMi Brand Guideline 2026. Use source vector files for production: logo.ai / logo.svg.", small),
                ],
            ]
        ],
        colWidths=[50 * mm, 218 * mm],
    )
    header.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FDF5E6")),
                ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#111111")),
                ("LEFTPADDING", (0, 0), (-1, -1), 5 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 4 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4 * mm),
            ]
        )
    )
    story.append(header)
    story.append(Spacer(1, 3 * mm))

    story.append(p("1. Color System", section))
    core_colors = [
        [p("Swatch", th), p("Name", th), p("Use", th), p("Rule", th)],
        swatch("Vibrant Red", "#E31837", "Heart icon / key logo accent", "Do not recolor the heart in official logo artwork.", body),
        swatch("Mustard Yellow", "#FFC107", "Primary legacy logo/accent color", "Use only when matching approved legacy artwork or vendor reference.", body),
        swatch("Pure White", "#FFFFFF", "Logo lettering, decals, secondary elements", "Check visibility on transparent film and dark surfaces.", body),
        swatch("Logo Black", "#111111", "Logo outline, key contrast, text", "Keep high contrast; avoid weak gray substitutes.", body),
        swatch("Herb Green", "#159C46", "Herb/leaf details in the logo", "Keep as a small detail color, not a dominant packaging field.", body),
    ]
    color_table = Table(core_colors, colWidths=[31 * mm, 39 * mm, 88 * mm, 105 * mm], repeatRows=1)
    color_table.setStyle(table_style())
    story.append(color_table)

    story.append(Spacer(1, 2 * mm))
    support_colors = [
        [p("Swatch", th), p("Name", th), p("Use", th), p("Rule", th)],
        swatch("Mint Fresh", "#A8E6CF", "Support palette for packaging UI, tabs, accent panels", "Use as a fresh support color; do not cover natural kraft surfaces too heavily.", body),
        swatch("Warm Cream", "#FDF5E6", "Background, paper, calm negative space", "Use for panels, menus, quote sheets, and soft contrast.", body),
        swatch("Soft Pink", "#FFD1DC", "Secondary packaging band, sticker accents", "Use lightly; avoid candy-like full-field coverage.", body),
        swatch("Terracotta", "#E07A5F", "Small highlight / warmer CTA accent", "Use as an accent, not as a replacement for official heart red.", body),
        swatch("Muted Brown", "#5F5B53", "Support text, notes, kraft-compatible linework", "Good for subtle illustrations on kraft packaging.", body),
    ]
    support_table = Table(support_colors, colWidths=[31 * mm, 39 * mm, 88 * mm, 105 * mm], repeatRows=1)
    support_table.setStyle(table_style())
    story.append(support_table)

    story.append(p("2. Logo, Typography, and Usage Rules", section))
    rules = [
        [p("Area", th), p("Requirement", th), p("Production Check", th)],
        [
            p("<b>Logo Source</b>", body),
            p("Always use vector source files for final production: <b>logo.ai</b> or <b>logo.svg</b>. Do not trace from mockup screenshots.", body),
            p("Ask vendor to confirm they received the vector file and did not recreate the logo manually.", body),
        ],
        [
            p("<b>Clear Space</b>", body),
            p("Keep clear space around the full logo at least equal to the height of the red heart icon.", body),
            p("No text, borders, structural frames, or dieline cuts inside this protected space.", body),
        ],
        [
            p("<b>Minimum Size</b>", body),
            p("Print/production: logo width must be at least <b>1.5 cm</b>. Digital screen use: at least <b>40 px</b> wide.", body),
            p("Request a 1:1 proof if the mark is used on small stickers, seals, or packaging corners.", body),
        ],
        [
            p("<b>Typography</b>", body),
            p("Primary headings and menus: <b>Montserrat Black</b> or <b>Montserrat Medium</b>. Approved exception: the supplied cursive/script file for “vietnamese food & coffee”.", body),
            p("Do not re-type the logo or substitute similar fonts for logo artwork.", body),
        ],
        [
            p("<b>Packaging Direction</b>", body),
            p("Natural kraft may stay dominant. Use mint, cream, soft pink, and terracotta as controlled accents. Official logo colors stay unchanged.", body),
            p("Avoid heavy color filters, fake AI text, pasted rectangles, oversaturated red/yellow fields, or full-panel recolors.", body),
        ],
    ]
    rules_table = Table(rules, colWidths=[44 * mm, 130 * mm, 89 * mm], repeatRows=1)
    rules_table.setStyle(table_style())
    story.append(rules_table)

    story.append(p("3. Do / Do Not Checklist", section))
    checklist = [
        [p("Do", th), p("Do Not", th)],
        [
            p("Use the provided vector logo; keep proportions locked; preserve heart red, white letters, black outline, and herb green details.", body),
            p("Do not stretch, squish, warp, rotate casually, change colors, re-type, redraw, or place the logo inside a generic circle/plate.", body),
        ],
        [
            p("Use kraft-compatible line art, warm cream space, and small fresh accents for packaging concepts.", body),
            p("Do not let mint/pink overpower kraft texture or make mockups look like a flat color filter.", body),
        ],
        [
            p("For signage, allow physical halo lighting or handmade neon glow when it is part of fabrication.", body),
            p("Do not add artificial drop shadows/glows to the logo file for print production.", body),
        ],
        [
            p("Ask for printed color proof, material sample, dieline, bleed, and finish before mass production.", body),
            p("Do not approve production from a low-resolution screenshot or AI mockup with incorrect lettering.", body),
        ],
    ]
    checklist_table = Table(checklist, colWidths=[131.5 * mm, 131.5 * mm], repeatRows=1)
    checklist_table.setStyle(table_style())
    story.append(checklist_table)

    story.append(Spacer(1, 3 * mm))
    footer = Table(
        [[p("Vendor acknowledgment: by accepting production, supplier agrees to follow this brand compliance table and submit proofs before mass production.", small)]],
        colWidths=[263 * mm],
    )
    footer.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FDF5E6")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D7C9B5")),
                ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 3 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
            ]
        )
    )
    story.append(footer)

    doc.build(story)


def table_style() -> TableStyle:
    return TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111111")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#D7C9B5")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FFFDFA")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#FFFDFA"), colors.HexColor("#FDF5E6")]),
            ("LEFTPADDING", (0, 0), (-1, -1), 3 * mm),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
            ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2 * mm),
        ]
    )


if __name__ == "__main__":
    build()
    print(OUT)
