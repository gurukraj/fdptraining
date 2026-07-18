#!/usr/bin/env python3
"""Build the condensed AI-Native Software Development presentation."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import datetime

# ── Dimensions ──────────────────────────────────────────────
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

# ── Colour palette (academic, no dark) ──────────────────────
C_PRIMARY   = RGBColor(0x2E, 0x74, 0xB5)   # Professional blue
C_SECONDARY = RGBColor(0x2E, 0x86, 0xAB)   # Teal
C_ACCENT    = RGBColor(0x27, 0xAE, 0x60)   # Green
C_WARN      = RGBColor(0xF3, 0x9C, 0x12)   # Amber
C_RED       = RGBColor(0xE7, 0x4C, 0x3C)   # Red accent
C_PURPLE    = RGBColor(0x8E, 0x44, 0xAD)   # Purple accent
C_DARK_TEXT = RGBColor(0x2C, 0x3E, 0x50)   # Dark text
C_LIGHT_TXT = RGBColor(0x7F, 0x8C, 0x8D)   # Muted text
C_WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
C_LIGHT_BG  = RGBColor(0xF5, 0xF7, 0xFA)   # Card bg
C_CARD_BDR  = RGBColor(0xDE, 0xE2, 0xE6)   # Card border
C_TITLE_BAR = RGBColor(0x2E, 0x74, 0xB5)   # Title bar

prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H
BLANK_LAYOUT = prs.slide_layouts[6]  # Blank

# ────────────────────────── helpers ──────────────────────────
def _add_shape(slide, left, top, w, h, fill=None, border=None, radius=None):
    """Add a rounded rectangle shape."""
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    s = slide.shapes.add_shape(shape_type, left, top, w, h)
    s.line.fill.background()
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    else:
        s.fill.background()
    if border:
        s.line.fill.solid()
        s.line.fill.fore_color.rgb = border
        s.line.width = Pt(1)
    return s

def _set_text(shape, text, size=12, bold=False, color=C_DARK_TEXT, align=PP_ALIGN.LEFT):
    tf = shape.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    p = tf.paragraphs[0]
    p.text = ""
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    p.alignment = align
    return tf

def _add_text_box(slide, left, top, w, h, text, size=12, bold=False, color=C_DARK_TEXT, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(left, top, w, h)
    _set_text(tb, text, size, bold, color, align)
    return tb

def _add_multi_text(shape, lines, size=11, color=C_DARK_TEXT, bold_first=False, line_spacing=1.15):
    """Set multiple lines with optional bold first line."""
    tf = shape.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.space_after = Pt(2)
        run = p.add_run()
        run.text = line
        run.font.size = Pt(size)
        run.font.color.rgb = color
        if bold_first and i == 0:
            run.font.bold = True
    return tf

def _title_bar(slide, title, section="", slide_num=""):
    """Standard title bar at top."""
    bar = _add_shape(slide, Inches(0), Inches(0), SLIDE_W, Inches(0.85), fill=C_PRIMARY)
    _set_text(bar, title, size=24, bold=True, color=C_WHITE, align=PP_ALIGN.LEFT)
    bar.text_frame.margin_left = Inches(0.5)
    bar.text_frame.margin_top = Inches(0.15)
    # Section tag
    if section:
        tag = _add_shape(slide, Inches(0.3), Inches(0.95), Inches(3.5), Inches(0.35),
                         fill=C_LIGHT_BG, border=C_PRIMARY, radius=True)
        _set_text(tag, f"AI-Native Software Development  |  {section}", size=9,
                  color=C_PRIMARY, align=PP_ALIGN.CENTER)
    # Slide number
    if slide_num:
        _add_text_box(slide, Inches(12.5), Inches(7.1), Inches(0.6), Inches(0.3),
                      slide_num, size=10, color=C_LIGHT_TXT, align=PP_ALIGN.RIGHT)

def _footer(slide, left_text):
    """Standard footer."""
    _add_text_box(slide, Inches(0.3), Inches(7.1), Inches(8), Inches(0.3),
                  left_text, size=8, color=C_LIGHT_TXT)

def _card(slide, left, top, w, h, title, body_lines, accent=C_PRIMARY):
    """Card with left accent border."""
    # Border accent
    _add_shape(slide, left, top, Inches(0.06), h, fill=accent)
    # Card body
    card = _add_shape(slide, left + Inches(0.06), top, w - Inches(0.06), h,
                      fill=C_WHITE, border=C_CARD_BDR)
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.15)
    tf.margin_top = Inches(0.1)
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = title
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = C_DARK_TEXT
    for line in body_lines:
        p2 = tf.add_paragraph()
        p2.space_before = Pt(2)
        r2 = p2.add_run()
        r2.text = line
        r2.font.size = Pt(9)
        r2.font.color.rgb = C_LIGHT_TXT
    return card

def _pill(slide, left, top, w, h, text, fill=C_PRIMARY, text_color=C_WHITE, size=10):
    """Small pill / badge."""
    s = _add_shape(slide, left, top, w, h, fill=fill, radius=True)
    _set_text(s, text, size=size, bold=True, color=text_color, align=PP_ALIGN.CENTER)
    s.text_frame.margin_top = Inches(0.02)
    return s

def _block_box(slide, left, top, w, h, title, fill=C_SECONDARY):
    """Diagram block box."""
    s = _add_shape(slide, left, top, w, h, fill=fill, radius=True)
    _set_text(s, title, size=10, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    s.text_frame.margin_top = Inches(0.05)
    s.text_frame.word_wrap = True
    return s

def _arrow_right(slide, left, top, w=Inches(0.4)):
    """Simple right arrow indicator."""
    _add_text_box(slide, left, top, w, Inches(0.3), "\u2192", size=18,
                  bold=True, color=C_PRIMARY, align=PP_ALIGN.CENTER)

def _notes(slide, text):
    """Add speaker notes."""
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = text

# ═══════════════════════════════════════════════════════════
#  SLIDE 1 — Title & Welcome
# ═══════════════════════════════════════════════════════════
def slide_01():
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    # Big title area
    _add_shape(sl, Inches(0), Inches(0), SLIDE_W, Inches(3.5), fill=C_PRIMARY)
    _add_text_box(sl, Inches(0.8), Inches(0.8), Inches(11), Inches(1.2),
                  "AI-Native Software Development", size=36, bold=True, color=C_WHITE)
    _add_text_box(sl, Inches(0.8), Inches(2.0), Inches(11), Inches(0.6),
                  "Theory, Methodology & Hands-On Practical Sessions", size=20, color=RGBColor(0xBB,0xDE,0xFB))
    _add_text_box(sl, Inches(0.8), Inches(2.7), Inches(11), Inches(0.5),
                  "Faculty Development Program  |  3-Hour Interactive Workshop", size=14, color=RGBColor(0x90,0xCA,0xF9))
    # Flow diagram
    stages = ["Human\nIntent", "Executable\nSpecification", "AI-Assisted\nDesign",
              "Code\nGeneration", "Automated\nTesting", "CI/CD\nPipeline", "Continuous\nFeedback"]
    colors = [C_SECONDARY, C_PRIMARY, C_PURPLE, C_ACCENT, C_WARN, C_RED, C_SECONDARY]
    x_start = Inches(0.5)
    for i, (stage, clr) in enumerate(zip(stages, colors)):
        _block_box(sl, x_start + Inches(i * 1.8), Inches(4.2), Inches(1.5), Inches(0.9), stage, fill=clr)
        if i < len(stages) - 1:
            _arrow_right(sl, x_start + Inches(i * 1.8 + 1.5), Inches(4.4))
    # Key equation
    eq = _add_shape(sl, Inches(0.5), Inches(5.5), Inches(12.3), Inches(0.5),
                    fill=C_LIGHT_BG, border=C_PRIMARY, radius=True)
    _set_text(eq, "AI-Native = Human Intent  +  Executable Specification  +  AI Generation  +  Automated Validation  +  Feedback",
              size=12, bold=True, color=C_PRIMARY, align=PP_ALIGN.CENTER)
    _add_text_box(sl, Inches(0.8), Inches(6.3), Inches(11), Inches(0.6),
                  "From foundational concepts to advanced AI-native engineering\nIncludes guided practical labs, spec-driven development & multi-agent workflows",
                  size=11, color=C_LIGHT_TXT)
    _footer(sl, "AI-Native Software Development  |  Faculty Development Program")
    _add_text_box(sl, Inches(12.5), Inches(7.1), Inches(0.6), Inches(0.3), "1", size=10, color=C_LIGHT_TXT, align=PP_ALIGN.RIGHT)

    _notes(sl, """SPEAKER NOTES - Slide 1: Title & Welcome
-----------------------------------------
Welcome the faculty participants and introduce yourself. Set the tone: this is NOT a passive lecture -- it is an interactive, hands-on workshop.

KEY POINTS TO COVER:
1. INTRODUCTIONS: Ask participants to briefly introduce themselves -- name, department, and their current experience with AI tools in teaching or development.

2. WORKSHOP STRUCTURE: Explain the 3-hour format:
   - Part 1 (~60-75 min): Theory & methodology -- we build the conceptual foundation
   - Break (15 min)
   - Part 2 (~60-90 min): Guided practical labs -- hands-on implementation using AI tools

3. THE FLOW DIAGRAM: Walk through the 7-stage pipeline on screen:
   - Human Intent: Every project starts with a human expressing what they want
   - Executable Specification: That intent is captured in a structured, machine-readable format
   - AI-Assisted Design: AI proposes architecture, data models, UML diagrams
   - Code Generation: AI generates implementation from the spec
   - Automated Testing: Tests are generated from the same spec
   - CI/CD Pipeline: Automated build, scan, deploy with quality gates
   - Continuous Feedback: Production telemetry feeds back into the next iteration

4. THE KEY EQUATION: Emphasize that AI-Native is not just "use ChatGPT to write code." It's a fundamental shift in how software is conceived, specified, built, and maintained. The specification becomes the source of truth, not the code.

5. SET EXPECTATIONS: By the end, participants will:
   - Understand the AI-Native SDLC methodology
   - Have written a spec and used AI to generate working code
   - Be ready to incorporate these practices into their curriculum""")
    return sl

# ═══════════════════════════════════════════════════════════
#  SLIDE 2 — Session Agenda & Learning Outcomes
# ═══════════════════════════════════════════════════════════
def slide_02():
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "Session Agenda & Learning Outcomes", "Opening", "2")

    # Timeline blocks
    parts = [
        ("Part 1: Theory & Methodology", "~65 min", C_PRIMARY,
         ["AI-Native concepts & principles", "Spec-driven development methodology",
          "Architecture, testing & CI/CD", "Multi-agent & AI governance"]),
        ("Break", "15 min", C_LIGHT_TXT, []),
        ("Part 2: Guided Practical Labs", "~90 min", C_ACCENT,
         ["Hands-on spec writing", "AI code generation & review",
          "Testing & validation", "CI/CD pipeline setup"]),
    ]
    y = Inches(1.5)
    for title, duration, clr, items in parts:
        _pill(sl, Inches(0.5), y, Inches(2.8), Inches(0.4), title, fill=clr)
        _add_text_box(sl, Inches(3.5), y, Inches(1), Inches(0.4), duration, size=11, bold=True, color=clr)
        if items:
            for j, item in enumerate(items):
                _add_text_box(sl, Inches(4.6), y + Inches(j * 0.22), Inches(4), Inches(0.22),
                              f"\u2022 {item}", size=10, color=C_DARK_TEXT)
        y += Inches(max(len(items) * 0.22, 0.5) + 0.15)

    # Learning outcomes on right side
    _add_text_box(sl, Inches(8.5), Inches(1.5), Inches(4.5), Inches(0.3),
                  "Learning Outcomes", size=16, bold=True, color=C_PRIMARY)
    outcomes = [
        ("Understand", "AI-Native SDLC vs traditional approaches"),
        ("Apply", "Spec-driven development methodology"),
        ("Practice", "AI-assisted code generation & review"),
        ("Implement", "Automated testing from specifications"),
        ("Design", "CI/CD pipelines with AI quality gates"),
        ("Evaluate", "Multi-agent systems & AI governance"),
    ]
    for i, (verb, desc) in enumerate(outcomes):
        _pill(sl, Inches(8.5), Inches(2.1 + i * 0.55), Inches(1.2), Inches(0.35),
              verb, fill=C_SECONDARY)
        _add_text_box(sl, Inches(9.8), Inches(2.1 + i * 0.55), Inches(3.2), Inches(0.35),
                      desc, size=10, color=C_DARK_TEXT)

    # Balance bar
    bal = _add_shape(sl, Inches(0.5), Inches(6.2), Inches(12.3), Inches(0.4),
                     fill=C_LIGHT_BG, border=C_PRIMARY, radius=True)
    _set_text(bal, "Suggested Balance:  40% Concepts & Theory   |   60% Guided Practice & Discussion",
              size=11, bold=True, color=C_PRIMARY, align=PP_ALIGN.CENTER)
    _footer(sl, "3-Hour Interactive Workshop  |  Faculty Development Program")

    _notes(sl, """SPEAKER NOTES - Slide 2: Session Agenda & Learning Outcomes
-----------------------------------------------------
Walk through each section so participants know what to expect:

