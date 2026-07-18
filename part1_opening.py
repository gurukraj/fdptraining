"""Part 1 – Opening & Foundations (Slides 1-6)"""
from slide_helpers import *

def build(prs, start_num=1):
    n = start_num

    # ── Slide 1: TITLE SLIDE ──────────────────────────────────────────
    slide = add_slide(prs, bg_color=LIGHT_BLUE)
    # Top accent band
    band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_W, Inches(1.6))
    band.fill.solid(); band.fill.fore_color.rgb = TITLE_BAR; band.line.fill.background()
    add_textbox(slide, 0.6, 0.25, 12, 0.7,
                "AI-Native Software Development", 38, True, WHITE, PP_ALIGN.LEFT)
    add_textbox(slide, 0.6, 0.9, 12, 0.5,
                "Theory, Methodology & Hands-On Practical Sessions", 22, False, RGBColor(0xDD,0xEB,0xF7), PP_ALIGN.LEFT)

    add_textbox(slide, 0.6, 2.0, 8, 0.5,
                "Faculty Development Program  |  4-5 Hour Interactive Workshop", 18, False, TEXT_DARK)
    add_textbox(slide, 0.6, 2.6, 10, 0.8,
                "From foundational concepts to advanced AI-native engineering\nIncludes guided practical labs, spec-driven development & multi-agent workflows",
                14, False, TEXT_MID)

    # AI-Native lifecycle flow diagram
    stages = ["Human\nIntent", "Executable\nSpecification", "AI-Assisted\nDesign", "Code\nGeneration",
              "Automated\nTesting", "CI/CD\nPipeline", "Continuous\nFeedback"]
    colors = [ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE, ACCENT_PURPLE,
              ACCENT_GREEN, ACCENT_ORANGE, ACCENT_TEAL]
    x_start = 0.6
    for i, (label, clr) in enumerate(zip(stages, colors)):
        add_rounded_box(slide, x_start + i * 1.75, 3.8, 1.5, 0.85,
                        label, fill_color=clr, text_color=WHITE, font_size=11, bold=True)
        if i < len(stages) - 1:
            add_arrow_right(slide, x_start + i * 1.75 + 1.52, 4.05, 0.2, 0.01, color=TEXT_MID)

    # Tagline box
    add_rounded_box(slide, 1.5, 5.1, 10.3, 0.55,
                    "AI-Native = Human Intent  +  Executable Specification  +  Automated Feedback Loops",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=14, bold=True,
                    border_color=ACCENT_ORANGE)

    # Footer
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.4), Inches(6.85), Inches(4.5), Inches(0.38))
    pill.fill.solid(); pill.fill.fore_color.rgb = ACCENT_BLUE; pill.line.fill.background()
    ptf = pill.text_frame; ptf.margin_left = Inches(0.15); ptf.margin_top = Inches(0.02)
    pr = ptf.paragraphs[0].add_run()
    pr.text = "AI-Native Software Development  |  Opening"; pr.font.size = Pt(10); pr.font.color.rgb = WHITE; pr.font.name = "Calibri"
    add_textbox(slide, 12.4, 6.85, 0.7, 0.35, str(n), font_size=11, bold=True, color=TEXT_MID, alignment=PP_ALIGN.RIGHT)

    add_notes(slide, """SPEAKER NOTES – Slide 1: Title & Welcome
-----------------------------------------
Welcome the faculty participants and introduce yourself. Set the tone: this is NOT a passive lecture — it is an interactive, hands-on workshop where participants will build a real application using AI-native practices.

Key talking points:
1. Explain what "AI-Native" means: AI is embedded across the ENTIRE software development lifecycle — from requirements capture, through architecture, code generation, testing, security, CI/CD, and continuous feedback — not bolted on as an afterthought.
2. Walk through the lifecycle flow on screen: Human Intent -> Specification -> Design -> Code -> Tests -> CI/CD -> Feedback. Emphasize that each stage has AI augmentation but human oversight remains critical.
3. Mention the workshop structure: ~2 hours of concepts and methodology, ~2-3 hours of guided implementation lab.
4. Set expectations: By end of session, participants will have hands-on experience with spec-driven development, AI-assisted code generation, automated testing, and CI/CD pipeline setup.
5. Highlight the tagline: AI-Native = Human Intent + Executable Specification + Automated Feedback Loops. This is the foundational equation they should remember.

Audience engagement: Ask how many have used AI coding assistants (GitHub Copilot, Cursor, ChatGPT for code). This gauges the room's baseline.""")
    n += 1

    # ── Slide 2: WORKSHOP OUTCOMES ─────────────────────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "Workshop Learning Outcomes", "Opening", n)

    outcomes = [
        ("Understand AI-Native SDLC", [
            "Grasp how AI transforms every phase of software development",
            "Distinguish AI-native from AI-assisted approaches"
        ]),
        ("Apply Spec-Driven Development", [
            "Write structured specifications BEFORE generating code",
            "Use AI to refine requirements, resolve ambiguity"
        ]),
        ("Build & Test an Application End-to-End", [
            "Design, implement, test, secure, and deploy a working system",
            "Experience the full AI-native workflow hands-on"
        ]),
        ("Evaluate Governance & Security", [
            "Apply responsible AI principles to software engineering",
            "Implement security reviews and quality gates"
        ]),
        ("Explore Multi-Agent Development", [
            "Understand orchestrated AI agent roles in SDLC",
            "See how specialized agents collaborate on complex tasks"
        ]),
    ]
    add_bullet_list(slide, 0.6, 1.3, 6.5, 5.2, outcomes, font_size=15)

    # Right side: visual cards
    card_data = [
        ("Teaching Approach", "Explain -> Demonstrate ->\nValidate -> Reflect", LIGHT_GREEN, ACCENT_GREEN),
        ("Practical Lab", "Task Management REST API\nSpec -> Code -> Test -> Deploy", LIGHT_ORANGE, ACCENT_ORANGE),
        ("Deliverables", "Spec | API | Code | Tests |\nCI/CD Pipeline", LIGHT_PURPLE, ACCENT_PURPLE),
    ]
    for i, (title, desc, bg, border) in enumerate(card_data):
        y = 1.5 + i * 1.7
        add_rounded_box(slide, 7.8, y, 5.0, 1.35, f"{title}\n{desc}",
                        fill_color=bg, text_color=TEXT_DARK, font_size=13, bold=True,
                        border_color=border)

    add_notes(slide, """SPEAKER NOTES – Slide 2: Workshop Learning Outcomes
-----------------------------------------------------
Walk through each learning outcome and explain WHY it matters:

1. UNDERSTAND AI-NATIVE SDLC: This is not about using ChatGPT to write code snippets. AI-native means AI is woven into requirements gathering, architecture decisions, code generation, testing strategy, security analysis, CI/CD automation, and continuous improvement. Ask: "How many of you currently use AI only for code completion? By the end of today, you'll see AI participating in every single phase."

2. APPLY SPEC-DRIVEN DEVELOPMENT: The #1 mistake teams make with AI is jumping straight to code generation. Spec-driven development means you write clear, structured specifications first — functional requirements, non-functional requirements, API contracts, acceptance criteria — and THEN use AI to generate implementation. This dramatically improves output quality.

3. BUILD & TEST END-TO-END: Theory alone won't stick. Participants will build a Task Management REST API from scratch using AI-native practices. They'll experience the full cycle: requirement spec -> architecture design -> code generation -> unit tests -> integration tests -> CI/CD pipeline.

4. EVALUATE GOVERNANCE & SECURITY: AI-generated code introduces unique risks — hallucinated dependencies, insecure defaults, data exposure in prompts. We'll cover governance frameworks, responsible AI principles, and practical security checklists.

5. EXPLORE MULTI-AGENT DEVELOPMENT: The cutting edge of AI-native development uses multiple specialized AI agents (Requirements Agent, Architect Agent, Coder, Tester, Security, DevOps) orchestrated together. We'll explore this emerging paradigm.

Point out the three cards on the right:
- Teaching approach follows a structured cycle
- The practical lab is a real, implementable example
- Participants will produce concrete, reviewable artifacts""")
    n += 1

    # ── Slide 3: SESSION AGENDA / TIMELINE ─────────────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "4-5 Hour Session Agenda", "Opening", n)

    # Timeline visual
    phases = [
        ("Part 1: Foundations\n& Methodology", "~90 min", ACCENT_BLUE, LIGHT_BLUE,
         "AI-Native concepts\nSpec-driven development\nTools & prompt engineering\nArchitecture design"),
        ("Break", "15 min", TEXT_MID, WHITE, ""),
        ("Part 2: Guided\nHands-On Lab", "~120 min", ACCENT_GREEN, LIGHT_GREEN,
         "Spec writing exercise\nCode generation & review\nTesting & validation\nCI/CD pipeline setup"),
        ("Break", "15 min", TEXT_MID, WHITE, ""),
        ("Part 3: Advanced\nTopics & Wrap-up", "~60 min", ACCENT_PURPLE, LIGHT_PURPLE,
         "Multi-agent development\nAI governance & security\nHomework & discussion\nKey takeaways"),
    ]
    x = 0.5
    for i, (title, dur, clr, bg, details) in enumerate(phases):
        w = 1.2 if "Break" in title else 3.5
        add_rounded_box(slide, x, 1.3, w, 0.7, title, fill_color=clr,
                        text_color=WHITE, font_size=12, bold=True)
        add_textbox(slide, x, 2.05, w, 0.3, dur, 11, True, clr, PP_ALIGN.CENTER)
        if details:
            add_rounded_box(slide, x, 2.4, w, 1.8, details, fill_color=bg,
                            text_color=TEXT_DARK, font_size=11, border_color=clr,
                            alignment=PP_ALIGN.LEFT)
        x += w + 0.2

    # Bottom summary bar
    add_rounded_box(slide, 0.5, 4.7, 12.3, 0.6,
                    "Suggested balance:  40% Concepts & Theory   |   60% Guided Practice & Discussion",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=14, bold=True,
                    border_color=ACCENT_ORANGE)

    # Flow icons
    flow_items = ["Concepts", "Demo", "Hands-on", "Review", "Discuss"]
    flow_colors = [ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE, ACCENT_PURPLE, ACCENT_TEAL]
    for i, (fi, fc) in enumerate(zip(flow_items, flow_colors)):
        add_rounded_box(slide, 1.0 + i * 2.4, 5.7, 1.8, 0.55, fi,
                        fill_color=fc, text_color=WHITE, font_size=13, bold=True)
        if i < len(flow_items) - 1:
            add_arrow_right(slide, 1.0 + i * 2.4 + 1.82, 5.82, 0.5, 0.01, TEXT_MID)

    add_notes(slide, """SPEAKER NOTES – Slide 3: Session Agenda
-----------------------------------------
Walk through the timeline so participants know what to expect:

PART 1 - FOUNDATIONS & METHODOLOGY (~90 minutes):
- Start with "What is AI-Native?" — the core concepts and why this matters NOW
- Cover the AI tool landscape — what's available, what works, what doesn't
- Deep dive into spec-driven development — the methodology that makes AI code generation actually useful
- Architecture design principles — how to make architectural decisions with AI assistance
- Prompt engineering for software engineering — not generic prompting, but structured approaches for code, specs, and tests

BREAK (15 minutes) — Encourage participants to install any required tools if not already done

PART 2 - GUIDED HANDS-ON LAB (~120 minutes):
- This is the core of the workshop. Participants will build a Task Management REST API
- Exercise 1: Write the specification using a structured template
- Exercise 2: Generate architecture and API contracts
- Exercise 3: Generate and review backend code
- Exercise 4: Write and run tests
- Exercise 5: Set up a CI/CD pipeline
- Each exercise builds on the previous one — it's a continuous flow

BREAK (15 minutes)

PART 3 - ADVANCED TOPICS & WRAP-UP (~60 minutes):
- Multi-agent development — the future of AI-native SDLC
- AI governance and responsible use
- Security considerations specific to AI-generated code
- Homework assignments for continued practice
- Discussion, Q&A, and key takeaways

Emphasize the flow at the bottom: every topic follows Concepts -> Demo -> Hands-on -> Review -> Discuss. This is a pedagogical loop that ensures deep understanding.""")
    n += 1

    # ── Slide 4: WHAT IS AI-NATIVE SOFTWARE DEVELOPMENT? ───────────────
    slide = add_slide(prs)
    add_title_bar(slide, "What is AI-Native Software Development?", "Foundations", n)

    # Left column: definition
    add_textbox(slide, 0.6, 1.3, 6.0, 0.4, "Definition", 18, True, ACCENT_BLUE)
    add_bullet_list(slide, 0.6, 1.8, 6.0, 2.5, [
        "AI participates across the ENTIRE lifecycle, not just coding",
        "Specifications become the primary control mechanism",
        "Humans review intent, architecture, safety & fitness",
        "Continuous feedback loops improve every iteration",
        "Code is a generated artifact — specs are the source of truth",
    ], font_size=14)

    # Right: Key Principles cards
    add_textbox(slide, 7.5, 1.3, 5.0, 0.4, "Core Principles", 18, True, ACCENT_BLUE)
    principles = [
        ("Spec-First", "Specifications before code.\nAI refines, humans approve.", LIGHT_GREEN, ACCENT_GREEN),
        ("Human-in-the-Loop", "Critical decisions require\nhuman judgment & review.", LIGHT_ORANGE, ACCENT_ORANGE),
        ("Automated Validation", "Tests, scans & CI/CD verify\nevery generated artifact.", LIGHT_PURPLE, ACCENT_PURPLE),
        ("Continuous Learning", "Feedback from production\nimproves future generations.", LIGHT_TEAL, ACCENT_TEAL),
    ]
    for i, (t, d, bg, bdr) in enumerate(principles):
        add_rounded_box(slide, 7.5, 1.85 + i * 1.15, 5.2, 0.95,
                        f"{t}\n{d}", fill_color=bg, text_color=TEXT_DARK,
                        font_size=12, bold=True, border_color=bdr)

    # Bottom: equation
    add_rounded_box(slide, 1.0, 6.1, 11.3, 0.55,
                    "AI-Native  =  Human Intent  +  Executable Specification  +  AI Generation  +  Automated Validation  +  Feedback",
                    fill_color=TITLE_BAR, text_color=WHITE, font_size=14, bold=True)

    add_notes(slide, """SPEAKER NOTES – Slide 4: What is AI-Native Software Development?
------------------------------------------------------------------
This is the foundational slide. Spend time here — make sure everyone understands the paradigm shift.

KEY DISTINCTION - AI-Assisted vs AI-Native:
- AI-ASSISTED: You write code, AI helps with autocomplete, suggestions, and refactoring. AI is a tool you use occasionally. The human drives the process.
- AI-NATIVE: AI is embedded in EVERY phase. Requirements are captured in structured formats that AI can process. Architecture decisions are proposed by AI and validated by humans. Code, tests, and pipelines are generated from specifications. Feedback from CI/CD and production flows back to improve the next iteration.

Walk through each principle:
1. SPEC-FIRST: "The biggest mistake teams make is opening an IDE and asking AI to 'build me a todo app.' Instead, you write a structured specification — functional requirements, non-functional requirements, API contracts, acceptance criteria — and THEN generate. The spec IS the product; code is a byproduct."

2. HUMAN-IN-THE-LOOP: "AI is powerful but not infallible. It hallucinates APIs that don't exist, generates plausible but incorrect business logic, and can introduce security vulnerabilities. Every critical decision — architecture choices, security boundaries, data model design — requires human review."

3. AUTOMATED VALIDATION: "When code is generated at scale, you cannot manually review everything. Automated tests, static analysis, security scans, and CI/CD pipelines become your safety net. If the generated code doesn't pass the validation suite, it doesn't ship."

4. CONTINUOUS LEARNING: "Production telemetry, bug reports, and user feedback become inputs for the next generation cycle. The system gets better over time."

Ask the audience: "In your current teaching, where does AI fit? Is it a tool students use for homework, or is it part of how you teach the engineering process itself?" This question frames the rest of the workshop.""")
    n += 1

    # ── Slide 5: TRADITIONAL vs AI-NATIVE SDLC ────────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "Traditional SDLC vs AI-Native SDLC", "Foundations", n)

    rows = [
        ["Dimension", "Traditional SDLC", "AI-Native SDLC"],
        ["Requirements", "Written documents, often outdated", "Structured, machine-readable specs"],
        ["Design", "Manual architecture, static diagrams", "AI-proposed designs, validated by humans"],
        ["Implementation", "Developers write all code manually", "AI generates code from specs + review"],
        ["Testing", "Manual test writing, often late", "AI generates tests from acceptance criteria"],
        ["Code Review", "Peer review of finished code", "Review starts at specification stage"],
        ["CI/CD", "Pipeline configured separately", "Pipeline generated alongside code"],
        ["Security", "Penetration testing at the end", "Continuous security scanning in pipeline"],
        ["Documentation", "Docs drift from code over time", "Specs, code, tests stay synchronized"],
        ["Feedback", "Quarterly retrospectives", "Continuous automated feedback loops"],
    ]
    add_table_shape(slide, 0.5, 1.3, 12.3, 5.0, rows, 3)

    # Bottom insight
    add_rounded_box(slide, 1.5, 6.15, 10.3, 0.5,
                    "Key Insight: In AI-native development, specifications and tests are MORE important than code itself",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=13, bold=True,
                    border_color=ACCENT_ORANGE)

    add_notes(slide, """SPEAKER NOTES – Slide 5: Traditional vs AI-Native SDLC
--------------------------------------------------------
Use this comparison table to make the paradigm shift concrete. Walk through each row:

1. REQUIREMENTS: Traditional — someone writes a Word doc or Confluence page; it gets outdated within weeks. AI-Native — requirements are structured (YAML, JSON, or templated markdown) so AI can consume them programmatically. They are version-controlled alongside code.

2. DESIGN: Traditional — architects draw diagrams in Visio or Lucidchart; they live in a separate repo and drift. AI-Native — AI proposes architecture based on requirements, generates UML diagrams, and humans validate the choices. Diagrams are generated from specs.

3. IMPLEMENTATION: Traditional — developers spend 60-80% of their time writing code. AI-Native — developers spend 60-80% of their time reviewing and refining specs and generated outputs. Code writing shifts to code curation.

4. TESTING: This is where the biggest ROI is. Traditional testing is often an afterthought — "we'll write tests later." AI-native generates tests FROM acceptance criteria, which means tests exist BEFORE code.

5. CODE REVIEW: In traditional development, you review code someone already spent hours writing. In AI-native, you review the SPECIFICATION first. If the spec is wrong, regenerating code is cheap. Catching errors at the spec level saves enormous time.

6-9. Walk through CI/CD, Security, Documentation, and Feedback similarly.

KEY INSIGHT at bottom: "In AI-native development, the specification and test suite are more valuable than the code itself. Code can be regenerated in minutes; a well-crafted specification represents the team's understanding of the problem."

Discussion question for the audience: "Which of these shifts do you think would have the biggest impact on how you teach software engineering?" This gets faculty thinking about curriculum implications.""")
    n += 1

    # ── Slide 6: AI-NATIVE SDLC LIFECYCLE DIAGRAM ──────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "AI-Native SDLC Lifecycle", "Foundations", n)

    # Circular lifecycle diagram
    import math
    center_x, center_y = 4.2, 3.9
    radius = 2.2
    stages_cycle = [
        ("1. Capture\nIntent", ACCENT_BLUE),
        ("2. Write\nSpecification", ACCENT_GREEN),
        ("3. AI-Assisted\nDesign", ACCENT_ORANGE),
        ("4. Generate\nCode", ACCENT_PURPLE),
        ("5. Automated\nTesting", ACCENT_GREEN),
        ("6. CI/CD\nDeploy", ACCENT_ORANGE),
        ("7. Monitor &\nFeedback", ACCENT_TEAL),
    ]
    n_stages = len(stages_cycle)
    for i, (label, clr) in enumerate(stages_cycle):
        angle = -90 + i * (360 / n_stages)
        rad = math.radians(angle)
        cx = center_x + radius * math.cos(rad)
        cy = center_y + radius * math.sin(rad)
        add_rounded_box(slide, cx - 0.7, cy - 0.35, 1.4, 0.7,
                        label, fill_color=clr, text_color=WHITE, font_size=10, bold=True)

    # Center label
    add_rounded_box(slide, center_x - 0.8, center_y - 0.35, 1.6, 0.7,
                    "AI-Native\nSDLC", fill_color=TITLE_BAR, text_color=WHITE,
                    font_size=14, bold=True)

    # Right side: detail cards
    add_textbox(slide, 7.5, 1.3, 5.0, 0.4, "What Happens at Each Stage", 16, True, ACCENT_BLUE)
    details = [
        ("Intent Capture", "Stakeholder needs converted to structured requirements", LIGHT_BLUE),
        ("Specification", "Functional/non-functional reqs, API contracts, acceptance criteria", LIGHT_GREEN),
        ("AI Design", "Architecture proposals, trade-off analysis, UML generation", LIGHT_ORANGE),
        ("Code Generation", "AI generates implementation; humans review & refine", LIGHT_PURPLE),
        ("Testing", "Unit, integration, E2E tests generated from specs", LIGHT_GREEN),
        ("CI/CD Deploy", "Automated build, scan, deploy with quality gates", LIGHT_ORANGE),
        ("Feedback", "Telemetry, bug reports, and metrics feed next cycle", LIGHT_TEAL),
    ]
    for i, (t, d, bg) in enumerate(details):
        y = 1.85 + i * 0.7
        add_rounded_box(slide, 7.5, y, 5.2, 0.55,
                        f"{t}:  {d}", fill_color=bg, text_color=TEXT_DARK,
                        font_size=10, alignment=PP_ALIGN.LEFT)

    add_notes(slide, """SPEAKER NOTES – Slide 6: AI-Native SDLC Lifecycle
---------------------------------------------------
This diagram shows the continuous cycle of AI-native development. Unlike traditional waterfall (linear) or even agile (iterative but still human-driven), AI-native is a CONTINUOUS FEEDBACK LOOP where AI participates at every stage.

Walk through each stage clockwise:

1. CAPTURE INTENT: Everything starts with human intent. What problem are we solving? Who are the users? What are the constraints? This is captured in structured formats — not free-form emails, but templated requirement documents that AI can process.

2. WRITE SPECIFICATION: Requirements are formalized into executable specifications: functional requirements with acceptance criteria, non-functional requirements with measurable targets, API contracts in OpenAPI format, data models with constraints. KEY POINT: This step is the most important. The quality of AI-generated output is directly proportional to the quality of input specifications.

3. AI-ASSISTED DESIGN: AI proposes architecture options — microservices vs monolith, database choices, API patterns. It generates UML class diagrams, sequence diagrams, and deployment views. Humans evaluate trade-offs and approve. Architecture Decision Records (ADRs) document the rationale.

4. GENERATE CODE: With approved specs and architecture, AI generates implementation code — controllers, services, repositories, DTOs. The code follows the approved patterns and conventions. But it MUST be reviewed. Generation is fast; review is where engineering skill matters.

5. AUTOMATED TESTING: Tests are generated from acceptance criteria. Unit tests cover business rules, integration tests cover API behavior, E2E tests cover user journeys. The test suite becomes the contract — if generated code passes all tests, it meets the specification.

6. CI/CD DEPLOY: Every commit triggers an automated pipeline: build -> test -> security scan -> package -> deploy to staging -> smoke test. Quality gates enforce minimum coverage, zero critical vulnerabilities, and performance budgets.

7. MONITOR & FEEDBACK: Production telemetry (response times, error rates, user behavior) feeds back into the next cycle. Bugs become new acceptance criteria. Performance bottlenecks become new non-functional requirements. The cycle never stops.

CRITICAL INSIGHT: The arrow from step 7 back to step 1 is what makes this AI-NATIVE, not just AI-ASSISTED. The system learns and improves continuously.""")
    n += 1

    return n

if __name__ == "__main__":
    prs = new_presentation()
    build(prs)
    save_deck(prs, "_part1_opening.pptx")
