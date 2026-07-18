"""Part 5 – Multi-Agent, Governance, Closing & Backup (Slides 33-50)"""
from slide_helpers import *

def build(prs, start_num=33):
    n = start_num

    # ── Slide 33: MULTI-AGENT DEVELOPMENT ARCHITECTURE ─────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "Multi-Agent AI Development: Architecture", "Multi-Agent", n)

    # Center hub: Orchestrator
    cx, cy = 4.5, 3.5
    add_rounded_box(slide, cx - 1.0, cy - 0.45, 2.0, 0.9,
                    "Orchestrator\n(Planner + Memory)",
                    fill_color=TITLE_BAR, text_color=WHITE, font_size=12, bold=True)

    # 6 agent boxes around the hub
    agents = [
        ("Requirements\nAgent", LIGHT_BLUE,   1.5, 1.6),
        ("Architect\nAgent",    LIGHT_GREEN,   4.5, 1.3),
        ("Coding\nAgent",       LIGHT_ORANGE,  7.3, 1.6),
        ("Testing\nAgent",      LIGHT_YELLOW,  7.3, 4.8),
        ("Security\nAgent",     LIGHT_PURPLE,  4.5, 5.3),
        ("DevOps\nAgent",       LIGHT_TEAL,    1.5, 4.8),
    ]
    for label, color, ax, ay in agents:
        add_rounded_box(slide, ax - 0.75, ay, 1.5, 0.75, label,
                        fill_color=color, text_color=TEXT_DARK, font_size=10, bold=True)
        # Connector line from agent center to orchestrator center
        agent_cx = ax
        agent_cy = ay + 0.375
        orch_cx = cx
        orch_cy = cy
        add_connector_line(slide, agent_cx, agent_cy, orch_cx, orch_cy,
                           color=ACCENT_BLUE, width=1.5)

    # Right side: key points
    add_textbox(slide, 8.8, 1.3, 4.2, 0.4, "Why Multi-Agent?", 16, True, ACCENT_PURPLE)
    add_bullet_list(slide, 8.8, 1.8, 4.2, 4.5, [
        "Specialized agents excel at focused tasks",
        "Orchestrator coordinates workflow & resolves conflicts",
        "Shared memory enables context across agents",
        "Parallel execution accelerates the SDLC",
        "Human checkpoints at critical decision points",
        "Each agent has its own tools & permissions",
    ], font_size=13)

    add_notes(slide, """SPEAKER NOTES – Slide 33: Multi-Agent AI Development Architecture
--------------------------------------------------------------------
This slide introduces the concept of multi-agent AI development, which represents the next evolution of AI-native software engineering.

WHAT IS MULTI-AGENT DEVELOPMENT?
Multi-agent development uses multiple specialized AI agents, each responsible for a distinct phase of the software development lifecycle, coordinated by a central orchestrator. Think of it like a well-organized engineering team — except the team members are AI agents with specialized capabilities.

WHY CAN'T A SINGLE LLM DO EVERYTHING?
1. Context window limitations — a single LLM can't hold an entire codebase, all test results, security reports, and deployment configs simultaneously.
2. Specialization — an agent fine-tuned or prompted for security analysis performs better than a general-purpose LLM doing security review.
3. Tool access — different agents need different tools (code editor, test runner, CI/CD system, security scanner).
4. Accountability — when agents have clear boundaries, it's easier to audit what happened and why.

ORCHESTRATION PATTERNS:
- Sequential: agents work in order (requirements -> architecture -> code -> test -> security -> deploy)
- Parallel: independent agents work simultaneously (security and testing run in parallel)
- Iterative: agents loop until quality criteria are met (test agent sends failures back to coding agent)
- Human-gated: certain transitions require human approval (architecture decisions, deployment to production)

REAL-WORLD EXAMPLES:
- Microsoft AutoGen: framework for building multi-agent conversations
- CrewAI: role-based multi-agent orchestration with memory
- LangGraph: graph-based agent orchestration
- Custom solutions: many organizations build bespoke multi-agent pipelines using LLM APIs + tool calling

CHALLENGES:
- Coordination overhead: agents must share context without losing information
- Conflict resolution: what if the coding agent and security agent disagree?
- Cost management: multiple LLM calls add up quickly
- Debugging: tracing issues across multiple agent interactions is complex
- Determinism: ensuring reproducible results across agent runs

This is the future direction of AI-native development — moving from single-prompt interactions to orchestrated multi-agent workflows.""")
    n += 1

    # ── Slide 34: AGENT ROLES & ORCHESTRATION WORKFLOW ─────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "Agent Roles & Orchestration Workflow", "Multi-Agent", n)

    # Horizontal workflow at top
    workflow_items = [
        ("User\nRequest",       ACCENT_BLUE),
        ("Requirements\nAgent", ACCENT_GREEN),
        ("Architect\nAgent",    ACCENT_ORANGE),
        ("Coding\nAgent",       ACCENT_PURPLE),
        ("Testing\nAgent",      ACCENT_GREEN),
        ("Security\nAgent",     ACCENT_TEAL),
        ("DevOps\nAgent",       ACCENT_ORANGE),
        ("Deployed\nSystem",    ACCENT_BLUE),
    ]
    x_pos = 0.35
    for i, (label, clr) in enumerate(workflow_items):
        add_rounded_box(slide, x_pos, 1.25, 1.35, 0.7, label,
                        fill_color=clr, text_color=WHITE, font_size=9, bold=True)
        if i < len(workflow_items) - 1:
            add_arrow_right(slide, x_pos + 1.37, 1.42, 0.2, 0.01, color=TEXT_MID)
        x_pos += 1.57

    # Table: Agent, Responsibility, Output Artifacts
    rows = [
        ["Agent", "Responsibility", "Output Artifacts"],
        ["Requirements Agent", "Clarifies scope, acceptance criteria", "Requirement doc, acceptance tests"],
        ["Architect Agent", "Proposes design, evaluates trade-offs", "Architecture diagrams, ADRs"],
        ["Coding Agent", "Implements features from specs", "Source code, unit tests"],
        ["Testing Agent", "Validates correctness & coverage", "Test results, coverage report"],
        ["Security Agent", "Reviews for vulnerabilities", "Security report, fixes"],
        ["DevOps Agent", "Automates build & deployment", "CI/CD pipeline, deploy config"],
    ]
    add_table_shape(slide, 0.4, 2.3, 12.5, 4.2, rows, 3,
                    row_colors=[LIGHT_BLUE, LIGHT_GREEN, LIGHT_ORANGE,
                                LIGHT_YELLOW, LIGHT_PURPLE, LIGHT_TEAL])

    add_notes(slide, """SPEAKER NOTES – Slide 34: Agent Roles & Orchestration Workflow
-----------------------------------------------------------------
This slide maps each agent to its specific responsibilities and outputs. Walk through the workflow from left to right.

THE FLOW:
1. USER REQUEST: A human provides the initial intent — "Build a task management API" or "Add authentication to the existing service."
2. REQUIREMENTS AGENT: Takes the vague request and produces a structured specification. It asks clarifying questions, identifies edge cases, writes acceptance criteria. Output: a formal requirements document and draft acceptance tests.
3. ARCHITECT AGENT: Takes the requirements and proposes a system design. It evaluates trade-offs (monolith vs. microservice, SQL vs. NoSQL, REST vs. GraphQL) and documents decisions. Output: architecture diagrams, API contracts, Architecture Decision Records (ADRs).
4. CODING AGENT: Takes the approved architecture and specs and generates implementation code. It follows established patterns, naming conventions, and project structure. Output: source code files and unit tests.
5. TESTING AGENT: Runs the generated tests, analyzes coverage, identifies gaps. It may generate additional tests for edge cases not covered. Output: test results, coverage reports, quality metrics.
6. SECURITY AGENT: Scans the code for vulnerabilities — SQL injection, XSS, insecure dependencies, exposed secrets. It proposes fixes for any issues found. Output: security analysis report and remediation code.
7. DEVOPS AGENT: Creates or updates the CI/CD pipeline, Dockerfiles, Kubernetes manifests, and deployment configurations. Output: CI/CD configs, infrastructure-as-code, deployment scripts.
8. DEPLOYED SYSTEM: The final output — a running, tested, secured, and deployed application.

HOW THE ORCHESTRATOR COORDINATES:
- Maintains a shared memory/context that all agents can read from
- Decides when to hand off from one agent to the next
- Implements quality gates — e.g., code can't go to security review until tests pass
- Handles iteration — if the testing agent finds failures, the orchestrator routes them back to the coding agent
- Logs every decision for audit trail

HUMAN CHECKPOINTS:
- After requirements (approve scope)
- After architecture (approve design decisions)
- After security review (approve deployment)
These are non-negotiable in production workflows.""")
    n += 1

    # ── Slide 35: MODEL CONTEXT PROTOCOL & AGENT COMMUNICATION ─────────
    slide = add_slide(prs)
    add_title_bar(slide, "Model Context Protocol & Tool Integration", "Multi-Agent", n)

    # Left column: MCP explanation
    add_textbox(slide, 0.6, 1.3, 5.5, 0.4, "What is MCP?", 18, True, ACCENT_PURPLE)
    add_bullet_list(slide, 0.6, 1.8, 5.5, 2.5, [
        "Standardized protocol for agent-tool communication",
        "Agents request controlled access to external tools",
        "Permissioned, auditable actions on real systems",
        "Context optimization — agents get only relevant data",
        "Enables multi-agent collaboration via shared context",
    ], font_size=14)

    # Visual: Agent <-> MCP Server <-> Tools
    add_rounded_box(slide, 0.8, 4.6, 1.8, 0.8, "AI Agent\n(LLM + Prompt)",
                    fill_color=ACCENT_BLUE, text_color=WHITE, font_size=11, bold=True)
    add_arrow_right(slide, 2.65, 4.8, 0.5, 0.01, color=ACCENT_BLUE)
    add_rounded_box(slide, 3.2, 4.4, 2.2, 1.2, "MCP Server\n(Protocol Layer)\nAuth + Routing",
                    fill_color=ACCENT_PURPLE, text_color=WHITE, font_size=11, bold=True)
    add_arrow_right(slide, 5.45, 4.8, 0.5, 0.01, color=ACCENT_PURPLE)

    # Tool boxes
    tools_list = [
        ("Git / GitHub", LIGHT_BLUE),
        ("Jira / Linear", LIGHT_GREEN),
        ("Jenkins / CI", LIGHT_ORANGE),
        ("Database", LIGHT_YELLOW),
    ]
    for i, (tool_name, clr) in enumerate(tools_list):
        add_rounded_box(slide, 6.1, 4.15 + i * 0.45, 1.6, 0.38, tool_name,
                        fill_color=clr, text_color=TEXT_DARK, font_size=9, bold=True)

    # Right column: Key principles & context
    add_textbox(slide, 8.2, 1.3, 4.8, 0.4, "Key MCP Principles", 16, True, ACCENT_PURPLE)
    principle_cards = [
        ("Permissioned Access", "Each agent gets only the tools\nit needs — principle of least privilege", LIGHT_BLUE, ACCENT_BLUE),
        ("Auditable Actions", "Every tool call is logged with\nagent identity, timestamp, and result", LIGHT_GREEN, ACCENT_GREEN),
        ("Context Optimization", "Agents receive curated context\nnot entire codebases — reduces cost", LIGHT_ORANGE, ACCENT_ORANGE),
        ("Tool Discovery", "Agents can discover available\ntools and their capabilities at runtime", LIGHT_PURPLE, ACCENT_PURPLE),
    ]
    for i, (t, d, bg, bdr) in enumerate(principle_cards):
        add_rounded_box(slide, 8.2, 1.8 + i * 1.2, 4.8, 1.0,
                        f"{t}\n{d}", fill_color=bg, text_color=TEXT_DARK,
                        font_size=11, bold=True, border_color=bdr)

    add_notes(slide, """SPEAKER NOTES – Slide 35: Model Context Protocol & Tool Integration
----------------------------------------------------------------------
This slide explains the Model Context Protocol (MCP) and why it's critical for multi-agent AI development.

WHAT IS MCP?
MCP is a standardized protocol (pioneered by Anthropic) that defines how AI models/agents connect to external tools and data sources. Think of it as a USB-C for AI — a universal interface that allows any AI agent to connect to any compatible tool.

Without MCP, every agent-tool integration is custom — you'd write separate code for each AI model to talk to each tool. MCP standardizes this with a clean client-server architecture.

HOW IT WORKS:
1. The AI agent (client) connects to an MCP server
2. The server exposes available tools (e.g., "read_file", "create_issue", "run_tests")
3. The agent discovers tools and their schemas
4. The agent makes tool calls through the protocol
5. The server executes actions and returns results
6. All interactions are logged for audit

WHY IT MATTERS FOR MULTI-AGENT WORKFLOWS:
- Different agents need different tools — the Requirements Agent needs Jira access, the Coding Agent needs the code editor, the DevOps Agent needs CI/CD systems
- MCP provides a uniform interface so you don't have to build custom integrations for each agent-tool pair
- Permissions can be set per-agent — the Testing Agent shouldn't be able to deploy to production
- Shared context servers allow agents to pass information to each other without expensive LLM-to-LLM conversations

PRACTICAL SETUP:
- MCP servers can be local (filesystem access, local databases) or remote (GitHub API, cloud services)
- Configuration is typically done via JSON config files that map tools to servers
- Popular MCP servers exist for: GitHub, GitLab, Slack, PostgreSQL, filesystem, web search
- You can build custom MCP servers for your organization's internal tools

ANTHROPIC'S MCP PROTOCOL:
- Open-source specification (github.com/modelcontextprotocol)
- Adopted by Claude, Cursor, Windsurf, and other AI development tools
- Growing ecosystem of community-built MCP servers
- Represents the emerging standard for agent-tool communication

This is important for faculty to understand because it shows how AI agents will interact with real-world systems — not just generate text, but actually take actions in the development pipeline.""")
    n += 1

    # ── Slide 36: AI GOVERNANCE FRAMEWORK ──────────────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "AI Governance Framework for Software Development", "Governance", n)

    # Layered pyramid (bottom to top, widest at bottom)
    pyramid_layers = [
        ("Policies & Standards",         LIGHT_BLUE,   0.8, 5.4, 5.8, 0.7),
        ("Data Protection & Privacy",    LIGHT_GREEN,  1.4, 4.6, 4.6, 0.7),
        ("Model Management & Validation",LIGHT_ORANGE, 2.0, 3.8, 3.4, 0.7),
        ("Human Review & Oversight",     LIGHT_PURPLE, 2.6, 3.0, 2.2, 0.7),
        ("Audit Trail &\nAccountability",LIGHT_YELLOW, 3.1, 2.2, 1.2, 0.7),
    ]
    for label, color, lft, tp, w, h in pyramid_layers:
        add_rounded_box(slide, lft, tp, w, h, label,
                        fill_color=color, text_color=TEXT_DARK, font_size=11, bold=True)

    # Right side: governance checklist
    add_textbox(slide, 7.5, 1.3, 5.3, 0.4, "Governance Checklist", 16, True, ACCENT_BLUE)
    add_bullet_list(slide, 7.5, 1.8, 5.3, 4.8, [
        "Establish AI usage policies for development teams",
        "Define data handling rules for prompts & outputs",
        "Validate AI models against bias & accuracy benchmarks",
        "Require human review at architectural decisions",
        "Log all AI interactions for audit & compliance",
        "Set up feedback loops for continuous improvement",
        "Train teams on responsible AI practices",
        "Define escalation procedures for AI failures",
        "Review AI tools for license & IP compliance",
        "Conduct regular governance framework reviews",
    ], font_size=12)

    add_notes(slide, """SPEAKER NOTES – Slide 36: AI Governance Framework for Software Development
------------------------------------------------------------------------------
This is one of the most important slides in the entire workshop. As AI becomes embedded in software development, governance is not optional — it's a necessity.

THE PYRAMID FRAMEWORK (bottom to top):

1. POLICIES & STANDARDS (Base Layer):
- Every organization needs a clear AI usage policy: what tools are approved, what data can be shared with AI services, what review processes are required
- Standards define: coding conventions for AI-generated code, documentation requirements, testing minimums, security baselines
- This is the foundation — without clear policies, individual teams will make inconsistent decisions

2. DATA PROTECTION & PRIVACY:
- What data can be included in prompts? Can you paste production data into an AI chat?
- GDPR, CCPA, HIPAA implications — AI services may store prompts and outputs
- Sensitive data (API keys, credentials, PII) must NEVER appear in prompts
- Consider on-premises or private AI deployments for sensitive projects

3. MODEL MANAGEMENT & VALIDATION:
- Which AI models are approved for use? (Not all models are equal in quality or safety)
- How do you validate that AI outputs meet quality standards?
- Version control for prompts and AI configurations
- Benchmark AI performance on your specific domain/codebase

4. HUMAN REVIEW & OVERSIGHT:
- Define which decisions require human approval (architecture, security, deployment)
- Establish review workflows — who reviews AI-generated code, how is it tracked?
- Set clear accountability — if AI-generated code causes a production incident, who is responsible?
- Create escalation paths for when AI outputs are uncertain or conflicting

5. AUDIT TRAIL & ACCOUNTABILITY (Top Layer):
- Every AI interaction should be logged: what was asked, what was generated, who approved it
- Audit trails enable: post-incident analysis, compliance reporting, continuous improvement
- Traceability from requirement to spec to code to test to deployment

REGULATORY CONSIDERATIONS:
- EU AI Act — classifies AI systems by risk level; development tools may fall under various categories
- Industry-specific regulations (healthcare, finance, government) may impose additional requirements
- Export controls and data residency requirements affect which AI services you can use
- Intellectual property questions: who owns AI-generated code? (Currently a legal gray area)

ORGANIZATIONAL POLICIES:
- Start small: begin with a pilot team, iterate on governance processes, then expand
- Appoint an AI governance champion or committee
- Regular training and awareness programs
- Quarterly reviews of governance effectiveness""")
    n += 1

    # ── Slide 37: RESPONSIBLE AI PRINCIPLES & ETHICS ───────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "Responsible AI Principles in Practice", "Governance", n)

    # 6 principle cards in 2 rows of 3
    principles_data = [
        ("Fairness", "Avoid biased assumptions\nin generated systems", LIGHT_BLUE, ACCENT_BLUE),
        ("Reliability", "Validate outputs with\ntests and evidence", LIGHT_GREEN, ACCENT_GREEN),
        ("Privacy", "Minimize sensitive data\nexposure in prompts", LIGHT_ORANGE, ACCENT_ORANGE),
        ("Transparency", "Document AI usage,\nlimitations & decisions", LIGHT_PURPLE, ACCENT_PURPLE),
        ("Accountability", "Maintain audit trails,\nassign ownership", LIGHT_TEAL, ACCENT_TEAL),
        ("Safety", "Implement guardrails,\nhuman oversight, rollback", LIGHT_YELLOW, ACCENT_ORANGE),
    ]
    for i, (title, desc, bg, bdr) in enumerate(principles_data):
        col = i % 3
        row = i // 3
        lft = 0.6 + col * 4.15
        tp = 1.3 + row * 2.0
        add_rounded_box(slide, lft, tp, 3.8, 1.6,
                        f"{title}\n\n{desc}",
                        fill_color=bg, text_color=TEXT_DARK, font_size=13, bold=True,
                        border_color=bdr)

    # Bottom: Academic Integrity
    add_rounded_box(slide, 0.6, 5.6, 12.1, 0.9,
                    "Academic Integrity:  Define clear policies on AI use in assignments  |  "
                    "Teach students WHEN and HOW to use AI responsibly  |  "
                    "Assess understanding, not just output",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=12, bold=True,
                    border_color=ACCENT_ORANGE)

    add_notes(slide, """SPEAKER NOTES – Slide 37: Responsible AI Principles in Practice
------------------------------------------------------------------
Walk through each principle and connect it specifically to software engineering practice:

1. FAIRNESS:
- AI models can embed biases from training data. Generated code may make assumptions about user demographics, language, accessibility needs.
- Example: An AI-generated user registration form might default to "Mr/Mrs" titles — excluding non-binary options.
- Mitigation: Include diversity and accessibility requirements in your specifications. Review generated UIs for inclusive design.
- In teaching: Use biased AI outputs as teaching moments. Have students analyze AI-generated code for implicit assumptions.

2. RELIABILITY:
- AI-generated code can look correct but contain subtle logic errors, edge case failures, or hallucinated API calls.
- Every AI output must be validated through testing — unit tests, integration tests, property-based tests.
- Example: AI might generate a function that works for typical inputs but fails for empty arrays, negative numbers, or unicode strings.
- In teaching: Emphasize that "AI generated it" is never a valid acceptance criterion. Tests and evidence are the standard.

3. PRIVACY:
- Developers often paste code snippets, error messages, and data samples into AI prompts. This can inadvertently expose sensitive information.
- Production database queries, API keys, customer data, and proprietary algorithms should NEVER appear in AI prompts.
- Use sanitized examples and mock data when working with AI.
- In teaching: Establish classroom rules about what data can be shared with AI tools.

4. TRANSPARENCY:
- Document when and how AI was used in development. Include AI attribution in code comments, PR descriptions, and documentation.
- Be transparent about AI limitations — generated code may not handle all edge cases, may not be optimized for performance.
- In teaching: Require students to document their AI interactions — what they asked, what they got, what they changed and why.

5. ACCOUNTABILITY:
- When AI-generated code causes a production incident, someone must be accountable.
- Audit trails track: who requested the generation, what prompt was used, who reviewed and approved the output.
- In organizations: establish clear ownership — the developer who approves AI-generated code owns its behavior.
- In teaching: Teach students that using AI doesn't absolve them of responsibility for their code.

6. SAFETY:
- Implement guardrails: code review requirements, automated security scanning, deployment approval gates.
- Have rollback plans — if AI-generated code causes issues in production, can you quickly revert?
- In teaching: Discuss real-world AI failures and their consequences. Safety is not theoretical.

ACADEMIC INTEGRITY SECTION:
This is critical for faculty. Discussion points:
- How do you assess student work when AI can generate most of it?
- Strategy 1: Assess understanding through oral explanations, code walkthroughs, and modification exercises
- Strategy 2: Focus on specification quality, not just code output
- Strategy 3: Require process documentation — the AI conversation log, revision history, decision rationale
- Strategy 4: Design assessments that require contextual judgment AI cannot provide""")
    n += 1

    # ── Slide 38: ORGANIZATIONAL ADOPTION & MATURITY MODEL ─────────────
    slide = add_slide(prs)
    add_title_bar(slide, "AI-Native Adoption Maturity Model", "Governance", n)

    # Staircase maturity model (ascending boxes)
    levels = [
        ("Level 1: Ad-hoc", "Individual developers\nuse AI informally",
         LIGHT_BLUE, ACCENT_BLUE, 0.6, 5.1, 2.2, 1.0),
        ("Level 2: Experimentation", "Teams pilot AI tools\non selected projects",
         LIGHT_GREEN, ACCENT_GREEN, 2.9, 4.3, 2.2, 1.0),
        ("Level 3: Standardized", "AI practices formalized,\ngovernance in place",
         LIGHT_ORANGE, ACCENT_ORANGE, 5.2, 3.5, 2.2, 1.0),
        ("Level 4: Optimized", "AI deeply embedded,\nmulti-agent workflows",
         LIGHT_PURPLE, ACCENT_PURPLE, 7.5, 2.7, 2.2, 1.0),
        ("Level 5: Transformational", "AI-native is default,\nculture shift & innovation",
         LIGHT_YELLOW, ACCENT_ORANGE, 9.8, 1.9, 2.2, 1.0),
    ]
    for title, desc, bg, bdr, lft, tp, w, h in levels:
        add_rounded_box(slide, lft, tp, w, h,
                        f"{title}\n{desc}",
                        fill_color=bg, text_color=TEXT_DARK, font_size=10, bold=True,
                        border_color=bdr)

    # Connecting arrows between levels
    for i in range(len(levels) - 1):
        _, _, _, _, lft, tp, w, h = levels[i]
        _, _, _, _, lft2, tp2, _, _ = levels[i + 1]
        add_arrow_right(slide, lft + w + 0.02, tp + 0.2, 0.55, 0.01, color=TEXT_MID)

    # Bottom: what it takes at each level
    add_rounded_box(slide, 0.6, 6.2, 11.7, 0.5,
                    "Progression requires:  Training & Skills  >>  Tool Adoption  >>  "
                    "Policy & Governance  >>  Culture Shift  >>  Organizational Transformation",
                    fill_color=LIGHT_BLUE, text_color=TEXT_DARK, font_size=12, bold=True,
                    border_color=ACCENT_BLUE)

    add_notes(slide, """SPEAKER NOTES – Slide 38: AI-Native Adoption Maturity Model
--------------------------------------------------------------
This maturity model helps organizations (and academic institutions) assess where they are and plan their AI-native adoption journey.

LEVEL 1 - AD-HOC:
- Individual developers use ChatGPT, Copilot, or similar tools on their own initiative
- No organizational policy or standardization
- Benefits are inconsistent — some developers see productivity gains, others don't
- Risks: no governance, potential data leaks, inconsistent code quality
- What's needed to advance: awareness training, initial tool evaluation

LEVEL 2 - EXPERIMENTATION:
- Teams formally pilot AI tools on selected projects
- Some measurement of benefits (productivity, quality, speed)
- Initial guidelines emerging (which tools are approved, basic data handling rules)
- Risks: pilots may not represent broader use; success metrics may be biased
- What's needed: formal evaluation framework, pilot results documentation, initial policies

LEVEL 3 - STANDARDIZED:
- AI-native practices are documented and formalized across the organization
- Governance framework in place: approved tools, data policies, review requirements
- Training programs for all developers
- Consistent workflows: spec-driven development, automated testing, CI/CD integration
- What's needed: measurement systems, feedback loops, governance reviews

LEVEL 4 - OPTIMIZED:
- AI is deeply embedded in every phase of development
- Multi-agent workflows are in production
- Continuous measurement and optimization of AI impact
- Advanced governance: automated compliance checks, AI-assisted code review
- What's needed: cultural change, organizational restructuring, advanced tooling

LEVEL 5 - TRANSFORMATIONAL:
- AI-native is the default development paradigm
- Organization culture has shifted — "specification-first" is how everyone thinks
- Innovation-driven: using AI to explore new architectures, products, and approaches
- Continuous learning: AI models are fine-tuned on organizational context
- Faculty role: training the next generation of developers who think AI-natively

FACULTY'S ROLE IN THIS PROGRESSION:
- Faculty train the developers who will drive Levels 1-5 in their organizations
- Curriculum that teaches AI-native practices prepares students for the modern workplace
- Research opportunities exist at every level — measuring effectiveness, developing new methods, studying human-AI collaboration patterns
- Academic institutions themselves can progress through these maturity levels in their own development practices""")
    n += 1

    # ── Slide 39: HANDS-ON LAB SUMMARY & PRACTICAL EXAMPLES ───────────
    slide = add_slide(prs)
    add_title_bar(slide, "Hands-On Practical Examples", "Practical", n)

    # Example 1 card
    add_textbox(slide, 0.6, 1.25, 6.0, 0.4, "Primary Lab Exercise", 16, True, ACCENT_GREEN)
    add_rounded_box(slide, 0.6, 1.7, 6.0, 2.2,
                    "Example 1: Task Management REST API\n"
                    "Duration: 1-2 hours\n\n"
                    "Build a REST API with full CRUD operations\n"
                    "Apply spec-driven development methodology\n"
                    "Generate tests (unit + integration)\n"
                    "Set up CI/CD pipeline with quality gates",
                    fill_color=LIGHT_GREEN, text_color=TEXT_DARK, font_size=12, bold=True,
                    border_color=ACCENT_GREEN, alignment=PP_ALIGN.LEFT)

    # Example 2 card
    add_rounded_box(slide, 0.6, 4.15, 6.0, 1.6,
                    "Example 2: Student Grade Calculator\n"
                    "Duration: 1 hour\n\n"
                    "Calculate and report student grades\n"
                    "Focus on business logic and testing\n"
                    "Ideal for shorter sessions or beginners",
                    fill_color=LIGHT_ORANGE, text_color=TEXT_DARK, font_size=12, bold=True,
                    border_color=ACCENT_ORANGE, alignment=PP_ALIGN.LEFT)

    # Right side: Lab exercise flow
    add_textbox(slide, 7.2, 1.25, 5.5, 0.4, "Lab Exercise Flow", 16, True, ACCENT_GREEN)
    flow_stages = [
        ("Spec", ACCENT_BLUE),
        ("Architecture", ACCENT_GREEN),
        ("Code", ACCENT_ORANGE),
        ("Test", ACCENT_PURPLE),
        ("Deploy", ACCENT_TEAL),
    ]
    for i, (label, clr) in enumerate(flow_stages):
        add_rounded_box(slide, 7.2 + i * 1.15, 1.75, 1.0, 0.6, label,
                        fill_color=clr, text_color=WHITE, font_size=10, bold=True)
        if i < len(flow_stages) - 1:
            add_arrow_right(slide, 7.2 + i * 1.15 + 1.02, 1.9, 0.1, 0.01, color=TEXT_MID)

    # Homework section
    add_textbox(slide, 7.2, 2.7, 5.5, 0.4, "Homework Exercises", 16, True, ACCENT_ORANGE)
    add_bullet_list(slide, 7.2, 3.15, 5.5, 3.0, [
        ("Book Library Management System", [
            "CRUD for books, authors, categories",
            "Search & filtering capabilities",
            "Full spec-driven workflow"
        ]),
        ("Event Registration Platform", [
            "Event creation & attendee registration",
            "Capacity management & notifications",
            "Multi-tier architecture"
        ]),
    ], font_size=13)

    # Bottom key message
    add_rounded_box(slide, 0.6, 6.0, 12.1, 0.55,
                    "Key Principle:  Every exercise follows Spec-First -> AI-Assisted Design -> "
                    "Generate & Review -> Test & Validate -> Deploy & Monitor",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=13, bold=True,
                    border_color=ACCENT_ORANGE)

    add_notes(slide, """SPEAKER NOTES – Slide 39: Hands-On Practical Examples
-------------------------------------------------------
This slide summarizes the practical exercises available in the workshop and provides guidance for facilitation.

EXAMPLE 1 — TASK MANAGEMENT REST API (Primary, 1-2 hours):
This is the main hands-on exercise. Walk participants through:
1. Writing the specification: functional requirements (CRUD for tasks), non-functional requirements (response time, data validation), API contract (endpoints, request/response schemas)
2. Generating architecture: project structure, database schema, service layer design
3. Code generation: controllers, services, repositories using AI tools
4. Testing: unit tests for business logic, integration tests for API endpoints
5. CI/CD: GitHub Actions workflow with build, test, lint, security scan stages

Time allocation:
- Spec writing: 20 minutes
- Architecture review: 15 minutes
- Code generation & review: 30 minutes
- Test generation & execution: 20 minutes
- CI/CD setup: 15 minutes

EXAMPLE 2 — STUDENT GRADE CALCULATOR (Secondary, 1 hour):
A simpler exercise for shorter sessions or as a warm-up:
- Calculate weighted grades from multiple assignments
- Generate grade reports with statistics
- Focus on business logic correctness and comprehensive testing
- Good for participants new to AI-native practices

HOMEWORK EXERCISES:
These are designed for participants to practice independently after the workshop:
1. Book Library System: Full CRUD with relationships (books-authors-categories), search functionality, pagination. This exercises the complete spec-driven workflow.
2. Event Registration Platform: More complex — includes business rules (capacity limits, registration deadlines), notifications, and multi-tier architecture.

FACILITATION TIPS:
- Have pre-written partial specs available for participants who struggle to start from scratch
- Pair experienced and novice participants for pair-programming exercises
- Use screen sharing to demonstrate each step before participants try it themselves
- Common issue: participants want to jump straight to code — gently redirect to spec-first
- Have backup solutions ready in case of tool/network issues
- Allow time for discussion after each exercise — "What surprised you?" "What was harder/easier than expected?"
- Encourage experimentation — there's no single "right" way to prompt AI""")
    n += 1

    # ── Slide 40: KEY TAKEAWAYS & NEXT STEPS ──────────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "Key Takeaways & Next Steps", "Closing", n)

    # 6 key takeaways as numbered cards
    takeaways = [
        ("1", "AI-native development starts with\nSPECIFICATIONS, not code", LIGHT_BLUE, ACCENT_BLUE),
        ("2", "Human oversight remains essential\nat every stage", LIGHT_GREEN, ACCENT_GREEN),
        ("3", "Testing and security are\nmandatory guardrails", LIGHT_ORANGE, ACCENT_ORANGE),
        ("4", "CI/CD automates quality\nenforcement", LIGHT_PURPLE, ACCENT_PURPLE),
        ("5", "Multi-agent workflows represent\nthe future of SDLC", LIGHT_TEAL, ACCENT_TEAL),
        ("6", "Governance ensures responsible,\nsustainable AI adoption", LIGHT_YELLOW, ACCENT_ORANGE),
    ]
    for i, (num, text, bg, bdr) in enumerate(takeaways):
        col = i % 3
        row = i // 3
        lft = 0.6 + col * 4.15
        tp = 1.3 + row * 1.55
        # Number circle
        add_rounded_box(slide, lft, tp, 0.45, 0.45, num,
                        fill_color=bdr, text_color=WHITE, font_size=14, bold=True)
        # Text card
        add_rounded_box(slide, lft + 0.55, tp, 3.2, 1.2, text,
                        fill_color=bg, text_color=TEXT_DARK, font_size=12, bold=True,
                        border_color=bdr, alignment=PP_ALIGN.LEFT)

    # Lifecycle flow (visual anchor same as title slide)
    stages = ["Human\nIntent", "Executable\nSpec", "AI-Assisted\nDesign", "Code\nGeneration",
              "Automated\nTesting", "CI/CD\nPipeline", "Continuous\nFeedback"]
    colors = [ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE, ACCENT_PURPLE,
              ACCENT_GREEN, ACCENT_ORANGE, ACCENT_TEAL]
    x_start = 0.6
    for i, (label, clr) in enumerate(zip(stages, colors)):
        add_rounded_box(slide, x_start + i * 1.75, 4.65, 1.5, 0.7,
                        label, fill_color=clr, text_color=WHITE, font_size=9, bold=True)
        if i < len(stages) - 1:
            add_arrow_right(slide, x_start + i * 1.75 + 1.52, 4.82, 0.2, 0.01, color=TEXT_MID)

    # Next Steps box
    add_rounded_box(slide, 0.6, 5.65, 12.1, 0.9,
                    "Next Steps:   Complete homework exercises   |   "
                    "Explore AI tools (Cursor, Copilot, Claude)   |   "
                    "Apply spec-driven practices in your curriculum   |   "
                    "Share learnings with colleagues",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=13, bold=True,
                    border_color=ACCENT_ORANGE)

    add_notes(slide, """SPEAKER NOTES – Slide 40: Key Takeaways & Next Steps
------------------------------------------------------
This is your closing slide for the main content. Make it impactful and action-oriented.

WALK THROUGH EACH TAKEAWAY — connect it back to what they experienced:

1. SPECS, NOT CODE: "Remember how we started every exercise with a specification? That's the foundation. When you teach your students, start with 'What are we building and why?' before 'How do we code it?'"

2. HUMAN OVERSIGHT: "AI is powerful but not infallible. Every piece of generated code we reviewed today had at least something that needed human judgment — an edge case, a naming convention, a security consideration. Teach your students to be critical reviewers, not passive acceptors of AI output."

3. TESTING & SECURITY: "The test suite is your contract. If you have comprehensive tests, you can regenerate code with confidence. If you skip tests, you're building on sand. Security scanning isn't optional — it's a hygiene practice like testing."

4. CI/CD: "Automation isn't about convenience — it's about consistency. Every commit gets the same rigorous checks. No human can maintain that consistency manually across hundreds of commits."

5. MULTI-AGENT FUTURE: "Today we saw the foundations of multi-agent development. Within 2-3 years, most professional development environments will use orchestrated AI agents for different phases of the SDLC. Your students need to understand this paradigm."

6. GOVERNANCE: "As AI becomes more powerful, governance becomes more important. Teach your students not just how to USE AI, but how to use it RESPONSIBLY — with policies, audit trails, and ethical consideration."

NEXT STEPS — Make these concrete and actionable:
1. Complete the homework exercises within the next 2 weeks
2. Try using AI tools in your own development work before introducing them to students
3. Start adapting one course to include spec-driven development concepts
4. Share your experience with other faculty — be an advocate for AI-native practices
5. Consider research opportunities — measuring AI impact on student learning, developing new assessment methods

CALL TO ACTION: "You are the bridge between the AI revolution and the next generation of software engineers. How you teach will shape how they build. Thank you for investing this time in your professional development."

RESOURCES:
- Workshop materials will be shared via the course repository
- Follow-up office hours available for implementation questions
- Community of practice Slack/Discord channel for ongoing discussion""")
    n += 1

    # ================================================================
    # ============= BACKUP SLIDES (41-50) ============================
    # ================================================================

    # ── Slide 41: BACKUP - PROMPT ENGINEERING TEMPLATES ────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "BACKUP: Prompt Engineering Templates", "Backup", n)

    add_textbox(slide, 0.5, 1.15, 4.0, 0.3, "1. Requirements Gathering Prompt", 13, True, ACCENT_BLUE)
    add_code_box(slide, 0.5, 1.5, 5.9, 1.6,
                 'You are a requirements analyst.\n'
                 'Given this feature request:\n'
                 '  "{feature_description}"\n\n'
                 'Produce:\n'
                 '1. Functional requirements (numbered)\n'
                 '2. Non-functional requirements\n'
                 '3. Acceptance criteria (Given/When/Then)\n'
                 '4. Edge cases and error scenarios',
                 font_size=9)

    add_textbox(slide, 0.5, 3.3, 4.0, 0.3, "2. Code Generation Prompt", 13, True, ACCENT_GREEN)
    add_code_box(slide, 0.5, 3.6, 5.9, 1.6,
                 'You are a senior backend developer.\n'
                 'Given this specification:\n'
                 '  {specification}\n\n'
                 'Generate a RESTful API implementation:\n'
                 '- Language: Python / FastAPI\n'
                 '- Follow clean architecture patterns\n'
                 '- Include input validation & error handling\n'
                 '- Add docstrings and type hints',
                 font_size=9)

    add_textbox(slide, 0.5, 5.4, 4.0, 0.3, "3. Test Generation Prompt", 13, True, ACCENT_PURPLE)
    add_code_box(slide, 0.5, 5.7, 5.9, 1.0,
                 'Given this code: {code}\n'
                 'And acceptance criteria: {criteria}\n'
                 'Generate: unit tests (pytest), edge case\n'
                 'tests, and integration tests with mocks.',
                 font_size=9)

    # Right side: tips
    add_textbox(slide, 6.8, 1.15, 5.8, 0.3, "Prompt Engineering Tips", 16, True, ACCENT_ORANGE)
    add_bullet_list(slide, 6.8, 1.6, 5.8, 5.0, [
        "Always assign a ROLE to the AI (analyst, developer, tester)",
        "Provide CONTEXT — specs, constraints, existing code",
        "Be SPECIFIC about output format and requirements",
        "Include EXAMPLES of desired output when possible",
        "Iterate: refine prompts based on output quality",
        "Use CHAIN-OF-THOUGHT for complex reasoning tasks",
        "Break large tasks into smaller, focused prompts",
        "Include constraints: language, framework, patterns",
        "Ask AI to explain its reasoning and trade-offs",
        "Save effective prompts as reusable templates",
    ], font_size=12)

    add_notes(slide, """SPEAKER NOTES – Slide 41 (BACKUP): Prompt Engineering Templates
-----------------------------------------------------------------
This backup slide provides ready-to-use prompt templates for common software development tasks. Use this when participants need concrete examples.

TEMPLATE 1 — REQUIREMENTS GATHERING:
This template transforms a vague feature request into a structured specification. Key elements:
- Role assignment: "You are a requirements analyst" — this primes the AI to think in terms of requirements, not code
- Structured output: numbered functional requirements, non-functional requirements, acceptance criteria in Given/When/Then format
- Edge cases: explicitly asking for edge cases catches scenarios humans often miss
- Customization: replace {feature_description} with the actual feature. Be as detailed as possible.

TEMPLATE 2 — CODE GENERATION:
This template generates implementation code from an approved specification. Key elements:
- Role: "senior backend developer" — encourages production-quality patterns
- Input: the full specification, not just a one-line description
- Constraints: specific language, framework, and patterns to follow
- Quality requirements: validation, error handling, docstrings, type hints
- Customization: adjust language/framework as needed, add project-specific conventions

TEMPLATE 3 — TEST GENERATION:
This template generates comprehensive tests. Key elements:
- Dual input: both the code and the acceptance criteria — this ensures tests validate business requirements, not just code coverage
- Multiple test types: unit, edge case, and integration
- Customization: add specific testing framework preferences, mocking strategies

GENERAL TIPS:
- The "tips" column on the right provides meta-guidance for effective prompting
- Chain-of-thought prompting is especially useful for architecture decisions
- Iterative refinement is normal — first prompt rarely produces perfect output
- Templates should be version-controlled alongside code
- Encourage participants to build their own template library""")
    n += 1

    # ── Slide 42: BACKUP - KUBERNETES DEPLOYMENT DETAILS ───────────────
    slide = add_slide(prs)
    add_title_bar(slide, "BACKUP: Kubernetes Deployment Architecture", "Backup", n)

    # K8s YAML snippet
    add_textbox(slide, 0.5, 1.15, 5.5, 0.3, "Deployment YAML", 14, True, ACCENT_BLUE)
    add_code_box(slide, 0.5, 1.5, 5.8, 3.5,
                 'apiVersion: apps/v1\n'
                 'kind: Deployment\n'
                 'metadata:\n'
                 '  name: task-api\n'
                 'spec:\n'
                 '  replicas: 3\n'
                 '  selector:\n'
                 '    matchLabels:\n'
                 '      app: task-api\n'
                 '  template:\n'
                 '    spec:\n'
                 '      containers:\n'
                 '      - name: task-api\n'
                 '        image: task-api:latest\n'
                 '        ports:\n'
                 '        - containerPort: 8000\n'
                 '        resources:\n'
                 '          limits:\n'
                 '            memory: "256Mi"\n'
                 '            cpu: "500m"',
                 font_size=9)

    # Architecture diagram (right side)
    add_textbox(slide, 6.8, 1.15, 5.5, 0.3, "K8s Architecture", 14, True, ACCENT_BLUE)
    k8s_components = [
        ("Ingress\nController", ACCENT_BLUE,   7.5, 1.7, 2.0, 0.65),
        ("Service\n(Load Balancer)", ACCENT_GREEN, 7.5, 2.7, 2.0, 0.65),
        ("Pod 1\ntask-api", ACCENT_ORANGE,     6.8, 3.7, 1.4, 0.6),
        ("Pod 2\ntask-api", ACCENT_ORANGE,     8.4, 3.7, 1.4, 0.6),
        ("Pod 3\ntask-api", ACCENT_ORANGE,     10.0, 3.7, 1.4, 0.6),
        ("PersistentVolume\n(Database)", ACCENT_PURPLE, 7.5, 4.7, 2.8, 0.65),
    ]
    for label, clr, lft, tp, w, h in k8s_components:
        add_rounded_box(slide, lft, tp, w, h, label,
                        fill_color=clr, text_color=WHITE, font_size=9, bold=True)

    # Arrows
    add_arrow_down(slide, 8.35, 2.4, 0.3, 0.25, color=TEXT_MID)
    add_arrow_down(slide, 8.35, 3.4, 0.3, 0.25, color=TEXT_MID)

    # Bottom: key concepts
    add_bullet_list(slide, 0.5, 5.3, 12.3, 1.3, [
        "Pods: smallest deployable unit — one or more containers sharing network",
        "Services: stable network endpoint — load-balances across pods",
        "Deployments: declarative updates — rolling upgrades with zero downtime",
    ], font_size=12)

    add_notes(slide, """SPEAKER NOTES – Slide 42 (BACKUP): Kubernetes Deployment Architecture
----------------------------------------------------------------------
Use this slide when participants ask about container orchestration or production deployment.

KUBERNETES CONCEPTS FOR FACULTY:
- Kubernetes (K8s) is the industry standard for container orchestration
- It automates deployment, scaling, and management of containerized applications
- Even if students don't use K8s directly, understanding the concepts is valuable

DEPLOYMENT YAML EXPLAINED:
- apiVersion/kind: declares this is a Deployment resource
- replicas: 3: runs three identical copies for availability
- selector: tells K8s which pods belong to this deployment
- container spec: which image to run, which ports to expose
- resources: CPU and memory limits prevent runaway consumption

ARCHITECTURE COMPONENTS:
- Ingress Controller: routes external traffic to internal services (like a reverse proxy)
- Service: provides a stable internal DNS name and load-balances across pods
- Pods: the actual running containers — if one crashes, K8s restarts it automatically
- PersistentVolume: durable storage that survives pod restarts (for databases)

WHEN TO INTRODUCE TO STUDENTS:
- After they understand Docker basics (containerization)
- When discussing production deployment and scaling
- In advanced courses on cloud computing or DevOps
- Not necessary for introductory courses — Docker Compose is a simpler alternative

AI-NATIVE CONNECTION:
- AI can generate K8s YAML from high-level descriptions
- "Deploy a Python API with 3 replicas, 256MB memory limit, and a PostgreSQL database"
- AI can also generate Helm charts, Kustomize overlays, and ArgoCD configurations""")
    n += 1

    # ── Slide 43: BACKUP - OPENTELEMETRY & MONITORING ─────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "BACKUP: Observability with OpenTelemetry", "Backup", n)

    # Monitoring architecture
    add_textbox(slide, 0.5, 1.15, 8.0, 0.3, "Observability Architecture", 16, True, ACCENT_TEAL)

    arch_boxes = [
        ("Application\n(Instrumented)", ACCENT_BLUE,  0.6, 1.8, 2.0, 0.8),
        ("OTel\nCollector",             ACCENT_GREEN,  3.4, 1.8, 1.8, 0.8),
        ("Prometheus\n(Metrics)",       ACCENT_ORANGE, 5.9, 1.55, 1.8, 0.6),
        ("Jaeger\n(Traces)",            ACCENT_PURPLE, 5.9, 2.25, 1.8, 0.6),
        ("Grafana\n(Dashboards)",       ACCENT_TEAL,   8.4, 1.8, 2.0, 0.8),
    ]
    for label, clr, lft, tp, w, h in arch_boxes:
        add_rounded_box(slide, lft, tp, w, h, label,
                        fill_color=clr, text_color=WHITE, font_size=10, bold=True)

    add_arrow_right(slide, 2.65, 2.0, 0.7, 0.01, color=TEXT_MID)
    add_arrow_right(slide, 5.25, 2.0, 0.6, 0.01, color=TEXT_MID)
    add_arrow_right(slide, 7.75, 2.0, 0.6, 0.01, color=TEXT_MID)

    # Key metrics table
    add_textbox(slide, 0.5, 3.0, 12.0, 0.3, "Key Metrics to Track", 16, True, ACCENT_TEAL)
    metrics_rows = [
        ["Metric Category", "Examples", "Why It Matters"],
        ["Latency", "P50, P95, P99 response times", "User experience & SLA compliance"],
        ["Throughput", "Requests/second, transactions/min", "Capacity planning & scaling"],
        ["Error Rate", "4xx/5xx rates, exception counts", "System health & reliability"],
        ["Saturation", "CPU, memory, disk, connection pools", "Bottleneck identification"],
    ]
    add_table_shape(slide, 0.5, 3.4, 12.3, 2.4, metrics_rows, 3)

    # OTel code snippet
    add_textbox(slide, 0.5, 5.95, 5.0, 0.3, "Quick OTel Setup (Python)", 12, True, ACCENT_TEAL)
    add_code_box(slide, 0.5, 6.2, 5.8, 0.55,
                 'pip install opentelemetry-api opentelemetry-sdk\n'
                 'opentelemetry-instrument python app.py',
                 font_size=9)

    add_notes(slide, """SPEAKER NOTES – Slide 43 (BACKUP): Observability with OpenTelemetry
---------------------------------------------------------------------
Use this slide when discussing production monitoring or when participants ask about how to know if AI-generated code performs well in production.

WHAT IS OBSERVABILITY?
Observability is the ability to understand a system's internal state by examining its external outputs. The three pillars are:
1. Metrics: numerical measurements over time (latency, throughput, error rates)
2. Traces: end-to-end request journeys through distributed systems
3. Logs: discrete events with context (error messages, audit records)

OPENTELEMETRY (OTel):
- Vendor-neutral, open-source observability framework
- Provides APIs and SDKs for instrumenting applications
- Supports all three pillars: metrics, traces, and logs
- Works with most programming languages (Python, Java, Go, Node.js, etc.)
- The OTel Collector receives, processes, and exports telemetry data

ARCHITECTURE EXPLAINED:
1. Application is instrumented with OTel SDK — adds automatic and custom telemetry
2. OTel Collector aggregates data — acts as a pipeline for processing and routing
3. Prometheus stores metrics — time-series database optimized for monitoring
4. Jaeger stores traces — distributed tracing backend for request flow analysis
5. Grafana visualizes everything — dashboards, alerts, and exploration

WHY IT MATTERS FOR AI-NATIVE DEVELOPMENT:
- AI-generated code may have performance characteristics you didn't expect
- Monitoring helps you identify issues before users are affected
- Feedback from production metrics feeds back into the AI-native cycle
- Automated alerts can trigger re-generation or rollback of problematic code

SETUP GUIDANCE:
- Start simple: just metrics (Prometheus + Grafana)
- Add traces when debugging distributed systems
- OpenTelemetry auto-instrumentation requires minimal code changes
- Docker Compose setups available for local development""")
    n += 1

    # ── Slide 44: BACKUP - PERFORMANCE TEST EXAMPLE (K6) ──────────────
    slide = add_slide(prs)
    add_title_bar(slide, "BACKUP: Load Testing with k6", "Backup", n)

    add_textbox(slide, 0.5, 1.15, 6.0, 0.3, "k6 Load Test Script", 14, True, ACCENT_TEAL)
    add_code_box(slide, 0.5, 1.5, 6.0, 4.0,
                 'import http from "k6/http";\n'
                 'import { check, sleep } from "k6";\n'
                 '\n'
                 'export const options = {\n'
                 '  stages: [\n'
                 '    { duration: "30s", target: 20 },\n'
                 '    { duration: "1m",  target: 50 },\n'
                 '    { duration: "30s", target: 0  },\n'
                 '  ],\n'
                 '  thresholds: {\n'
                 '    http_req_duration: ["p(95)<500"],\n'
                 '    http_req_failed: ["rate<0.01"],\n'
                 '  },\n'
                 '};\n'
                 '\n'
                 'export default function () {\n'
                 '  const res = http.get(\n'
                 '    "http://localhost:8000/api/tasks"\n'
                 '  );\n'
                 '  check(res, {\n'
                 '    "status is 200": (r) => r.status === 200,\n'
                 '    "response < 500ms": (r) =>\n'
                 '      r.timings.duration < 500,\n'
                 '  });\n'
                 '  sleep(1);\n'
                 '}',
                 font_size=9)

    # Right side: metrics explanation
    add_textbox(slide, 7.0, 1.15, 5.5, 0.3, "Performance Metrics Explained", 14, True, ACCENT_TEAL)
    perf_cards = [
        ("Ramp-Up Pattern", "Gradually increase load\n30s to 20 users -> 1m at 50 -> ramp down", LIGHT_BLUE, ACCENT_BLUE),
        ("Thresholds", "P95 latency < 500ms\nError rate < 1%", LIGHT_GREEN, ACCENT_GREEN),
        ("Checks", "Validate response status\nand timing per request", LIGHT_ORANGE, ACCENT_ORANGE),
        ("Key Metrics", "req_duration, req_failed,\niterations, vus, data_received", LIGHT_PURPLE, ACCENT_PURPLE),
    ]
    for i, (t, d, bg, bdr) in enumerate(perf_cards):
        add_rounded_box(slide, 7.0, 1.6 + i * 1.25, 5.5, 1.05,
                        f"{t}\n{d}", fill_color=bg, text_color=TEXT_DARK,
                        font_size=11, bold=True, border_color=bdr)

    # Bottom: when to use
    add_rounded_box(slide, 0.5, 5.9, 12.3, 0.65,
                    "When to load test:  Before production deployment  |  After major code changes  |  "
                    "Before expected traffic spikes  |  As part of CI/CD pipeline",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=12, bold=True,
                    border_color=ACCENT_ORANGE)

    add_notes(slide, """SPEAKER NOTES – Slide 44 (BACKUP): Load Testing with k6
---------------------------------------------------------
Use this slide to demonstrate performance testing concepts and practices.

WHAT IS K6?
- Open-source load testing tool by Grafana Labs
- Written in Go but tests are scripted in JavaScript
- Designed for developer experience — tests are code, not GUI configurations
- Integrates with CI/CD pipelines, Grafana dashboards, and cloud execution

SCRIPT WALKTHROUGH:
1. Import statements: http for making requests, check for assertions, sleep for pacing
2. Options block defines the test profile:
   - stages: ramp up to 20 virtual users over 30s, then to 50 users for 1 minute, then ramp down
   - thresholds: the test FAILS if 95th percentile latency exceeds 500ms or if more than 1% of requests fail
3. Default function: what each virtual user does per iteration
   - Makes a GET request to the tasks API
   - Checks the response status and timing
   - Sleeps 1 second (simulates user think time)

INTERPRETING RESULTS:
- http_req_duration: how long requests take (look at p50, p90, p95, p99)
- http_req_failed: percentage of failed requests
- iterations: total number of complete test iterations
- vus: number of active virtual users at any point
- data_received/sent: network throughput

COMMON BOTTLENECKS k6 HELPS IDENTIFY:
- Database connection pool exhaustion
- Memory leaks under sustained load
- CPU-bound operations that don't scale
- Network timeouts and connection limits
- Thread/process starvation

AI-NATIVE CONNECTION:
- AI can generate k6 scripts from API specs
- "Generate a k6 load test for the Task Management API that tests all CRUD endpoints with realistic data"
- AI can also help interpret results and suggest optimizations""")
    n += 1

    # ── Slide 45: BACKUP - E2E TEST WITH PLAYWRIGHT ───────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "BACKUP: End-to-End Testing with Playwright", "Backup", n)

    add_textbox(slide, 0.5, 1.15, 6.0, 0.3, "Playwright Test Example", 14, True, ACCENT_GREEN)
    add_code_box(slide, 0.5, 1.5, 6.0, 3.8,
                 'import { test, expect } from "@playwright/test";\n'
                 '\n'
                 'test("create a new task", async ({ page }) => {\n'
                 '  // Navigate to the app\n'
                 '  await page.goto("http://localhost:3000");\n'
                 '\n'
                 '  // Click the "New Task" button\n'
                 '  await page.click(\n'
                 '    \'button:has-text("New Task")\'\n'
                 '  );\n'
                 '\n'
                 '  // Fill in task details\n'
                 '  await page.fill(\n'
                 '    \'input[name="title"]\',\n'
                 '    "Write unit tests"\n'
                 '  );\n'
                 '  await page.fill(\n'
                 '    \'textarea[name="description"]\',\n'
                 '    "Cover all edge cases"\n'
                 '  );\n'
                 '\n'
                 '  // Submit and verify\n'
                 '  await page.click(\'button:has-text("Save")\');\n'
                 '  await expect(\n'
                 '    page.locator(".task-item")\n'
                 '  ).toContainText("Write unit tests");\n'
                 '});',
                 font_size=9)

    # Right side: when to use each test type
    add_textbox(slide, 7.0, 1.15, 5.5, 0.3, "Testing Pyramid", 16, True, ACCENT_GREEN)

    pyramid_tests = [
        ("E2E Tests\n(Playwright, Cypress)", LIGHT_ORANGE, 8.2, 1.7, 2.6, 0.7),
        ("Integration Tests\n(API, Database)", LIGHT_GREEN, 7.7, 2.6, 3.6, 0.7),
        ("Unit Tests\n(pytest, Jest)", LIGHT_BLUE, 7.2, 3.5, 4.6, 0.7),
    ]
    for label, clr, lft, tp, w, h in pyramid_tests:
        add_rounded_box(slide, lft, tp, w, h, label,
                        fill_color=clr, text_color=TEXT_DARK, font_size=11, bold=True)

    # Comparison table
    add_textbox(slide, 7.0, 4.5, 5.5, 0.3, "When to Use Each Type", 13, True, ACCENT_GREEN)
    test_rows = [
        ["Type", "Speed", "Confidence", "Use For"],
        ["Unit", "Fast", "Low-Med", "Business logic, utils"],
        ["Integration", "Medium", "Medium", "API contracts, DB queries"],
        ["E2E", "Slow", "High", "User workflows, UI"],
    ]
    add_table_shape(slide, 7.0, 4.85, 5.8, 1.6, test_rows, 4)

    add_notes(slide, """SPEAKER NOTES – Slide 45 (BACKUP): End-to-End Testing with Playwright
----------------------------------------------------------------------
Use this slide when discussing comprehensive testing strategies or when participants ask about UI testing.

WHAT IS PLAYWRIGHT?
- Modern end-to-end testing framework by Microsoft
- Supports Chromium, Firefox, and WebKit browsers
- Auto-waits for elements — no manual sleep/wait statements needed
- Supports multiple programming languages (JavaScript, Python, Java, C#)
- Built-in test runner with parallel execution and reporting

SCRIPT WALKTHROUGH:
1. Import test and expect from Playwright's test library
2. Define a test case: "create a new task"
3. Navigate to the application URL
4. Interact with UI elements: click buttons, fill inputs
5. Submit the form
6. Assert that the expected result appears on the page

KEY PLAYWRIGHT FEATURES:
- Auto-waiting: Playwright waits for elements to be ready before interacting
- Locator strategies: text, CSS selectors, role-based selectors, XPath
- Network interception: mock API responses for isolated testing
- Screenshot and video recording for debugging
- Parallel execution across browsers for faster CI/CD

TESTING PYRAMID CONCEPT:
- Unit Tests (base, most numerous): fast, isolated, test individual functions
- Integration Tests (middle): test how components work together, API contracts
- E2E Tests (top, fewest): test full user workflows through the actual UI
- Rule of thumb: 70% unit, 20% integration, 10% E2E
- E2E tests are expensive to write and maintain — use them for critical user journeys only

AI-NATIVE CONNECTION:
- AI can generate Playwright tests from user stories or UI mockups
- "Given this user story: 'As a user, I can create a task with a title and description', generate a Playwright E2E test"
- AI can also generate Page Object Models from HTML structure
- Combine with visual regression testing for comprehensive coverage""")
    n += 1

    # ── Slide 46: BACKUP - RESEARCH OPPORTUNITIES ─────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "BACKUP: Research Opportunities for Faculty", "Backup", n)

    add_textbox(slide, 0.5, 1.15, 12.0, 0.4, "Emerging Research Areas in AI-Native Software Engineering", 16, True, ACCENT_BLUE)

    research_areas = [
        ("AI-Assisted SE Education", "How does AI-native methodology impact student learning outcomes?\n"
         "What assessment methods work best for AI-augmented coursework?",
         LIGHT_BLUE, ACCENT_BLUE),
        ("Spec-to-Code Traceability", "Can we maintain formal traceability from specs through AI generation?\n"
         "How do we verify generated code satisfies original requirements?",
         LIGHT_GREEN, ACCENT_GREEN),
        ("Agentic SDLC Effectiveness", "How effective are multi-agent workflows vs. single-agent approaches?\n"
         "What orchestration patterns yield the best results?",
         LIGHT_ORANGE, ACCENT_ORANGE),
        ("Security of Generated Code", "What vulnerability patterns are common in AI-generated code?\n"
         "Can AI-based security review catch AI-introduced vulnerabilities?",
         LIGHT_PURPLE, ACCENT_PURPLE),
        ("Human-AI Collaboration", "How do developers' roles change in AI-native workflows?\n"
         "What skills become more/less important with AI-native practices?",
         LIGHT_TEAL, ACCENT_TEAL),
        ("Cost-Benefit Analysis", "What is the true ROI of AI-native development?\n"
         "How do we measure productivity gains accurately?",
         LIGHT_YELLOW, ACCENT_ORANGE),
    ]
    for i, (title, desc, bg, bdr) in enumerate(research_areas):
        col = i % 2
        row = i // 2
        lft = 0.5 + col * 6.3
        tp = 1.65 + row * 1.6
        add_rounded_box(slide, lft, tp, 5.9, 1.35,
                        f"{title}\n{desc}",
                        fill_color=bg, text_color=TEXT_DARK, font_size=11, bold=True,
                        border_color=bdr, alignment=PP_ALIGN.LEFT)

    # Bottom: collaboration call
    add_rounded_box(slide, 0.5, 6.15, 12.3, 0.5,
                    "Collaboration Welcome:  Joint publications  |  Cross-institutional studies  |  "
                    "Industry partnerships  |  Grant proposals",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=12, bold=True,
                    border_color=ACCENT_ORANGE)

    add_notes(slide, """SPEAKER NOTES – Slide 46 (BACKUP): Research Opportunities for Faculty
----------------------------------------------------------------------
This slide is specifically for faculty who are interested in conducting research in AI-native software engineering. Use it to spark research conversations.

RESEARCH AREA 1 — AI-ASSISTED SE EDUCATION:
- Research questions: Does AI-native methodology improve student learning outcomes? Does it help or hinder conceptual understanding? How do students' problem-solving strategies change?
- Methods: controlled studies comparing AI-native vs. traditional teaching, surveys, code quality analysis
- Potential venues: SIGCSE, ITiCSE, ICSE-SEET, ACM TOCE

RESEARCH AREA 2 — SPEC-TO-CODE TRACEABILITY:
- Research questions: Can formal traceability be maintained when AI generates code from specs? How do we verify that generated code satisfies the original requirements?
- Methods: static analysis, formal verification, mutation testing of generated code
- Potential venues: ICSE, FSE, ASE, TOSEM

RESEARCH AREA 3 — AGENTIC SDLC EFFECTIVENESS:
- Research questions: Are multi-agent workflows more effective than single LLM approaches? What orchestration patterns yield the best results? How does agent specialization affect output quality?
- Methods: empirical studies, case studies, benchmarking frameworks
- Potential venues: ICSE, FSE, AAAI, NeurIPS (AI agent tracks)

RESEARCH AREA 4 — SECURITY OF GENERATED CODE:
- Research questions: What vulnerability patterns are common in AI-generated code? Are they different from human-introduced vulnerabilities? Can AI-based security tools catch AI-introduced bugs?
- Methods: static analysis of generated codebases, vulnerability benchmarks, red-team exercises
- Potential venues: USENIX Security, CCS, S&P, NDSS

RESEARCH AREA 5 — HUMAN-AI COLLABORATION:
- Research questions: How do developers' roles evolve? What skills become more important? How does team dynamics change?
- Methods: ethnographic studies, longitudinal observations, interview studies

RESEARCH AREA 6 — COST-BENEFIT ANALYSIS:
- Research questions: What is the true ROI? How do we measure it? What are the hidden costs?
- Methods: case studies, time-motion studies, productivity metrics analysis""")
    n += 1

    # ── Slide 47: BACKUP - INSTRUCTOR GUIDE & COMMON PITFALLS ─────────
    slide = add_slide(prs)
    add_title_bar(slide, "BACKUP: Instructor Guide & Pitfalls", "Backup", n)

    add_textbox(slide, 0.5, 1.15, 5.8, 0.4, "Common Pitfalls", 16, True, ACCENT_ORANGE)

    pitfalls = [
        ["Pitfall", "Mitigation Strategy"],
        ["Students skip the spec\nand jump to code", "Require spec submission before\ncode generation is allowed"],
        ["Over-reliance on AI\nwithout understanding", "Assess via oral explanation\nand code modification exercises"],
        ["Copy-paste without\nreview or testing", "Mandate code review checklists\nand minimum test coverage"],
        ["Ignoring security\nvulnerabilities", "Integrate security scanning in\nCI/CD; grade on security posture"],
        ["Prompt engineering\nfrustration", "Provide starter templates;\nteach iterative refinement"],
        ["Tool access issues\n(cost, availability)", "Use free tiers; have\noffline backup exercises"],
    ]
    add_table_shape(slide, 0.5, 1.6, 6.0, 4.8, pitfalls, 2,
                    row_colors=[LIGHT_BLUE, LIGHT_GREEN, LIGHT_ORANGE,
                                LIGHT_YELLOW, LIGHT_PURPLE, LIGHT_TEAL])

    # Right side: facilitation tips
    add_textbox(slide, 7.0, 1.15, 5.5, 0.4, "Facilitation Tips", 16, True, ACCENT_GREEN)
    add_bullet_list(slide, 7.0, 1.65, 5.5, 5.0, [
        "Start with a live demo before hands-on exercises",
        "Pair experienced and novice participants",
        "Keep exercises time-boxed (20-30 min each)",
        "Circulate during hands-on time; don't just observe",
        "Have pre-written backup solutions ready",
        "Encourage questions; create safe failure space",
        "Debrief after each exercise: what surprised you?",
        "Adjust pace based on room experience level",
        "Use screen sharing for collaborative debugging",
        "End each section with a reflection question",
        "Document common issues for future sessions",
    ], font_size=12)

    add_notes(slide, """SPEAKER NOTES – Slide 47 (BACKUP): Instructor Guide & Pitfalls
----------------------------------------------------------------
This slide is a practical guide for facilitators delivering this workshop or teaching AI-native practices in their own courses.

COMMON PITFALLS IN DETAIL:

1. SKIPPING THE SPEC: The most common issue. Students (and professionals!) want to immediately start generating code. Mitigation: make spec submission a prerequisite for the next stage. Grade the spec independently. Show examples of how bad specs produce bad code.

2. OVER-RELIANCE WITHOUT UNDERSTANDING: Students may produce working code without understanding how it works. This is dangerous in professional settings. Mitigation: require oral defenses, code modification exercises ("change the data model from X to Y and explain what else needs to change"), and design justification documentation.

3. COPY-PASTE WITHOUT REVIEW: AI output is treated as gospel. Mitigation: implement mandatory code review checklists, require students to annotate generated code with comments explaining what each section does, mandate minimum test coverage.

4. IGNORING SECURITY: AI-generated code may include vulnerabilities that students don't recognize. Mitigation: integrate automated security scanning (Snyk, Bandit, etc.) into the CI/CD pipeline, make security findings a graded component.

5. PROMPT FRUSTRATION: Students may struggle to get useful outputs from AI. Mitigation: provide starter prompt templates, teach the iterative refinement process (prompt -> review -> refine -> repeat), share examples of effective vs. ineffective prompts.

6. TOOL ACCESS: Not all students have access to paid AI tools. Mitigation: use free tiers (GitHub Copilot for students, free ChatGPT), have offline exercises as backup, consider institutional licenses.

FACILITATION BEST PRACTICES:
- Read the room: if participants are experienced, go faster through basics; if novice, spend more time on fundamentals
- Use the "I do, we do, you do" progression for each exercise
- Keep energy high: alternate between presentation, discussion, and hands-on every 20-30 minutes
- Collect feedback: end-of-session survey to improve future deliveries""")
    n += 1

    # ── Slide 48: BACKUP - ACADEMIC ASSESSMENT RUBRIC ─────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "BACKUP: Assessment Rubric for AI-Native Projects", "Backup", n)

    add_textbox(slide, 0.5, 1.15, 12.0, 0.3, "Rubric for Evaluating AI-Native Software Projects", 15, True, ACCENT_BLUE)

    rubric_rows = [
        ["Criteria", "Excellent (A)", "Good (B)", "Needs Improvement (C)"],
        ["Specification\nQuality",
         "Complete, structured spec\nwith acceptance criteria",
         "Adequate spec with\nsome gaps",
         "Minimal or vague\nspecification"],
        ["Architecture\nDecision",
         "Well-reasoned design with\ndocumented trade-offs",
         "Reasonable design but\nlimited justification",
         "No clear architecture\nor rationale"],
        ["Code Quality\n& Review",
         "Clean, reviewed code with\nmeaningful modifications",
         "Functional code with\nsome review evidence",
         "Unreviewed AI output\nwith no changes"],
        ["Testing\nCoverage",
         "Comprehensive tests:\nunit, integration, edge cases",
         "Basic unit tests\nwith decent coverage",
         "Minimal or no tests;\nlow coverage"],
        ["Security\nPractice",
         "Security scan integrated;\nvulnerabilities addressed",
         "Basic security awareness;\nsome scanning",
         "No security consideration\nin the project"],
        ["Process\nDocumentation",
         "Full AI interaction log;\ndecision rationale documented",
         "Partial documentation\nof AI usage",
         "No documentation of\nAI-assisted process"],
    ]
    add_table_shape(slide, 0.3, 1.5, 12.7, 5.0, rubric_rows, 4,
                    row_colors=[LIGHT_BLUE, LIGHT_GREEN, LIGHT_ORANGE,
                                LIGHT_YELLOW, LIGHT_PURPLE, LIGHT_TEAL])

    add_notes(slide, """SPEAKER NOTES – Slide 48 (BACKUP): Assessment Rubric for AI-Native Projects
---------------------------------------------------------------------------
This rubric provides a framework for fairly assessing student work in AI-native development courses.

THE CHALLENGE: When AI can generate most of the code, how do you assess student learning?

RUBRIC WALKTHROUGH:

1. SPECIFICATION QUALITY (Most Important):
- Excellent: Complete functional and non-functional requirements, structured format, clear acceptance criteria in Given/When/Then, edge cases identified
- This is the primary indicator of student understanding — writing a good spec requires deep domain knowledge
- Tip: Weight this criterion heavily (25-30% of total grade)

2. ARCHITECTURE DECISION:
- Excellent: Clear architecture choice with documented trade-offs, Architecture Decision Records (ADRs), consideration of alternatives
- This tests critical thinking — can the student evaluate options and justify choices?
- Tip: Require oral defense of architecture decisions

3. CODE QUALITY & REVIEW:
- Excellent: Evidence of human review — meaningful modifications to AI output, comments explaining changes, consistent style
- Red flag: code that looks 100% AI-generated with no human fingerprint
- Tip: Use diff tools to compare AI-generated code with submitted version

4. TESTING COVERAGE:
- Excellent: Multiple test types, edge cases covered, meaningful assertions (not just "test passes")
- Tests should validate spec requirements, not just code paths
- Tip: Review test quality, not just coverage percentage

5. SECURITY PRACTICE:
- Excellent: Automated security scanning in CI/CD, vulnerabilities identified and addressed, security considerations documented
- This teaches professional practice — security is not optional

6. PROCESS DOCUMENTATION:
- Excellent: Full log of AI interactions (what prompts were used, what was generated, what was changed and why)
- This is unique to AI-native assessment — it shows the student's thinking process
- Tip: Use this as the primary evidence of learning when code quality alone is ambiguous

RECOMMENDED GRADE WEIGHTS:
- Specification: 25%
- Architecture: 15%
- Code Quality: 15%
- Testing: 20%
- Security: 10%
- Documentation: 15%""")
    n += 1

    # ── Slide 49: BACKUP - TOOL COMPARISON MATRIX ─────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "BACKUP: AI Development Tool Comparison", "Backup", n)

    add_textbox(slide, 0.5, 1.15, 12.0, 0.3, "AI-Powered Development Tools: Feature Comparison", 15, True, ACCENT_BLUE)

    tool_rows = [
        ["Tool", "Type", "Key Strength", "Best For", "Cost"],
        ["GitHub Copilot", "Code completion", "Deep IDE integration", "Inline code suggestions", "Free for students"],
        ["Cursor", "AI-native IDE", "Full-file editing, agents", "Agentic coding workflows", "$20/month"],
        ["Claude (Anthropic)", "Chat + code", "Long context, reasoning", "Architecture & specs", "Free tier available"],
        ["ChatGPT (OpenAI)", "Chat + code", "Broad knowledge base", "General-purpose coding", "Free tier available"],
        ["Windsurf", "AI-native IDE", "Cascade flows, agents", "End-to-end development", "$15/month"],
        ["Amazon Q Dev", "AWS integrated", "Cloud-native dev", "AWS infrastructure", "Free tier available"],
        ["Tabnine", "Code completion", "Privacy-focused", "Enterprise, on-prem", "Free tier available"],
    ]
    add_table_shape(slide, 0.3, 1.5, 12.7, 4.2, tool_rows, 5,
                    row_colors=[LIGHT_BLUE, LIGHT_GREEN, LIGHT_ORANGE,
                                LIGHT_YELLOW, LIGHT_PURPLE, LIGHT_TEAL, LIGHT_BLUE])

    # Bottom: selection criteria
    add_textbox(slide, 0.5, 5.9, 12.0, 0.3, "Selection Criteria", 14, True, ACCENT_ORANGE)
    add_bullet_list(slide, 0.5, 6.2, 12.0, 0.6, [
        "Consider: privacy policies, institutional licenses, student accessibility, language/framework support, and integration with existing workflows"
    ], font_size=12)

    add_notes(slide, """SPEAKER NOTES – Slide 49 (BACKUP): AI Development Tool Comparison
-------------------------------------------------------------------
This comparison helps participants choose the right tools for their teaching context.

TOOL DETAILS:

GITHUB COPILOT:
- Best for: inline code completion, test generation, code explanation
- Integration: VS Code, JetBrains, Neovim
- Free for verified students and teachers through GitHub Education
- Strengths: seamless IDE integration, learns from your codebase context
- Limitations: less effective for architectural decisions, doesn't do full-file edits

CURSOR:
- Best for: agentic coding workflows, full-file editing, multi-file changes
- Built on VS Code — familiar interface with AI superpowers
- Composer mode for multi-file generation, chat for Q&A, agent mode for autonomous tasks
- Strengths: context-aware across entire projects, supports multiple AI models
- Cost consideration: $20/month may be a barrier for students

CLAUDE (ANTHROPIC):
- Best for: long-context analysis, architecture discussions, specification writing
- 200K token context window — can analyze large codebases
- Strong reasoning capabilities for complex design decisions
- Artifacts feature for generating structured documents
- MCP integration for tool connectivity

CHATGPT (OPENAI):
- Best for: general-purpose coding assistance, explaining concepts, brainstorming
- Broad training data covers many languages and frameworks
- Code Interpreter for running Python code directly
- Plugin ecosystem for extended capabilities

WINDSURF:
- Best for: end-to-end AI-native development with Cascade flows
- Unique approach: multi-step workflows that chain AI actions
- Good for demonstrating AI-native SDLC in practice

COST CONSIDERATIONS FOR ACADEMIC USE:
- Start with free tiers to evaluate
- Apply for educational discounts where available
- Consider institutional licenses for class-wide access
- Have offline alternatives ready for students without access
- Mix of tools often works best — different tools for different tasks""")
    n += 1

    # ── Slide 50: BACKUP - ADDITIONAL ARCHITECTURE PATTERNS ───────────
    slide = add_slide(prs)
    add_title_bar(slide, "BACKUP: Architecture Patterns for AI-Native Systems", "Backup", n)

    add_textbox(slide, 0.5, 1.15, 12.0, 0.4, "Advanced Architecture Patterns", 16, True, ACCENT_BLUE)

    # Three pattern cards
    patterns = [
        ("Event-Driven Architecture",
         "Components communicate via events\n\n"
         "Producer -> Event Bus -> Consumer\n\n"
         "Benefits:\n"
         "  Loose coupling between services\n"
         "  Scalable and resilient\n"
         "  Natural fit for async workflows",
         LIGHT_BLUE, ACCENT_BLUE),
        ("CQRS (Command Query\nResponsibility Segregation)",
         "Separate read and write models\n\n"
         "Commands -> Write Model\n"
         "Queries  -> Read Model\n\n"
         "Benefits:\n"
         "  Optimized read/write paths\n"
         "  Better scalability\n"
         "  Clearer domain model",
         LIGHT_GREEN, ACCENT_GREEN),
        ("Hexagonal Architecture\n(Ports & Adapters)",
         "Core logic isolated from I/O\n\n"
         "Adapters -> Ports -> Core\n\n"
         "Benefits:\n"
         "  Testable business logic\n"
         "  Swappable infrastructure\n"
         "  AI generates adapters easily",
         LIGHT_ORANGE, ACCENT_ORANGE),
    ]
    for i, (title, desc, bg, bdr) in enumerate(patterns):
        lft = 0.5 + i * 4.2
        add_rounded_box(slide, lft, 1.65, 3.9, 4.3,
                        f"{title}\n\n{desc}",
                        fill_color=bg, text_color=TEXT_DARK, font_size=10, bold=True,
                        border_color=bdr, alignment=PP_ALIGN.LEFT)

    # Bottom: when to use
    add_rounded_box(slide, 0.5, 6.15, 12.3, 0.5,
                    "Pattern Selection:  Event-Driven for microservices  |  "
                    "CQRS for read-heavy systems  |  "
                    "Hexagonal for testable, maintainable systems",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=12, bold=True,
                    border_color=ACCENT_ORANGE)

    add_notes(slide, """SPEAKER NOTES – Slide 50 (BACKUP): Architecture Patterns for AI-Native Systems
--------------------------------------------------------------------------------
Use this slide when discussing advanced architecture topics or when participants ask about more complex system designs.

EVENT-DRIVEN ARCHITECTURE:
- Components communicate by producing and consuming events through an event bus (Kafka, RabbitMQ, AWS SNS/SQS)
- Producers don't know about consumers — loose coupling
- Events are immutable facts: "TaskCreated", "UserRegistered", "PaymentProcessed"
- Benefits for AI-native: AI can generate event schemas, producers, and consumers independently
- When to use: microservices that need to communicate asynchronously, systems with complex workflows, real-time data processing
- Example prompt: "Design an event-driven architecture for a task management system where task creation triggers notification and audit logging"

CQRS (COMMAND QUERY RESPONSIBILITY SEGREGATION):
- Separate the read model (optimized for queries) from the write model (optimized for commands)
- Commands change state: CreateTask, UpdateTask, DeleteTask
- Queries read state: GetTasks, GetTaskById, SearchTasks
- Often combined with Event Sourcing — store events instead of current state
- Benefits for AI-native: clear separation makes it easier for AI to generate each side independently
- When to use: systems with very different read and write patterns, complex domains, audit requirements
- Example prompt: "Generate a CQRS implementation for task management with separate command and query handlers"

HEXAGONAL ARCHITECTURE (PORTS & ADAPTERS):
- Core business logic is isolated in the center with no external dependencies
- Ports: interfaces that define how the core communicates with the outside world
- Adapters: implementations of ports for specific technologies (REST adapter, database adapter, message queue adapter)
- Benefits for AI-native: the core logic is testable without infrastructure, AI can generate adapters for different technologies without touching business logic
- When to use: any system where you want maintainability, testability, and flexibility
- Example prompt: "Generate a hexagonal architecture for a grade calculator with ports for input (REST API) and output (database, PDF report)"

AI-NATIVE CONNECTION:
- These patterns make AI-generated code more maintainable because they enforce clear boundaries
- AI excels at generating adapter code (boilerplate) while humans focus on core business rules
- Pattern selection itself can be AI-assisted: describe your requirements and ask AI to recommend and justify a pattern choice
- Each pattern has well-documented templates that AI can follow""")
    n += 1

    return n

if __name__ == "__main__":
    prs = new_presentation()
    build(prs)
    save_deck(prs, "_part5_agent_gov_close.pptx")