PART 1 - THEORY & METHODOLOGY (~65 minutes):
- Start with WHY AI-native matters (industry context, market trends)
- Define what AI-native software development IS (and isn't)
- Deep dive into spec-driven development -- the core methodology
- Cover architecture, testing, CI/CD with AI integration
- Touch on advanced topics: multi-agent systems, AI governance
- This isn't just slides -- we'll have interactive discussions throughout

BREAK (15 minutes):
- Let participants set up their development environment if they haven't already
- Install required tools: IDE with AI assistant, Docker, language runtime

PART 2 - GUIDED PRACTICAL LABS (~90 minutes):
- Hands-on implementation of a real API using spec-driven development
- Choice of labs: Task Management API (Java) or Grade Calculator (Python)
- Step-by-step: spec writing -> AI generation -> review -> test -> deploy
- Participants will have working, tested, deployable code by the end

LEARNING OUTCOMES - Use Bloom's taxonomy verbs intentionally:
- Understand (knowledge): grasp the paradigm shift
- Apply (application): use SDD methodology hands-on
- Practice (skill): work with AI tools for code generation
- Implement (creation): build automated tests from specs
- Design (synthesis): create CI/CD pipelines
- Evaluate (judgment): assess governance and responsible AI practices

TEACHING APPROACH: Explain -> Demonstrate -> Validate -> Reflect
Each concept follows this cycle. We explain the theory, demonstrate with examples, validate understanding through discussion, and reflect on how it applies to their teaching.""")
    return sl

# ═══════════════════════════════════════════════════════════
#  SLIDE 3 — Why AI-Native Matters Now
# ═══════════════════════════════════════════════════════════
def slide_03():
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "Why AI-Native Software Development Matters Now", "Foundations", "3")

    # Industry stats
    stats = [
        ("92%", "of developers use\nAI coding tools", C_PRIMARY),
        ("55%", "faster code\ngeneration", C_ACCENT),
        ("$50B+", "AI dev tools\nmarket by 2028", C_SECONDARY),
        ("40%", "of new code will be\nAI-generated by 2027", C_PURPLE),
    ]
    for i, (num, label, clr) in enumerate(stats):
        box = _add_shape(sl, Inches(0.5 + i * 3.1), Inches(1.3), Inches(2.8), Inches(1.2),
                         fill=C_WHITE, border=clr, radius=True)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = num
        r.font.size = Pt(28)
        r.font.bold = True
        r.font.color.rgb = clr
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        r2 = p2.add_run()
        r2.text = label
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_LIGHT_TXT

    # Why now section
    _add_text_box(sl, Inches(0.5), Inches(2.8), Inches(6), Inches(0.3),
                  "The Paradigm Shift", size=16, bold=True, color=C_PRIMARY)
    shifts = [
        "LLMs have reached production-quality code generation capability",
        "Organizations adopting AI-native see 30-50% faster delivery cycles",
        "Software engineering is evolving from 'writing code' to 'curating intent'",
        "Academic curricula must prepare students for AI-augmented workplaces",
        "Companies that don't adopt risk falling behind in talent and productivity",
    ]
    for i, s in enumerate(shifts):
        _add_text_box(sl, Inches(0.7), Inches(3.2 + i * 0.32), Inches(6), Inches(0.3),
                      f"\u2022 {s}", size=11, color=C_DARK_TEXT)

    # Right side: adoption drivers
    _add_text_box(sl, Inches(7.5), Inches(2.8), Inches(5.5), Inches(0.3),
                  "Industry Adoption Drivers", size=16, bold=True, color=C_PRIMARY)
    drivers = [
        ("Developer Productivity", "AI tools reduce boilerplate, accelerate prototyping", C_ACCENT),
        ("Quality at Scale", "Automated testing, review, and security scanning", C_PRIMARY),
        ("Talent Transformation", "Engineers become architects and spec writers", C_SECONDARY),
        ("Competitive Pressure", "Faster time-to-market, reduced development costs", C_WARN),
    ]
    for i, (title, desc, clr) in enumerate(drivers):
        _card(sl, Inches(7.5), Inches(3.2 + i * 0.85), Inches(5.3), Inches(0.75),
              title, [desc], accent=clr)

    _footer(sl, "Sources: GitHub Survey 2025, Gartner Predictions, McKinsey Digital Report")

    _notes(sl, """SPEAKER NOTES - Slide 3: Why AI-Native Matters Now
---------------------------------------------------
This slide sets the URGENCY. Faculty need to understand this isn't a trend -- it's a fundamental shift.

STATISTICS (walk through each):
1. 92% of developers now use AI coding tools (GitHub 2025 Developer Survey) -- this is near-universal adoption
2. 55% faster code generation -- documented across multiple enterprise studies
3. $50B+ market by 2028 -- investment is massive and accelerating
4. 40% of new code AI-generated by 2027 (Gartner) -- the code-writing role is transforming

THE PARADIGM SHIFT:
- Emphasize that this changes WHAT we teach. If 40% of code is AI-generated, students need to learn:
  * How to write specifications that AI can understand
  * How to review and validate AI-generated code
  * How to design systems, not just write functions
  * How to test, govern, and secure AI-generated artifacts

- Use the analogy: "Just as calculators changed math education from computation to problem-solving, AI tools are changing CS education from code-writing to system-thinking."

INDUSTRY ADOPTION DRIVERS:
1. Developer Productivity: Not about replacing developers -- about amplifying them
2. Quality at Scale: AI doesn't get tired, doesn't forget edge cases (when properly specified)
3. Talent Transformation: The job title stays "software engineer" but the daily work changes
4. Competitive Pressure: Companies that adopt faster ship faster

DISCUSSION PROMPT: Ask faculty -- "How many of your students already use ChatGPT or Copilot for assignments? How does your curriculum address this?" This usually generates lively discussion and surfaces the real challenges faculty face.""")
    return sl

# ═══════════════════════════════════════════════════════════
#  SLIDE 4 — What is AI-Native Software Development?
# ═══════════════════════════════════════════════════════════
def slide_04():
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "What is AI-Native Software Development?", "Foundations", "4")

    # Definition
    _add_text_box(sl, Inches(0.5), Inches(1.3), Inches(6.5), Inches(0.3),
                  "Definition", size=16, bold=True, color=C_PRIMARY)
    defs = [
        "AI participates across the ENTIRE lifecycle, not just coding",
        "Specifications become the primary control mechanism",
        "Humans review intent, architecture, safety & fitness",
        "Continuous feedback loops improve every iteration",
        "Code is a generated artifact \u2014 specs are the source of truth",
    ]
    for i, d in enumerate(defs):
        _add_text_box(sl, Inches(0.7), Inches(1.7 + i * 0.32), Inches(6), Inches(0.3),
                      f"\u2022 {d}", size=12, color=C_DARK_TEXT)

    # Core principles
    _add_text_box(sl, Inches(0.5), Inches(3.5), Inches(12), Inches(0.3),
                  "Core Principles", size=16, bold=True, color=C_PRIMARY)
    principles = [
        ("Spec-First", "Specifications before code.\nAI refines, humans approve.", C_PRIMARY),
        ("Human-in-the-Loop", "Critical decisions require\nhuman judgment & review.", C_SECONDARY),
        ("Automated Validation", "Tests, scans & CI/CD verify\nevery generated artifact.", C_ACCENT),
        ("Continuous Learning", "Feedback from production\nimproves future generations.", C_PURPLE),
    ]
    for i, (title, desc, clr) in enumerate(principles):
        box = _add_shape(sl, Inches(0.5 + i * 3.1), Inches(3.9), Inches(2.8), Inches(1.3),
                         fill=C_WHITE, border=clr, radius=True)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        tf.margin_top = Inches(0.1)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = title
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = clr
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        p2.space_before = Pt(6)
        r2 = p2.add_run()
        r2.text = desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_LIGHT_TXT

    # AI-Native vs AI-Assisted distinction (right side)
    _add_text_box(sl, Inches(7.5), Inches(1.3), Inches(5.5), Inches(0.3),
                  "AI-Assisted vs AI-Native", size=14, bold=True, color=C_PRIMARY)
    _card(sl, Inches(7.5), Inches(1.7), Inches(5.3), Inches(0.75),
          "AI-Assisted (Level 1)", ["AI helps with autocomplete & suggestions", "Human writes most code, AI fills gaps"], accent=C_WARN)
    _card(sl, Inches(7.5), Inches(2.6), Inches(5.3), Inches(0.75),
          "AI-Native (Level 3)", ["AI generates from specs; human reviews & governs", "Specs are source of truth, code is derived artifact"], accent=C_ACCENT)

    # Equation
    eq = _add_shape(sl, Inches(0.5), Inches(5.6), Inches(12.3), Inches(0.45),
                    fill=C_LIGHT_BG, border=C_PRIMARY, radius=True)
    _set_text(eq, "AI-Native  =  Human Intent  +  Executable Specification  +  AI Generation  +  Automated Validation  +  Feedback",
              size=12, bold=True, color=C_PRIMARY, align=PP_ALIGN.CENTER)
    _footer(sl, "Key Insight: In AI-native development, specifications and tests are MORE important than code itself")

    _notes(sl, """SPEAKER NOTES - Slide 4: What is AI-Native Software Development?
------------------------------------------------------------------
This is the foundational slide. Spend time here -- make sure everyone understands the paradigm shift.

DEFINITION - Walk through each bullet:
1. "Across the ENTIRE lifecycle" -- not just code completion. AI helps with requirements, design, architecture, testing, deployment, monitoring. Every phase.
2. "Specifications as control mechanism" -- this is THE key insight. In traditional dev, we control quality through code review. In AI-native, we control quality through spec precision.
3. "Humans review intent" -- AI generates, humans validate. The human role shifts from writer to architect and reviewer.
4. "Continuous feedback loops" -- production metrics, bug reports, test failures all feed back to improve specs and generation.
5. "Code is generated" -- this is provocative. Push back expected! Explain: we don't mean ALL code is generated, but the development model treats code as a derived artifact from the spec.

AI-ASSISTED vs AI-NATIVE:
- AI-Assisted (where most people are today): You write code, AI helps with autocomplete, suggestions, explanations. The human is still the primary code author.
- AI-Native (where the industry is heading): You write specifications, AI generates code. The human is the architect, reviewer, and governor. Code is regenerable from specs.
- There's a spectrum between these two. Most teams today are somewhere in the middle.

CORE PRINCIPLES:
1. Spec-First: The spec is written BEFORE any code. AI helps refine the spec. Once approved, AI generates from it.
2. Human-in-the-Loop: Architectural decisions, security choices, trade-offs -- these require human judgment. AI proposes, humans dispose.
3. Automated Validation: Every generated artifact is automatically tested, scanned, and validated. No manual verification bottleneck.
4. Continuous Learning: The system gets better over time. Failed tests improve specs. Production bugs improve generation.

DISCUSSION: "If code is generated from specs, what skills do your students need to learn? What becomes more important? What becomes less important?"
Answer: Design thinking, specification writing, system architecture, testing strategy, security awareness become MORE important. Syntax memorization, boilerplate writing become LESS important.""")
    return sl

# ═══════════════════════════════════════════════════════════
#  SLIDE 5 — Traditional vs AI-Native SDLC
# ═══════════════════════════════════════════════════════════
def slide_05():
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "Traditional SDLC vs AI-Native SDLC", "Foundations", "5")

    # Comparison table header
    headers = ["Aspect", "Traditional SDLC", "AI-Native SDLC"]
    col_x = [Inches(0.5), Inches(3.8), Inches(8.3)]
    col_w = [Inches(3.0), Inches(4.2), Inches(4.5)]
    for i, h in enumerate(headers):
        hdr = _add_shape(sl, col_x[i], Inches(1.3), col_w[i], Inches(0.4), fill=C_PRIMARY)
        _set_text(hdr, h, size=12, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)

    rows = [
        ("Requirements", "Natural language docs,\noften ambiguous", "Structured executable specs,\nmachine-readable"),
        ("Design", "Manual UML, whiteboard\nsketches", "AI-generated diagrams from\nspec descriptions"),
        ("Coding", "Hand-written by developers\nline by line", "AI-generated from specs,\nhuman-reviewed"),
        ("Testing", "Tests written after code,\noften incomplete", "Tests generated from specs\nBEFORE code"),
        ("Code Review", "Manual peer review,\ntime-consuming", "AI-assisted review + human\njudgment for critical paths"),
        ("CI/CD", "Manual pipeline config,\nbasic checks", "AI-optimized pipelines with\nintelligent quality gates"),
        ("Documentation", "Written separately, often\noutdated", "Auto-generated from specs,\nalways current"),
        ("Source of Truth", "Code is the source of truth", "Specification is the\nsource of truth"),
    ]
    for i, (aspect, trad, ainative) in enumerate(rows):
        y = Inches(1.8 + i * 0.6)
        bg = C_LIGHT_BG if i % 2 == 0 else C_WHITE
        _add_shape(sl, col_x[0], y, col_w[0], Inches(0.55), fill=bg)
        _add_shape(sl, col_x[1], y, col_w[1], Inches(0.55), fill=bg)
        _add_shape(sl, col_x[2], y, col_w[2], Inches(0.55), fill=bg)
        _add_text_box(sl, col_x[0] + Inches(0.1), y + Inches(0.02), Inches(2.8), Inches(0.5),
                      aspect, size=11, bold=True, color=C_DARK_TEXT)
        _add_text_box(sl, col_x[1] + Inches(0.1), y + Inches(0.02), Inches(4), Inches(0.5),
                      trad, size=10, color=C_LIGHT_TXT)
        _add_text_box(sl, col_x[2] + Inches(0.1), y + Inches(0.02), Inches(4.3), Inches(0.5),
                      ainative, size=10, color=C_ACCENT)

    # Key insight
    eq = _add_shape(sl, Inches(0.5), Inches(6.6), Inches(12.3), Inches(0.4),
                    fill=C_LIGHT_BG, border=C_ACCENT, radius=True)
    _set_text(eq, "Key Insight: In AI-native development, specifications and tests are MORE important than code itself",
              size=11, bold=True, color=C_ACCENT, align=PP_ALIGN.CENTER)
    _footer(sl, "The shift from code-centric to spec-centric development")

    _notes(sl, """SPEAKER NOTES - Slide 5: Traditional vs AI-Native SDLC
--------------------------------------------------------
Use this comparison table to make the paradigm shift concrete. Walk through each row:

1. REQUIREMENTS: Traditional = Word docs with ambiguous language. AI-Native = structured specs with acceptance criteria, edge cases, data types. The spec IS the requirements doc AND the input to code generation.

2. DESIGN: Traditional = someone draws UML on a whiteboard, maybe enters in a tool. AI-Native = describe your domain in the spec, AI generates UML class diagrams, sequence diagrams, ER diagrams automatically.

3. CODING: This is the biggest shift. Traditional = a developer writes every line. AI-Native = AI generates the implementation from the spec. The developer reviews, adjusts, and approves. Think: spec is the "source code", generated code is the "binary."

4. TESTING: Traditional = tests are written AFTER code (often skipped under time pressure). AI-Native = tests are generated FROM the spec BEFORE code. The spec defines what correct behavior looks like; tests verify it.

5. CODE REVIEW: Traditional = 2-3 reviewers read every line, days of back-and-forth. AI-Native = AI does the first pass (style, security, patterns), humans focus on architecture, business logic, edge cases.

6. CI/CD: Traditional = manually configured pipelines. AI-Native = AI generates pipeline configs, suggests optimal stages, adds intelligent quality gates.

7. DOCUMENTATION: Traditional = separate wiki/docs that fall out of sync. AI-Native = docs generated from the same spec, always current.

8. SOURCE OF TRUTH: THE KEY ROW. Traditional = "the code is the spec." AI-Native = "the spec is the code." This is the fundamental inversion.

EXERCISE PROMPT: "Pick one row where you see the biggest impact on your teaching. Share with your neighbor."
""")
    return sl

# ═══════════════════════════════════════════════════════════
#  SLIDE 6 — AI-Native SDLC Lifecycle
# ═══════════════════════════════════════════════════════════
def slide_06():
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "AI-Native SDLC Lifecycle", "Foundations", "6")

    # Circular lifecycle diagram (represented as connected boxes)
    stages = [
        ("1. Capture\nIntent", C_SECONDARY),
        ("2. Write\nSpecification", C_PRIMARY),
        ("3. AI-Assisted\nDesign", C_PURPLE),
        ("4. Generate\nCode", C_ACCENT),
        ("5. Automated\nTesting", C_WARN),
        ("6. CI/CD\nDeploy", C_RED),
        ("7. Monitor &\nFeedback", C_SECONDARY),
    ]
    # Top row: stages 1-4
    for i in range(4):
        _block_box(sl, Inches(0.5 + i * 3.1), Inches(1.4), Inches(2.5), Inches(0.9),
                   stages[i][0], fill=stages[i][1])
        if i < 3:
            _arrow_right(sl, Inches(3.0 + i * 3.1), Inches(1.6))
    # Bottom row: stages 5-7 (right to left visually, but still LTR)
    for i in range(3):
        _block_box(sl, Inches(0.5 + i * 3.1), Inches(2.8), Inches(2.5), Inches(0.9),
                   stages[4 + i][0], fill=stages[4 + i][1])
        if i < 2:
            _arrow_right(sl, Inches(3.0 + i * 3.1), Inches(3.0))

    # Center label
    center = _add_shape(sl, Inches(10.0), Inches(1.8), Inches(2.8), Inches(1.5),
                        fill=C_LIGHT_BG, border=C_PRIMARY, radius=True)
    _set_text(center, "AI-Native\nSDLC", size=16, bold=True, color=C_PRIMARY, align=PP_ALIGN.CENTER)

    # Stage descriptions
    _add_text_box(sl, Inches(0.5), Inches(4.0), Inches(12), Inches(0.3),
                  "What Happens at Each Stage", size=14, bold=True, color=C_PRIMARY)
    descriptions = [
        ("Intent Capture:", "Stakeholder needs converted to structured requirements", C_SECONDARY),
        ("Specification:", "Functional/non-functional reqs, API contracts, acceptance criteria", C_PRIMARY),
        ("AI Design:", "Architecture proposals, trade-off analysis, UML generation", C_PURPLE),
        ("Code Generation:", "AI generates implementation; humans review & refine", C_ACCENT),
        ("Testing:", "Unit, integration, E2E tests generated from specs", C_WARN),
        ("CI/CD Deploy:", "Automated build, scan, deploy with quality gates", C_RED),
        ("Feedback:", "Telemetry, bug reports, and metrics feed next cycle", C_SECONDARY),
    ]
    for i, (stage, desc, clr) in enumerate(descriptions):
        row = _add_shape(sl, Inches(0.5), Inches(4.4 + i * 0.38), Inches(12.3), Inches(0.35),
                         fill=C_WHITE, border=C_CARD_BDR, radius=True)
        tf = row.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = stage + "  "
        r1.font.size = Pt(10)
        r1.font.bold = True
        r1.font.color.rgb = clr
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_DARK_TEXT

    _footer(sl, "Each stage involves AI assistance with human oversight at decision points")

    _notes(sl, """SPEAKER NOTES - Slide 6: AI-Native SDLC Lifecycle
---------------------------------------------------
This diagram shows the continuous cycle of AI-native development. Unlike traditional waterfall (linear) or even agile (iterative but still human-centric), AI-native is a continuous loop where AI participates at every stage.

Walk through each stage with a concrete example (use the Task Management API as the running example):

1. CAPTURE INTENT: "We need a REST API for managing team tasks with categories, comments, and role-based access."
   - AI helps: "What about audit logging? Soft deletes? Pagination?" AI identifies gaps in requirements.

2. WRITE SPECIFICATION: The SDD document you'll work with in the lab. Includes FRs, acceptance criteria, edge cases, data types.
   - This is WHERE THE MAGIC HAPPENS. A well-written spec enables everything downstream.
   - Think of the spec as a "prompt" for the entire project, not just a single code generation.

3. AI-ASSISTED DESIGN: From the spec, AI generates:
   - UML class diagrams (Task, User, Category, Comment entities)
   - Sequence diagrams (Create Task flow: Client -> API Gateway -> Service -> DB)
   - API contracts (OpenAPI/Swagger YAML)
   - Database schemas (DDL statements)

4. CODE GENERATION: AI generates from the spec AND the design:
   - Entity classes, repository interfaces, service layer, REST controllers
   - DTOs, validators, exception handlers
   - Configuration files (application.yml, Docker Compose)

5. AUTOMATED TESTING: Tests generated from the SAME spec:
   - Unit tests for each FR's acceptance criteria
   - Integration tests for API contracts
   - Edge case tests from the spec's "Edge Cases" section

6. CI/CD DEPLOY: Pipeline that automatically:
   - Builds the code, runs all tests
   - Runs SonarQube for code quality, Snyk for vulnerabilities
   - Builds Docker image, deploys to staging

7. FEEDBACK: Monitor the deployed system:
   - API response times (are we meeting NFRs?)
   - Error rates (are edge cases we missed?)
   - Usage patterns (which endpoints need optimization?)
   - Feed all this back into the spec for the next iteration.""")
    return sl

# Continue building remaining slides...
# Slides 7-25 (main) + backup slides

def slide_07():
    """AI Tool Ecosystem & IDE Deep Dive"""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "AI Tool Ecosystem for Software Development", "Tools", "7")

    _add_text_box(sl, Inches(0.5), Inches(1.2), Inches(12), Inches(0.3),
                  "Categorized Landscape of AI-Powered Development Tools", size=14, bold=True, color=C_PRIMARY)

    tools = [
        ("IDE Assistants", "GitHub Copilot | Cursor | Windsurf | JetBrains AI",
         "Inline code completion, refactoring, chat-in-editor", C_PRIMARY),
        ("Chat / LLM Interfaces", "ChatGPT | Claude | Gemini | Devin",
         "Conversational coding, explanation, brainstorming", C_SECONDARY),
        ("Workflow & Agent Frameworks", "LangChain | CrewAI | AutoGen | Semantic Kernel",
         "Orchestrate multi-step AI pipelines & agent teams", C_PURPLE),
        ("DevOps & CI/CD Intelligence", "GitHub Actions AI | SonarQube AI | Snyk AI",
         "Automated quality gates, vulnerability detection", C_RED),
        ("Code Review & PR Analysis", "CodeRabbit | Copilot PR Review | Qodo",
         "Automated code review, PR summaries, test suggestions", C_ACCENT),
    ]

    for i, (cat, names, desc, clr) in enumerate(tools):
        y = Inches(1.65 + i * 0.95)
        _card(sl, Inches(0.5), y, Inches(6), Inches(0.85), cat,
              [names, desc], accent=clr)

    # Right side: tool comparison
    _add_text_box(sl, Inches(7.0), Inches(1.2), Inches(6), Inches(0.3),
                  "IDE Assistant Comparison", size=14, bold=True, color=C_PRIMARY)
    comparisons = [
        ("GitHub Copilot", "Widest IDE support, strong autocomplete, enterprise features", "General-purpose coding", C_PRIMARY),
        ("Cursor", "Codebase-aware context, Composer mode, multi-file edits", "Complex refactors, full features", C_SECONDARY),
        ("Devin / Windsurf", "Autonomous execution, end-to-end implementation, planning loops", "Complete feature implementation", C_ACCENT),
    ]
    for i, (name, strengths, best_for, clr) in enumerate(comparisons):
        y = Inches(1.65 + i * 1.4)
        box = _add_shape(sl, Inches(7.0), y, Inches(5.8), Inches(1.25),
                         fill=C_WHITE, border=clr, radius=True)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        tf.margin_top = Inches(0.08)
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = name
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = clr
        for line in [f"Strengths: {strengths}", f"Best for: {best_for}"]:
            p2 = tf.add_paragraph()
            r2 = p2.add_run()
            r2.text = line
            r2.font.size = Pt(9)
            r2.font.color.rgb = C_LIGHT_TXT

    # Practical tip
    tip = _add_shape(sl, Inches(0.5), Inches(6.4), Inches(12.3), Inches(0.45),
                     fill=C_LIGHT_BG, border=C_PRIMARY, radius=True)
    _set_text(tip, "Practical Tip:  Use Copilot for quick completions  |  Cursor for complex multi-file work  |  Devin for end-to-end tasks",
              size=11, bold=True, color=C_PRIMARY, align=PP_ALIGN.CENTER)
    _footer(sl, "No single tool covers everything \u2014 build a complementary toolchain across categories")

    _notes(sl, """SPEAKER NOTES - Slide 7: AI Tool Ecosystem
----------------------------------------------------------------------
This slide gives a bird's-eye view of the AI-powered development tool landscape. The key message: no single tool does everything, so teams build complementary toolchains.

TOOL CATEGORIES (walk through each):
1. IDE ASSISTANTS: The most mature category. These integrate directly into your editor.
   - Copilot: The most widely adopted. Works in VS Code, JetBrains, etc. Strong at autocomplete.
   - Cursor: Fork of VS Code, built AI-native. Excels at codebase-aware context and multi-file edits.
   - Windsurf: Cascade model -- understands entire project context, not just current file.

2. CHAT/LLM INTERFACES: General-purpose AI for brainstorming, explaining, and prototyping.
   - ChatGPT/Claude: Great for "explain this code," "design this architecture," "write this spec."
   - Devin: Goes beyond chat -- it's an autonomous AI software engineer that can plan, code, test, and deploy.

3. WORKFLOW & AGENT FRAMEWORKS: For building custom AI pipelines.
   - LangChain/CrewAI: Orchestrate multiple AI agents to collaborate on complex tasks.
   - This is the "multi-agent" pattern we'll cover later in the session.

4. DEVOPS & CI/CD: AI-powered quality assurance in the pipeline.
   - SonarQube AI: Not just static analysis -- AI-powered pattern detection for bugs and security.
   - Snyk AI: Dependency vulnerability scanning with AI-powered fix suggestions.

5. CODE REVIEW: Automated first-pass review of pull requests.
   - CodeRabbit: Provides detailed, line-by-line review comments automatically.
   - Copilot PR Review: Summarizes changes, suggests improvements.

COMPARISON TABLE: Discuss when to use which IDE assistant:
- Copilot: Best for individual line/function completion. Works everywhere.
- Cursor: Best when you need to refactor across multiple files or generate a complete feature.
- Devin/Windsurf: Best for greenfield features or when you have a clear spec and want end-to-end generation.

FACULTY PERSPECTIVE: Encourage faculty to let students use at least 2 different tools so they can compare approaches and understand trade-offs.""")
    return sl

def slide_08():
    """LLM Capabilities & Limitations"""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "LLM Capabilities & Limitations", "Tools", "8")

    # What AI does well
    _pill(sl, Inches(0.5), Inches(1.3), Inches(4.5), Inches(0.4), "What AI Does Well", fill=C_ACCENT)
    strengths = [
        "\u2713 Code pattern generation & boilerplate",
        "\u2713 Test scaffolding from descriptions",
        "\u2713 Documentation & comment generation",
        "\u2713 Explaining and summarizing code",
        "\u2713 Refactoring suggestions",
        "\u2713 CRUD operations & REST APIs",
        "\u2713 Regex, SQL queries, config files",
        "\u2713 Converting between languages/frameworks",
    ]
    for i, s in enumerate(strengths):
        _add_text_box(sl, Inches(0.7), Inches(1.85 + i * 0.3), Inches(5), Inches(0.28),
                      s, size=11, color=C_DARK_TEXT)

    # What AI struggles with
    _pill(sl, Inches(6.5), Inches(1.3), Inches(4.5), Inches(0.4), "What AI Struggles With", fill=C_RED)
    weaknesses = [
        "\u2717 Novel / unique algorithms",
        "\u2717 Complex business logic & domain rules",
        "\u2717 Security guarantees & crypto implementation",
        "\u2717 Performance optimization at scale",
        "\u2717 System-level architecture decisions",
        "\u2717 Cross-service consistency",
        "\u2717 Legacy system integration",
        "\u2717 Regulatory / compliance requirements",
    ]
    for i, w in enumerate(weaknesses):
        _add_text_box(sl, Inches(6.7), Inches(1.85 + i * 0.3), Inches(5.5), Inches(0.28),
                      w, size=11, color=C_DARK_TEXT)

    # Critical thinking box
    _add_text_box(sl, Inches(0.5), Inches(4.5), Inches(12), Inches(0.3),
                  "Critical Thinking Framework", size=14, bold=True, color=C_PRIMARY)
    framework = [
        ("Always Verify", "AI-generated code can contain subtle bugs, hallucinated APIs, or security vulnerabilities", C_RED),
        ("Provide Context", "Better input = better output. Include specs, constraints, existing code in prompts", C_PRIMARY),
        ("Iterate & Refine", "First generation is rarely perfect. Review, adjust prompt, regenerate", C_WARN),
        ("Know the Boundaries", "Use AI for what it does well; apply human expertise where it struggles", C_ACCENT),
    ]
    for i, (title, desc, clr) in enumerate(framework):
        _card(sl, Inches(0.5 + i * 3.1), Inches(4.9), Inches(2.9), Inches(1.1),
              title, [desc], accent=clr)

    _footer(sl, "Golden Rule: Trust but verify \u2014 AI is a powerful assistant, not an infallible oracle")

    _notes(sl, """SPEAKER NOTES - Slide 8: LLM Capabilities & Limitations
----------------------------------------------------------
This is a critical reality-check slide. Faculty need to understand both what AI can and cannot do reliably.

WHAT AI DOES WELL (walk through strengths):
- Pattern generation: AI excels at generating code that follows established patterns (CRUD, MVC, REST).
- Test scaffolding: Given a description of behavior, AI can generate comprehensive test suites.
- Documentation: AI can generate accurate docstrings, README files, and API documentation.
- Refactoring: AI can suggest and implement common refactoring patterns.
- Translation: Converting Python to Java, REST to GraphQL, SQL to NoSQL schemas.
- Configuration: Generating Docker Compose files, GitHub Actions workflows, Terraform configs.

WHAT AI STRUGGLES WITH (walk through weaknesses):
- Novel algorithms: If it hasn't seen it in training data, AI will generate plausible-looking but incorrect solutions.
- Complex business logic: Domain-specific rules with many conditions and exceptions -- AI often misses edge cases.
- Security: NEVER trust AI for crypto implementations. AI-generated auth code must be rigorously reviewed.
- Performance: AI doesn't understand your specific scale requirements or hardware constraints.
- Architecture: System-level decisions require understanding trade-offs AI can't fully evaluate.
- Legacy integration: AI doesn't know your specific legacy APIs, data formats, or constraints.

CRITICAL THINKING FRAMEWORK:
1. Always Verify: Don't copy-paste AI output. Read every line. Run the tests. Check the edge cases.
2. Provide Context: The difference between mediocre and excellent AI output is context quality.
3. Iterate & Refine: Use AI interactively. First pass, review, refine the prompt, regenerate.
4. Know the Boundaries: This is the most important skill to teach students.

TEACHING IMPLICATION: Students should learn to critically evaluate AI output -- this is a new meta-skill that didn't exist before. Consider adding "AI output review" as an assessment criterion in your courses.""")
    return sl

def slide_09():
    """Spec-Driven Development (SDD)"""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "Spec-Driven Development (SDD) Methodology", "Methodology", "9")

    # What is SDD
    _add_text_box(sl, Inches(0.5), Inches(1.2), Inches(6.5), Inches(0.3),
                  "What is Spec-Driven Development?", size=16, bold=True, color=C_PRIMARY)
    sdd_points = [
        "Write a complete, structured specification BEFORE any code",
        "Specification includes: FRs, NFRs, acceptance criteria, edge cases",
        "AI generates implementation directly from the specification",
        "Tests are derived from the same spec \u2014 spec = single source of truth",
        "Changes flow through specs, not through code patches",
    ]
    for i, p in enumerate(sdd_points):
        _add_text_box(sl, Inches(0.7), Inches(1.6 + i * 0.32), Inches(6), Inches(0.3),
                      f"\u2022 {p}", size=11, color=C_DARK_TEXT)

    # SDD Flow diagram
    _add_text_box(sl, Inches(0.5), Inches(3.3), Inches(12), Inches(0.3),
                  "SDD Workflow", size=14, bold=True, color=C_PRIMARY)
    flow_stages = [
        ("Define\nRequirements", C_SECONDARY),
        ("Write\nSpecification", C_PRIMARY),
        ("Review &\nApprove Spec", C_PURPLE),
        ("Generate\nCode from Spec", C_ACCENT),
        ("Generate\nTests from Spec", C_WARN),
        ("Run & Validate", C_RED),
    ]
    for i, (stage, clr) in enumerate(flow_stages):
        _block_box(sl, Inches(0.3 + i * 2.1), Inches(3.7), Inches(1.8), Inches(0.9), stage, fill=clr)
        if i < len(flow_stages) - 1:
            _arrow_right(sl, Inches(2.1 + i * 2.1), Inches(3.9))

    # SDD spec structure (right side)
    _add_text_box(sl, Inches(7.5), Inches(1.2), Inches(5.5), Inches(0.3),
                  "Anatomy of an SDD Specification", size=14, bold=True, color=C_PRIMARY)
    spec_parts = [
        ("1. Functional Requirements", "What the system must DO"),
        ("2. Non-Functional Requirements", "Performance, security, scalability targets"),
        ("3. Acceptance Criteria", "Machine-testable conditions (Given/When/Then)"),
        ("4. Edge Cases & Error Handling", "What happens when things go wrong"),
        ("5. Domain Model", "Entities, relationships, constraints"),
        ("6. API Contract", "OpenAPI/Swagger with request/response schemas"),
        ("7. Data Model", "Database schema, indexes, migrations"),
        ("8. Test Strategy", "Test types, coverage targets, tools"),
    ]
    for i, (part, desc) in enumerate(spec_parts):
        y = Inches(1.6 + i * 0.52)
        pill_w = Inches(3.0)
        _pill(sl, Inches(7.5), y, pill_w, Inches(0.25), part, fill=C_PRIMARY, size=8)
        _add_text_box(sl, Inches(10.6), y, Inches(2.5), Inches(0.25), desc, size=9, color=C_LIGHT_TXT)

    # Key insight
    eq = _add_shape(sl, Inches(0.5), Inches(5.0), Inches(12.3), Inches(0.45),
                    fill=C_LIGHT_BG, border=C_ACCENT, radius=True)
    _set_text(eq, "SDD Principle:  A well-written spec is the highest-leverage artifact in AI-native development",
              size=12, bold=True, color=C_ACCENT, align=PP_ALIGN.CENTER)

    # Why SDD works
    _add_text_box(sl, Inches(0.5), Inches(5.7), Inches(12), Inches(0.3),
                  "Why SDD Works with AI", size=14, bold=True, color=C_PRIMARY)
    reasons = [
        ("Deterministic Input", "Same spec \u2192 consistent output across re-generations"),
        ("Testable by Design", "Acceptance criteria become automated test assertions"),
        ("Change Management", "Update the spec, regenerate \u2014 no manual code archaeology"),
    ]
    for i, (title, desc) in enumerate(reasons):
        _card(sl, Inches(0.5 + i * 4.15), Inches(6.0), Inches(3.9), Inches(0.7),
              title, [desc], accent=C_PRIMARY)

    _footer(sl, "The spec is to AI-native development what source code is to traditional development")

    _notes(sl, """SPEAKER NOTES - Slide 9: Spec-Driven Development (SDD) Methodology
----------------------------------------------------------------------
This is the CORE METHODOLOGY slide. Everything in the workshop builds on this concept.

WHAT IS SDD:
- SDD inverts the traditional workflow. Instead of: think -> code -> test -> document
- SDD says: think -> SPECIFY -> generate code -> generate tests -> validate
- The specification is the primary development artifact, not the code.

WHY THIS MATTERS:
- Analogy for faculty: "Think of the spec as a detailed blueprint. A good blueprint allows any contractor to build the house correctly. A good spec allows any AI tool to generate the code correctly."
- The spec captures INTENT and CONSTRAINTS. AI handles the translation to code.

SDD WORKFLOW (walk through the 6 stages):
1. Define Requirements: What does the customer need? What problem are we solving?
2. Write Specification: Structured document with FRs, NFRs, acceptance criteria, edge cases
3. Review & Approve: Human experts review the spec for completeness, correctness, feasibility
4. Generate Code: AI generates implementation from the approved spec
5. Generate Tests: AI generates test cases from the same spec's acceptance criteria
6. Run & Validate: Execute tests, run security scans, validate against the spec

ANATOMY OF A SPEC:
Walk through each section briefly. Emphasize that each section serves a specific purpose in AI code generation:
- FRs tell AI WHAT to build
- NFRs tell AI HOW WELL to build it
- Acceptance criteria tell AI WHAT TO TEST
- Edge cases tell AI WHAT COULD GO WRONG
- Domain model tells AI the DATA STRUCTURE
- API contract tells AI the INTERFACE
- Test strategy tells AI HOW TO VERIFY

KEY INSIGHT: "A 10x improvement in spec quality leads to a 10x improvement in generated code quality." This is the leverage point of AI-native development.

EXERCISE: In the practical lab, participants will write a spec section and immediately see how it influences AI code generation quality.""")
    return sl

