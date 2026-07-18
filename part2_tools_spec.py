"""Part 2 – Tools & Spec-Driven Development (Slides 7-13)"""
from slide_helpers import *

def build(prs, start_num=7):
    n = start_num

    # ── Slide 7: AI TOOL ECOSYSTEM & LANDSCAPE ─────────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "AI Tool Ecosystem for Software Development", "Tools", n)

    add_textbox(slide, 0.5, 1.15, 12.3, 0.4,
                "Categorized Landscape of AI-Powered Development Tools",
                16, True, ACCENT_TEAL)

    add_rounded_box(slide, 0.5, 1.7, 6.0, 1.3,
                    "IDE Assistants\nGitHub Copilot  |  Cursor  |  JetBrains AI  |  Windsurf\nInline code completion, refactoring, chat-in-editor",
                    fill_color=LIGHT_GREEN, text_color=TEXT_DARK,
                    font_size=12, bold=True, border_color=ACCENT_GREEN)

    add_rounded_box(slide, 6.8, 1.7, 5.9, 1.3,
                    "Chat / LLM Interfaces\nChatGPT  |  Claude  |  Gemini  |  M365 Copilot\nConversational coding, explanation, brainstorming",
                    fill_color=LIGHT_ORANGE, text_color=TEXT_DARK,
                    font_size=12, bold=True, border_color=ACCENT_ORANGE)

    add_rounded_box(slide, 0.5, 3.2, 6.0, 1.3,
                    "Workflow & Agent Frameworks\nLangChain  |  Semantic Kernel  |  CrewAI  |  AutoGen\nOrchestrate multi-step AI pipelines & agent teams",
                    fill_color=LIGHT_PURPLE, text_color=TEXT_DARK,
                    font_size=12, bold=True, border_color=ACCENT_PURPLE)

    add_rounded_box(slide, 6.8, 3.2, 5.9, 1.3,
                    "DevOps & CI/CD Intelligence\nGitHub Actions AI  |  SonarQube AI  |  Snyk AI\nAutomated quality gates, vulnerability detection",
                    fill_color=LIGHT_TEAL, text_color=TEXT_DARK,
                    font_size=12, bold=True, border_color=ACCENT_TEAL)

    add_rounded_box(slide, 3.2, 4.7, 6.9, 1.0,
                    "Code Review & PR Analysis\nCodeRabbit  |  Copilot PR Review  |  Qodo (formerly CodiumAI)\nAutomated code review, PR summaries, test suggestions",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK,
                    font_size=12, bold=True, border_color=ACCENT_ORANGE)

    add_rounded_box(slide, 1.5, 5.95, 10.3, 0.55,
                    "Key Takeaway: No single tool covers everything \u2014 build a complementary toolchain across categories",
                    fill_color=LIGHT_BLUE, text_color=TEXT_DARK, font_size=13, bold=True,
                    border_color=ACCENT_BLUE)

    add_notes(slide, """SPEAKER NOTES - Slide 7: AI Tool Ecosystem for Software Development
----------------------------------------------------------------------
This slide gives a bird's-eye view of the AI-powered development tool landscape. The goal is to help faculty understand that there is no single "AI tool" - there is an entire ecosystem, and effective AI-native development requires choosing the right tools for each role.

Walk through each category:

1. IDE ASSISTANTS (Green box):
- GitHub Copilot: The most widely adopted. Works inside VS Code, JetBrains, Neovim. Strong at code completion, inline suggestions, and chat-based refactoring.
- Cursor: A fork of VS Code built from the ground up for AI-first development. Excellent at multi-file edits, codebase-aware context, and composer mode for complex changes.
- JetBrains AI: Integrated into IntelliJ, PyCharm, etc. Leverages JetBrains deep code analysis with AI suggestions. Great for Java/Kotlin ecosystems.
- Windsurf: Another AI-native IDE with Cascade (agentic) and autocomplete flows. Emphasizes deep contextual understanding.
- WHEN TO USE: Always-on during coding. These are your primary coding companions. Best for implementation phase.

2. CHAT / LLM INTERFACES (Orange box):
- ChatGPT: General-purpose, great for brainstorming, explaining concepts, debugging complex issues.
- Claude: Strong at long-context understanding, analysis, and careful reasoning. Excellent for reviewing specifications and architecture documents.
- Gemini: Google's multimodal model. Strong integration with Google Cloud ecosystem.
- M365 Copilot: Integrated into Microsoft tools - useful for documentation, project planning, and team communication.
- WHEN TO USE: For exploration, learning, debugging complex issues, reviewing architecture decisions.

3. WORKFLOW & AGENT FRAMEWORKS (Purple box):
- LangChain: The most popular framework for building LLM-powered applications. Chains, agents, retrieval-augmented generation.
- Semantic Kernel: Microsoft's SDK for integrating AI into applications. Strong .NET integration.
- CrewAI: Framework for orchestrating multiple AI agents that collaborate on tasks.
- AutoGen: Microsoft Research framework for multi-agent conversations.
- WHEN TO USE: When building AI-powered features in your applications, or when orchestrating multi-agent development workflows.

4. DEVOPS & CI/CD INTELLIGENCE (Teal box):
- GitHub Actions AI: AI-powered workflow suggestions, automated PR checks.
- SonarQube AI: AI-enhanced static analysis, code smell detection, and quality scoring.
- Snyk AI: AI-powered security vulnerability detection, dependency scanning, and fix suggestions.
- WHEN TO USE: Integrated into your CI/CD pipeline. These run automatically on every commit and PR.

5. CODE REVIEW (Yellow box):
- CodeRabbit: Automated PR review bot that provides detailed, contextual code review comments.
- Copilot PR Review: GitHub's built-in PR review summarization.
- Qodo: Focuses on test generation and code quality analysis.
- WHEN TO USE: On every pull request. Augments human review, catches issues human reviewers miss.

Emphasize: The best AI-native teams use tools from MULTIPLE categories. A typical stack might be: Cursor (IDE) + Claude (reasoning/review) + GitHub Actions (CI/CD) + CodeRabbit (PR review). The tools complement each other.""")
    n += 1

    # ── Slide 8: IDE ASSISTANTS & CODE GENERATION DEEP DIVE ────────────
    slide = add_slide(prs)
    add_title_bar(slide, "IDE Assistants & Code Generation Deep Dive", "Tools", n)

    add_textbox(slide, 0.5, 1.2, 5.5, 0.4, "Key Capabilities", 16, True, ACCENT_TEAL)
    add_bullet_list(slide, 0.5, 1.7, 5.5, 4.0, [
        ("Inline Code Completion", [
            "Real-time suggestions as you type",
            "Context-aware multi-line completions"
        ]),
        ("Explain & Document Code", [
            "Explain selected code in plain English",
            "Generate docstrings and comments"
        ]),
        ("Refactoring Suggestions", [
            "Rename, extract, restructure code",
            "Convert patterns (e.g., loops to streams)"
        ]),
        ("Test Generation", [
            "Generate unit tests from implementation",
            "Suggest edge cases and boundary tests"
        ]),
        ("Chat-in-Editor", [
            "Ask questions without leaving the IDE",
            "Multi-file edits from natural language"
        ]),
    ], font_size=13)

    add_textbox(slide, 6.8, 1.2, 5.8, 0.4, "Tool Comparison", 16, True, ACCENT_TEAL)

    add_rounded_box(slide, 6.8, 1.7, 5.8, 1.35,
                    "GitHub Copilot\nStrengths: Widest IDE support, strong autocomplete,\nenterprise features, Copilot Chat & Workspace\nBest for: General-purpose coding across languages",
                    fill_color=LIGHT_BLUE, text_color=TEXT_DARK,
                    font_size=11, bold=True, border_color=ACCENT_BLUE,
                    alignment=PP_ALIGN.LEFT)

    add_rounded_box(slide, 6.8, 3.2, 5.8, 1.35,
                    "Cursor\nStrengths: Codebase-aware context, Composer mode,\nmulti-file edits, agentic workflows\nBest for: Complex refactors, full-feature development",
                    fill_color=LIGHT_GREEN, text_color=TEXT_DARK,
                    font_size=11, bold=True, border_color=ACCENT_GREEN,
                    alignment=PP_ALIGN.LEFT)

    add_rounded_box(slide, 6.8, 4.7, 5.8, 1.35,
                    "Devin / AI Agents\nStrengths: Autonomous task execution, end-to-end\nimplementation, planning & debugging loops\nBest for: Complete feature implementation, boilerplate",
                    fill_color=LIGHT_PURPLE, text_color=TEXT_DARK,
                    font_size=11, bold=True, border_color=ACCENT_PURPLE,
                    alignment=PP_ALIGN.LEFT)

    add_rounded_box(slide, 0.5, 6.2, 12.3, 0.45,
                    "Practical Tip:  Use Copilot for quick completions  |  Cursor for complex multi-file work  |  Devin for end-to-end tasks",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=13, bold=True,
                    border_color=ACCENT_ORANGE)

    add_notes(slide, """SPEAKER NOTES - Slide 8: IDE Assistants & Code Generation Deep Dive
----------------------------------------------------------------------
This slide goes deeper into the IDE assistant category, which is what most developers interact with daily.

LEFT SIDE - KEY CAPABILITIES:
Walk through each capability with live examples if possible:

1. INLINE CODE COMPLETION: The bread-and-butter feature. As you type, AI suggests completions - sometimes single lines, sometimes entire functions. The suggestions are context-aware, looking at your current file, open files, imports, and variable names. Tip: Write clear function signatures and docstrings FIRST, then let AI complete the implementation.

2. EXPLAIN & DOCUMENT CODE: Select a block of code and ask "explain this." The AI provides a plain-English explanation. Extremely valuable for onboarding to unfamiliar codebases, understanding legacy code, and generating documentation.

3. REFACTORING SUGGESTIONS: AI can suggest renaming variables for clarity, extracting methods, converting imperative code to functional style. This goes beyond simple IDE refactoring because AI understands INTENT, not just syntax.

4. TEST GENERATION: One of the highest-ROI features. Point AI at a method and ask it to generate unit tests. LIMITATION: AI-generated tests may have incorrect assertions if the AI misunderstands the business logic. Always review test assertions.

5. CHAT-IN-EDITOR: Cursor's Composer and Copilot Chat let you describe what you want in natural language and get multi-file edits.

RIGHT SIDE - TOOL COMPARISON:
GITHUB COPILOT: Most mature and widely adopted. Enterprise tier offers organization-level policy controls, code reference tracking, and IP indemnity.
CURSOR: Built specifically for AI-first development. Killer features: codebase indexing, Composer mode, better at complex multi-step tasks.
DEVIN / AI AGENTS: Next evolution - autonomous AI agents that can plan, implement, test, and debug entire features. Still requires significant review.

PRACTICAL GUIDANCE for faculty:
- Start students with Copilot (most accessible, free for students)
- Introduce Cursor for project work requiring multi-file changes
- Discuss Devin/agents as the future direction
- Emphasize that ALL tools require human review""")
    n += 1

    # ── Slide 9: LLM CAPABILITIES & LIMITATIONS ────────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "LLM Capabilities & Limitations", "Tools", n)

    add_rounded_box(slide, 0.5, 1.2, 5.8, 0.5,
                    "What AI Does Well",
                    fill_color=ACCENT_GREEN, text_color=WHITE,
                    font_size=16, bold=True)
    add_bullet_list(slide, 0.6, 1.85, 5.6, 3.2, [
        "Code pattern generation & boilerplate",
        "Test scaffolding from descriptions",
        "Documentation & comment generation",
        "Explaining and summarizing code",
        "Suggesting refactoring approaches",
        "Translating between languages/frameworks",
        "Generating CRUD operations & REST APIs",
        "Regex, SQL queries, config files",
    ], font_size=13, color=TEXT_DARK, bullet_char="\u2713")

    add_rounded_box(slide, 6.9, 1.2, 5.8, 0.5,
                    "What AI Struggles With",
                    fill_color=ACCENT_ORANGE, text_color=WHITE,
                    font_size=16, bold=True)
    add_bullet_list(slide, 7.0, 1.85, 5.6, 3.2, [
        "Novel / unique algorithms",
        "Complex business logic & domain rules",
        "Security guarantees & threat modeling",
        "Large codebase holistic understanding",
        "Up-to-date API knowledge (training cutoff)",
        "Stateful debugging across sessions",
        "Performance optimization trade-offs",
        "Architectural consistency over time",
    ], font_size=13, color=TEXT_DARK, bullet_char="\u2717")

    add_rounded_box(slide, 0.5, 5.2, 12.3, 1.2,
                    "Critical Considerations for AI-Generated Code\n"
                    "\u2022 Context Windows: LLMs have finite context - large codebases exceed their memory\n"
                    "\u2022 Hallucinations: AI may generate plausible but non-existent APIs, libraries, or methods\n"
                    "\u2022 Verification Required: Every AI output must be reviewed, tested, and validated by humans\n"
                    "\u2022 Prompt Sensitivity: Small changes in prompts can dramatically change output quality",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK,
                    font_size=12, bold=True, border_color=ACCENT_ORANGE,
                    alignment=PP_ALIGN.LEFT)

    add_notes(slide, """SPEAKER NOTES - Slide 9: LLM Capabilities & Limitations
----------------------------------------------------------
This is a critical reality-check slide. Faculty need to understand both what AI can and cannot do so they can set appropriate expectations for students.

LEFT SIDE - WHAT AI DOES WELL:
1. CODE PATTERN GENERATION: AI excels at generating standard patterns - design patterns (factory, singleton, observer), framework boilerplate (Spring Boot controllers, React components), and common algorithms.
2. TEST SCAFFOLDING: Given a method signature and description, AI can generate comprehensive test structures: happy path, error cases, boundary conditions.
3. DOCUMENTATION: AI can generate JavaDoc/JSDoc/docstrings, README files, API documentation, and inline comments.
4. EXPLAINING CODE: Paste complex code and ask "explain this." AI will break it down step-by-step. Extremely valuable for teaching.
5. REFACTORING: AI can suggest how to simplify complex methods, extract common logic, apply SOLID principles.
6. LANGUAGE TRANSLATION: Convert Python to Java, SQL to ORM queries, REST to GraphQL.

RIGHT SIDE - WHAT AI STRUGGLES WITH:
1. NOVEL ALGORITHMS: If the problem requires a truly novel algorithm not well-represented in training data, AI will either fail or generate something plausible but wrong.
2. COMPLEX BUSINESS LOGIC: AI may miss domain-specific rules. Domain expertise is still human territory.
3. SECURITY: AI may generate code with SQL injection vulnerabilities, improper authentication, or insecure defaults.
4. LARGE CODEBASE: Current context windows cannot hold an entire enterprise codebase. AI may generate code that conflicts with existing patterns.
5. TRAINING CUTOFF: APIs change. Libraries release new versions. AI may suggest deprecated methods or non-existent API endpoints.

BOTTOM BOX - CRITICAL CONSIDERATIONS:
- Context windows are real constraints
- Hallucinations are common and dangerous
- Every AI output requires human verification - treat AI output like code from a junior developer
- Prompt quality directly affects output quality

Discussion prompt: "Has anyone experienced an AI hallucination in their work? What happened?" This generates great discussion.""")
    n += 1

    # ── Slide 10: PROMPT ENGINEERING FOR SOFTWARE DEVELOPMENT ──────────
    slide = add_slide(prs)
    add_title_bar(slide, "Prompt Engineering for Software Engineering", "Spec-Driven", n)

    add_textbox(slide, 0.5, 1.15, 5.5, 0.4, "Structured Prompt Template", 16, True, ACCENT_GREEN)

    add_code_box(slide, 0.5, 1.6, 6.2, 4.6,
                 "## ROLE\n"
                 "You are a senior backend engineer with\n"
                 "expertise in Spring Boot and REST APIs.\n"
                 "\n"
                 "## CONTEXT\n"
                 "We are building a Task Management API.\n"
                 "Tech stack: Java 17, Spring Boot 3,\n"
                 "PostgreSQL, JUnit 5.\n"
                 "\n"
                 "## TASK\n"
                 "Create the TaskService class that\n"
                 "implements CRUD operations with\n"
                 "validation and error handling.\n"
                 "\n"
                 "## CONSTRAINTS\n"
                 "- Follow SOLID principles\n"
                 "- Use constructor injection\n"
                 "- Throw custom exceptions\n"
                 "- Include input validation\n"
                 "\n"
                 "## OUTPUT FORMAT\n"
                 "- Complete Java class with annotations\n"
                 "- Inline Javadoc comments\n"
                 "- Corresponding unit test class",
                 font_size=10)

    add_textbox(slide, 7.2, 1.15, 5.5, 0.4, "Why Each Section Matters", 16, True, ACCENT_GREEN)

    section_cards = [
        ("Role", "Sets the AI's expertise level and\ndomain knowledge persona", LIGHT_BLUE, ACCENT_BLUE),
        ("Context", "Provides project background, tech\nstack, and architectural decisions", LIGHT_GREEN, ACCENT_GREEN),
        ("Task", "Defines the specific deliverable\nwith clear scope boundaries", LIGHT_ORANGE, ACCENT_ORANGE),
        ("Constraints", "Enforces coding standards, patterns,\nand non-negotiable requirements", LIGHT_PURPLE, ACCENT_PURPLE),
        ("Output Format", "Specifies structure, format, and\ncompleteness expectations", LIGHT_TEAL, ACCENT_TEAL),
    ]
    for i, (title, desc, bg, border) in enumerate(section_cards):
        add_rounded_box(slide, 7.2, 1.65 + i * 0.95, 5.5, 0.8,
                        f"{title}\n{desc}",
                        fill_color=bg, text_color=TEXT_DARK,
                        font_size=12, bold=True, border_color=border,
                        alignment=PP_ALIGN.LEFT)

    add_rounded_box(slide, 0.5, 6.2, 12.3, 0.45,
                    "Golden Rule:  Vague prompts -> vague code  |  Structured prompts -> production-quality code  |  Iterate & refine!",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=13, bold=True,
                    border_color=ACCENT_ORANGE)

    add_notes(slide, """SPEAKER NOTES - Slide 10: Prompt Engineering for Software Engineering
-----------------------------------------------------------------------
This slide bridges general prompt engineering and SOFTWARE-SPECIFIC prompt engineering. The key insight: prompting for code is fundamentally different from prompting for essays or summaries.

THE STRUCTURED PROMPT TEMPLATE:
Walk through each section:

1. ROLE: Setting a role dramatically improves output quality. "You are a senior backend engineer" produces different (better) code than "Write some code." The role establishes expertise level, domain context, and quality expectations.
   Bad: "You are an AI assistant" (too generic)
   Good: "You are a senior Java developer with 10 years of Spring Boot experience, specializing in microservices architecture"

2. CONTEXT: Provide project-specific information: Tech stack and versions (Java 17, not just "Java"), architecture decisions already made, existing code patterns, database choice.
   WHY IT MATTERS: Without context, AI will use its most common training patterns, which may not match your project.

3. TASK: Be specific and bounded. Compare:
   Bad: "Write a service class"
   Good: "Create the TaskService class that implements CRUD operations for Task entities with validation and error handling"

4. CONSTRAINTS: Non-negotiable engineering requirements: coding standards, dependency injection approach, error handling strategy, security requirements.

5. OUTPUT FORMAT: Tell AI exactly what you want back: "Complete class with imports" vs "just the method body", "Include unit tests" vs "code only."

ADVANCED TECHNIQUES:
- CHAIN PROMPTING: Break complex tasks into steps. First: "Design the API contract." Second: "Given this API contract, generate the controller."
- FEW-SHOT EXAMPLES: "Here is an example of our service pattern: [example]. Now generate TaskService following the same pattern."
- ITERATIVE REFINEMENT: Start broad, then narrow. "Generate the service" -> "Add error handling" -> "Add logging" -> "Add caching."

DEMO IDEA: Show the same task prompted two ways - vaguely and with the structured template - and compare the output quality.""")
    n += 1

    # ── Slide 11: SPEC-DRIVEN DEVELOPMENT METHODOLOGY ──────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "Spec-Driven Development: Core Methodology", "Spec-Driven", n)

    add_textbox(slide, 0.5, 1.15, 12, 0.4, "The Spec-Driven Development Flow", 16, True, ACCENT_GREEN)

    flow_steps = [
        ("Requirements", ACCENT_BLUE),
        ("Domain\nModel", ACCENT_GREEN),
        ("API\nContract", ACCENT_ORANGE),
        ("Acceptance\nTests", ACCENT_PURPLE),
        ("Code\nGeneration", ACCENT_TEAL),
        ("Review &\nRefine", ACCENT_BLUE),
    ]
    x_pos = 0.5
    box_w = 1.7
    gap = 0.35
    for i, (label, clr) in enumerate(flow_steps):
        add_rounded_box(slide, x_pos + i * (box_w + gap), 1.65, box_w, 0.85,
                        label, fill_color=clr, text_color=WHITE,
                        font_size=12, bold=True)
        if i < len(flow_steps) - 1:
            add_arrow_right(slide, x_pos + i * (box_w + gap) + box_w + 0.02, 1.92,
                            0.28, 0.01, color=TEXT_MID)

    add_rounded_box(slide, 9.5, 2.65, 3.1, 0.4,
                    "\u21bb  Iterate until spec is reviewable",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK,
                    font_size=10, bold=True, border_color=ACCENT_ORANGE)

    add_textbox(slide, 0.5, 3.2, 12, 0.4, "Key Principles", 16, True, ACCENT_GREEN)

    principles = [
        ("Never start with code generation", [
            "Code is a byproduct of good specifications, not the starting point"
        ]),
        ("First create requirements, domain model, APIs, acceptance tests", [
            "Each artifact feeds the next - requirements inform the domain model, which shapes the API"
        ]),
        ("Use AI to refine ambiguity BEFORE implementation", [
            "Ask AI: 'What edge cases does this requirement miss?' - before writing a single line of code"
        ]),
        ("Generate code only after reviewable specs exist", [
            "If a teammate cannot review your spec and understand the system, it is not ready for generation"
        ]),
        ("Specs are version-controlled alongside code", [
            "Specs live in the same repository, same branch, same PR as the code they describe"
        ]),
    ]
    add_bullet_list(slide, 0.6, 3.65, 7.5, 3.0, principles, font_size=13)

    add_rounded_box(slide, 8.5, 3.65, 4.2, 1.2,
                    "Code-First (Anti-Pattern)\n\"Hey AI, build me a task app\"\n-> Unclear scope, inconsistent logic,\n   missing edge cases, rework",
                    fill_color=LIGHT_ORANGE, text_color=TEXT_DARK,
                    font_size=11, bold=True, border_color=ACCENT_ORANGE,
                    alignment=PP_ALIGN.LEFT)

    add_rounded_box(slide, 8.5, 5.05, 4.2, 1.2,
                    "Spec-First (Best Practice)\nRequirements -> Domain -> API -> Tests\n-> Clear scope, verified logic,\n   predictable, reviewable output",
                    fill_color=LIGHT_GREEN, text_color=TEXT_DARK,
                    font_size=11, bold=True, border_color=ACCENT_GREEN,
                    alignment=PP_ALIGN.LEFT)

    add_notes(slide, """SPEAKER NOTES - Slide 11: Spec-Driven Development: Core Methodology
----------------------------------------------------------------------
This is one of the most important slides in the entire workshop. Spec-driven development is the METHODOLOGY that makes AI-native development reliable and repeatable.

THE FLOW DIAGRAM:
Walk through each step and explain why the ORDER matters:

1. REQUIREMENTS: Start with structured requirements. Not "build a todo app" but specific functional and non-functional requirements with acceptance criteria.

2. DOMAIN MODEL: Define the core entities, their attributes, relationships, and business rules. For a Task Management system: Task (id, title, description, status, priority, assignee, due_date). Status transitions: OPEN -> IN_PROGRESS -> DONE.

3. API CONTRACT: Define endpoints, HTTP methods, request/response formats, status codes, and error responses. Use OpenAPI/Swagger format.

4. ACCEPTANCE TESTS: Write test scenarios BEFORE code. "Given a user with create permission, when they POST a valid task, then the response is 201 and the task appears in GET /tasks."

5. CODE GENERATION: NOW - and only now - feed the spec to AI and generate implementation. Output quality is dramatically better with a clear spec.

6. REVIEW & REFINE: Review generated code against the spec. Does it implement all requirements? Do all acceptance tests pass?

KEY PRINCIPLES:
"NEVER START WITH CODE GENERATION" - This is the number one mistake. Demo: Show what happens when you just say "build a task API" to an LLM vs when you provide a structured spec. The difference in output quality is dramatic.

RIGHT SIDE COMPARISON:
The Code-First anti-pattern produces: unclear scope, inconsistent logic, missing edge cases, and expensive rework.
The Spec-First approach produces: clear scope, verified logic, predictable output, and reviewable artifacts at every stage.""")
    n += 1

    # ── Slide 12: SDD STRUCTURE & TEMPLATE ─────────────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "Software Design Document (SDD) Structure", "Spec-Driven", n)

    sdd_sections = [
        ("1", "Overview", "Purpose, scope, definitions,\nstakeholders, glossary", LIGHT_BLUE, ACCENT_BLUE),
        ("2", "Functional Requirements", "Features, user stories, actors,\nbusiness rules, use cases", LIGHT_GREEN, ACCENT_GREEN),
        ("3", "Non-Functional Reqs", "Performance targets, security\npolicies, scalability, SLAs", LIGHT_ORANGE, ACCENT_ORANGE),
        ("4", "Architecture & Design", "System diagrams, patterns,\ndecision records (ADRs)", LIGHT_PURPLE, ACCENT_PURPLE),
        ("5", "API Contracts", "Endpoints, request/response\nschemas, status codes, errors", LIGHT_TEAL, ACCENT_TEAL),
        ("6", "Data Model", "Entities, relationships,\nconstraints, migrations", LIGHT_YELLOW, ACCENT_ORANGE),
        ("7", "Test Strategy", "Unit, integration, E2E tests,\nacceptance criteria, coverage", LIGHT_GREEN, ACCENT_GREEN),
        ("8", "Deployment & CI/CD", "Pipeline stages, environments,\nrollback, monitoring", LIGHT_BLUE, ACCENT_BLUE),
    ]

    col1_x = 0.5
    col2_x = 6.7
    card_w = 5.8
    card_h = 1.1
    start_y = 1.2

    for i, (num, title, desc, bg, border) in enumerate(sdd_sections):
        col = i % 2
        row = i // 2
        x = col1_x if col == 0 else col2_x
        y = start_y + row * (card_h + 0.15)
        add_rounded_box(slide, x, y, card_w, card_h,
                        f"Section {num}: {title}\n{desc}",
                        fill_color=bg, text_color=TEXT_DARK,
                        font_size=12, bold=True, border_color=border,
                        alignment=PP_ALIGN.LEFT)

    add_rounded_box(slide, 0.5, 6.2, 12.3, 0.45,
                    "Principle:  The SDD is the single source of truth - AI generates code FROM the SDD, not the other way around",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=13, bold=True,
                    border_color=ACCENT_ORANGE)

    add_notes(slide, """SPEAKER NOTES - Slide 12: Software Design Document (SDD) Structure
----------------------------------------------------------------------
This slide provides the concrete template that participants will use in the practical exercise.

SECTION 1 - OVERVIEW: Purpose, scope, definitions, stakeholders. Provides context that shapes all AI-generated output.

SECTION 2 - FUNCTIONAL REQUIREMENTS: Features listed with acceptance criteria, user stories, actors and permissions, business rules and validation constraints. These directly map to controller endpoints, service methods, and test cases.

SECTION 3 - NON-FUNCTIONAL REQUIREMENTS: Performance targets ("API response time < 200ms at P95"), security policies, scalability targets, availability SLAs. These shape architectural decisions.

SECTION 4 - ARCHITECTURE & DESIGN: High-level system architecture, technology choices with rationale, design patterns, Architecture Decision Records (ADRs).

SECTION 5 - API CONTRACTS: REST endpoints with HTTP methods, paths, descriptions. Request/response schemas with validation rules. Error response formats. Auth requirements per endpoint.

SECTION 6 - DATA MODEL: Entity definitions with attributes and data types. Relationships, constraints, foreign keys. Database migration strategy.

SECTION 7 - TEST STRATEGY: Unit test scope and coverage targets. Integration test approach. E2E test scenarios. Acceptance criteria mapped to test cases.

SECTION 8 - DEPLOYMENT & CI/CD: Pipeline stages, environment definitions, rollback strategy, monitoring configuration.

IMPORTANT: Emphasize that students should fill in EVERY section before generating code. Incomplete SDDs produce incomplete code.""")
    n += 1

    # ── Slide 13: EXAMPLE REQUIREMENT SPECIFICATION ────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "Example: Task Management API Specification", "Spec-Driven", n)

    add_textbox(slide, 0.5, 1.15, 6.0, 0.35, "Specification Excerpt", 16, True, ACCENT_GREEN)

    add_code_box(slide, 0.5, 1.55, 6.2, 3.0,
                 "Feature: Task Management\n"
                 "  Create and manage tasks with priority\n"
                 "  and status tracking.\n"
                 "\n"
                 "Actors:\n"
                 "  - Admin: Full CRUD, assign tasks, manage users\n"
                 "  - User:  Create, view, update own tasks\n"
                 "\n"
                 "Functional Rules:\n"
                 "  FR-1: Task title is required (3-100 chars)\n"
                 "  FR-2: Priority: LOW, MEDIUM, HIGH, CRITICAL\n"
                 "  FR-3: Status: OPEN -> IN_PROGRESS -> DONE\n"
                 "  FR-4: Only Admin can delete tasks\n"
                 "  FR-5: Due date must be in the future\n"
                 "  FR-6: Assignee must be a valid user",
                 font_size=10)

    add_textbox(slide, 0.5, 4.7, 6.0, 0.35, "Acceptance Criteria (BDD Format)", 14, True, ACCENT_GREEN)

    add_code_box(slide, 0.5, 5.1, 6.2, 1.45,
                 "Scenario: Create a valid task\n"
                 "  Given an authenticated User\n"
                 "  When  POST /api/tasks with valid body:\n"
                 "        {title, description, priority}\n"
                 "  Then  response status is 201\n"
                 "  And   response contains task with id\n"
                 "  And   task status defaults to OPEN",
                 font_size=10)

    add_textbox(slide, 7.2, 1.15, 5.5, 0.35, "How This Spec Drives Development", 16, True, ACCENT_GREEN)

    feed_cards = [
        ("Domain Model", "Task entity with title, description,\nstatus, priority, assignee, dueDate\n+ Status enum + Priority enum", LIGHT_BLUE, ACCENT_BLUE),
        ("API Contract", "POST /api/tasks -> 201 Created\nGET  /api/tasks -> 200 + List\nPUT  /api/tasks/{id} -> 200\nDEL  /api/tasks/{id} -> 204 (Admin)", LIGHT_GREEN, ACCENT_GREEN),
        ("Generated Tests", "testCreateTask_ValidInput_201()\ntestCreateTask_MissingTitle_400()\ntestDeleteTask_NonAdmin_403()\ntestStatusTransition_Valid()", LIGHT_PURPLE, ACCENT_PURPLE),
        ("Code Generation", "TaskController -> TaskService ->\nTaskRepository -> Task entity\n+ DTOs + Validation + Exceptions", LIGHT_ORANGE, ACCENT_ORANGE),
    ]
    for i, (title, desc, bg, border) in enumerate(feed_cards):
        add_rounded_box(slide, 7.2, 1.6 + i * 1.3, 5.5, 1.15,
                        f"{title}\n{desc}",
                        fill_color=bg, text_color=TEXT_DARK,
                        font_size=11, bold=True, border_color=border,
                        alignment=PP_ALIGN.LEFT)

    add_arrow_right(slide, 6.75, 3.5, 0.4, 0.01, color=ACCENT_GREEN)

    add_notes(slide, """SPEAKER NOTES - Slide 13: Example Task Management API Specification
----------------------------------------------------------------------
This slide is the bridge to the practical exercise. It shows a CONCRETE, REALISTIC specification.

LEFT SIDE - THE SPECIFICATION:
Walk through each element:

FEATURE DESCRIPTION: "Create and manage tasks with priority and status tracking." One-sentence summary.

ACTORS: Two roles with different permissions:
- Admin: Full CRUD plus administrative actions
- User: Can create tasks, view all tasks, update own tasks
NOTE: Ask the audience - "Should users see ALL tasks or only their own? This is exactly the kind of ambiguity that specs should resolve BEFORE coding."

FUNCTIONAL RULES (FR-1 through FR-6):
- FR-1 (Title validation): 3-100 characters. These numbers are design decisions that should be in the spec.
- FR-2 (Priority enum): Exactly four values. This generates an enum class and validation logic.
- FR-3 (Status transitions): OPEN -> IN_PROGRESS -> DONE. Ask: "Can a task go from DONE back to IN_PROGRESS?"
- FR-4 (Delete permission): Only Admin can delete. Generates authorization checks.
- FR-5 (Due date validation): Must be in the future. Generates validation logic.
- FR-6 (Assignee validation): Must be a valid user. Creates foreign key relationship.

ACCEPTANCE CRITERIA (BDD Format):
Behavior-Driven Development format: Given/When/Then. Maps directly to test methods.

RIGHT SIDE - HOW THE SPEC DRIVES DEVELOPMENT:
1. DOMAIN MODEL: Spec defines Task entity attributes and enums
2. API CONTRACT: From actors and rules, we derive endpoints
3. GENERATED TESTS: From acceptance criteria, AI generates test methods
4. CODE GENERATION: With all above defined, AI generates the full stack

TRANSITION: "In our practical exercise, you will take this specification, expand it, and use it to generate a working API."
""")
    n += 1

    return n

if __name__ == "__main__":
    prs = new_presentation()
    build(prs)
    save_deck(prs, "_part2_tools_spec.pptx")
