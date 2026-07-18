"""Part 3 – Architecture & Code Generation (Slides 14-22)"""
from slide_helpers import *


def build(prs, start_num=14):
    n = start_num

    # ── Slide 14: Architecture Design with AI Assistance ───────────────
    slide = add_slide(prs)
    add_title_bar(slide, "Architecture Design with AI Assistance", "Architecture", n)

    add_textbox(slide, 0.6, 1.2, 5.5, 0.4, "AI-Assisted Architecture Decisions", 17, True, ACCENT_ORANGE)
    add_bullet_list(slide, 0.6, 1.75, 5.8, 3.0, [
        "AI proposes architecture options based on requirements",
        "Evaluate trade-offs: simplicity vs scalability, monolith vs microservices",
        "Generate Architecture Decision Records (ADRs) automatically",
        "Humans validate and approve all design decisions",
        ("AI provides rationale for each option", [
            "Cost analysis, team expertise, time-to-market",
            "Scalability projections and failure modes",
        ]),
    ], font_size=14)

    add_textbox(slide, 7.2, 1.2, 5.5, 0.4, "Architecture Decision Matrix", 17, True, ACCENT_ORANGE)
    matrix_rows = [
        ["Criteria", "Monolith", "Microservices", "Serverless"],
        ["Complexity", "Low", "High", "Medium"],
        ["Scalability", "Limited", "High", "Auto-scale"],
        ["Team Size", "Small", "Large", "Any"],
        ["Deploy Speed", "Slower", "Independent", "Instant"],
        ["Cost (start)", "Low", "High", "Pay-per-use"],
        ["Debugging", "Easy", "Complex", "Moderate"],
    ]
    add_table_shape(slide, 7.2, 1.75, 5.6, 3.2, matrix_rows, 4,
                    header_color=ACCENT_ORANGE)

    add_rounded_box(slide, 0.6, 5.3, 12.2, 0.7,
                    "Recommendation for Task Management API:  Modular Monolith\n"
                    "Start simple, evolve to microservices when team/scale demands it  |  AI can generate migration paths",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=12, bold=True,
                    border_color=ACCENT_ORANGE)

    principle_cards = [
        ("Start Simple", LIGHT_GREEN, ACCENT_GREEN),
        ("Document Decisions", LIGHT_BLUE, ACCENT_BLUE),
        ("Plan for Evolution", LIGHT_ORANGE, ACCENT_ORANGE),
        ("Validate with AI", LIGHT_PURPLE, ACCENT_PURPLE),
    ]
    for i, (txt, bg, bdr) in enumerate(principle_cards):
        add_rounded_box(slide, 0.6 + i * 3.15, 6.15, 2.85, 0.5,
                        txt, fill_color=bg, text_color=TEXT_DARK,
                        font_size=12, bold=True, border_color=bdr)

    add_notes(slide, """SPEAKER NOTES -- Slide 14: Architecture Design with AI Assistance
-------------------------------------------------------------------
This slide introduces how AI transforms the architecture decision process.

1. HOW AI PROPOSES ARCHITECTURE:
   - Feed your requirements specification into the AI (functional reqs, NFRs, constraints)
   - Ask it to propose 2-3 architecture options with trade-offs
   - AI considers factors like team size, deployment target, scale requirements, budget
   - Example prompt: "Given these requirements for a Task Management API serving 1000 users, propose three architecture options with trade-offs"

2. THE DECISION MATRIX:
   - Walk through each row comparing Monolith, Microservices, and Serverless
   - Complexity: Monoliths are simpler to build and deploy initially
   - Scalability: Microservices scale independently; serverless auto-scales
   - Team Size: Microservices need larger teams due to operational overhead

3. WHEN TO OVERRIDE AI SUGGESTIONS:
   - AI may recommend microservices because it is trained on large-scale examples
   - For a teaching context or small team, a monolith is almost always the right starting point

4. ARCHITECTURE DECISION RECORDS (ADRs):
   - ADRs document the WHY behind architecture decisions
   - Template: Title, Status, Context, Decision, Consequences
   - AI can generate ADRs from a conversation about trade-offs

5. OUR RECOMMENDATION:
   - For the Task Management API, we choose a Modular Monolith
   - Simple to start, clear module boundaries, can be split later

DISCUSSION: Ask faculty what architecture they would choose for a student project.""")
    n += 1

    # ── Slide 15: System Architecture Block Diagram ────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "System Architecture: Task Management API", "Architecture", n)

    add_textbox(slide, 0.3, 1.35, 1.5, 0.4, "Presentation", 11, True, ACCENT_BLUE, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, 0.3, 2.75, 1.5, 0.4, "Gateway", 11, True, ACCENT_GREEN, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, 0.3, 4.15, 1.5, 0.4, "Business\nLogic", 11, True, ACCENT_ORANGE, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, 0.3, 5.55, 1.5, 0.4, "Data", 11, True, ACCENT_PURPLE, alignment=PP_ALIGN.CENTER)

    add_connector_line(slide, 1.9, 2.35, 8.8, 2.35, color=TEXT_MID, width=0.75)
    add_connector_line(slide, 1.9, 3.7, 8.8, 3.7, color=TEXT_MID, width=0.75)
    add_connector_line(slide, 1.9, 5.1, 8.8, 5.1, color=TEXT_MID, width=0.75)

    add_rounded_box(slide, 3.2, 1.2, 4.3, 0.7, "Client (Web / Mobile)",
                    fill_color=LIGHT_BLUE, text_color=TEXT_DARK, font_size=14, bold=True, border_color=ACCENT_BLUE)
    add_arrow_down(slide, 5.2, 1.95, 0.3, 0.35, ACCENT_BLUE)

    add_rounded_box(slide, 3.2, 2.55, 4.3, 0.7, "API Gateway  /  Auth Middleware",
                    fill_color=LIGHT_GREEN, text_color=TEXT_DARK, font_size=14, bold=True, border_color=ACCENT_GREEN)
    add_arrow_down(slide, 5.2, 3.3, 0.3, 0.35, ACCENT_GREEN)

    add_rounded_box(slide, 2.3, 3.9, 3.0, 0.75, "Task Service\ncreate | read | update | delete",
                    fill_color=LIGHT_ORANGE, text_color=TEXT_DARK, font_size=12, bold=True, border_color=ACCENT_ORANGE)
    add_rounded_box(slide, 5.7, 3.9, 3.0, 0.75, "User Service\nauth | profile | roles",
                    fill_color=LIGHT_ORANGE, text_color=TEXT_DARK, font_size=12, bold=True, border_color=ACCENT_ORANGE)

    add_arrow_down(slide, 3.65, 4.7, 0.3, 0.35, ACCENT_ORANGE)
    add_arrow_down(slide, 7.05, 4.7, 0.3, 0.35, ACCENT_ORANGE)

    add_rounded_box(slide, 2.3, 5.3, 3.0, 0.75, "PostgreSQL\nPrimary Database",
                    fill_color=LIGHT_PURPLE, text_color=TEXT_DARK, font_size=12, bold=True, border_color=ACCENT_PURPLE)
    add_rounded_box(slide, 5.7, 5.3, 3.0, 0.75, "Redis Cache\nSession & Query Cache",
                    fill_color=LIGHT_PURPLE, text_color=TEXT_DARK, font_size=12, bold=True, border_color=ACCENT_PURPLE)

    add_textbox(slide, 9.3, 1.2, 3.5, 0.4, "Design Rationale", 15, True, ACCENT_ORANGE)
    rationale = [
        ("Layered Separation", "Each layer has clear\nresponsibility boundary", LIGHT_BLUE),
        ("Service Modularity", "Task & User services\ncan evolve independently", LIGHT_GREEN),
        ("Caching Strategy", "Redis reduces DB load\nfor read-heavy queries", LIGHT_ORANGE),
        ("Auth at Gateway", "Single auth checkpoint\nbefore any service call", LIGHT_PURPLE),
    ]
    for i, (t, d, bg) in enumerate(rationale):
        add_rounded_box(slide, 9.3, 1.75 + i * 1.15, 3.7, 0.95,
                        f"{t}\n{d}", fill_color=bg, text_color=TEXT_DARK, font_size=11, bold=True)

    add_notes(slide, """SPEAKER NOTES -- Slide 15: System Architecture Block Diagram
--------------------------------------------------------------
This slide presents the layered architecture for our Task Management API. Walk through each layer:

1. PRESENTATION LAYER (Client): The consumer of our API -- could be web frontend, mobile app, or other services.

2. GATEWAY LAYER (API Gateway / Auth): All requests pass through authentication middleware first. JWT token validation happens here. Rate limiting, logging, CORS handled at this layer.

3. BUSINESS LOGIC LAYER (Services): Task Service handles CRUD operations. User Service handles auth, profiles, roles. Separate modules within our modular monolith.

4. DATA LAYER: PostgreSQL for primary storage with ACID transactions. Redis for caching frequently read data.

5. DESIGN RATIONALE (right cards): Walk through each rationale card and explain WHY this architecture was chosen.

HOW AI HELPED: Prompted AI with functional requirements and NFRs. AI proposed this layered architecture with rationale. We validated against constraints (small team, moderate scale).

DISCUSSION: Ask participants which layer they think is most important to get right. Answer: the interfaces between layers.""")
    n += 1

    # ── Slide 16: UML Class Diagram - Domain Model ─────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "UML Class Diagram: Task Management Domain", "Architecture", n)

    add_rounded_box(slide, 0.6, 1.3, 3.0, 2.8,
                    "Task\n" + "~" * 24 + "\n"
                    "  id: UUID (PK)\n"
                    "  title: String\n"
                    "  description: Text\n"
                    "  status: Enum\n"
                    "  priority: Enum\n"
                    "  assigneeId: UUID (FK)\n"
                    "  categoryId: UUID (FK)\n"
                    "  createdAt: DateTime\n"
                    "  updatedAt: DateTime",
                    fill_color=LIGHT_BLUE, text_color=TEXT_DARK, font_size=10,
                    bold=True, border_color=ACCENT_BLUE, alignment=PP_ALIGN.LEFT)

    add_rounded_box(slide, 4.2, 1.3, 2.7, 1.8,
                    "User\n" + "~" * 24 + "\n"
                    "  id: UUID (PK)\n"
                    "  name: String\n"
                    "  email: String\n"
                    "  role: Enum\n"
                    "  createdAt: DateTime",
                    fill_color=LIGHT_GREEN, text_color=TEXT_DARK, font_size=10,
                    bold=True, border_color=ACCENT_GREEN, alignment=PP_ALIGN.LEFT)

    add_rounded_box(slide, 7.4, 1.3, 2.7, 1.6,
                    "Category\n" + "~" * 24 + "\n"
                    "  id: UUID (PK)\n"
                    "  name: String\n"
                    "  description: Text",
                    fill_color=LIGHT_ORANGE, text_color=TEXT_DARK, font_size=10,
                    bold=True, border_color=ACCENT_ORANGE, alignment=PP_ALIGN.LEFT)

    add_rounded_box(slide, 4.2, 3.6, 2.7, 2.0,
                    "Comment\n" + "~" * 24 + "\n"
                    "  id: UUID (PK)\n"
                    "  taskId: UUID (FK)\n"
                    "  userId: UUID (FK)\n"
                    "  content: Text\n"
                    "  createdAt: DateTime",
                    fill_color=LIGHT_PURPLE, text_color=TEXT_DARK, font_size=10,
                    bold=True, border_color=ACCENT_PURPLE, alignment=PP_ALIGN.LEFT)

    # Relationship lines
    add_connector_line(slide, 3.6, 2.1, 4.2, 2.1, color=ACCENT_BLUE, width=2)
    add_textbox(slide, 3.3, 1.75, 0.5, 0.3, "*", 10, True, ACCENT_BLUE, PP_ALIGN.CENTER)
    add_textbox(slide, 4.15, 1.75, 0.5, 0.3, "1", 10, True, ACCENT_GREEN, PP_ALIGN.CENTER)

    add_connector_line(slide, 3.6, 2.6, 7.4, 2.0, color=ACCENT_ORANGE, width=2)
    add_textbox(slide, 3.2, 2.55, 0.5, 0.3, "*", 10, True, ACCENT_BLUE, PP_ALIGN.CENTER)
    add_textbox(slide, 7.3, 1.65, 0.5, 0.3, "1", 10, True, ACCENT_ORANGE, PP_ALIGN.CENTER)

    add_connector_line(slide, 2.1, 4.1, 4.2, 4.3, color=ACCENT_PURPLE, width=2)
    add_textbox(slide, 1.7, 3.85, 0.5, 0.3, "1", 10, True, ACCENT_BLUE, PP_ALIGN.CENTER)
    add_textbox(slide, 4.15, 4.0, 0.5, 0.3, "*", 10, True, ACCENT_PURPLE, PP_ALIGN.CENTER)

    add_connector_line(slide, 5.5, 3.6, 5.5, 3.1, color=ACCENT_GREEN, width=2)

    add_textbox(slide, 10.5, 1.2, 2.5, 0.4, "Domain Rules", 15, True, ACCENT_ORANGE)
    domain_rules = [
        ("Relationships", "Task belongs to User (assignee)\nTask belongs to Category\nTask has many Comments\nComment belongs to User", LIGHT_BLUE),
        ("Enumerations", "Status: TODO, IN_PROGRESS,\n  REVIEW, DONE\nPriority: LOW, MEDIUM,\n  HIGH, CRITICAL\nRole: ADMIN, MEMBER, VIEWER", LIGHT_GREEN),
        ("Constraints", "Email must be unique\nTitle is required (max 200)\nStatus transitions validated\nFK integrity enforced", LIGHT_ORANGE),
    ]
    for i, (t, d, bg) in enumerate(domain_rules):
        add_rounded_box(slide, 10.5, 1.75 + i * 1.65, 2.5, 1.45,
                        f"{t}\n{d}", fill_color=bg, text_color=TEXT_DARK, font_size=9, bold=True, alignment=PP_ALIGN.LEFT)

    add_rounded_box(slide, 0.6, 6.0, 9.5, 0.6,
                    "Legend:   1 = one   |   * = many   |   Lines show foreign key relationships   |   "
                    "AI generates these diagrams from natural language descriptions",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=11, bold=True, border_color=ACCENT_ORANGE)

    add_notes(slide, """SPEAKER NOTES -- Slide 16: UML Class Diagram - Domain Model
-------------------------------------------------------------
Walk through each entity:

1. TASK ENTITY: Central entity. UUID primary key. title/description for content. status and priority as enums with validated transitions. assigneeId and categoryId as foreign keys. Audit timestamps.

2. USER ENTITY: email has UNIQUE constraint. role is ENUM (ADMIN, MEMBER, VIEWER). Password hash NOT in this table for security.

3. CATEGORY ENTITY: Simple grouping mechanism for tasks. Separate table because categories are reusable entities.

4. COMMENT ENTITY: Links tasks and users for collaboration. Both task_id and user_id are foreign keys.

5. RELATIONSHIPS: Task to User is many-to-one. Task to Category is many-to-one. Task to Comment is one-to-many.

HOW AI GENERATES CLASS DIAGRAMS:
   - Provide natural language description of your domain
   - AI proposes entities, attributes, and relationships
   - Human reviews for correctness, validates cardinality
   - AI can output PlantUML, Mermaid, or direct code

DISCUSSION: Ask participants to identify a missing entity. Example: task attachments? task history/audit log?""")
    n += 1

    # ── Slide 17: UML Sequence Diagram ──────────────────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "UML Sequence Diagram: Create Task Flow", "Architecture", n)

    actors = [
        ("Client", 1.5, ACCENT_BLUE),
        ("API Gateway", 4.3, ACCENT_GREEN),
        ("Task Service", 7.1, ACCENT_ORANGE),
        ("Database", 9.9, ACCENT_PURPLE),
    ]
    for label, x, clr in actors:
        add_rounded_box(slide, x, 1.15, 1.8, 0.5, label,
                        fill_color=clr, text_color=WHITE, font_size=12, bold=True)

    for _, x, clr in actors:
        add_connector_line(slide, x + 0.9, 1.65, x + 0.9, 6.2, color=clr, width=1.5)

    y = 2.0
    add_connector_line(slide, 2.4, y, 4.3, y, color=ACCENT_BLUE, width=2)
    add_textbox(slide, 2.5, y - 0.3, 2.0, 0.3, "1. POST /api/tasks", 9, True, ACCENT_BLUE)

    y = 2.6
    add_rounded_box(slide, 4.6, y - 0.15, 1.5, 0.35, "validateToken()",
                    fill_color=LIGHT_GREEN, text_color=TEXT_DARK, font_size=9, bold=True, border_color=ACCENT_GREEN)
    add_textbox(slide, 4.1, y - 0.35, 2.5, 0.25, "2. self-call", 8, False, TEXT_MID)

    y = 3.2
    add_connector_line(slide, 5.2, y, 7.1, y, color=ACCENT_GREEN, width=2)
    add_textbox(slide, 5.3, y - 0.3, 2.0, 0.3, "3. createTask(dto)", 9, True, ACCENT_GREEN)

    y = 3.8
    add_connector_line(slide, 8.0, y, 9.9, y, color=ACCENT_ORANGE, width=2)
    add_textbox(slide, 8.1, y - 0.3, 2.0, 0.3, "4. validate & INSERT", 9, True, ACCENT_ORANGE)

    y = 4.4
    add_connector_line(slide, 9.9, y, 8.0, y, color=ACCENT_PURPLE, width=2)
    add_textbox(slide, 8.1, y - 0.3, 2.0, 0.3, "5. return taskId", 9, True, ACCENT_PURPLE)

    y = 5.0
    add_connector_line(slide, 8.0, y, 2.4, y, color=ACCENT_ORANGE, width=2)
    add_textbox(slide, 4.5, y - 0.3, 2.2, 0.3, "6. 201 Created { taskId }", 9, True, ACCENT_ORANGE)

    add_textbox(slide, 10.8, 1.15, 2.3, 0.4, "Key Points", 14, True, ACCENT_ORANGE)
    takeaway_items = [
        ("Auth First", "Token validated\nbefore any logic", LIGHT_GREEN),
        ("DTO Pattern", "Data Transfer Object\nisolates layers", LIGHT_BLUE),
        ("DB Validation", "Constraints checked\nat persistence level", LIGHT_ORANGE),
        ("Clear Response", "Status code + created\nresource returned", LIGHT_PURPLE),
    ]
    for i, (t, d, bg) in enumerate(takeaway_items):
        add_rounded_box(slide, 10.8, 1.65 + i * 1.1, 2.2, 0.9,
                        f"{t}\n{d}", fill_color=bg, text_color=TEXT_DARK, font_size=9, bold=True)

    add_rounded_box(slide, 0.6, 5.6, 9.8, 0.5,
                    "Sequence diagrams model runtime interactions -- essential for understanding API flows before writing code",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=11, bold=True, border_color=ACCENT_ORANGE)

    add_notes(slide, """SPEAKER NOTES -- Slide 17: UML Sequence Diagram - Create Task Flow
--------------------------------------------------------------------
Walk through each message in order:

1. POST /api/tasks (Client -> API Gateway): HTTP POST with task data. Authorization: Bearer JWT in header.

2. validateToken() (API Gateway self-call): Validates JWT token. Checks token not expired, signature valid, user has CREATE permission. If fails: 401 Unauthorized.

3. createTask(dto) (API Gateway -> Task Service): Forwards validated request using DTO. Strips fields user should not set (id, createdAt).

4. validate & INSERT (Task Service -> Database): Validates business rules: title required, valid status, assignee exists. Executes INSERT. Database enforces FK constraints.

5. return taskId (Database -> Task Service): Returns generated UUID for new task.

6. 201 Created (Task Service -> Client): Response includes created task with ID. HTTP 201 indicates new resource created.

WHY SEQUENCE DIAGRAMS MATTER:
   - Reveal runtime behavior that class diagrams cannot show
   - Help identify performance bottlenecks
   - Expose error handling gaps

EXERCISE PREVIEW: Participants will ask AI to generate a sequence diagram for "Update Task Status" flow.""")
    n += 1

    # ── Slide 18: API Contract-First Design ────────────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "API Contract-First Design (OpenAPI)", "Architecture", n)

    add_textbox(slide, 0.6, 1.2, 5.5, 0.4, "Contract-First Approach", 17, True, ACCENT_ORANGE)
    add_bullet_list(slide, 0.6, 1.75, 5.8, 3.5, [
        "Define endpoints, request/response bodies BEFORE coding",
        "Use OpenAPI/Swagger as the single source of truth",
        "Generate server stubs and client SDKs from the spec",
        "Contract becomes the testing baseline",
        ("Benefits of API-first", [
            "Frontend and backend teams work in parallel",
            "Auto-generate documentation and mock servers",
            "Contract tests catch breaking changes early",
        ]),
    ], font_size=14)

    add_textbox(slide, 6.8, 1.2, 6.0, 0.4, "OpenAPI Snippet -- POST /api/tasks", 14, True, ACCENT_ORANGE)
    openapi_code = (
        "openapi: 3.0.3\n"
        "paths:\n"
        "  /api/tasks:\n"
        "    post:\n"
        "      summary: Create a new task\n"
        "      operationId: createTask\n"
        "      tags: [Tasks]\n"
        "      requestBody:\n"
        "        required: true\n"
        "        content:\n"
        "          application/json:\n"
        "            schema:\n"
        "              $ref: '#/components/schemas/CreateTaskDTO'\n"
        "      responses:\n"
        "        '201':\n"
        "          description: Task created\n"
        "          content:\n"
        "            application/json:\n"
        "              schema:\n"
        "                $ref: '#/components/schemas/Task'\n"
        "        '400':\n"
        "          description: Validation error\n"
        "        '401':\n"
        "          description: Unauthorized"
    )
    add_code_box(slide, 6.8, 1.65, 6.0, 4.0, openapi_code, font_size=9)

    flow_steps = [
        ("Write\nOpenAPI Spec", ACCENT_BLUE),
        ("Review &\nValidate", ACCENT_GREEN),
        ("Generate\nStubs", ACCENT_ORANGE),
        ("Implement\nLogic", ACCENT_PURPLE),
        ("Contract\nTests", ACCENT_TEAL),
    ]
    for i, (txt, clr) in enumerate(flow_steps):
        add_rounded_box(slide, 0.6 + i * 2.55, 5.85, 2.15, 0.7, txt,
                        fill_color=clr, text_color=WHITE, font_size=11, bold=True)
        if i < len(flow_steps) - 1:
            add_arrow_right(slide, 0.6 + i * 2.55 + 2.17, 6.02, 0.35, 0.01, TEXT_MID)

    add_notes(slide, """SPEAKER NOTES -- Slide 18: API Contract-First Design
------------------------------------------------------
Contract-first API design using OpenAPI is a cornerstone of AI-native development.

1. WHAT IS CONTRACT-FIRST? Define the API contract FIRST, then generate code. The OpenAPI spec describes every endpoint, schema, status code.

2. WALK THROUGH THE OPENAPI SNIPPET: paths, HTTP method, requestBody, responses, $ref for reusable schemas.

3. BENEFITS: Parallel development (frontend mocks from spec), auto-generated docs, contract tests, breaking change detection, client SDK generation.

4. WORKFLOW (bottom flow): Write spec -> Review -> Generate stubs -> Implement logic -> Contract tests.

5. HOW AI HELPS: AI generates entire OpenAPI spec from requirements. AI validates spec for consistency. AI generates mock data from schemas. Always review: AI may generate overly permissive schemas.

TOOLS: Swagger Editor, Stoplight Studio, Spectral (linting), Prism (mock server).""")
    n += 1

    # ── Slide 19: Data Model Design ────────────────────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "Data Model Design Considerations", "Architecture", n)

    add_rounded_box(slide, 0.5, 1.2, 3.5, 2.8,
                    "tasks\n" + "-" * 30 + "\n"
                    "  id          UUID PK\n"
                    "  title       VARCHAR(200) NOT NULL\n"
                    "  description TEXT\n"
                    "  status      ENUM NOT NULL\n"
                    "  priority    ENUM NOT NULL\n"
                    "  assignee_id UUID FK -> users\n"
                    "  category_id UUID FK -> categories\n"
                    "  created_at  TIMESTAMP\n"
                    "  updated_at  TIMESTAMP",
                    fill_color=LIGHT_BLUE, text_color=TEXT_DARK, font_size=9,
                    bold=True, border_color=ACCENT_BLUE, alignment=PP_ALIGN.LEFT)

    add_rounded_box(slide, 4.3, 1.2, 3.0, 1.9,
                    "users\n" + "-" * 30 + "\n"
                    "  id         UUID PK\n"
                    "  name       VARCHAR(100)\n"
                    "  email      VARCHAR(255) UNIQUE\n"
                    "  role       ENUM NOT NULL\n"
                    "  created_at TIMESTAMP",
                    fill_color=LIGHT_GREEN, text_color=TEXT_DARK, font_size=9,
                    bold=True, border_color=ACCENT_GREEN, alignment=PP_ALIGN.LEFT)

    add_rounded_box(slide, 7.6, 1.2, 2.8, 1.5,
                    "categories\n" + "-" * 30 + "\n"
                    "  id          UUID PK\n"
                    "  name        VARCHAR(100)\n"
                    "  description TEXT",
                    fill_color=LIGHT_ORANGE, text_color=TEXT_DARK, font_size=9,
                    bold=True, border_color=ACCENT_ORANGE, alignment=PP_ALIGN.LEFT)

    add_rounded_box(slide, 4.3, 3.4, 3.0, 1.9,
                    "comments\n" + "-" * 30 + "\n"
                    "  id         UUID PK\n"
                    "  task_id    UUID FK -> tasks\n"
                    "  user_id    UUID FK -> users\n"
                    "  content    TEXT NOT NULL\n"
                    "  created_at TIMESTAMP",
                    fill_color=LIGHT_PURPLE, text_color=TEXT_DARK, font_size=9,
                    bold=True, border_color=ACCENT_PURPLE, alignment=PP_ALIGN.LEFT)

    add_connector_line(slide, 4.0, 2.8, 4.3, 2.2, color=ACCENT_BLUE, width=1.5)
    add_connector_line(slide, 4.0, 3.0, 7.6, 1.9, color=ACCENT_ORANGE, width=1.5)
    add_connector_line(slide, 4.3, 4.0, 2.5, 4.0, color=ACCENT_PURPLE, width=1.5)
    add_connector_line(slide, 5.8, 3.4, 5.8, 3.1, color=ACCENT_GREEN, width=1.5)

    add_textbox(slide, 10.8, 1.2, 2.3, 0.4, "Design Principles", 14, True, ACCENT_ORANGE)
    db_principles = [
        ("Normalization", "3NF to reduce redundancy\nEach fact stored once", LIGHT_BLUE),
        ("Constraints", "NOT NULL, UNIQUE, FK\nfor data integrity", LIGHT_GREEN),
        ("Indexing", "Index FKs and common\nquery columns (status)", LIGHT_ORANGE),
        ("Audit Fields", "created_at, updated_at\non every table", LIGHT_PURPLE),
        ("Soft Deletes", "deleted_at column instead\nof permanent removal", LIGHT_TEAL),
    ]
    for i, (t, d, bg) in enumerate(db_principles):
        add_rounded_box(slide, 10.8, 1.7 + i * 0.95, 2.2, 0.8,
                        f"{t}\n{d}", fill_color=bg, text_color=TEXT_DARK, font_size=9, bold=True)

    add_rounded_box(slide, 0.5, 5.7, 10.0, 0.9,
                    "Key Data Modeling Practices\n"
                    "Normalize to 3NF  |  Enforce constraints at DB level  |  Index FK columns  |  "
                    "Add audit timestamps  |  Use migrations for schema changes  |  AI generates DDL from ER diagrams",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=11, bold=True, border_color=ACCENT_ORANGE)

    add_notes(slide, """SPEAKER NOTES -- Slide 19: Data Model Design
----------------------------------------------
Walk through each table and design decisions:

1. TASKS TABLE: UUID primary key (globally unique, better for distributed systems). Status/priority as ENUMs enforced at DB level. FK to users and categories.

2. USERS TABLE: Email UNIQUE constraint. Password hash NOT in this table (separate auth table for security).

3. CATEGORIES TABLE: Simple lookup table. Separate table because categories are reusable entities.

4. COMMENTS TABLE: Links tasks and users. Both FKs ensure referential integrity.

KEY DESIGN PRINCIPLES:
- NORMALIZATION: 3NF to reduce redundancy
- CONSTRAINTS: Let the database enforce business rules
- INDEXING: FK columns and common query columns
- AUDIT FIELDS: created_at, updated_at on every table
- SOFT DELETES: deleted_at instead of permanent removal

HOW AI HELPS: Generates CREATE TABLE statements, suggests indexes, generates migration scripts. Always review: AI may miss unique constraints or incorrect FK directions.""")
    n += 1

    # ── Slide 20: AI Code Generation Workflow ──────────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "AI Code Generation Workflow", "Implementation", n)

    flow_steps = [
        ("Approved\nSpec", ACCENT_BLUE),
        ("Prompt\nConstruction", ACCENT_GREEN),
        ("AI\nGeneration", ACCENT_ORANGE),
        ("Human\nReview", ACCENT_PURPLE),
        ("Refactor\n& Improve", ACCENT_TEAL),
        ("Commit\n& Push", ACCENT_GREEN),
    ]
    for i, (txt, clr) in enumerate(flow_steps):
        add_rounded_box(slide, 0.5 + i * 2.15, 1.25, 1.85, 0.85, txt,
                        fill_color=clr, text_color=WHITE, font_size=12, bold=True)
        if i < len(flow_steps) - 1:
            add_arrow_right(slide, 0.5 + i * 2.15 + 1.87, 1.5, 0.25, 0.01, TEXT_MID)

    add_textbox(slide, 0.6, 2.5, 6.5, 0.4, "Best Practices for AI Code Generation", 16, True, ACCENT_PURPLE)
    add_bullet_list(slide, 0.6, 3.0, 6.3, 3.5, [
        "Generate ONE component/layer at a time",
        "Review before asking AI for the next layer",
        "Keep prompts tied to specs and file names",
        "Commit working increments frequently",
        "Never skip human review -- even for simple code",
        "Include test expectations in generation prompts",
        "Ask AI to explain its implementation choices",
    ], font_size=14)

    add_textbox(slide, 7.5, 2.5, 5.5, 0.4, "Sample Generation Prompt", 16, True, ACCENT_PURPLE)
    prompt_code = (
        "Context: Task Management API\n"
        "Spec file: task-service.spec.yaml\n"
        "Layer: Service layer\n"
        "Component: TaskService\n"
        "---\n"
        "Generate the TaskService class that:\n"
        "1. Implements createTask(dto)\n"
        "2. Validates title is non-empty\n"
        "3. Sets status to TODO by default\n"
        "4. Saves via TaskRepository\n"
        "5. Returns the created task\n"
        "---\n"
        "Tech stack: Java + Spring Boot 3\n"
        "Follow project conventions in:\n"
        "  src/services/UserService.java"
    )
    add_code_box(slide, 7.5, 3.0, 5.5, 3.2, prompt_code, font_size=10)

    add_rounded_box(slide, 0.6, 6.2, 12.2, 0.5,
                    "Anti-Pattern:  'Build me the entire app'  ->  Always decompose into small, reviewable units",
                    fill_color=LIGHT_ORANGE, text_color=TEXT_DARK, font_size=13, bold=True, border_color=ACCENT_ORANGE)

    add_notes(slide, """SPEAKER NOTES -- Slide 20: AI Code Generation Workflow
--------------------------------------------------------
Disciplined workflow for generating code with AI. This is where many teams go wrong.

1. WORKFLOW: Approved Spec -> Prompt Construction -> AI Generation -> Human Review -> Refactor -> Commit.

2. BEST PRACTICES:
   - ONE COMPONENT AT A TIME: Generate controller, then service, then repository, reviewing each.
   - REVIEW BEFORE NEXT: If the service layer has a bug, generating the controller on top compounds the error.
   - PROMPTS TIED TO SPECS: "Implement FR-3 from task-management.spec.yaml" is better than generic requests.
   - COMMIT FREQUENTLY: Working increments create rollback points.
   - NEVER SKIP REVIEW: AI makes subtle errors -- off-by-one, incorrect null handling, wrong status codes.

3. SAMPLE PROMPT: Walk through each section -- Context, Spec file, Layer, Component, numbered requirements, tech stack, convention reference.

4. ANTI-PATTERN: "Build me a task management API" produces a monolithic blob that is hard to review. Decompose into 10-15 focused generation prompts.""")
    n += 1

    # ── Slide 21: Code Review in AI-Native Development ─────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "Code Review in AI-Native Development", "Implementation", n)

    add_textbox(slide, 0.5, 1.2, 6.0, 0.4, "What to Review (Checklist)", 17, True, ACCENT_PURPLE)
    checklist_items = [
        ("Spec Compliance", "Does it match the specification exactly?", LIGHT_BLUE, ACCENT_BLUE),
        ("Business Rules", "Are business rules correctly implemented?", LIGHT_GREEN, ACCENT_GREEN),
        ("Error Handling", "Is error handling appropriate and complete?", LIGHT_ORANGE, ACCENT_ORANGE),
        ("Naming & Style", "Are naming conventions and style guide followed?", LIGHT_PURPLE, ACCENT_PURPLE),
        ("Security", "Auth, input validation, data exposure checked?", LIGHT_TEAL, ACCENT_TEAL),
        ("Test Coverage", "Are generated tests meaningful, not trivial?", LIGHT_YELLOW, ACCENT_ORANGE),
    ]
    for i, (title, desc, bg, bdr) in enumerate(checklist_items):
        add_rounded_box(slide, 0.5, 1.75 + i * 0.78, 6.0, 0.62,
                        f"{title}:  {desc}", fill_color=bg, text_color=TEXT_DARK,
                        font_size=11, bold=True, border_color=bdr, alignment=PP_ALIGN.LEFT)

    add_textbox(slide, 7.0, 1.2, 6.0, 0.4, "Review Workflow", 17, True, ACCENT_PURPLE)
    review_flow = [
        ("AI Generates Code", ACCENT_BLUE, LIGHT_BLUE),
        ("Static Analysis\n(lint, type-check)", ACCENT_GREEN, LIGHT_GREEN),
        ("AI-Assisted Review\n(detect patterns & smells)", ACCENT_ORANGE, LIGHT_ORANGE),
        ("Human Review\n(intent, logic, security)", ACCENT_PURPLE, LIGHT_PURPLE),
        ("Approve / Reject", ACCENT_TEAL, LIGHT_TEAL),
    ]
    for i, (txt, clr, bg) in enumerate(review_flow):
        add_rounded_box(slide, 7.3, 1.75 + i * 0.95, 5.0, 0.7, txt,
                        fill_color=bg, text_color=TEXT_DARK, font_size=12, bold=True, border_color=clr)
        if i < len(review_flow) - 1:
            add_arrow_down(slide, 9.65, 1.75 + i * 0.95 + 0.72, 0.25, 0.2, clr)

    add_rounded_box(slide, 0.5, 6.2, 12.5, 0.5,
                    "AI-Native Code Review Principle:  Review INTENT (spec) first, then CODE -- "
                    "if the spec is wrong, the code will be wrong regardless of quality",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=12, bold=True, border_color=ACCENT_ORANGE)

    add_notes(slide, """SPEAKER NOTES -- Slide 21: Code Review in AI-Native Development
-----------------------------------------------------------------
Code review becomes MORE important when code is AI-generated.

LEFT COLUMN -- WHAT TO REVIEW:
1. SPEC COMPLIANCE: Does generated code implement what the specification says? AI may add extra features or miss edge cases.
2. BUSINESS RULES: Domain-specific rules correctly implemented? "Only ADMIN can delete" -- is this enforced?
3. ERROR HANDLING: All error cases handled? AI tends to generate optimistic code.
4. NAMING & STYLE: Follows project naming conventions?
5. SECURITY: Authentication enforced? Input validated? Sensitive data excluded from responses?
6. TEST COVERAGE: Tests actually testing business logic, not just trivially asserting?

RIGHT COLUMN -- REVIEW WORKFLOW: AI generates -> Static analysis -> AI-assisted review -> Human review -> Approve/Reject. The final decision is always human.

KEY INSIGHT: Review the spec first. In AI-native development, 60% of review effort on specifications, 40% on code.""")
    n += 1

    # ── Slide 22: Refactoring AI-Generated Code ────────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "Refactoring AI-Generated Code", "Implementation", n)

    add_textbox(slide, 0.5, 1.2, 5.8, 0.4, "Common Issues in AI-Generated Code", 16, True, ACCENT_PURPLE)
    issues = [
        ("Duplication", "Repeated logic from separate prompts", LIGHT_ORANGE, ACCENT_ORANGE),
        ("Unclear Naming", "Generic names: data, result, handler", LIGHT_BLUE, ACCENT_BLUE),
        ("Missing Error Boundaries", "No try-catch, no validation", LIGHT_GREEN, ACCENT_GREEN),
        ("Over-Engineering", "Complex patterns where simple suffices", LIGHT_PURPLE, ACCENT_PURPLE),
        ("Hardcoded Values", "URLs, ports, keys embedded in code", LIGHT_TEAL, ACCENT_TEAL),
    ]
    for i, (title, desc, bg, bdr) in enumerate(issues):
        add_rounded_box(slide, 0.5, 1.75 + i * 0.85, 5.8, 0.68,
                        f"{title}:  {desc}", fill_color=bg, text_color=TEXT_DARK,
                        font_size=12, bold=True, border_color=bdr, alignment=PP_ALIGN.LEFT)

    add_arrow_right(slide, 6.4, 3.5, 0.5, 0.01, ACCENT_PURPLE)

    add_textbox(slide, 7.2, 1.2, 5.8, 0.4, "Refactoring Strategies", 16, True, ACCENT_PURPLE)
    strategies = [
        ("Extract Services", "Move business rules into dedicated service classes", LIGHT_ORANGE, ACCENT_ORANGE),
        ("Apply Conventions", "Rename to match project style guide consistently", LIGHT_BLUE, ACCENT_BLUE),
        ("Add Error Handling", "Wrap in try-catch, validate inputs, return proper codes", LIGHT_GREEN, ACCENT_GREEN),
        ("Simplify Patterns", "Replace complex abstractions with straightforward code", LIGHT_PURPLE, ACCENT_PURPLE),
        ("Use Configuration", "Move environment-specific values to .env / config files", LIGHT_TEAL, ACCENT_TEAL),
    ]
    for i, (title, desc, bg, bdr) in enumerate(strategies):
        add_rounded_box(slide, 7.2, 1.75 + i * 0.85, 5.8, 0.68,
                        f"{title}:  {desc}", fill_color=bg, text_color=TEXT_DARK,
                        font_size=12, bold=True, border_color=bdr, alignment=PP_ALIGN.LEFT)

    add_textbox(slide, 0.5, 5.85, 6.0, 0.3, "Before (AI-generated)", 12, True, ACCENT_ORANGE)
    add_code_box(slide, 0.5, 6.1, 6.0, 0.65,
        "// Hardcoded, no validation, generic names\n"
        "app.post('/api/tasks', (req, res) => {\n"
        "  const data = req.body;\n"
        "  db.query('INSERT INTO tasks...', data)\n"
        "    .then(r => res.json(r));\n"
        "});", font_size=8)

    add_textbox(slide, 7.2, 5.85, 5.8, 0.3, "After (Refactored)", 12, True, ACCENT_GREEN)
    add_code_box(slide, 7.2, 6.1, 5.8, 0.65,
        "// Validated, typed, error-handled, configured\n"
        "router.post('/api/tasks',\n"
        "  auth, validate(CreateTaskDTO),\n"
        "  taskController.create  // -> service -> repo\n"
        ");", font_size=8)

    add_notes(slide, """SPEAKER NOTES -- Slide 22: Refactoring AI-Generated Code
-----------------------------------------------------------
AI-generated code almost always needs refactoring.

LEFT COLUMN -- COMMON ISSUES:
1. DUPLICATION: Each prompt is independent so AI duplicates validation, error handling, utility functions.
2. UNCLEAR NAMING: Generic variable names (data, result, response). Should be specific (task, userProfile).
3. MISSING ERROR BOUNDARIES: AI generates happy path but skips error handling.
4. OVER-ENGINEERING: AI sometimes applies unnecessary design patterns. Simplicity is a feature.
5. HARDCODED VALUES: Database URLs, port numbers, API keys embedded directly in code.

RIGHT COLUMN -- REFACTORING STRATEGIES:
1. EXTRACT SERVICES: One service per domain entity.
2. APPLY CONVENTIONS: Systematic renaming.
3. ADD ERROR HANDLING: Try-catch around DB calls, proper HTTP status codes.
4. SIMPLIFY: Remove unnecessary abstractions.
5. USE CONFIGURATION: Environment variables for env-specific values.

BOTTOM EXAMPLE: Walk through before/after. Before: flat handler with no layers. After: layered architecture with middleware.

PRACTICAL TIP: Ask AI to review its own output: "Review this code for duplication, naming issues, missing error handling." AI is good at reviewing when specifically asked.""")
    n += 1

    return n


if __name__ == "__main__":
    prs = new_presentation()
    build(prs)
    save_deck(prs, "_part3_arch_codegen.pptx")