# Build remaining slides more concisely to keep total manageable
def slide_10():
    """Writing an Executable Specification"""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "Writing an Executable Specification", "Methodology", "10")

    # Example spec snippet
    _add_text_box(sl, Inches(0.5), Inches(1.2), Inches(6), Inches(0.3),
                  "Example: FR-1 Create Task (from Lab Exercise)", size=14, bold=True, color=C_PRIMARY)

    spec_text = """FR-1: Create a New Task
\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
Description: Users can create a new task with
title, description, priority, and category.
Status defaults to OPEN.

Acceptance Criteria:
  1. Valid request \u2192 task created with status OPEN
  2. Response includes task ID + creation timestamp
  3. Title: required, 3-200 characters
  4. Priority: LOW | MEDIUM | HIGH (default MEDIUM)
  5. Category ID: optional, must exist if provided

Edge Cases:
  \u2022 Empty title \u2192 400 Bad Request
  \u2022 Title > 200 chars \u2192 400 + validation msg
  \u2022 Invalid category \u2192 400 "Category not found"
  \u2022 Unauthenticated \u2192 401 Unauthorized"""

    spec_box = _add_shape(sl, Inches(0.5), Inches(1.6), Inches(6.2), Inches(4.2),
                          fill=RGBColor(0xF8, 0xF9, 0xFA), border=C_PRIMARY, radius=True)
    tf = spec_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_top = Inches(0.15)
    for line in spec_text.split('\n'):
        if tf.paragraphs[0].text == "":
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        r = p.add_run()
        r.text = line
        r.font.size = Pt(9)
        r.font.name = "Consolas"
        r.font.color.rgb = C_DARK_TEXT
        if line.startswith("FR-1") or line.startswith("Description") or line.startswith("Acceptance") or line.startswith("Edge"):
            r.font.bold = True
            r.font.color.rgb = C_PRIMARY

    # Best practices on right
    _add_text_box(sl, Inches(7.0), Inches(1.2), Inches(6), Inches(0.3),
                  "Spec Writing Best Practices", size=14, bold=True, color=C_PRIMARY)
    practices = [
        ("Be Specific", "Use exact data types, ranges, and formats.\n'Integer 0-100' not 'a number'"),
        ("Define Boundaries", "State min/max values, character limits,\nallowed enum values explicitly"),
        ("Cover Error Paths", "Every happy path needs corresponding\nerror scenarios with HTTP status codes"),
        ("Use Given/When/Then", "Acceptance criteria should be directly\ntranslatable to test assertions"),
        ("Include Examples", "Provide sample request/response JSON.\nAI generates better code from examples"),
    ]
    for i, (title, desc) in enumerate(practices):
        _card(sl, Inches(7.0), Inches(1.6 + i * 1.0), Inches(5.8), Inches(0.9),
              title, desc.split('\n'), accent=C_PRIMARY)

    _footer(sl, "A precise spec is the difference between AI generating 'close enough' code and 'production-ready' code")

    _notes(sl, """SPEAKER NOTES - Slide 10: Writing an Executable Specification
--------------------------------------------------------------
This slide bridges from theory to practice. Show participants what a real spec looks like.

THE EXAMPLE SPEC:
Walk through FR-1 (Create Task) line by line:
- Title: Clear, action-oriented. "Create a New Task" not "Task Creation Module"
- Description: One paragraph explaining WHAT and WHY.
- Acceptance Criteria: Numbered, specific, testable. Each one becomes a test case.
  * Criterion 3 says "3-200 characters" -- this DIRECTLY generates validation code.
  * Criterion 4 lists enum values -- AI generates the exact enum from this.
  * Criterion 5 says "must exist if provided" -- AI generates a DB lookup.
- Edge Cases: These are CRITICAL. Without them, AI generates only happy-path code.
  * "Empty title -> 400" becomes a validation test.
  * "Invalid category -> 400 'Category not found'" becomes both a lookup and a specific error message.

BEST PRACTICES (discuss each):
1. Be Specific: Vague specs = vague code. "A number" could be int, float, BigDecimal, String.
2. Define Boundaries: AI needs to know limits. Without "max 200 chars," it might not add validation.
3. Cover Error Paths: This is where most specs fall short. EVERY endpoint needs error scenarios.
4. Given/When/Then: "GIVEN an authenticated user, WHEN they POST a task with an empty title, THEN the system returns 400 with a validation message."
5. Include Examples: Show actual JSON payloads. AI generates more accurate code from examples than from descriptions.

LIVE EXERCISE (if time permits):
Ask participants to write acceptance criteria for FR-2 (View Tasks with Filtering). Compare their specs:
- Did they specify pagination defaults?
- Did they define what happens with invalid filter values?
- Did they specify sort order?
- Did they define the response format?""")
    return sl

# ── Slides 11-25 + Backup slides ──────────────────────────
# (Continuing with the same pattern for all remaining slides)

def slide_11():
    """Architecture: Domain Modeling & API Contract"""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "Architecture: Domain Model & API Contract-First", "Architecture", "11")

    # UML Class Diagram (simplified using shapes)
    _add_text_box(sl, Inches(0.5), Inches(1.2), Inches(6), Inches(0.3),
                  "UML Class Diagram: Task Management Domain", size=14, bold=True, color=C_PRIMARY)

    entities = [
        ("Task", "id: UUID (PK)\ntitle: String\ndescription: Text\nstatus: Enum\npriority: Enum\nassigneeId: UUID (FK)\ncategoryId: UUID (FK)\ncreatedAt: DateTime", Inches(0.5), Inches(1.7)),
        ("User", "id: UUID (PK)\nname: String\nemail: String (UNIQUE)\nrole: Enum\ncreatedAt: DateTime", Inches(3.5), Inches(1.7)),
        ("Category", "id: UUID (PK)\nname: String\ndescription: Text", Inches(0.5), Inches(4.5)),
        ("Comment", "id: UUID (PK)\ntaskId: UUID (FK)\nuserId: UUID (FK)\ncontent: Text\ncreatedAt: DateTime", Inches(3.5), Inches(4.5)),
    ]
    for name, attrs, x, y in entities:
        box = _add_shape(sl, x, y, Inches(2.7), Inches(2.2) if "assignee" in attrs else Inches(1.6),
                         fill=C_WHITE, border=C_PRIMARY, radius=True)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.1)
        tf.margin_top = Inches(0.05)
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = name
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = C_PRIMARY
        for line in attrs.split('\n'):
            p2 = tf.add_paragraph()
            r2 = p2.add_run()
            r2.text = line
            r2.font.size = Pt(8)
            r2.font.name = "Consolas"
            r2.font.color.rgb = C_DARK_TEXT

    # Relationships annotation
    _add_text_box(sl, Inches(2.8), Inches(3.5), Inches(1), Inches(0.3), "1    *", size=10, bold=True, color=C_RED)
    _add_text_box(sl, Inches(2.8), Inches(5.2), Inches(1), Inches(0.3), "1    *", size=10, bold=True, color=C_RED)

    # API Contract-First (right side)
    _add_text_box(sl, Inches(7.0), Inches(1.2), Inches(6), Inches(0.3),
                  "Contract-First API Design (OpenAPI)", size=14, bold=True, color=C_PRIMARY)

    api_code = """openapi: 3.0.3
paths:
  /api/tasks:
    post:
      summary: Create a new task
      operationId: createTask
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/.../CreateTaskDTO'
      responses:
        '201':
          description: Task created
        '400':
          description: Validation error
        '401':
          description: Unauthorized"""

    api_box = _add_shape(sl, Inches(7.0), Inches(1.6), Inches(5.8), Inches(3.2),
                         fill=RGBColor(0xF8, 0xF9, 0xFA), border=C_SECONDARY, radius=True)
    tf = api_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.15)
    tf.margin_top = Inches(0.1)
    for line in api_code.strip().split('\n'):
        if tf.paragraphs[0].text == "":
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        r = p.add_run()
        r.text = line
        r.font.size = Pt(8)
        r.font.name = "Consolas"
        r.font.color.rgb = C_DARK_TEXT

    # Contract-first flow
    _add_text_box(sl, Inches(7.0), Inches(5.0), Inches(6), Inches(0.25),
                  "Contract-First Workflow", size=12, bold=True, color=C_PRIMARY)
    cf_stages = ["Write\nOpenAPI", "Review &\nValidate", "Generate\nStubs", "Implement\nLogic", "Contract\nTests"]
    cf_colors = [C_PRIMARY, C_PURPLE, C_ACCENT, C_WARN, C_RED]
    for i, (s, c) in enumerate(zip(cf_stages, cf_colors)):
        _block_box(sl, Inches(7.0 + i * 1.15), Inches(5.35), Inches(1.0), Inches(0.7), s, fill=c)

    _footer(sl, "Domain model + API contract = complete interface specification for AI code generation")

    _notes(sl, """SPEAKER NOTES - Slide 11: Architecture - Domain Modeling & API Contract
-----------------------------------------------------------------------
Two critical architecture artifacts in SDD: the domain model (UML class diagram) and the API contract (OpenAPI).

UML CLASS DIAGRAM:
Walk through each entity:
1. TASK: Central entity. UUID primary key (globally unique). Status and Priority as enums (constrained values). Foreign keys to User and Category.
2. USER: Simple authentication entity. Email uniqueness constraint. Role enum (ADMIN, MEMBER, VIEWER).
3. CATEGORY: Organizational grouping. Tasks belong to categories.
4. COMMENT: Collaboration entity. Many-to-one with both Task and User.

Relationships: 1-to-many (User has many Tasks, Task has many Comments, Category has many Tasks).

KEY POINT: AI generates these diagrams from natural language descriptions in the spec. The spec says "Task belongs to User (assignee) and Category" and AI generates the entity model with correct FK relationships.

API CONTRACT-FIRST DESIGN:
- Define the API interface BEFORE writing any code
- OpenAPI/Swagger is the industry standard for REST API contracts
- Benefits:
  * Frontend and backend teams work in parallel
  * Auto-generate server stubs and client SDKs
  * Contract becomes the testing baseline
  * Documentation is always up-to-date

CONTRACT-FIRST WORKFLOW:
1. Write OpenAPI spec (YAML/JSON)
2. Review with stakeholders
3. Generate server stubs (Spring Boot, FastAPI, Express)
4. Implement business logic in the stubs
5. Run contract tests to verify implementation matches the spec

TEACHING TIP: Have students write the OpenAPI spec first, generate stubs, then implement. This teaches them to think about interfaces before implementation -- a crucial skill for system design.""")
    return sl

def slide_12():
    """AI Code Generation Workflow"""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "AI Code Generation Workflow", "Implementation", "12")

    # 6-step workflow
    steps = [
        ("1", "Approved\nSpec", C_PRIMARY, "Start with reviewed,\napproved specification"),
        ("2", "Prompt\nConstruction", C_SECONDARY, "Build context-rich prompt\nwith spec + constraints"),
        ("3", "AI\nGeneration", C_ACCENT, "AI generates code\nfrom prompt + spec"),
        ("4", "Human\nReview", C_PURPLE, "Developer reviews for\ncorrectness & quality"),
        ("5", "Refactor &\nImprove", C_WARN, "Clean up, optimize,\nhandle edge cases"),
        ("6", "Commit\n& Push", C_RED, "Version control +\ntrigger CI/CD pipeline"),
    ]
    for i, (num, title, clr, desc) in enumerate(steps):
        x = Inches(0.3 + i * 2.1)
        _block_box(sl, x, Inches(1.4), Inches(1.8), Inches(0.8), title, fill=clr)
        if i < 5:
            _arrow_right(sl, x + Inches(1.8), Inches(1.55))
        _add_text_box(sl, x, Inches(2.3), Inches(1.8), Inches(0.6), desc, size=9, color=C_LIGHT_TXT, align=PP_ALIGN.CENTER)

    # Best practices
    _add_text_box(sl, Inches(0.5), Inches(3.2), Inches(12), Inches(0.3),
                  "Best Practices for AI Code Generation", size=14, bold=True, color=C_PRIMARY)
    practices = [
        "Generate ONE component/layer at a time (entity \u2192 repository \u2192 service \u2192 controller)",
        "Review before asking AI for the next layer \u2014 errors compound across layers",
        "Keep prompts focused: include relevant spec section + existing code context",
        "Prefer generating from spec sections over free-form descriptions",
        "Use AI to generate tests from the SAME acceptance criteria that drove the code",
    ]
    for i, p in enumerate(practices):
        _add_text_box(sl, Inches(0.7), Inches(3.6 + i * 0.3), Inches(12), Inches(0.3),
                      f"\u2022 {p}", size=11, color=C_DARK_TEXT)

    # Code generation example
    _add_text_box(sl, Inches(0.5), Inches(5.2), Inches(12), Inches(0.3),
                  "Generation Order (Layer-by-Layer)", size=14, bold=True, color=C_PRIMARY)
    layers = [
        ("Layer 1", "Domain Entities\n(Task, User, Category)", C_PRIMARY),
        ("Layer 2", "Repository Interfaces\n(TaskRepository, etc.)", C_SECONDARY),
        ("Layer 3", "Service Layer\n(Business logic, validation)", C_ACCENT),
        ("Layer 4", "REST Controllers\n(Endpoints, DTOs, error handling)", C_PURPLE),
        ("Layer 5", "Tests\n(Unit, Integration, E2E)", C_WARN),
        ("Layer 6", "Config & CI/CD\n(Docker, pipeline YAML)", C_RED),
    ]
    for i, (layer, desc, clr) in enumerate(layers):
        _block_box(sl, Inches(0.3 + i * 2.1), Inches(5.6), Inches(1.85), Inches(1.0), f"{layer}\n{desc}", fill=clr)

    _footer(sl, "Disciplined workflow prevents the 'generate-everything-at-once' anti-pattern")

    _notes(sl, """SPEAKER NOTES - Slide 12: AI Code Generation Workflow
--------------------------------------------------------
This is the disciplined workflow for generating code with AI. This is where many teams go wrong -- they try to generate everything at once and get inconsistent, buggy results.

THE 6-STEP WORKFLOW:
1. APPROVED SPEC: Start with a reviewed spec. Don't generate from rough notes or verbal descriptions.
2. PROMPT CONSTRUCTION: Build a context-rich prompt. Include the specific FR, acceptance criteria, edge cases, AND any code already generated (entities, interfaces).
3. AI GENERATION: Let the AI generate. Don't interrupt mid-generation.
4. HUMAN REVIEW: Read every line. Check: Does it match the spec? Are edge cases handled? Any security issues?
5. REFACTOR & IMPROVE: Clean up naming, add missing error handling, optimize queries.
6. COMMIT & PUSH: Version control. This triggers CI/CD which validates the code against tests.

LAYER-BY-LAYER GENERATION:
Why this order matters:
- Layer 1 (Entities): Foundation. Everything else depends on the data model being correct.
- Layer 2 (Repositories): Data access patterns. Spring Data auto-generates SQL from method names.
- Layer 3 (Services): Business logic. This is where most complexity lives.
- Layer 4 (Controllers): Thin layer mapping HTTP to service calls.
- Layer 5 (Tests): Generated from the same spec. Test each layer independently.
- Layer 6 (Config): Infrastructure as code. Docker, CI/CD, monitoring.

ANTI-PATTERN: "Generate the entire application" -- this produces inconsistent code with naming conflicts, missing error handling, and tangled dependencies. Always generate layer-by-layer.

LIVE DEMO (if time): Show generating a Task entity from the spec using Cursor or Copilot. Then show generating the TaskRepository interface. Then the TaskService. Each step references the previously generated code.""")
    return sl

def slide_13():
    """Code Review & Security"""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "Code Review & Security in AI-Native Development", "Implementation", "13")

    _add_text_box(sl, Inches(0.5), Inches(1.2), Inches(6), Inches(0.3),
                  "AI Code Review Checklist", size=14, bold=True, color=C_PRIMARY)

    checklist = [
        ("\u2610 Spec Fidelity", "Does the code implement ALL acceptance criteria?"),
        ("\u2610 Edge Cases", "Are all documented error paths handled?"),
        ("\u2610 Input Validation", "Are all inputs validated at boundaries?"),
        ("\u2610 SQL Injection", "Parameterized queries? No string concatenation?"),
        ("\u2610 Auth & AuthZ", "Authentication checked? Role permissions enforced?"),
        ("\u2610 Error Messages", "No sensitive data in error responses?"),
        ("\u2610 Logging", "No secrets/PII in logs? Sufficient audit trail?"),
        ("\u2610 Dependencies", "Known vulnerabilities in imported libraries?"),
    ]
    for i, (item, desc) in enumerate(checklist):
        _add_text_box(sl, Inches(0.6), Inches(1.6 + i * 0.42), Inches(2.5), Inches(0.4),
                      item, size=11, bold=True, color=C_DARK_TEXT)
        _add_text_box(sl, Inches(3.2), Inches(1.6 + i * 0.42), Inches(3.5), Inches(0.4),
                      desc, size=10, color=C_LIGHT_TXT)

    # Security section (right)
    _add_text_box(sl, Inches(7.0), Inches(1.2), Inches(6), Inches(0.3),
                  "OWASP Top 10 for AI-Generated Code", size=14, bold=True, color=C_RED)
    owasp = [
        ("Injection", "AI may generate string-concatenated SQL. Always use parameterized queries.", C_RED),
        ("Broken Auth", "AI-generated auth is often incomplete. Verify token validation, session management.", C_RED),
        ("Sensitive Data", "AI may log or expose sensitive fields. Review all error responses and logs.", C_WARN),
        ("Insecure Dependencies", "AI picks popular libraries, not necessarily secure ones. Run Snyk/Dependabot.", C_WARN),
    ]
    for i, (vuln, desc, clr) in enumerate(owasp):
        _card(sl, Inches(7.0), Inches(1.6 + i * 1.1), Inches(5.8), Inches(1.0),
              f"OWASP: {vuln}", [desc], accent=clr)

    # Security scanning tools
    _add_text_box(sl, Inches(7.0), Inches(5.7), Inches(6), Inches(0.25),
                  "Automated Security Pipeline", size=12, bold=True, color=C_PRIMARY)
    sec_tools = [("SAST\nSonarQube", C_PRIMARY), ("SCA\nSnyk/Dependabot", C_SECONDARY),
                 ("DAST\nOWASP ZAP", C_ACCENT), ("Secrets\nGitGuardian", C_PURPLE)]
    for i, (t, c) in enumerate(sec_tools):
        _block_box(sl, Inches(7.0 + i * 1.55), Inches(6.0), Inches(1.4), Inches(0.7), t, fill=c)

    _footer(sl, "AI generates code quickly \u2014 security review ensures it's generated SAFELY")

    _notes(sl, """SPEAKER NOTES - Slide 13: Code Review & Security
---------------------------------------------------
AI-generated code MUST be reviewed with extra scrutiny for security. AI tools are trained on public repos, many of which contain insecure patterns.

CODE REVIEW CHECKLIST:
Walk through each item. For faculty teaching security-conscious development:
1. Spec Fidelity: Compare every acceptance criterion to the code. Missing criteria = missing functionality.
2. Edge Cases: Each edge case in the spec should have corresponding error handling in the code.
3. Input Validation: AI often validates at the wrong layer. Validation should happen at the boundary (controller) AND in the service layer.
4. SQL Injection: This is the #1 risk with AI code. AI sometimes generates: "SELECT * FROM tasks WHERE status = '" + status + "'" instead of parameterized queries.
5. Auth & AuthZ: AI may generate endpoints without authentication checks. Every endpoint must verify the user's token and role.
6. Error Messages: AI loves helpful error messages like "User admin@example.com not found in database users table" -- this leaks schema info.
7. Logging: AI may log request bodies including passwords, tokens, PII.
8. Dependencies: AI picks well-known libraries, but doesn't check for CVEs.

OWASP TOP 10: Focus on the 4 most relevant to AI-generated code:
- Injection: Most common vulnerability in AI-generated code
- Broken Auth: AI generates "looks correct" auth that has subtle gaps
- Sensitive Data: AI doesn't understand what's sensitive in YOUR domain
- Insecure Dependencies: AI picks popular, not necessarily patched, versions

AUTOMATED SECURITY PIPELINE:
- SAST (Static Application Security Testing): SonarQube scans source code
- SCA (Software Composition Analysis): Snyk scans dependencies
- DAST (Dynamic Application Security Testing): OWASP ZAP tests running app
- Secrets scanning: GitGuardian catches committed API keys, passwords""")
    return sl

def slide_14():
    """Testing Strategy"""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "Testing Strategy: From Specification to Tests", "Testing", "14")

    # Test pyramid
    _add_text_box(sl, Inches(0.5), Inches(1.2), Inches(5), Inches(0.3),
                  "Test Pyramid for AI-Native Development", size=14, bold=True, color=C_PRIMARY)

    pyramid_levels = [
        ("E2E / UI Tests", Inches(3.5), Inches(1.0), C_RED, "Few, slow, high confidence"),
        ("Integration Tests", Inches(2.8), Inches(1.6), C_WARN, "API contracts, DB queries"),
        ("Unit Tests", Inches(1.8), Inches(2.8), C_ACCENT, "Many, fast, isolated logic"),
    ]
    x_base = Inches(1.5)
    y_base = Inches(1.6)
    for i, (name, w_off, h_off, clr, desc) in enumerate(pyramid_levels):
        box = _add_shape(sl, x_base + Inches(i * 0.5), y_base + Inches(i * 1.0),
                         Inches(4.5 - i * 1.0), Inches(0.8), fill=clr, radius=True)
        _set_text(box, f"{name}  \u2014  {desc}", size=10, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)

    # Spec to test mapping
    _add_text_box(sl, Inches(6.5), Inches(1.2), Inches(6.5), Inches(0.3),
                  "Spec \u2192 Test Mapping", size=14, bold=True, color=C_PRIMARY)
    mappings = [
        ("Acceptance Criteria #1", "\u2192", "Unit test: testCreateTask_validRequest_returnsCreated()"),
        ("Acceptance Criteria #3", "\u2192", "Unit test: testCreateTask_titleTooShort_returns400()"),
        ("Edge Case: empty title", "\u2192", "Unit test: testCreateTask_emptyTitle_returns400()"),
        ("NFR: P95 < 200ms", "\u2192", "Load test: k6 scenario with 50 concurrent users"),
        ("API Contract: POST 201", "\u2192", "Integration test: POST /api/tasks returns 201 + body"),
    ]
    for i, (spec, arrow, test) in enumerate(mappings):
        y = Inches(1.65 + i * 0.55)
        _add_text_box(sl, Inches(6.5), y, Inches(2.5), Inches(0.5), spec, size=9, bold=True, color=C_PRIMARY)
        _add_text_box(sl, Inches(9.0), y, Inches(0.3), Inches(0.5), arrow, size=14, bold=True, color=C_ACCENT)
        _add_text_box(sl, Inches(9.4), y, Inches(3.5), Inches(0.5), test, size=8, color=C_DARK_TEXT)

    # Test generation approach
    _add_text_box(sl, Inches(0.5), Inches(4.8), Inches(12), Inches(0.3),
                  "AI-Generated Test Example", size=14, bold=True, color=C_PRIMARY)

    test_code = """@Test
void createTask_validRequest_returnsCreated() {
    CreateTaskDTO dto = new CreateTaskDTO("Fix login bug", "HIGH");
    ResponseEntity<TaskDTO> response =
        restTemplate.postForEntity("/api/tasks", dto, TaskDTO.class);

    assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
    assertThat(response.getBody().getTitle()).isEqualTo("Fix login bug");
    assertThat(response.getBody().getStatus()).isEqualTo("OPEN");
}"""
    code_box = _add_shape(sl, Inches(0.5), Inches(5.15), Inches(7), Inches(1.6),
                          fill=RGBColor(0xF8, 0xF9, 0xFA), border=C_ACCENT, radius=True)
    tf = code_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.15)
    tf.margin_top = Inches(0.08)
    for line in test_code.strip().split('\n'):
        if tf.paragraphs[0].text == "":
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        r = p.add_run()
        r.text = line
        r.font.size = Pt(8)
        r.font.name = "Consolas"
        r.font.color.rgb = C_DARK_TEXT

    _card(sl, Inches(8.0), Inches(5.15), Inches(4.8), Inches(1.6),
          "Key Testing Principles",
          ["Tests derived from acceptance criteria, not code",
           "Each criterion = at least one test method",
           "Edge cases from spec = negative test cases",
           "AI generates test skeleton; human verifies assertions"],
          accent=C_ACCENT)

    _footer(sl, "Tests generated from specs verify INTENT, not just implementation")

    _notes(sl, """SPEAKER NOTES - Slide 14: Testing Strategy
----------------------------------------------
Testing in AI-native development is fundamentally different because tests come from SPECIFICATIONS, not from code.

TEST PYRAMID:
- Unit Tests (base): Test individual functions/methods in isolation. Use mocks for dependencies. AI generates these directly from acceptance criteria.
- Integration Tests (middle): Test multiple components together. Verify API contracts, database queries, service interactions.
- E2E Tests (top): Test complete user flows. Browser automation (Playwright) or API-level scenarios.

SPEC-TO-TEST MAPPING:
This is the key insight. Walk through each mapping:
1. Acceptance Criterion #1 ("valid request returns created") -> Unit test verifying happy path
2. Criterion #3 ("title 3-200 characters") -> Boundary tests at 2, 3, 200, 201 characters
3. Edge case ("empty title") -> Negative test verifying 400 response
4. NFR ("P95 < 200ms") -> Load test with realistic concurrency
5. API contract ("POST returns 201") -> Integration test against running server

THE CODE EXAMPLE:
- This test is generated DIRECTLY from the spec. The assertions match the acceptance criteria.
- AI generated the test method name from the criterion description.
- The DTO matches the API contract in the spec.
- The assertions verify: status code (201), title (input), and default status (OPEN).

KEY PRINCIPLE: Tests verify INTENT (what the spec says should happen), not IMPLEMENTATION (how the code does it). This means tests survive code refactoring.""")
    return sl

def slide_15():
    """CI/CD Pipeline with AI"""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "CI/CD Pipeline with AI Integration", "DevOps", "15")

    # Pipeline architecture diagram
    _add_text_box(sl, Inches(0.5), Inches(1.2), Inches(12), Inches(0.3),
                  "AI-Enhanced CI/CD Pipeline Architecture", size=14, bold=True, color=C_PRIMARY)

    pipeline_stages = [
        ("Code\nPush", C_PRIMARY),
        ("Build &\nCompile", C_SECONDARY),
        ("Unit\nTests", C_ACCENT),
        ("SAST\nScan", C_PURPLE),
        ("Integration\nTests", C_WARN),
        ("Container\nBuild", C_RED),
        ("Deploy\nStaging", C_SECONDARY),
        ("Smoke\nTests", C_ACCENT),
    ]
    for i, (stage, clr) in enumerate(pipeline_stages):
        _block_box(sl, Inches(0.2 + i * 1.6), Inches(1.6), Inches(1.35), Inches(0.8), stage, fill=clr)
        if i < len(pipeline_stages) - 1:
            _arrow_right(sl, Inches(1.55 + i * 1.6), Inches(1.8), w=Inches(0.25))

    # Quality gates
    _add_text_box(sl, Inches(0.5), Inches(2.7), Inches(12), Inches(0.25),
                  "Quality Gates (automated checks that must pass)", size=12, bold=True, color=C_RED)
    gates = [
        ("Gate 1: Tests", "All unit + integration tests pass\nCode coverage > 80%", C_ACCENT),
        ("Gate 2: Security", "Zero critical vulnerabilities\nDependency scan clean", C_RED),
        ("Gate 3: Quality", "SonarQube: no new bugs or\ncode smells above threshold", C_PURPLE),
        ("Gate 4: Contract", "API responses match OpenAPI\ncontract specification", C_WARN),
    ]
    for i, (name, desc, clr) in enumerate(gates):
        _card(sl, Inches(0.5 + i * 3.1), Inches(3.05), Inches(2.9), Inches(1.0),
              name, desc.split('\n'), accent=clr)

    # GitHub Actions YAML
    _add_text_box(sl, Inches(0.5), Inches(4.3), Inches(6), Inches(0.25),
                  "GitHub Actions CI/CD (AI-generated)", size=12, bold=True, color=C_PRIMARY)
    yaml_code = """name: ai-native-ci
on: [push, pull_request]
jobs:
  build-test-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { java-version: '21' }
      - run: ./mvnw verify        # Build + test
      - run: ./mvnw sonar:sonar   # Code quality
      - uses: snyk/actions/maven@v1  # Dep scan
      - run: docker build -t app .   # Container"""
    yaml_box = _add_shape(sl, Inches(0.5), Inches(4.6), Inches(6), Inches(2.3),
                          fill=RGBColor(0xF8, 0xF9, 0xFA), border=C_PRIMARY, radius=True)
    tf = yaml_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.15)
    tf.margin_top = Inches(0.08)
    for line in yaml_code.strip().split('\n'):
        if tf.paragraphs[0].text == "":
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        r = p.add_run()
        r.text = line
        r.font.size = Pt(8)
        r.font.name = "Consolas"
        r.font.color.rgb = C_DARK_TEXT

    # AI's role in CI/CD (right)
    _add_text_box(sl, Inches(7.0), Inches(4.3), Inches(6), Inches(0.25),
                  "How AI Enhances CI/CD", size=12, bold=True, color=C_PRIMARY)
    ai_cicd = [
        ("Pipeline Generation", "AI generates entire workflow YAML\nfrom architecture decisions"),
        ("Intelligent Test Selection", "AI identifies which tests to run\nbased on changed files"),
        ("Auto-Fix Suggestions", "AI suggests fixes for failed\nsecurity scans or lint violations"),
        ("Deploy Decision Support", "AI analyzes metrics to recommend\ncanary % or rollback decisions"),
    ]
    for i, (title, desc) in enumerate(ai_cicd):
        _card(sl, Inches(7.0), Inches(4.6 + i * 0.85), Inches(5.8), Inches(0.75),
              title, desc.split('\n'), accent=C_PRIMARY)

    _footer(sl, "AI generates the pipeline | Quality gates enforce standards | Humans approve production deployments")

    _notes(sl, """SPEAKER NOTES - Slide 15: CI/CD Pipeline with AI Integration
-----------------------------------------------------------------
This slide shows how AI integrates into the CI/CD pipeline. Walk through the architecture diagram left to right.

PIPELINE STAGES:
1. Code Push: Developer pushes code (or AI-generated code) to the repository
2. Build & Compile: Maven/Gradle/npm compiles the code
3. Unit Tests: All unit tests run (generated from spec acceptance criteria)
4. SAST Scan: SonarQube checks for bugs, code smells, security vulnerabilities
5. Integration Tests: Tests against real database (Testcontainers), real HTTP endpoints
6. Container Build: Docker image built with production-ready configuration
7. Deploy Staging: Kubernetes deployment to staging environment
8. Smoke Tests: Basic health check and critical path verification

QUALITY GATES:
These are automated checkpoints that BLOCK the pipeline if standards aren't met:
- Gate 1: Test coverage threshold (e.g., 80%). If below, pipeline fails.
- Gate 2: Zero critical security vulnerabilities. One critical = pipeline blocked.
- Gate 3: Code quality metrics within threshold. New technical debt is flagged.
- Gate 4: API contract compliance. Response shapes must match OpenAPI spec.

THE YAML EXAMPLE:
Walk through the GitHub Actions file line by line:
- Triggers on push and PR (catches issues before merge)
- Uses Ubuntu runner (consistent, reproducible)
- Java 21 setup (matches spec)
- ./mvnw verify: Compiles AND runs ALL tests in one command
- sonar:sonar: Pushes results to SonarQube for quality analysis
- snyk/actions: Scans all Maven dependencies for known CVEs
- docker build: Creates the deployable artifact

AI'S ROLE: Emphasize that AI can:
1. Generate this entire YAML from a description of your tech stack
2. Suggest which tests to run based on which files changed (intelligent test selection)
3. Auto-suggest fixes when scans find issues
4. Recommend deployment strategies based on risk assessment""")
    return sl

def slide_16():
    """Performance & Scale Testing"""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "Performance & Scale Testing", "Performance", "16")

    # Performance risks
    _add_text_box(sl, Inches(0.5), Inches(1.2), Inches(6), Inches(0.3),
                  "Performance Risks in AI-Generated Code", size=14, bold=True, color=C_RED)
    risks = [
        ("N+1 Query Patterns", "AI generates loops with individual DB queries instead of JOINs"),
        ("Missing Indexes", "No indexes on frequently queried columns (status, assigneeId)"),
        ("Over-Fetching Data", "SELECT * instead of specific columns; no pagination"),
        ("No Caching Strategy", "Every request hits the database; no Redis/in-memory cache"),
        ("Inefficient Serialization", "Deep object graphs serialized without DTOs"),
    ]
    for i, (risk, desc) in enumerate(risks):
        _card(sl, Inches(0.5), Inches(1.6 + i * 0.7), Inches(6.2), Inches(0.6),
              risk, [desc], accent=C_RED)

    # Performance targets and testing approach
    _add_text_box(sl, Inches(7.0), Inches(1.2), Inches(6), Inches(0.3),
                  "Performance Testing Approach", size=14, bold=True, color=C_PRIMARY)

    targets = [("P95 Latency\n< 200ms", C_ACCENT), ("Throughput\n> 500 req/s", C_PRIMARY),
               ("Concurrent\n100 users", C_SECONDARY), ("Error Rate\n< 0.1%", C_RED)]
    for i, (t, c) in enumerate(targets):
        _block_box(sl, Inches(7.0 + i * 1.55), Inches(1.6), Inches(1.4), Inches(0.8), t, fill=c)

    _add_text_box(sl, Inches(7.0), Inches(2.6), Inches(6), Inches(0.25),
                  "Monitoring Stack", size=12, bold=True, color=C_PRIMARY)
    stack = [("OpenTelemetry", "Distributed tracing &\nmetrics collection"),
             ("Prometheus", "Time-series metrics\nstorage & alerting"),
             ("Grafana", "Real-time dashboards\n& visualization")]
    for i, (name, desc) in enumerate(stack):
        _card(sl, Inches(7.0), Inches(2.9 + i * 0.8), Inches(5.8), Inches(0.7),
              name, [desc], accent=C_PRIMARY)

    # k6 load test example
    _add_text_box(sl, Inches(0.5), Inches(5.2), Inches(5), Inches(0.25),
                  "Load Test Example (k6)", size=12, bold=True, color=C_PRIMARY)
    k6_code = """import http from 'k6/http';
export const options = {
  vus: 50, duration: '30s',
  thresholds: { http_req_duration: ['p(95)<500'] }
};
export default function() {
  http.post('http://localhost:8080/api/tasks',
    JSON.stringify({title:'Test',priority:'HIGH'}),
    {headers:{'Content-Type':'application/json'}});
}"""
    k6_box = _add_shape(sl, Inches(0.5), Inches(5.5), Inches(6.2), Inches(1.5),
                        fill=RGBColor(0xF8, 0xF9, 0xFA), border=C_SECONDARY, radius=True)
    tf = k6_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.15)
    tf.margin_top = Inches(0.08)
    for line in k6_code.strip().split('\n'):
        if tf.paragraphs[0].text == "":
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        r = p.add_run()
        r.text = line
        r.font.size = Pt(8)
        r.font.name = "Consolas"
        r.font.color.rgb = C_DARK_TEXT

    _footer(sl, "AI generates load test scripts from your NFRs | Performance testing should run in CI/CD")

    _notes(sl, """SPEAKER NOTES - Slide 16: Performance & Scale Testing
--------------------------------------------------------
AI-generated code often has performance issues because AI optimizes for correctness, not performance.

PERFORMANCE RISKS (walk through each):
1. N+1 QUERIES: AI generates: for each task, query the user. Fix: JOIN FETCH or @EntityGraph.
   Example: AI generates taskRepository.findAll() + for each task: userRepository.findById(task.assigneeId)
   Should be: taskRepository.findAllWithAssignees() using a JOIN query.

2. MISSING INDEXES: AI creates tables without indexes. Fix: add indexes on FK columns and filter columns.

3. OVER-FETCHING: AI uses SELECT * and loads all tasks without pagination. Fix: Spring Data Pageable.

4. NO CACHING: Every request hits the DB. Fix: @Cacheable for read-heavy endpoints, Redis for distributed.

5. INEFFICIENT SERIALIZATION: AI returns entity objects directly, causing deep serialization of relationships.

PERFORMANCE TARGETS: Define measurable, specific targets:
- P95 < 200ms: 95% of requests complete in under 200ms
- Throughput > 500 req/s: System handles 500 requests per second
- 100 concurrent users: System maintains performance under load
- Error rate < 0.1%: Less than 1 in 1000 requests fail

THE k6 EXAMPLE: Quick load test script. Key elements:
- vus: 50 virtual users sending requests simultaneously
- duration: 30 seconds of sustained load
- threshold: P95 must be under 500ms or the test FAILS
- The test sends realistic POST requests with proper JSON

MONITORING: Three-layer observability:
- OpenTelemetry: Instrument your code (traces, metrics, logs)
- Prometheus: Store and query time-series metrics
- Grafana: Visualize everything in dashboards""")
    return sl

def slide_17():
    """Multi-Agent AI Development"""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "Multi-Agent AI Development Architecture", "Advanced", "17")

    # Architecture diagram
    _add_text_box(sl, Inches(0.5), Inches(1.2), Inches(12), Inches(0.3),
                  "Multi-Agent System Architecture", size=14, bold=True, color=C_PRIMARY)

    # Orchestrator at center top
    _block_box(sl, Inches(4.5), Inches(1.6), Inches(4.0), Inches(0.8),
               "Orchestrator (Planner + Shared Memory)", fill=C_PRIMARY)

    # Agent boxes
    agents = [
        ("Requirements\nAgent", C_SECONDARY, Inches(0.3)),
        ("Architect\nAgent", C_PURPLE, Inches(2.5)),
        ("Coding\nAgent", C_ACCENT, Inches(4.7)),
        ("Testing\nAgent", C_WARN, Inches(6.9)),
        ("Security\nAgent", C_RED, Inches(9.1)),
        ("DevOps\nAgent", C_SECONDARY, Inches(11.3)),
    ]
    for name, clr, x in agents:
        _block_box(sl, x, Inches(2.8), Inches(1.8), Inches(0.8), name, fill=clr)

    # Agent role descriptions
    _add_text_box(sl, Inches(0.5), Inches(3.9), Inches(12), Inches(0.3),
                  "Agent Roles & Responsibilities", size=14, bold=True, color=C_PRIMARY)
    roles = [
        ("Requirements Agent", "Analyzes user stories, generates structured FRs/NFRs, validates completeness", C_SECONDARY),
        ("Architect Agent", "Proposes architecture, generates UML diagrams, evaluates trade-offs", C_PURPLE),
        ("Coding Agent", "Generates code from specs, implements patterns, refactors existing code", C_ACCENT),
        ("Testing Agent", "Generates tests from specs, runs mutation testing, coverage analysis", C_WARN),
        ("Security Agent", "SAST/DAST scans, OWASP compliance, dependency vulnerability analysis", C_RED),
        ("DevOps Agent", "Generates CI/CD pipelines, Dockerfiles, deployment manifests", C_SECONDARY),
    ]
    for i, (role, desc, clr) in enumerate(roles):
        col = i % 2
        row = i // 2
        _card(sl, Inches(0.5 + col * 6.3), Inches(4.25 + row * 0.7), Inches(6.0), Inches(0.6),
              role, [desc], accent=clr)

    # Key concepts
    eq = _add_shape(sl, Inches(0.5), Inches(6.5), Inches(12.3), Inches(0.45),
                    fill=C_LIGHT_BG, border=C_PURPLE, radius=True)
    _set_text(eq, "Key Concept: Agents are specialized, orchestrated, and human-supervised \u2014 each has its own tools, permissions, and scope",
              size=11, bold=True, color=C_PURPLE, align=PP_ALIGN.CENTER)

    _footer(sl, "Multi-agent = specialized expertise + coordinated workflow + human oversight at decision points")

    _notes(sl, """SPEAKER NOTES - Slide 17: Multi-Agent AI Development
--------------------------------------------------------------------
This slide introduces multi-agent AI development -- where multiple specialized AI agents collaborate on a software project.

WHY MULTI-AGENT:
- Single-prompt generation has limits: context window, task complexity, quality degradation
- Multi-agent breaks the problem into specialized roles
- Each agent is an expert in its domain (requirements, architecture, coding, testing, security, devops)
- The Orchestrator coordinates the workflow, resolves conflicts, maintains shared context

ARCHITECTURE:
- Orchestrator: Central coordinator with a planner (decides what to do next) and shared memory (context that all agents can access)
- Each agent has:
  * Specialized prompt/instructions for its role
  * Access to specific tools (e.g., Security Agent has Snyk, OWASP ZAP)
  * Defined permissions (Coding Agent can write code, Security Agent can only read/scan)
  * Clear inputs and outputs

AGENT ROLES:
1. Requirements Agent: Takes user stories, generates structured FRs with acceptance criteria. Identifies gaps and asks clarifying questions.
2. Architect Agent: Proposes architectures (monolith vs microservices, SQL vs NoSQL), generates UML diagrams, evaluates trade-offs.
3. Coding Agent: Takes approved spec + architecture, generates code layer-by-layer. Most compute-intensive agent.
4. Testing Agent: Takes the same spec, generates tests. Runs mutation testing to verify test quality. Reports coverage gaps.
5. Security Agent: Scans generated code for OWASP vulnerabilities. Checks dependencies. Reviews auth/authz patterns.
6. DevOps Agent: Generates Dockerfiles, CI/CD pipelines, deployment manifests. Configures monitoring and alerting.

REAL-WORLD EXAMPLE: Frameworks like CrewAI, AutoGen, and LangGraph enable this pattern today. The agents communicate through structured messages and shared context.

HUMAN CHECKPOINTS: Critical decision points where humans review and approve:
- After requirements: "Is this what we want?"
- After architecture: "Is this the right design?"
- After code generation: "Does this look correct?"
- Before deployment: "Is this safe to deploy?"

DISCUSSION: "How could multi-agent systems change software engineering education? Could students design agent teams as a project?"
""")
    return sl

def slide_18():
    """AI Governance & Responsible AI"""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "AI Governance & Responsible AI", "Advanced", "18")

    # Governance framework
    _add_text_box(sl, Inches(0.5), Inches(1.2), Inches(6), Inches(0.3),
                  "AI Governance Framework", size=14, bold=True, color=C_PRIMARY)

    pillars = [
        ("Transparency", "Document AI usage in development.\nLog what was AI-generated vs human-written.\nMaintain audit trail of AI decisions.", C_PRIMARY),
        ("Accountability", "Human approvers for all AI output.\nClear ownership of generated code.\nReview gates before production.", C_SECONDARY),
        ("Safety & Security", "Automated security scanning.\nVulnerability management.\nRegular dependency audits.", C_RED),
        ("Fairness & Bias", "Review AI-generated UX for bias.\nTest with diverse data sets.\nValidate against accessibility standards.", C_PURPLE),
    ]
    for i, (pillar, desc, clr) in enumerate(pillars):
        y = Inches(1.6 + i * 1.15)
        _card(sl, Inches(0.5), y, Inches(6.2), Inches(1.05), pillar, desc.split('\n'), accent=clr)

    # Regulatory landscape
    _add_text_box(sl, Inches(7.0), Inches(1.2), Inches(6), Inches(0.3),
                  "Regulatory & Industry Standards", size=14, bold=True, color=C_PRIMARY)
    regulations = [
        ("NIST AI RMF", "Risk Management Framework for AI systems.\nGovern, Map, Measure, Manage lifecycle.", C_PRIMARY),
        ("EU AI Act", "Risk-based classification of AI systems.\nHigh-risk requires conformity assessment.", C_SECONDARY),
        ("ISO/IEC 42001", "AI Management System standard.\nRequirements for responsible AI practices.", C_ACCENT),
        ("OWASP AI Security", "Top 10 security risks for AI/ML systems.\nPrompt injection, data poisoning, model theft.", C_RED),
    ]
    for i, (name, desc, clr) in enumerate(regulations):
        y = Inches(1.6 + i * 1.15)
        _card(sl, Inches(7.0), y, Inches(5.8), Inches(1.05), name, desc.split('\n'), accent=clr)

    # Organizational readiness
    _add_text_box(sl, Inches(0.5), Inches(6.2), Inches(12), Inches(0.3),
                  "Organizational AI Readiness Checklist", size=12, bold=True, color=C_PRIMARY)
    readiness = [
        "\u2610 AI usage policy documented & communicated",
        "\u2610 Code provenance tracking (AI vs human)",
        "\u2610 Automated security gates in CI/CD",
        "\u2610 Regular AI output quality audits",
        "\u2610 Developer training on responsible AI use",
        "\u2610 IP & licensing compliance review",
    ]
    for i, item in enumerate(readiness):
        col = i % 3
        row = i // 3
        _add_text_box(sl, Inches(0.5 + col * 4.1), Inches(6.5 + row * 0.25), Inches(4), Inches(0.25),
                      item, size=9, color=C_DARK_TEXT)

    _footer(sl, "AI governance is not optional \u2014 it's a regulatory requirement and an ethical imperative")

    _notes(sl, """SPEAKER NOTES - Slide 18: AI Governance & Responsible AI
----------------------------------------------------------------------
This slide covers the governance and ethical dimensions of AI-native development.

AI GOVERNANCE FRAMEWORK (four pillars):
1. TRANSPARENCY: Know what AI generated. Log it. Document it. This matters for:
   - Audit compliance (who wrote what)
   - Bug tracking (was this a human error or AI error?)
   - IP management (what was AI-generated vs original work?)

2. ACCOUNTABILITY: Humans are accountable for AI output. The AI is a tool, not a decision-maker.
   - Every piece of AI-generated code must have a human reviewer
   - Quality gates enforce standards before code reaches production
   - Clear ownership: the developer who accepted AI output owns it

3. SAFETY & SECURITY: AI-generated code can introduce vulnerabilities.
   - SAST/DAST in every pipeline
   - Dependency scanning for known CVEs
   - Regular penetration testing of AI-generated systems

4. FAIRNESS & BIAS: AI reflects its training data, which may contain biases.
   - Review generated UX for accessibility
   - Test with diverse datasets
   - Validate AI-suggested defaults (e.g., don't default to English-only)

REGULATORY LANDSCAPE:
- NIST AI RMF: US framework. Four functions: Govern, Map, Measure, Manage. Voluntary but influential.
- EU AI Act: Mandatory in EU from 2025. Classifies AI by risk level. Software development tools are generally "limited risk" but AI-generated systems may be "high risk" depending on domain.
- ISO/IEC 42001: International standard for AI management systems. Provides a certifiable framework.
- OWASP AI: Security-focused. Covers prompt injection, training data poisoning, model extraction.

TEACHING ANGLE: Faculty should consider adding AI ethics and governance modules to their CS curriculum. Students need to understand:
- Legal implications of using AI-generated code (IP, licensing)
- Ethical responsibilities when deploying AI-generated systems
- How to implement governance controls in their projects""")
    return sl

def slide_19():
    """Organizational Adoption Roadmap"""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "Organizational AI-Native Adoption Roadmap", "Advanced", "19")

    # Maturity model
    _add_text_box(sl, Inches(0.5), Inches(1.2), Inches(12), Inches(0.3),
                  "AI-Native Maturity Model", size=14, bold=True, color=C_PRIMARY)

    levels = [
        ("Level 1\nAd-hoc", "Individual developers use\nAI tools informally.\nNo standardization.", C_RED),
        ("Level 2\nGuided", "AI tools standardized.\nPrompt libraries shared.\nBasic review processes.", C_WARN),
        ("Level 3\nIntegrated", "SDD methodology adopted.\nAI in CI/CD pipeline.\nGovernance established.", C_PRIMARY),
        ("Level 4\nOptimized", "Multi-agent systems.\nFull spec-driven workflow.\nContinuous improvement.", C_ACCENT),
    ]
    for i, (level, desc, clr) in enumerate(levels):
        x = Inches(0.3 + i * 3.2)
        box = _add_shape(sl, x, Inches(1.6), Inches(2.9), Inches(2.0),
                         fill=C_WHITE, border=clr, radius=True)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        tf.margin_top = Inches(0.1)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = level
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = clr
        for line in desc.split('\n'):
            p2 = tf.add_paragraph()
            p2.alignment = PP_ALIGN.CENTER
            p2.space_before = Pt(3)
            r2 = p2.add_run()
            r2.text = line
            r2.font.size = Pt(9)
            r2.font.color.rgb = C_LIGHT_TXT
        if i < 3:
            _arrow_right(sl, x + Inches(2.9), Inches(2.3))

    # Adoption challenges
    _add_text_box(sl, Inches(0.5), Inches(4.0), Inches(6), Inches(0.3),
                  "Common Adoption Challenges", size=14, bold=True, color=C_RED)
    challenges = [
        ("Resistance to Change", "Developers fear job displacement.\nFrame AI as amplification, not replacement."),
        ("Quality Concerns", "AI output varies in quality.\nEstablish review gates and quality metrics."),
        ("IP & Legal Risk", "AI-generated code licensing unclear.\nEstablish IP policies and training data audit."),
        ("Skill Gaps", "Teams lack spec-writing and AI-prompting skills.\nInvest in training and mentoring."),
    ]
    for i, (ch, desc) in enumerate(challenges):
        _card(sl, Inches(0.5), Inches(4.4 + i * 0.75), Inches(6.2), Inches(0.65),
              ch, desc.split('\n'), accent=C_WARN)

    # Success factors
    _add_text_box(sl, Inches(7.0), Inches(4.0), Inches(6), Inches(0.3),
                  "Success Factors", size=14, bold=True, color=C_ACCENT)
    factors = [
        ("Executive Sponsorship", "Leadership commitment to AI-native transformation"),
        ("Start Small", "Pilot with one team, one project, measure results"),
        ("Measure Impact", "Track: velocity, quality, developer satisfaction"),
        ("Community of Practice", "Internal champions, knowledge sharing, best practices"),
        ("Continuous Learning", "Regular training, tool updates, methodology evolution"),
    ]
    for i, (factor, desc) in enumerate(factors):
        _card(sl, Inches(7.0), Inches(4.4 + i * 0.65), Inches(5.8), Inches(0.55),
              factor, [desc], accent=C_ACCENT)

    _footer(sl, "AI-native adoption is a journey, not a destination \u2014 start with Level 2, aim for Level 3")

    _notes(sl, """SPEAKER NOTES - Slide 19: Organizational Adoption Roadmap
----------------------------------------------------------------------
This slide provides a practical framework for organizations (and universities) to adopt AI-native practices.

MATURITY MODEL:
Level 1 (Ad-hoc): Where most organizations are today. Individual developers use ChatGPT/Copilot informally. No standards, no governance, no measurement.
Level 2 (Guided): Organization standardizes on specific tools. Shared prompt libraries. Basic code review for AI output. This is the MINIMUM target.
Level 3 (Integrated): SDD methodology is the default. AI is embedded in CI/CD. Governance policies enforced. Quality metrics tracked. This is the SWEET SPOT for most teams.
Level 4 (Optimized): Multi-agent systems, full automation, continuous improvement. Only leading-edge organizations achieve this today.

FOR ACADEMIC INSTITUTIONS:
- Level 1: "Students use ChatGPT for assignments" (current state)
- Level 2: "We teach structured prompt engineering and review practices"
- Level 3: "Our curriculum includes SDD, AI-assisted development, governance"
- Level 4: "Students build multi-agent systems and contribute to AI tool development"

ADOPTION CHALLENGES:
1. Resistance: Faculty may resist changing curriculum. Frame it as evolution, not revolution.
2. Quality: AI output quality is inconsistent. That's WHY we teach review and testing.
3. IP/Legal: Open discussion about academic integrity, plagiarism detection, attribution.
4. Skills: Both faculty and students need new skills. That's what this workshop addresses.

SUCCESS FACTORS: Practical advice for implementation.

DISCUSSION: "What maturity level is your institution at? What would it take to move to the next level?"
""")
    return sl

def slide_20():
    """Practical Labs Overview"""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "Practical Labs Overview", "Practical", "20")

    _add_text_box(sl, Inches(0.5), Inches(1.2), Inches(12), Inches(0.3),
                  "Hands-On Lab Exercises (Choose based on comfort level)", size=14, bold=True, color=C_PRIMARY)

    labs = [
        ("Lab 1: Task Management REST API", "Java 21 + Spring Boot + PostgreSQL + Docker",
         "1.5-2 hrs", "Full CRUD API with auth, categories, comments, filtering, pagination",
         "Intermediate", C_PRIMARY),
        ("Lab 2: Student Grade Calculator", "Python 3.12 + FastAPI + SQLite",
         "1-1.5 hrs", "Grade calculation, GPA computation, class statistics, reports",
         "Beginner-Intermediate", C_ACCENT),
        ("Lab 3: E-Commerce Product Catalog", "Node.js + Express + MongoDB",
         "1.5-2 hrs", "Product CRUD, search/filter, inventory tracking, image URLs",
         "Intermediate", C_SECONDARY),
        ("Lab 4: Weather Dashboard API", "Python + Flask + External API",
         "1-1.5 hrs", "External API integration, data aggregation, caching, alerts",
         "Beginner-Intermediate", C_PURPLE),
    ]
    for i, (title, tech, duration, desc, level, clr) in enumerate(labs):
        y = Inches(1.65 + i * 1.2)
        _pill(sl, Inches(0.5), y, Inches(4), Inches(0.35), title, fill=clr)
        _pill(sl, Inches(4.7), y, Inches(1.2), Inches(0.35), duration, fill=C_LIGHT_TXT)
        _pill(sl, Inches(6.1), y, Inches(2.2), Inches(0.35), level, fill=C_WARN)
        _add_text_box(sl, Inches(0.7), y + Inches(0.4), Inches(5), Inches(0.3),
                      f"Tech: {tech}", size=9, bold=True, color=C_DARK_TEXT)
        _add_text_box(sl, Inches(0.7), y + Inches(0.65), Inches(11), Inches(0.3),
                      desc, size=10, color=C_LIGHT_TXT)

    # Lab workflow
    _add_text_box(sl, Inches(0.5), Inches(6.3), Inches(12), Inches(0.25),
                  "Every Lab Follows the Same SDD Workflow", size=12, bold=True, color=C_PRIMARY)
    flow = ["Read\nSpec", "Write\nAcceptance", "Generate\nCode (AI)", "Review &\nRefine", "Generate\nTests", "Run &\nValidate"]
    flow_clr = [C_PRIMARY, C_SECONDARY, C_ACCENT, C_PURPLE, C_WARN, C_RED]
    for i, (s, c) in enumerate(zip(flow, flow_clr)):
        _block_box(sl, Inches(0.3 + i * 2.1), Inches(6.6), Inches(1.8), Inches(0.65), s, fill=c)
        if i < 5:
            _arrow_right(sl, Inches(2.1 + i * 2.1), Inches(6.7), w=Inches(0.3))

    _footer(sl, "All labs use AI tools (Cursor, Copilot, or Claude) for code generation from the provided SDD")

    _notes(sl, """SPEAKER NOTES - Slide 20: Practical Labs Overview
------------------------------------------------------
This slide presents all available lab exercises. Participants choose based on their comfort level.

LAB SELECTION GUIDANCE:
- Java/Spring Boot experience -> Lab 1 (Task Management API)
- Python experience -> Lab 2 (Grade Calculator) or Lab 4 (Weather Dashboard)
- JavaScript/Node.js experience -> Lab 3 (E-Commerce Catalog)
- Beginners -> Start with Lab 2 (simplest setup, SQLite, no Docker needed)

EVERY LAB FOLLOWS THE SAME SDD WORKFLOW:
1. Read the specification document (provided as markdown)
2. Write/review acceptance criteria for at least one FR
3. Use AI (Cursor/Copilot/Claude) to generate code from the spec
4. Review the generated code against the spec
5. Generate tests from the acceptance criteria
6. Run tests and validate the implementation

SETUP REQUIREMENTS:
- Lab 1: Java 21, Maven, Docker (for PostgreSQL), IDE with AI assistant
- Lab 2: Python 3.12, pip, any text editor with AI assistant
- Lab 3: Node.js 20+, npm, MongoDB (or Docker), IDE with AI assistant
- Lab 4: Python 3.12, pip, API key for weather service, any editor

FACILITATION TIP: Pair participants who chose the same lab. Have them work in pairs -- one types, one reviews. Swap roles halfway through.""")
    return sl

def slide_21():
    """Lab 1: Task Management REST API"""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "Lab 1: Task Management REST API (Java/Spring Boot)", "Practical", "21")

    _add_text_box(sl, Inches(0.5), Inches(1.2), Inches(4), Inches(0.3),
                  "Project Scope", size=14, bold=True, color=C_PRIMARY)
    scope = ["6 Functional Requirements (CRUD + Categories + Comments)",
             "Role-based access (Admin vs User)",
             "Pagination, filtering, soft deletes",
             "JWT authentication, audit logging",
             "Docker Compose deployment"]
    for i, s in enumerate(scope):
        _add_text_box(sl, Inches(0.7), Inches(1.6 + i * 0.28), Inches(5), Inches(0.28),
                      f"\u2022 {s}", size=10, color=C_DARK_TEXT)

    _add_text_box(sl, Inches(0.5), Inches(3.1), Inches(4), Inches(0.3),
                  "Tech Stack", size=14, bold=True, color=C_PRIMARY)
    tech = [("Java 21", "Spring Boot 3.x"), ("PostgreSQL 16", "Spring Data JPA"),
            ("JUnit 5", "Testcontainers"), ("Docker", "GitHub Actions")]
    for i, (t1, t2) in enumerate(tech):
        _add_text_box(sl, Inches(0.7), Inches(3.5 + i * 0.25), Inches(4), Inches(0.25),
                      f"\u2022 {t1} + {t2}", size=10, color=C_DARK_TEXT)

    # Implementation phases (right side)
    _add_text_box(sl, Inches(5.5), Inches(1.2), Inches(7.5), Inches(0.3),
                  "Implementation Phases (90 min)", size=14, bold=True, color=C_PRIMARY)
    phases = [
        ("Phase 1 (20 min)", "Read spec \u2192 Generate entities + repository interfaces", C_PRIMARY),
        ("Phase 2 (25 min)", "Generate service layer with business logic + validation", C_SECONDARY),
        ("Phase 3 (20 min)", "Generate REST controllers, DTOs, error handling", C_ACCENT),
        ("Phase 4 (15 min)", "Generate unit + integration tests from acceptance criteria", C_WARN),
        ("Phase 5 (10 min)", "Docker Compose setup + CI/CD pipeline YAML", C_RED),
    ]
    for i, (phase, desc, clr) in enumerate(phases):
        _card(sl, Inches(5.5), Inches(1.6 + i * 0.85), Inches(7.3), Inches(0.75),
              phase, [desc], accent=clr)

    # API endpoints
    _add_text_box(sl, Inches(0.5), Inches(4.8), Inches(4.5), Inches(0.25),
                  "Key API Endpoints", size=12, bold=True, color=C_PRIMARY)
    endpoints = [
        "POST   /api/tasks          Create task",
        "GET    /api/tasks          List + filter + paginate",
        "GET    /api/tasks/{id}     Get task by ID",
        "PUT    /api/tasks/{id}     Update task",
        "DELETE /api/tasks/{id}     Soft delete task",
        "POST   /api/tasks/{id}/comments  Add comment",
    ]
    ep_box = _add_shape(sl, Inches(0.5), Inches(5.1), Inches(4.5), Inches(1.8),
                        fill=RGBColor(0xF8, 0xF9, 0xFA), border=C_PRIMARY, radius=True)
    tf = ep_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.15)
    tf.margin_top = Inches(0.08)
    for ep in endpoints:
        if tf.paragraphs[0].text == "":
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        r = p.add_run()
        r.text = ep
        r.font.size = Pt(8)
        r.font.name = "Consolas"
        r.font.color.rgb = C_DARK_TEXT

    _footer(sl, "Full SDD specification provided in: SDD_Task_Management_API.md")

    _notes(sl, """SPEAKER NOTES - Slide 21: Lab 1 - Task Management REST API
-----------------------------------------------------------
This is the primary lab exercise. Walk through the scope and phases.

THE SDD DOCUMENT: Participants receive the complete SDD_Task_Management_API.md file. This is their "source of truth" for the entire lab.

PHASE-BY-PHASE GUIDANCE:
Phase 1 (20 min): Entity generation
- Open the SDD, go to Section 5 (Domain Model) and Section 7 (Data Model)
- Use AI: "Generate JPA entities for Task, User, Category, Comment based on this domain model: [paste spec]"
- Review: Check data types, annotations, relationships match the spec
- Generate Spring Data repository interfaces

Phase 2 (25 min): Service layer
- Go to Section 2 (Functional Requirements)
- For each FR, generate the corresponding service method
- Key: Include acceptance criteria and edge cases in the prompt
- Review: Verify all validation rules are implemented

Phase 3 (20 min): REST controllers
- Go to Section 6 (API Contract)
- Generate controllers with proper request/response DTOs
- Verify HTTP status codes match the spec (201 for create, 200 for list, etc.)
- Check error handling matches the documented edge cases

Phase 4 (15 min): Tests
- Go back to Section 2 (acceptance criteria)
- For each criterion, generate a test method
- Use Testcontainers for integration tests with PostgreSQL

Phase 5 (10 min): Infrastructure
- Generate Docker Compose with PostgreSQL + app containers
- Generate GitHub Actions CI/CD YAML

SUCCESS CRITERIA: At the end of 90 minutes, participants should have:
1. A running Spring Boot API with at least 3 endpoints working
2. At least 5 passing unit tests
3. A Docker Compose file that starts the stack""")
    return sl

def slide_22():
    """Lab 2: Student Grade Calculator"""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "Lab 2: Student Grade Calculator (Python/FastAPI)", "Practical", "22")

    _add_text_box(sl, Inches(0.5), Inches(1.2), Inches(5.5), Inches(0.3),
                  "Project Scope", size=14, bold=True, color=C_PRIMARY)
    scope = ["6 FRs: Students, Scores, Grades, GPA, Reports, Bulk Import",
             "Business logic focus: grade thresholds, GPA calculation",
             "Statistical reports: per-subject averages, min/max",
             "Zero Docker dependency (SQLite built-in)",
             "Automatic OpenAPI docs via FastAPI"]
    for i, s in enumerate(scope):
        _add_text_box(sl, Inches(0.7), Inches(1.6 + i * 0.28), Inches(6), Inches(0.28),
                      f"\u2022 {s}", size=10, color=C_DARK_TEXT)

    _add_text_box(sl, Inches(6.5), Inches(1.2), Inches(6.5), Inches(0.3),
                  "Grade Thresholds (from spec)", size=14, bold=True, color=C_PRIMARY)
    grades_data = [
        ("A", "90-100", "4.0", C_ACCENT),
        ("B", "80-89", "3.0", C_PRIMARY),
        ("C", "70-79", "2.0", C_SECONDARY),
        ("D", "60-69", "1.0", C_WARN),
        ("F", "0-59", "0.0", C_RED),
    ]
    for i, (grade, score_range, gpa, clr) in enumerate(grades_data):
        _pill(sl, Inches(6.5 + i * 1.3), Inches(1.6), Inches(1.1), Inches(0.8),
              f"{grade}\n{score_range}\nGPA: {gpa}", fill=clr, size=9)

    # Implementation phases
    _add_text_box(sl, Inches(0.5), Inches(3.2), Inches(12), Inches(0.3),
                  "Implementation Phases (60 min)", size=14, bold=True, color=C_PRIMARY)
    phases = [
        ("Phase 1 (15 min)", "Models + DB schema: Student, Score entities with SQLAlchemy", C_PRIMARY),
        ("Phase 2 (20 min)", "Core business logic: grade calculation, GPA computation", C_ACCENT),
        ("Phase 3 (15 min)", "REST endpoints: CRUD + reports + bulk operations", C_SECONDARY),
        ("Phase 4 (10 min)", "Tests: pytest for each FR's acceptance criteria + edge cases", C_WARN),
    ]
    for i, (phase, desc, clr) in enumerate(phases):
        _card(sl, Inches(0.5 + i * 3.1), Inches(3.6), Inches(2.9), Inches(0.85),
              phase, [desc], accent=clr)

    # Key endpoints and test example
    _add_text_box(sl, Inches(0.5), Inches(4.8), Inches(5.5), Inches(0.25),
                  "Key Endpoints", size=12, bold=True, color=C_PRIMARY)
    endpoints = [
        "POST /students           Register student",
        "POST /students/{id}/scores   Record score",
        "GET  /students/{id}/report   GPA + all grades",
        "GET  /reports/class          Class statistics",
    ]
    for i, ep in enumerate(endpoints):
        _add_text_box(sl, Inches(0.7), Inches(5.1 + i * 0.25), Inches(5), Inches(0.25),
                      ep, size=9, color=C_DARK_TEXT)

    _add_text_box(sl, Inches(6.5), Inches(4.8), Inches(6.5), Inches(0.25),
                  "Why This Lab Works for AI-Native", size=12, bold=True, color=C_ACCENT)
    reasons = [
        "Clear business rules \u2192 AI generates precise logic",
        "Boundary conditions in spec \u2192 complete edge case tests",
        "Simple stack (no Docker) \u2192 focus on methodology, not setup",
        "Testable outputs \u2192 immediate validation of AI-generated code",
    ]
    for i, r in enumerate(reasons):
        _add_text_box(sl, Inches(6.7), Inches(5.1 + i * 0.28), Inches(6), Inches(0.28),
                      f"\u2713 {r}", size=10, color=C_DARK_TEXT)

    _footer(sl, "Full SDD specification provided in: SDD_Student_Grade_Calculator.md")

    _notes(sl, """SPEAKER NOTES - Slide 22: Lab 2 - Student Grade Calculator
-----------------------------------------------------------
This is the simpler, faster lab. Ideal for participants who prefer Python or want a quicker exercise.

WHY THIS LAB IS EFFECTIVE:
1. Clear business rules: Grade thresholds are unambiguous. AI can implement them precisely from the spec.
2. Boundary testing: Score of 89 -> B, Score of 90 -> A. These boundaries are perfect for AI-generated tests.
3. Zero setup friction: SQLite requires no installation. pip install fastapi sqlalchemy uvicorn and you're coding.
4. Testable: Every FR has a deterministic, verifiable output.

THE GPA CALCULATION (core business logic from the spec):
GPA = sum(grade_points) / count(subjects)
Where grade_points are: A=4.0, B=3.0, C=2.0, D=1.0, F=0.0

This is exactly the kind of well-defined logic that AI generates perfectly when given a clear spec.

DISCUSSION: Compare the two labs:
- Lab 1 (Task Management): Complex architecture, multiple entities, auth, Docker -- teaches system design
- Lab 2 (Grade Calculator): Simple architecture, rich business logic, thorough testing -- teaches spec-driven TDD

Both demonstrate the same SDD methodology but emphasize different skills.""")
    return sl

def slide_23():
    """Labs 3 & 4 + Additional Projects"""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "Additional Practical Projects", "Practical", "23")

    # Lab 3
    _add_text_box(sl, Inches(0.5), Inches(1.2), Inches(6), Inches(0.3),
                  "Lab 3: E-Commerce Product Catalog API", size=14, bold=True, color=C_SECONDARY)
    _add_text_box(sl, Inches(0.7), Inches(1.55), Inches(5.5), Inches(0.25),
                  "Node.js + Express + MongoDB  |  1.5-2 hrs  |  Intermediate", size=10, bold=True, color=C_SECONDARY)
    lab3 = [
        "Product CRUD with categories, tags, and image URLs",
        "Full-text search across product name and description",
        "Inventory tracking with stock level alerts",
        "Price history and discount calculations",
        "Pagination with cursor-based navigation",
        "MongoDB aggregation pipelines for analytics",
    ]
    for i, item in enumerate(lab3):
        _add_text_box(sl, Inches(0.7), Inches(1.85 + i * 0.25), Inches(5.5), Inches(0.25),
                      f"\u2022 {item}", size=9, color=C_DARK_TEXT)

    # Lab 4
    _add_text_box(sl, Inches(7.0), Inches(1.2), Inches(6), Inches(0.3),
                  "Lab 4: Weather Dashboard Microservice", size=14, bold=True, color=C_PURPLE)
    _add_text_box(sl, Inches(7.2), Inches(1.55), Inches(5.5), Inches(0.25),
                  "Python + Flask + External API  |  1-1.5 hrs  |  Beginner", size=10, bold=True, color=C_PURPLE)
    lab4 = [
        "External weather API integration (OpenWeatherMap)",
        "Data aggregation: current, hourly, daily forecasts",
        "In-memory caching with TTL (avoid API rate limits)",
        "Temperature unit conversion (C/F/K)",
        "Severe weather alerts with threshold configuration",
        "Response caching and error handling for API failures",
    ]
    for i, item in enumerate(lab4):
        _add_text_box(sl, Inches(7.2), Inches(1.85 + i * 0.25), Inches(5.5), Inches(0.25),
                      f"\u2022 {item}", size=9, color=C_DARK_TEXT)

    # SDD methodology highlight
    _add_text_box(sl, Inches(0.5), Inches(3.8), Inches(12), Inches(0.3),
                  "All Projects Follow the Same SDD Methodology", size=14, bold=True, color=C_PRIMARY)

    method_steps = [
        ("Step 1", "Read the SDD specification document", C_PRIMARY),
        ("Step 2", "Identify FRs, acceptance criteria, edge cases", C_SECONDARY),
        ("Step 3", "Use AI to generate code from spec sections", C_ACCENT),
        ("Step 4", "Review generated code against the spec", C_PURPLE),
        ("Step 5", "Generate tests from acceptance criteria", C_WARN),
        ("Step 6", "Run, validate, iterate", C_RED),
    ]
    for i, (step, desc, clr) in enumerate(method_steps):
        col = i % 3
        row = i // 3
        _card(sl, Inches(0.5 + col * 4.1), Inches(4.2 + row * 0.7), Inches(3.8), Inches(0.6),
              step, [desc], accent=clr)

    # Project comparison matrix
    _add_text_box(sl, Inches(0.5), Inches(5.8), Inches(12), Inches(0.3),
                  "Project Selection Guide", size=14, bold=True, color=C_PRIMARY)
    guide = [
        ("Strong business logic focus?", "\u2192 Lab 2 (Grade Calculator)"),
        ("Full enterprise API experience?", "\u2192 Lab 1 (Task Management)"),
        ("NoSQL & search experience?", "\u2192 Lab 3 (E-Commerce)"),
        ("External API integration?", "\u2192 Lab 4 (Weather Dashboard)"),
    ]
    for i, (question, answer) in enumerate(guide):
        _add_text_box(sl, Inches(0.7 + (i % 2) * 6.3), Inches(6.15 + (i // 2) * 0.3), Inches(3), Inches(0.25),
                      question, size=9, bold=True, color=C_DARK_TEXT)
        _add_text_box(sl, Inches(3.5 + (i % 2) * 6.3), Inches(6.15 + (i // 2) * 0.3), Inches(3), Inches(0.25),
                      answer, size=9, color=C_PRIMARY)

    _footer(sl, "SDD specifications for Labs 3 & 4 will be provided as separate markdown documents")

    _notes(sl, """SPEAKER NOTES - Slide 23: Additional Practical Projects
--------------------------------------------------------------
These additional labs provide variety for different skill levels and interests.

LAB 3: E-COMMERCE PRODUCT CATALOG
Why Node.js/Express/MongoDB:
- Different tech stack from Labs 1 & 2 (Java, Python)
- MongoDB introduces NoSQL concepts
- Full-text search with MongoDB text indexes
- Aggregation pipelines for analytics (popular products, category stats)
Key learning: How SDD works across different tech stacks

LAB 4: WEATHER DASHBOARD
Why Flask + External API:
- Teaches API integration patterns (calling external services)
- Caching strategies (TTL-based, avoid rate limits)
- Error handling for unreliable external services
- Simpler architecture for beginners
Key learning: AI generates both internal logic AND external integration code from specs

METHODOLOGY CONSISTENCY:
The key insight is that ALL four labs follow the SAME SDD methodology. The tech stack changes, but the process is identical:
1. Read spec
2. Identify requirements
3. Generate code from spec
4. Review against spec
5. Generate tests from criteria
6. Validate

This consistency reinforces the methodology itself, independent of any specific technology.""")
    return sl

def slide_24():
    """Key Takeaways & Next Steps"""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "Key Takeaways & Next Steps", "Closing", "24")

    _add_text_box(sl, Inches(0.5), Inches(1.2), Inches(12), Inches(0.3),
                  "What We Covered Today", size=16, bold=True, color=C_PRIMARY)

    takeaways = [
        ("AI-Native is a Paradigm Shift", "Not just 'use AI to code' \u2014 it's a fundamental change in how software is conceived, specified, built, and validated.", C_PRIMARY),
        ("Specifications are the Source of Truth", "In AI-native development, the spec drives everything: code, tests, docs, and deployment.", C_SECONDARY),
        ("AI is an Amplifier, Not a Replacement", "Developers become architects, spec writers, and reviewers. AI handles the translation to code.", C_ACCENT),
        ("Quality Gates are Non-Negotiable", "Automated testing, security scanning, and code review MUST be in every pipeline.", C_RED),
        ("Governance Makes AI Safe", "Transparency, accountability, and human oversight ensure responsible AI-native development.", C_PURPLE),
    ]
    for i, (title, desc, clr) in enumerate(takeaways):
        _card(sl, Inches(0.5), Inches(1.6 + i * 0.9), Inches(12.3), Inches(0.8),
              title, [desc], accent=clr)

    # Next steps
    _add_text_box(sl, Inches(0.5), Inches(6.3), Inches(12), Inches(0.3),
                  "Next Steps for Faculty", size=14, bold=True, color=C_PRIMARY)
    steps = [
        "Complete the practical lab exercise you started today",
        "Explore AI tools (Cursor, Copilot, Claude) for your own projects",
        "Apply spec-driven practices when designing assignments",
        "Begin planning the 1-month faculty project (next slide)",
        "Share learnings with colleagues and students",
    ]
    for i, step in enumerate(steps):
        _add_text_box(sl, Inches(0.5 + (i % 3) * 4.1), Inches(6.6 + (i // 3) * 0.25), Inches(4), Inches(0.25),
                      f"\u2192 {step}", size=9, color=C_DARK_TEXT)

    _footer(sl, "Thank you! \u2014 Questions, discussion, and feedback welcome")

    _notes(sl, """SPEAKER NOTES - Slide 24: Key Takeaways
----------------------------------------------
Summarize the workshop with these five key messages. Ask participants to reflect on which resonated most.

1. PARADIGM SHIFT: This is the most important message. AI-native isn't a tool upgrade -- it's a methodology change. The analogy: automated testing didn't just add a tool; it changed how we think about quality.

2. SPECS AS SOURCE OF TRUTH: If participants remember one thing, it should be this. The spec drives everything. Invest in spec quality, and code quality follows.

3. AI AS AMPLIFIER: Address the "will AI replace programmers?" fear directly. No. It amplifies them. Like power tools amplify carpenters -- the skill and judgment still matter, but the output scales dramatically.

4. QUALITY GATES: AI generates fast, but quality comes from discipline. Automated testing, security scanning, and review gates are MORE important in AI-native because code is generated faster.

5. GOVERNANCE: Responsible AI use isn't optional. Students need to learn about IP, ethics, transparency, and accountability alongside the technical skills.

NEXT STEPS: Make these concrete and actionable. Each participant should leave with at least one commitment.

FEEDBACK: Ask for:
- What worked well?
- What would you change?
- What support do you need to implement this in your curriculum?""")
    return sl

def slide_25():
    """1-Month Faculty Project Assignments"""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    _title_bar(sl, "1-Month Faculty Project Assignments", "Closing", "25")

    _add_text_box(sl, Inches(0.5), Inches(1.1), Inches(12), Inches(0.3),
                  "Teams of 2-3  |  4 Weeks  |  Interim Milestones  |  AI-Native SDD Methodology", size=12, bold=True, color=C_PRIMARY)

    # Project A
    _add_text_box(sl, Inches(0.5), Inches(1.5), Inches(6), Inches(0.3),
                  "Project A: University Course Registration System", size=13, bold=True, color=C_PRIMARY)
    proj_a = [
        "Multi-module: Student Service, Course Catalog,",
        "  Registration Engine, Notification Service",
        "Microservices architecture with API Gateway",
        "Concurrent enrollment handling (race conditions)",
        "Prerequisite validation, waitlist management",
        "Admin dashboard with real-time statistics",
    ]
    for i, item in enumerate(proj_a):
        _add_text_box(sl, Inches(0.7), Inches(1.85 + i * 0.22), Inches(5.5), Inches(0.22),
                      f"\u2022 {item}" if not item.startswith("  ") else f"  {item}", size=9, color=C_DARK_TEXT)

    # Project A milestones
    milestones_a = [
        ("Week 1", "SDD spec writing for all modules\nAPI contracts + domain model", C_PRIMARY),
        ("Week 2", "Core services: Student + Course\nCRUD + basic validation", C_SECONDARY),
        ("Week 3", "Registration engine + concurrency\nIntegration tests", C_ACCENT),
        ("Week 4", "CI/CD pipeline + deployment\nLoad testing + documentation", C_WARN),
    ]
    for i, (week, desc, clr) in enumerate(milestones_a):
        _card(sl, Inches(0.5 + i * 1.5), Inches(3.3), Inches(1.35), Inches(1.1),
              week, desc.split('\n'), accent=clr)

    # Project B
    _add_text_box(sl, Inches(6.8), Inches(1.5), Inches(6.2), Inches(0.3),
                  "Project B: Smart Library Management System", size=13, bold=True, color=C_SECONDARY)
    proj_b = [
        "Book catalog with ISBN lookup + cover images",
        "Member management with borrowing limits",
        "Borrowing/returns with due date + fine calculation",
        "Search with full-text + filter by genre/author/year",
        "Recommendation engine (collaborative filtering)",
        "Analytics dashboard: popular books, active members",
    ]
    for i, item in enumerate(proj_b):
        _add_text_box(sl, Inches(7.0), Inches(1.85 + i * 0.22), Inches(5.8), Inches(0.22),
                      f"\u2022 {item}", size=9, color=C_DARK_TEXT)

    # Project B milestones
    milestones_b = [
        ("Week 1", "SDD specs + domain model\nAPI contracts + DB schema", C_PRIMARY),
        ("Week 2", "Book catalog + member CRUD\nSearch implementation", C_SECONDARY),
        ("Week 3", "Borrowing engine + fines\nRecommendation algorithm", C_ACCENT),
        ("Week 4", "CI/CD + deployment\nPerformance testing + docs", C_WARN),
    ]
    for i, (week, desc, clr) in enumerate(milestones_b):
        _card(sl, Inches(6.8 + i * 1.5), Inches(3.3), Inches(1.35), Inches(1.1),
              week, desc.split('\n'), accent=clr)

    # Deliverables
    _add_text_box(sl, Inches(0.5), Inches(4.7), Inches(12), Inches(0.3),
                  "Required Deliverables (Both Projects)", size=14, bold=True, color=C_PRIMARY)
    deliverables = [
        ("Week 1", "Complete SDD document (FRs, NFRs, API contracts, data model, test strategy)"),
        ("Week 2", "Working core API with unit tests (min 80% coverage for core modules)"),
        ("Week 3", "Integration tests + security scan report + code review evidence"),
        ("Week 4", "Deployed system + CI/CD pipeline + load test results + final presentation"),
    ]
    for i, (week, desc) in enumerate(deliverables):
        y = Inches(5.05 + i * 0.35)
        _pill(sl, Inches(0.5), y, Inches(1.0), Inches(0.3), week, fill=C_PRIMARY, size=9)
        _add_text_box(sl, Inches(1.6), y, Inches(11), Inches(0.3), desc, size=10, color=C_DARK_TEXT)

    # Evaluation criteria
    _add_text_box(sl, Inches(0.5), Inches(6.55), Inches(12), Inches(0.25),
                  "Evaluation: SDD Quality (25%) + Code Quality (25%) + Test Coverage (20%) + CI/CD (15%) + Documentation (15%)",
                  size=10, bold=True, color=C_PRIMARY)

    _footer(sl, "Full project specifications will be provided as detailed SDD markdown documents")

    _notes(sl, """SPEAKER NOTES - Slide 25: 1-Month Faculty Project Assignments
----------------------------------------------------------------------
These are the capstone projects that faculty teams will work on over 4 weeks.

PROJECT A: UNIVERSITY COURSE REGISTRATION SYSTEM
Why this project:
- Familiar domain for CS faculty -- they understand the requirements intuitively
- Multi-module architecture teaches microservice decomposition
- Concurrent enrollment creates real engineering challenges (race conditions, distributed transactions)
- Prerequisite validation is complex business logic
- Real-world applicability -- could potentially be used at their institution

Key challenges for AI-native approach:
- Writing specs for concurrent operations is hard -- teaches precision in specification
- Integration testing across services requires careful contract definition
- The waitlist system has complex state transitions that must be fully specified

PROJECT B: SMART LIBRARY MANAGEMENT SYSTEM
Why this project:
- Rich domain with clear business rules (borrowing limits, due dates, fines)
- Recommendation engine introduces basic ML/AI concepts
- Full-text search teaches indexing and query optimization
- Analytics dashboard combines backend with data visualization

Key challenges for AI-native approach:
- Fine calculation has many edge cases (weekends, holidays, grace periods)
- Recommendation algorithm needs clear spec for collaborative filtering logic
- Search ranking requires specification of relevance scoring

WEEKLY MILESTONES:
Emphasize that Week 1 (spec writing) is THE most important week. A poor spec leads to 3 weeks of struggling. A great spec leads to smooth AI-assisted development.

Each milestone has concrete deliverables:
- Week 1: The SDD document IS the deliverable. Review it as a team.
- Week 2: Working endpoints with passing tests. Demo to the group.
- Week 3: Integration tests passing, security scan clean. Show the pipeline.
- Week 4: Full system deployed, load tested, documented. Final presentation.

EVALUATION BREAKDOWN:
- SDD Quality (25%): Is the spec complete, precise, testable?
- Code Quality (25%): Clean architecture, proper error handling, security
- Test Coverage (20%): Unit + integration + edge cases
- CI/CD (15%): Automated pipeline with quality gates
- Documentation (15%): API docs, deployment guide, architecture decisions""")
    return sl

# ═══════════════════════════════════════════════════════════
#  BACKUP SLIDES
# ═══════════════════════════════════════════════════════════
def backup_slide(title, section_label, slide_num, content_lines):
    """Generic backup slide builder."""
    sl = prs.slides.add_slide(BLANK_LAYOUT)
    bar = _add_shape(sl, Inches(0), Inches(0), SLIDE_W, Inches(0.85),
                     fill=RGBColor(0x95, 0xA5, 0xA6))  # Gray for backup
    _set_text(bar, f"BACKUP: {title}", size=22, bold=True, color=C_WHITE, align=PP_ALIGN.LEFT)
    bar.text_frame.margin_left = Inches(0.5)
    bar.text_frame.margin_top = Inches(0.15)
    tag = _add_shape(sl, Inches(0.3), Inches(0.95), Inches(3.5), Inches(0.35),
                     fill=C_LIGHT_BG, border=RGBColor(0x95,0xA5,0xA6), radius=True)
    _set_text(tag, f"AI-Native Software Development  |  {section_label}", size=9,
              color=RGBColor(0x95,0xA5,0xA6), align=PP_ALIGN.CENTER)
    _add_text_box(sl, Inches(12.5), Inches(7.1), Inches(0.6), Inches(0.3),
                  slide_num, size=10, color=C_LIGHT_TXT, align=PP_ALIGN.RIGHT)
    for i, line in enumerate(content_lines):
        _add_text_box(sl, Inches(0.7), Inches(1.5 + i * 0.35), Inches(11), Inches(0.3),
                      f"\u2022 {line}", size=12, color=C_DARK_TEXT)
    _footer(sl, "Backup Reference Material")
    return sl

# ═══════════════════════════════════════════════════════════
#  BUILD ALL SLIDES
# ═══════════════════════════════════════════════════════════
print("Building slides...")
slide_01()
print("  Slide 1: Title")
slide_02()
print("  Slide 2: Agenda")
slide_03()
print("  Slide 3: Why AI-Native Matters")
slide_04()
print("  Slide 4: What is AI-Native")
slide_05()
print("  Slide 5: Traditional vs AI-Native")
slide_06()
print("  Slide 6: SDLC Lifecycle")
slide_07()
print("  Slide 7: Tool Ecosystem")
slide_08()
print("  Slide 8: LLM Capabilities")
slide_09()
print("  Slide 9: SDD Methodology")
slide_10()
print("  Slide 10: Writing Specs")
slide_11()
print("  Slide 11: Architecture")
slide_12()
print("  Slide 12: Code Generation")
slide_13()
print("  Slide 13: Code Review & Security")
slide_14()
print("  Slide 14: Testing Strategy")
slide_15()
print("  Slide 15: CI/CD Pipeline")
slide_16()
print("  Slide 16: Performance Testing")
slide_17()
print("  Slide 17: Multi-Agent")
slide_18()
print("  Slide 18: AI Governance")
slide_19()
print("  Slide 19: Adoption Roadmap")
slide_20()
print("  Slide 20: Labs Overview")
slide_21()
print("  Slide 21: Lab 1")
slide_22()
print("  Slide 22: Lab 2")
slide_23()
print("  Slide 23: Labs 3 & 4")
slide_24()
print("  Slide 24: Key Takeaways")
slide_25()
print("  Slide 25: 1-Month Project")

# Backup slides
print("Building backup slides...")
backup_topics = [
    ("Prompt Engineering Templates", "Backup", "26",
     ["Requirements gathering prompt: assign ROLE, provide CONTEXT, specify OUTPUT format",
      "Code generation prompt: include spec section, language, patterns, constraints",
      "Test generation prompt: reference acceptance criteria, edge cases, mocking strategy",
      "Code review prompt: include checklist, security focus areas, quality standards",
      "Architecture prompt: describe constraints, scale requirements, technology preferences",
      "Tips: assign a ROLE, provide CONTEXT, be SPECIFIC, include EXAMPLES, ITERATE on results"]),
    ("Kubernetes Deployment Architecture", "Backup", "27",
     ["Pods: smallest deployable unit \u2014 one or more containers sharing network and storage",
      "Services: stable network endpoint \u2014 load-balances across pods, enables discovery",
      "Deployments: declarative updates \u2014 rolling upgrades with zero-downtime, auto-rollback",
      "ConfigMaps & Secrets: externalized configuration, encrypted sensitive data",
      "Ingress: external traffic routing with TLS termination and path-based routing",
      "HPA (Horizontal Pod Autoscaler): auto-scale based on CPU/memory/custom metrics"]),
    ("Observability with OpenTelemetry", "Backup", "28",
     ["Three pillars: Traces (request flow), Metrics (system health), Logs (event details)",
      "OpenTelemetry Collector: vendor-neutral pipeline for collecting and exporting telemetry",
      "Prometheus: time-series database for metrics storage, PromQL for querying",
      "Jaeger/Zipkin: distributed tracing visualization and dependency analysis",
      "Grafana: unified dashboards combining metrics, traces, and logs",
      "Key metrics: request latency (P50/P95/P99), error rate, throughput, saturation"]),
    ("Load Testing with k6", "Backup", "29",
     ["k6: modern load testing tool, JavaScript-based test scripts",
      "Ramp-up pattern: gradually increase virtual users (VUs) to find breaking point",
      "Thresholds: define pass/fail criteria (P95 < 500ms, error rate < 1%)",
      "Scenarios: model realistic user behavior patterns (browse, search, checkout)",
      "Integration with CI/CD: run load tests as pipeline stages, fail build on threshold breach",
      "When to test: before production, after major changes, before expected traffic spikes"]),
    ("End-to-End Testing with Playwright", "Backup", "30",
     ["Playwright: cross-browser testing (Chromium, Firefox, WebKit) with single API",
      "Auto-waiting: built-in waiting for elements, no manual sleep/delay needed",
      "Network interception: mock API responses for deterministic testing",
      "Visual regression: screenshot comparison to detect UI changes",
      "Code generation: Playwright Inspector records user actions as test code",
      "AI can generate Playwright tests from user story descriptions"]),
    ("Git Workflow for AI-Native Development", "Backup", "31",
     ["Feature branches: one branch per FR or spec section",
      "Commit messages: reference spec FR IDs (e.g., 'Implement FR-1: Create Task endpoint')",
      "PR reviews: AI-assisted first pass + human review for architecture and security",
      "Branch protection: require passing CI/CD checks before merge",
      "Conventional commits: feat(task): add create endpoint, test(task): add FR-1 tests",
      "AI generates commit messages from code diffs and spec context"]),
    ("Error Handling Patterns", "Backup", "32",
     ["Global exception handler: @ControllerAdvice / @app.exception_handler for consistent responses",
      "Problem Details (RFC 7807): standardized error response format with type, title, detail, status",
      "Validation errors: return field-level error details (field name, rejected value, message)",
      "Business rule violations: custom exception classes mapped to appropriate HTTP status codes",
      "External service failures: circuit breaker pattern (Resilience4j / tenacity) with fallback",
      "Logging: structured logging (JSON) with correlation IDs for distributed tracing"]),
    ("Data Model Design Patterns", "Backup", "33",
     ["Normalization to 3NF to reduce redundancy; each fact stored once",
      "UUID primary keys for globally unique identifiers (better for distributed systems)",
      "Audit fields: created_at, updated_at, created_by on every table",
      "Soft deletes: deleted_at timestamp instead of permanent removal",
      "Database migrations: Flyway or Alembic for versioned schema changes",
      "Index strategy: index FK columns, filter columns (status, priority), unique constraints"]),
    ("Testing Hierarchy Deep Dive", "Backup", "34",
     ["Unit tests: test single function/method in isolation, mock all dependencies",
      "Integration tests: test component interactions (API + DB), use Testcontainers",
      "Contract tests: verify API responses match OpenAPI spec (Pact, Spring Cloud Contract)",
      "E2E tests: test complete user flows through the running application",
      "Performance tests: verify NFRs (latency, throughput) under realistic load",
      "Security tests: SAST (SonarQube), DAST (OWASP ZAP), dependency scan (Snyk)"]),
    ("Emerging Trends in AI Development", "Backup", "35",
     ["Autonomous AI Engineers: Devin, SWE-Agent -- AI that plans, codes, tests, deploys independently",
      "AI-Generated UI: v0.dev, Vercel AI -- generate React/Vue components from descriptions",
      "Specification languages: Formal spec languages optimized for AI consumption emerging",
      "AI-Powered Debugging: AI analyzes stack traces, suggests fixes, writes regression tests",
      "Continuous AI Integration: AI agents as permanent CI/CD pipeline participants",
      "Model Context Protocol (MCP): standardized protocol for AI agents to access tools and data"]),
]

for title, section, num, lines in backup_topics:
    backup_slide(title, section, num, lines)
    print(f"  Backup Slide {num}: {title}")

# ── Save ────────────────────────────────────────────────────
output_path = "/home/gurukraj/github/faculty-program/AI_Native_SDD_Workshop_Condensed.pptx"
prs.save(output_path)
print(f"\nPresentation saved to: {output_path}")
print(f"Total slides: {len(prs.slides)} (25 main + {len(prs.slides) - 25} backup)")
