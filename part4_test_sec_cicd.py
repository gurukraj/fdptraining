"""Part 4 – Testing, Security & CI/CD (Slides 23-32)"""
from slide_helpers import *

def build(prs, start_num=23):
    n = start_num

    # ── Slide 23: Testing Strategy in AI-Native Development ────────────
    slide = add_slide(prs)
    add_title_bar(slide, "Testing Strategy in AI-Native Development", "Quality", n)

    add_textbox(slide, 0.6, 1.2, 5.5, 0.4, "Testing Pyramid", 18, True, ACCENT_GREEN)

    add_rounded_box(slide, 2.4, 1.8, 2.2, 0.7,
                    "E2E Tests\n(few, high-value)",
                    fill_color=LIGHT_ORANGE, text_color=TEXT_DARK,
                    font_size=11, bold=True, border_color=ACCENT_ORANGE)
    add_rounded_box(slide, 1.6, 2.65, 3.8, 0.7,
                    "Integration Tests\n(API, DB behavior)",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK,
                    font_size=11, bold=True, border_color=ACCENT_ORANGE)
    add_rounded_box(slide, 0.8, 3.5, 5.4, 0.7,
                    "Unit Tests\n(business rules, fast)",
                    fill_color=LIGHT_GREEN, text_color=TEXT_DARK,
                    font_size=11, bold=True, border_color=ACCENT_GREEN)

    add_textbox(slide, 1.0, 4.4, 5.0, 0.35,
                "Fewer tests              More tests",
                12, False, TEXT_MID, PP_ALIGN.CENTER)

    add_textbox(slide, 7.0, 1.2, 5.8, 0.4, "Key Principles", 18, True, ACCENT_GREEN)
    add_bullet_list(slide, 7.0, 1.75, 5.8, 4.5, [
        "Tests define whether generated code is acceptable",
        "Generate tests FROM acceptance criteria",
        "Unit tests cover business rules",
        "Integration tests cover API & database behavior",
        "E2E tests cover critical user journeys",
        "Tests are the specification's enforcement mechanism",
    ], font_size=14)

    add_rounded_box(slide, 1.0, 5.3, 11.3, 0.55,
                    "In AI-Native Development: Tests are written BEFORE code generation -- they define 'done'",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=13, bold=True,
                    border_color=ACCENT_ORANGE)

    flow_labels = ["Acceptance\nCriteria", "Test\nGeneration", "Code\nGeneration", "Validation"]
    flow_colors = [ACCENT_BLUE, ACCENT_GREEN, ACCENT_PURPLE, ACCENT_ORANGE]
    for i, (lbl, clr) in enumerate(zip(flow_labels, flow_colors)):
        add_rounded_box(slide, 1.2 + i * 2.8, 6.05, 2.2, 0.6,
                        lbl, fill_color=clr, text_color=WHITE, font_size=10, bold=True)
        if i < len(flow_labels) - 1:
            add_arrow_right(slide, 1.2 + i * 2.8 + 2.22, 6.18, 0.5, 0.01, TEXT_MID)

    add_notes(slide, """SPEAKER NOTES -- Slide 23: Testing Strategy in AI-Native Development
----------------------------------------------------------------------
THE TESTING PYRAMID:
- Base (Unit Tests): Most numerous. Test business rules, service methods, utility functions. Run in milliseconds. AI generates these FROM acceptance criteria.
- Middle (Integration Tests): Tests how components work together -- API endpoints, database queries. Slower but catch issues unit tests miss.
- Top (E2E Tests): Tests complete user journeys. Expensive to write/maintain, only cover critical paths.

WHY TESTING IS MORE IMPORTANT IN AI-NATIVE:
1. AI-generated code is plausible but potentially incorrect. Tests catch subtle bugs.
2. When specs change and code is regenerated, tests ensure no regressions.
3. Tests are executable documentation of what the system should do.

THE TEST-FIRST APPROACH:
- Prompt AI to generate tests from acceptance criteria BEFORE generating implementation code.
- This gives you a validation harness that every generated implementation must pass.

FLOW AT BOTTOM: Acceptance Criteria -> Tests -> Code -> Validation. This is the AI-native quality loop.

Discussion: "How does this change the way you teach testing? If tests come first and code is generated, what skills do students need?"
""")
    n += 1

    # ── Slide 24: AI-Assisted Test Generation ──────────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "AI-Assisted Test Generation", "Quality", n)

    flow_steps = ["Acceptance\nCriteria", "AI\nPrompt", "Generated\nTest Cases", "Human\nReview", "Test\nSuite"]
    flow_cols = [ACCENT_BLUE, ACCENT_ORANGE, ACCENT_PURPLE, ACCENT_GREEN, ACCENT_TEAL]
    for i, (lbl, clr) in enumerate(zip(flow_steps, flow_cols)):
        add_rounded_box(slide, 0.4 + i * 2.5, 1.2, 2.0, 0.7,
                        lbl, fill_color=clr, text_color=WHITE, font_size=11, bold=True)
        if i < len(flow_steps) - 1:
            add_arrow_right(slide, 0.4 + i * 2.5 + 2.02, 1.38, 0.4, 0.01, TEXT_MID)

    add_textbox(slide, 0.6, 2.1, 8.0, 0.35,
                "Example: Generated JUnit Tests for Task Management API", 14, True, ACCENT_BLUE)

    code = ("@Test\n"
            "void shouldCreateTaskSuccessfully() {\n"
            "    TaskRequest req = new TaskRequest(\n"
            "        \"Fix login bug\", \"HIGH\", \"user-1\");\n"
            "    TaskResponse res = taskService.create(req);\n"
            "    assertNotNull(res.getId());\n"
            "    assertEquals(\"OPEN\", res.getStatus());\n"
            "}\n"
            "\n"
            "@Test\n"
            "void shouldRejectDuplicateTask() {\n"
            "    // Given existing task with same title\n"
            "    assertThrows(DuplicateTaskException.class,\n"
            "        () -> taskService.create(duplicateReq));\n"
            "}")
    add_code_box(slide, 0.6, 2.5, 7.5, 3.6, code, font_size=11)

    add_textbox(slide, 8.5, 2.1, 4.5, 0.35,
                "Test Generation Best Practices", 14, True, ACCENT_GREEN)

    practice_cards = [
        ("Prompt Strategy", "Include acceptance criteria,\nedge cases, and expected\nbehaviors in the prompt", LIGHT_GREEN, ACCENT_GREEN),
        ("Review Checklist", "Verify assertions match spec,\ncheck boundary conditions,\nensure negative tests exist", LIGHT_ORANGE, ACCENT_ORANGE),
        ("Coverage Targets", "Line coverage > 80%\nBranch coverage > 70%\nMutation score > 60%", LIGHT_PURPLE, ACCENT_PURPLE),
    ]
    for i, (title, desc, bg, border) in enumerate(practice_cards):
        add_rounded_box(slide, 8.5, 2.55 + i * 1.35, 4.3, 1.15,
                        f"{title}\n{desc}", fill_color=bg, text_color=TEXT_DARK,
                        font_size=11, bold=True, border_color=border)

    add_notes(slide, """SPEAKER NOTES -- Slide 24: AI-Assisted Test Generation
--------------------------------------------------------
THE FLOW: Acceptance Criteria -> AI Prompt -> Generated Tests -> Human Review -> Test Suite.

THE CODE EXAMPLE:
- shouldCreateTaskSuccessfully(): Happy path. Creates valid request, verifies response has ID and status is OPEN.
- shouldRejectDuplicateTask(): Negative test. Verifies DuplicateTaskException on duplicate title. AI often misses negative tests.

BEST PRACTICES:
1. PROMPT STRATEGY: Include acceptance criteria, mention edge cases explicitly, specify framework.
2. REVIEW CHECKLIST: Verify assertions match spec, check boundaries, ensure negative tests exist.
3. COVERAGE TARGETS: Line > 80%, Branch > 70%, Mutation score > 60% (tests actually catch bugs).

Ask: "What's the difference between a test that runs code and a test that validates behavior?" High coverage doesn't mean good tests.
""")
    n += 1

    # ── Slide 25: Validation Matrix & Quality Gates ────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "Validation Matrix & Quality Gates", "Quality", n)

    rows = [
        ["Validation Type", "What it Checks", "Tools / Method", "When Applied"],
        ["Requirements Validation", "Correct features built", "Spec review, AI analysis", "Before coding"],
        ["Functional Validation", "Features work correctly", "Unit + integration tests", "Every commit"],
        ["Security Validation", "Access control, vulns", "SAST + DAST scans", "Every commit"],
        ["Performance Validation", "Response times, throughput", "Load tests (k6, JMeter)", "Before release"],
        ["Operational Validation", "Deploys correctly", "Smoke tests, health checks", "After deployment"],
    ]
    row_bg = [LIGHT_BLUE, LIGHT_GREEN, LIGHT_ORANGE, LIGHT_PURPLE, LIGHT_TEAL]
    add_table_shape(slide, 0.5, 1.2, 12.3, 3.5, rows, 4, row_colors=row_bg)

    add_textbox(slide, 0.6, 5.0, 12.0, 0.35, "Quality Gate Thresholds", 16, True, ACCENT_GREEN)

    gate_items = [
        ("Code Coverage\n> 80%", LIGHT_GREEN, ACCENT_GREEN),
        ("Critical Vulns\n= 0", LIGHT_ORANGE, ACCENT_ORANGE),
        ("P95 Response\n< 200ms", LIGHT_BLUE, ACCENT_BLUE),
        ("Mutation Score\n> 60%", LIGHT_PURPLE, ACCENT_PURPLE),
        ("Lint / Style\n0 Warnings", LIGHT_TEAL, ACCENT_TEAL),
    ]
    for i, (lbl, bg, border) in enumerate(gate_items):
        add_rounded_box(slide, 0.6 + i * 2.5, 5.45, 2.1, 0.8,
                        lbl, fill_color=bg, text_color=TEXT_DARK,
                        font_size=12, bold=True, border_color=border)

    add_rounded_box(slide, 2.0, 6.35, 9.3, 0.4,
                    "All gates must PASS before code is merged or deployed -- no exceptions",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=12, bold=True,
                    border_color=ACCENT_ORANGE)

    add_notes(slide, """SPEAKER NOTES -- Slide 25: Validation Matrix & Quality Gates
--------------------------------------------------------------
VALIDATION MATRIX:
1. Requirements Validation (Before Coding): Check that spec captures stakeholder needs. AI can help: "Review this spec for ambiguity and contradictions."
2. Functional Validation (Every Commit): Unit + integration tests verify code works correctly. Automated in CI.
3. Security Validation (Every Commit): SAST (SonarQube, Snyk Code) and DAST (OWASP ZAP). AI-generated code is particularly prone to security issues.
4. Performance Validation (Before Release): Load testing with measurable targets. AI code often has N+1 queries and missing indexes.
5. Operational Validation (After Deployment): Smoke tests, health checks in target environment.

QUALITY GATES: Non-negotiable thresholds:
- Code Coverage > 80%: Most code paths tested
- Critical Vulnerabilities = 0: No known critical security issues
- P95 Response < 200ms: Response time under 200ms
- Mutation Score > 60%: Tests actually catch injected bugs
- Lint 0 Warnings: Clean code standards enforced

KEY MESSAGE: All gates must pass. No manual overrides.
""")
    n += 1

    # ── Slide 26: Security in AI-Generated Software ────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "Security in AI-Generated Software", "Security", n)

    add_textbox(slide, 0.6, 1.2, 5.8, 0.4, "Unique Risks", 18, True, SECTION_COLORS["Security"])
    add_bullet_list(slide, 0.6, 1.75, 5.8, 3.8, [
        "AI may generate insecure defaults (open CORS, weak auth)",
        "Hallucinated dependencies that don't exist or are malicious",
        "Secrets may leak into prompts or generated code",
        "Over-permissive authorization patterns",
        "Missing input validation on user-facing endpoints",
        "Outdated security patterns from training data",
    ], font_size=14)

    risk_levels = [
        ("HIGH", LIGHT_ORANGE, ACCENT_ORANGE),
        ("HIGH", LIGHT_ORANGE, ACCENT_ORANGE),
        ("CRITICAL", LIGHT_ORANGE, SECTION_COLORS["Security"]),
        ("MEDIUM", LIGHT_YELLOW, ACCENT_ORANGE),
        ("HIGH", LIGHT_ORANGE, ACCENT_ORANGE),
        ("MEDIUM", LIGHT_YELLOW, ACCENT_ORANGE),
    ]
    for i, (level, bg, border) in enumerate(risk_levels):
        add_rounded_box(slide, 5.5, 1.85 + i * 0.62, 0.85, 0.4,
                        level, fill_color=bg, text_color=border,
                        font_size=9, bold=True, border_color=border)

    add_textbox(slide, 7.0, 1.2, 5.8, 0.4, "Mitigation Strategies", 18, True, ACCENT_GREEN)
    add_bullet_list(slide, 7.0, 1.75, 5.8, 3.8, [
        "Always review auth/authz code manually",
        "Scan dependencies automatically (Snyk, Dependabot)",
        "Use secret managers, never hardcode credentials",
        "Apply OWASP Top 10 checklist to generated code",
        "Include security tests in CI pipeline",
        "Conduct regular security-focused code reviews",
    ], font_size=14)

    add_rounded_box(slide, 1.0, 5.6, 11.3, 0.55,
                    "Security Mindset:  Trust but verify -- AI-generated code requires MORE security scrutiny, not less",
                    fill_color=LIGHT_ORANGE, text_color=TEXT_DARK, font_size=13, bold=True,
                    border_color=SECTION_COLORS["Security"])

    sec_flow = ["Generate\nCode", "SAST\nScan", "Dependency\nAudit", "Manual\nReview", "Secure\nCode"]
    sec_colors = [ACCENT_PURPLE, ACCENT_ORANGE, ACCENT_BLUE, ACCENT_GREEN, ACCENT_TEAL]
    for i, (lbl, clr) in enumerate(zip(sec_flow, sec_colors)):
        add_rounded_box(slide, 0.8 + i * 2.5, 6.2, 2.0, 0.55,
                        lbl, fill_color=clr, text_color=WHITE, font_size=10, bold=True)
        if i < len(sec_flow) - 1:
            add_arrow_right(slide, 0.8 + i * 2.5 + 2.02, 6.32, 0.4, 0.01, TEXT_MID)

    add_notes(slide, """SPEAKER NOTES -- Slide 26: Security in AI-Generated Software
--------------------------------------------------------------
UNIQUE RISKS:
1. INSECURE DEFAULTS: AI often generates CORS "*", .permitAll(), HTTP instead of HTTPS.
2. HALLUCINATED DEPENDENCIES: AI suggests packages that don't exist. Attackers register them ("dependency confusion").
3. SECRET LEAKAGE: Credentials in prompts may end up in generated code or AI training data.
4. OVER-PERMISSIVE AUTH: AI generates simple auth checks -- authenticated but not authorized for the specific resource.
5. MISSING INPUT VALIDATION: No @Valid annotations, no size limits, no format checks.
6. OUTDATED PATTERNS: MD5 for password hashing, JWT without expiration, etc.

MITIGATION STRATEGIES:
1. Manual auth review -- too critical for AI alone.
2. Snyk/Dependabot for dependency scanning.
3. Secret managers (Vault, AWS Secrets Manager).
4. OWASP Top 10 checklist per endpoint.
5. SAST/DAST in CI pipeline.
6. Regular security code reviews.

SECURITY WORKFLOW: Generate -> SAST -> Dependency Audit -> Manual Review -> Secure Code.
""")
    n += 1

    # ── Slide 27: OWASP Top 10 & Threat Modeling ───────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "OWASP-Oriented Security Review", "Security", n)

    add_textbox(slide, 0.6, 1.15, 12.0, 0.35,
                "Top OWASP Categories Relevant to AI-Generated Code", 16, True, SECTION_COLORS["Security"])

    owasp_items = [
        ("A01: Broken\nAccess Control", "Check: ownership validation,\nrole-based access, resource\nisolation between users", LIGHT_ORANGE, ACCENT_ORANGE),
        ("A03: Injection", "Check: parameterized queries,\ninput sanitization, ORM usage\nvs raw SQL", LIGHT_YELLOW, ACCENT_ORANGE),
        ("A05: Security\nMisconfiguration", "Check: CORS settings, debug\nmode off, default credentials\nremoved", LIGHT_BLUE, ACCENT_BLUE),
        ("A06: Vulnerable\nDependencies", "Check: dependency audit,\nno hallucinated packages,\nversion pinning", LIGHT_PURPLE, ACCENT_PURPLE),
        ("A02: Cryptographic\nFailures", "Check: proper hashing\n(bcrypt), TLS enforced,\nno sensitive data in logs", LIGHT_TEAL, ACCENT_TEAL),
    ]
    for i, (title, desc, bg, border) in enumerate(owasp_items):
        x = 0.5 + i * 2.5
        add_rounded_box(slide, x, 1.6, 2.2, 0.75,
                        title, fill_color=border, text_color=WHITE, font_size=10, bold=True)
        add_rounded_box(slide, x, 2.4, 2.2, 1.2,
                        desc, fill_color=bg, text_color=TEXT_DARK,
                        font_size=9, bold=False, border_color=border, alignment=PP_ALIGN.LEFT)

    add_textbox(slide, 0.6, 3.9, 12.0, 0.35, "Threat Modeling Mini-Framework", 16, True, ACCENT_BLUE)

    threat_steps = [
        ("Asset", "What are we\nprotecting?\n(user data, API keys)", LIGHT_BLUE, ACCENT_BLUE),
        ("Threat", "What could go\nwrong?\n(unauthorized access)", LIGHT_ORANGE, ACCENT_ORANGE),
        ("Control", "How do we\nprevent it?\n(auth, encryption)", LIGHT_GREEN, ACCENT_GREEN),
        ("Evidence", "How do we\nverify?\n(tests, scans, audits)", LIGHT_PURPLE, ACCENT_PURPLE),
    ]
    for i, (title, desc, bg, border) in enumerate(threat_steps):
        x = 1.0 + i * 3.0
        add_rounded_box(slide, x, 4.4, 2.5, 1.4,
                        f"{title}\n{desc}", fill_color=bg, text_color=TEXT_DARK,
                        font_size=11, bold=True, border_color=border)
        if i < len(threat_steps) - 1:
            add_arrow_right(slide, x + 2.52, 4.95, 0.4, 0.01, TEXT_MID)

    add_rounded_box(slide, 1.5, 6.1, 10.3, 0.5,
                    "Apply this framework to EVERY AI-generated endpoint: identify assets, model threats, implement controls, verify with tests",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=12, bold=True,
                    border_color=ACCENT_ORANGE)

    add_notes(slide, """SPEAKER NOTES -- Slide 27: OWASP-Oriented Security Review
------------------------------------------------------------
OWASP CATEGORIES:
1. A01 - BROKEN ACCESS CONTROL: AI checks auth but not authorization. Does every endpoint validate resource ownership?
2. A03 - INJECTION: AI sometimes generates raw SQL with string concatenation. Always use parameterized queries.
3. A05 - SECURITY MISCONFIGURATION: Debug mode, open CORS, default accounts. Create a security config checklist.
4. A06 - VULNERABLE DEPENDENCIES: Outdated versions with CVEs. Hallucinated packages. Run npm audit / mvn dependency-check.
5. A02 - CRYPTOGRAPHIC FAILURES: MD5 instead of bcrypt. Sensitive data in logs. Missing TLS.

THREAT MODELING FRAMEWORK:
- ASSET: What you're protecting (user data, auth tokens, API keys)
- THREAT: What could go wrong (unauthorized access, data exposure, injection)
- CONTROL: How to prevent (authentication, authorization, input validation)
- EVIDENCE: How to verify (security tests, SAST scans, penetration testing)

Exercise idea: Take one endpoint and apply this framework.
""")
    n += 1

    # ── Slide 28: Secure Coding Practices ──────────────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "Secure Coding Practices & DevSecOps", "Security", n)

    add_textbox(slide, 0.6, 1.15, 7.0, 0.35, "Secure Endpoint Pattern (Spring Boot)", 14, True, ACCENT_BLUE)

    secure_code = ("@PreAuthorize(\"hasRole('USER')\")\n"
                   "@PostMapping(\"/api/tasks\")\n"
                   "public ResponseEntity<TaskResponse> create(\n"
                   "    @Valid @RequestBody TaskRequest req,\n"
                   "    @AuthenticationPrincipal UserDetails user) {\n"
                   "    // Service validates ownership\n"
                   "    return ResponseEntity.status(201)\n"
                   "        .body(taskService.create(req, user.getId()));\n"
                   "}")
    add_code_box(slide, 0.6, 1.55, 7.0, 2.5, secure_code, font_size=11)

    annotations = [
        ("@PreAuthorize", "Method-level\nauthorization", LIGHT_GREEN, ACCENT_GREEN),
        ("@Valid", "Input\nvalidation", LIGHT_ORANGE, ACCENT_ORANGE),
        ("@AuthPrincipal", "User context\ninjection", LIGHT_BLUE, ACCENT_BLUE),
        ("user.getId()", "Ownership\nenforcement", LIGHT_PURPLE, ACCENT_PURPLE),
    ]
    for i, (label, desc, bg, border) in enumerate(annotations):
        add_rounded_box(slide, 8.0, 1.55 + i * 0.7, 2.2, 0.55,
                        f"{label}\n{desc}", fill_color=bg, text_color=TEXT_DARK,
                        font_size=9, bold=True, border_color=border)

    add_textbox(slide, 0.6, 4.3, 12.0, 0.35, "Key Secure Coding Practices", 16, True, SECTION_COLORS["Security"])

    practices = [
        ("Method-Level Auth", "Use @PreAuthorize or\nequivalent on every endpoint", LIGHT_GREEN, ACCENT_GREEN),
        ("Input Validation", "Always use @Valid, define\nconstraints on DTOs", LIGHT_ORANGE, ACCENT_ORANGE),
        ("Audit Logging", "Log security events: login,\naccess denied, data changes", LIGHT_BLUE, ACCENT_BLUE),
        ("Secret Management", "Use Vault or env vars,\nnever hardcode secrets", LIGHT_PURPLE, ACCENT_PURPLE),
        ("Dependency Audit", "Scan on every build,\nblock on critical CVEs", LIGHT_TEAL, ACCENT_TEAL),
    ]
    for i, (title, desc, bg, border) in enumerate(practices):
        add_rounded_box(slide, 0.5 + i * 2.5, 4.75, 2.2, 1.1,
                        f"{title}\n{desc}", fill_color=bg, text_color=TEXT_DARK,
                        font_size=10, bold=True, border_color=border)

    add_rounded_box(slide, 1.5, 6.1, 10.3, 0.55,
                    "DevSecOps: Security is not a phase -- it is embedded in every stage of the pipeline",
                    fill_color=LIGHT_YELLOW, text_color=TEXT_DARK, font_size=13, bold=True,
                    border_color=ACCENT_ORANGE)

    add_notes(slide, """SPEAKER NOTES -- Slide 28: Secure Coding Practices & DevSecOps
-----------------------------------------------------------------
CODE EXAMPLE WALKTHROUGH:
1. @PreAuthorize("hasRole('USER')"): Method-level authorization. AI often omits this.
2. @Valid on @RequestBody: Triggers Bean Validation. AI sometimes skips validation.
3. @AuthenticationPrincipal: Injects authenticated user. Critical for ownership validation.
4. user.getId() passed to service: Prevents horizontal privilege escalation. AI often accepts userId from request body.

KEY PRACTICES:
1. Method-Level Auth: Every endpoint needs authorization.
2. Input Validation: @NotBlank, @Size, @Email on DTOs.
3. Audit Logging: Log security events for forensic analysis.
4. Secret Management: Environment variables or secret managers.
5. Dependency Audit: Run scans on every build.

DEVSECOPS: Security is embedded in spec review, code generation prompts, CI pipeline, and post-deployment monitoring.
""")
    n += 1

    # ── Slide 29: CI/CD Pipeline Architecture ──────────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "CI/CD Pipeline Architecture", "DevOps", n)

    row1_stages = [
        ("Commit", ACCENT_BLUE),
        ("Build", ACCENT_BLUE),
        ("Unit\nTests", ACCENT_GREEN),
        ("SAST\nScan", ACCENT_ORANGE),
        ("Integration\nTests", ACCENT_GREEN),
        ("Docker\nBuild", ACCENT_BLUE),
    ]
    for i, (label, clr) in enumerate(row1_stages):
        x = 0.5 + i * 2.1
        add_rounded_box(slide, x, 1.3, 1.7, 0.7,
                        label, fill_color=clr, text_color=WHITE, font_size=10, bold=True)
        if i < len(row1_stages) - 1:
            add_arrow_right(slide, x + 1.72, 1.48, 0.3, 0.01, TEXT_MID)

    add_arrow_down(slide, 12.15, 2.05, 0.3, 0.35, TEXT_MID)

    row2_stages = [
        ("Security\nScan", ACCENT_ORANGE),
        ("Deploy\nStaging", ACCENT_PURPLE),
        ("Smoke\nTests", ACCENT_GREEN),
        ("Approval\nGate", ACCENT_ORANGE),
        ("Deploy\nProd", ACCENT_PURPLE),
    ]
    for i, (label, clr) in enumerate(row2_stages):
        x = 0.5 + i * 2.5
        add_rounded_box(slide, x, 2.6, 1.9, 0.7,
                        label, fill_color=clr, text_color=WHITE, font_size=10, bold=True)
        if i < len(row2_stages) - 1:
            add_arrow_right(slide, x + 1.92, 2.78, 0.5, 0.01, TEXT_MID)

    add_textbox(slide, 0.6, 3.6, 12.0, 0.35, "Stage Categories", 14, True, ACCENT_BLUE)
    legend_items = [("Build", ACCENT_BLUE), ("Test", ACCENT_GREEN), ("Security", ACCENT_ORANGE), ("Deploy", ACCENT_PURPLE)]
    for i, (lbl, clr) in enumerate(legend_items):
        add_rounded_box(slide, 0.6 + i * 2.2, 4.0, 1.8, 0.4,
                        lbl, fill_color=clr, text_color=WHITE, font_size=11, bold=True)

    add_textbox(slide, 0.6, 4.65, 6.0, 0.35, "Quality Gates (enforced automatically)", 14, True, ACCENT_GREEN)
    add_bullet_list(slide, 0.6, 5.0, 6.0, 1.5, [
        "All unit & integration tests pass",
        "Code coverage >= 80%",
        "Zero critical security vulnerabilities",
        "Docker image scanned and signed",
        "Staging smoke tests pass",
    ], font_size=12)

    add_textbox(slide, 7.2, 4.65, 5.5, 0.35, "Release Strategy", 14, True, ACCENT_PURPLE)
    add_bullet_list(slide, 7.2, 5.0, 5.5, 1.5, [
        "Feature branches -> PR -> main (trunk-based)",
        "Automated deployment to staging on merge",
        "Manual approval gate for production",
        "Blue-green or canary deployment",
        "Automatic rollback on health check failure",
    ], font_size=12)

    add_notes(slide, """SPEAKER NOTES -- Slide 29: CI/CD Pipeline Architecture
--------------------------------------------------------
PIPELINE STAGES:
1. COMMIT: Push triggers pipeline.
2. BUILD: Compile, resolve dependencies, generate artifacts. Fails fast on compilation errors.
3. UNIT TESTS: Run all unit tests (< 60 seconds). Pipeline stops on failure.
4. SAST SCAN: SonarQube/Snyk Code analyzes source for vulnerabilities.
5. INTEGRATION TESTS: Test API endpoints, DB interactions. Use Testcontainers.
6. DOCKER BUILD: Build minimal image, tag with commit SHA.
7. SECURITY SCAN: Scan Docker image with Trivy/Snyk Container.
8. DEPLOY STAGING: Apply K8s manifests to staging environment.
9. SMOKE TESTS: Hit health endpoints, verify key flows.
10. APPROVAL GATE: Manual checkpoint before production.
11. DEPLOY PROD: Blue-green or canary with automatic rollback.

QUALITY GATES: Non-negotiable. No manual overrides.
RELEASE STRATEGY: Trunk-based development with feature branches and PRs.

Ask: "Does your curriculum include CI/CD? This is critical for industry readiness."
""")
    n += 1

    # ── Slide 30: CI/CD Implementation - GitHub Actions ────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "CI/CD Implementation: GitHub Actions", "DevOps", n)

    yaml_code = ("name: ai-native-ci\n"
                 "on: [push, pull_request]\n"
                 "jobs:\n"
                 "  build-test-scan:\n"
                 "    runs-on: ubuntu-latest\n"
                 "    steps:\n"
                 "      - uses: actions/checkout@v4\n"
                 "      - uses: actions/setup-java@v4\n"
                 "        with: { java-version: '21' }\n"
                 "      - run: ./mvnw verify\n"
                 "      - run: ./mvnw sonar:sonar\n"
                 "      - uses: snyk/actions/maven@master\n"
                 "      - uses: docker/build-push-action@v5\n"
                 "        with:\n"
                 "          push: true\n"
                 "          tags: app:${{ github.sha }}\n"
                 "  deploy-staging:\n"
                 "    needs: build-test-scan\n"
                 "    runs-on: ubuntu-latest\n"
                 "    steps:\n"
                 "      - run: kubectl apply -f k8s/\n"
                 "      - run: ./scripts/smoke-test.sh")
    add_code_box(slide, 0.6, 1.2, 7.5, 5.0, yaml_code, font_size=11)

    add_textbox(slide, 8.5, 1.2, 4.5, 0.35, "Pipeline Breakdown", 16, True, ACCENT_ORANGE)

    annotation_cards = [
        ("Trigger", "Runs on every push and\npull request to any branch", LIGHT_BLUE, ACCENT_BLUE),
        ("Build & Test", "./mvnw verify compiles,\nruns unit + integration tests", LIGHT_GREEN, ACCENT_GREEN),
        ("Code Quality", "SonarQube scans for bugs,\ncode smells, vulnerabilities", LIGHT_ORANGE, ACCENT_ORANGE),
        ("Dependency Scan", "Snyk checks all Maven\ndependencies for CVEs", LIGHT_PURPLE, ACCENT_PURPLE),
        ("Docker Build", "Builds and pushes image\ntagged with commit SHA", LIGHT_TEAL, ACCENT_TEAL),
        ("Deploy Staging", "Applies K8s manifests and\nruns smoke test scripts", LIGHT_YELLOW, ACCENT_ORANGE),
    ]
    for i, (title, desc, bg, border) in enumerate(annotation_cards):
        add_rounded_box(slide, 8.5, 1.65 + i * 0.82, 4.3, 0.7,
                        f"{title}: {desc}", fill_color=bg, text_color=TEXT_DARK,
                        font_size=10, bold=True, border_color=border, alignment=PP_ALIGN.LEFT)

    add_rounded_box(slide, 1.0, 6.35, 11.3, 0.4,
                    "Tip: AI can generate the entire pipeline YAML from your specification and architecture decisions",
                    fill_color=LIGHT_GREEN, text_color=TEXT_DARK, font_size=12, bold=True,
                    border_color=ACCENT_GREEN)

    add_notes(slide, """SPEAKER NOTES -- Slide 30: CI/CD Implementation: GitHub Actions
-----------------------------------------------------------------
LINE-BY-LINE:
- on: [push, pull_request]: Triggers on every push and PR.
- actions/checkout@v4: Checks out code.
- actions/setup-java@v4: Installs Java 21.
- ./mvnw verify: Compiles, runs tests, packages. Fails on test failure.
- ./mvnw sonar:sonar: Code quality analysis.
- snyk/actions/maven@master: Dependency vulnerability scan.
- docker/build-push-action@v5: Build Docker image tagged with commit SHA.
- deploy-staging needs build-test-scan: Only deploys after all checks pass.
- kubectl apply + smoke-test.sh: Deploy and verify.

HOW AI HELPS: Prompt "Generate GitHub Actions workflow for Spring Boot with Maven, SonarQube, Snyk, Docker build, K8s deployment." AI generates 80-90%.

Ask: "Does your curriculum include CI/CD? This is critical for industry readiness."
""")
    n += 1

    # ── Slide 31: Docker & Deployment ──────────────────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "Containerization & Deployment", "DevOps", n)

    add_textbox(slide, 0.6, 1.15, 5.5, 0.35, "Dockerfile (Production-Ready)", 14, True, ACCENT_BLUE)

    dockerfile_code = ("FROM eclipse-temurin:21-jre-alpine\n"
                       "WORKDIR /app\n"
                       "COPY target/task-api.jar app.jar\n"
                       "EXPOSE 8080\n"
                       "USER 1001\n"
                       "ENTRYPOINT [\"java\", \"-jar\", \"app.jar\"]")
    add_code_box(slide, 0.6, 1.55, 5.5, 2.0, dockerfile_code, font_size=11)

    df_notes = [
        ("Alpine base", "Minimal image (~80MB vs ~400MB)", LIGHT_GREEN),
        ("Non-root user", "Security: runs as UID 1001", LIGHT_ORANGE),
        ("Single JAR", "Fat JAR includes all dependencies", LIGHT_BLUE),
    ]
    for i, (title, desc, bg) in enumerate(df_notes):
        add_rounded_box(slide, 0.6 + i * 1.85, 3.7, 1.7, 0.75,
                        f"{title}\n{desc}", fill_color=bg, text_color=TEXT_DARK, font_size=9, bold=True)

    add_textbox(slide, 6.8, 1.15, 6.0, 0.35, "Deployment Architecture", 14, True, ACCENT_PURPLE)

    deploy_flow = [
        ("Docker\nImage", ACCENT_BLUE),
        ("Container\nRegistry", ACCENT_ORANGE),
        ("Kubernetes\nCluster", ACCENT_PURPLE),
        ("Pod", ACCENT_GREEN),
    ]
    for i, (lbl, clr) in enumerate(deploy_flow):
        x = 6.8 + i * 1.6
        add_rounded_box(slide, x, 1.6, 1.3, 0.7,
                        lbl, fill_color=clr, text_color=WHITE, font_size=10, bold=True)
        if i < len(deploy_flow) - 1:
            add_arrow_right(slide, x + 1.32, 1.78, 0.2, 0.01, TEXT_MID)

    k8s_components = [
        ("ConfigMap", "App config,\nenvironment vars", LIGHT_BLUE, ACCENT_BLUE),
        ("Secret", "DB passwords,\nAPI keys", LIGHT_ORANGE, ACCENT_ORANGE),
        ("Service", "Internal load\nbalancing", LIGHT_GREEN, ACCENT_GREEN),
        ("Ingress", "External traffic\nrouting + TLS", LIGHT_PURPLE, ACCENT_PURPLE),
    ]
    for i, (title, desc, bg, border) in enumerate(k8s_components):
        x = 6.8 + i * 1.6
        add_rounded_box(slide, x, 2.55, 1.3, 0.95,
                        f"{title}\n{desc}", fill_color=bg, text_color=TEXT_DARK,
                        font_size=9, bold=True, border_color=border)

    add_textbox(slide, 0.6, 4.7, 12.0, 0.35, "Deployment Strategies", 16, True, ACCENT_ORANGE)

    strategies = [
        ("Rolling Update", "Replace pods gradually\nZero-downtime deployment\nAutomatic rollback on failure", LIGHT_BLUE, ACCENT_BLUE),
        ("Blue-Green", "Two identical environments\nSwitch traffic instantly\nEasy rollback to old version", LIGHT_GREEN, ACCENT_GREEN),
        ("Canary", "Route small % to new version\nMonitor error rates\nGradual traffic increase", LIGHT_ORANGE, ACCENT_ORANGE),
        ("Feature Flags", "Deploy code, toggle features\nTest in production safely\nGradual feature rollout", LIGHT_PURPLE, ACCENT_PURPLE),
    ]
    for i, (title, desc, bg, border) in enumerate(strategies):
        add_rounded_box(slide, 0.5 + i * 3.15, 5.1, 2.8, 1.2,
                        f"{title}\n{desc}", fill_color=bg, text_color=TEXT_DARK,
                        font_size=10, bold=True, border_color=border, alignment=PP_ALIGN.LEFT)

    add_notes(slide, """SPEAKER NOTES -- Slide 31: Containerization & Deployment
-----------------------------------------------------------
DOCKERFILE:
1. FROM eclipse-temurin:21-jre-alpine: JRE only (not JDK), Alpine for minimal size (~80MB vs ~400MB).
2. WORKDIR /app: Working directory inside container.
3. COPY target/task-api.jar: Copy compiled JAR.
4. EXPOSE 8080: Document the port (metadata only).
5. USER 1001: CRITICAL -- run as non-root. AI often generates root Dockerfiles.
6. ENTRYPOINT: Exec form for proper signal handling.

DEPLOYMENT ARCHITECTURE: Docker Image -> Registry -> K8s Cluster -> Pods. Supporting: ConfigMap, Secret, Service, Ingress.

DEPLOYMENT STRATEGIES:
1. Rolling Update: Replace pods one at a time. Zero downtime.
2. Blue-Green: Two environments, instant switch, easy rollback.
3. Canary: Route small traffic %, monitor, gradually increase.
4. Feature Flags: Deploy disabled, toggle for specific users.

AI generates K8s manifests from specs. Always review security (non-root, resource limits, secrets).
""")
    n += 1

    # ── Slide 32: Performance & Scale Testing ──────────────────────────
    slide = add_slide(prs)
    add_title_bar(slide, "Performance & Scale Testing", "Performance", n)

    add_textbox(slide, 0.6, 1.15, 5.8, 0.4,
                "Performance Risks in AI-Generated Code", 15, True, ACCENT_TEAL)
    perf_risks = [
        ("N+1 Query Patterns", ["AI generates loops with individual DB queries"]),
        ("Missing Database Indexes", ["No indexes on frequently queried columns"]),
        ("Inefficient Serialization", ["Deep object graphs without DTOs"]),
        ("Over-Fetching Data", ["SELECT * instead of specific columns"]),
        ("No Caching Strategy", ["Every request hits the database directly"]),
    ]
    add_bullet_list(slide, 0.6, 1.6, 5.8, 3.0, perf_risks, font_size=12)

    add_textbox(slide, 7.0, 1.15, 5.8, 0.4, "Performance Testing Approach", 15, True, ACCENT_GREEN)
    add_bullet_list(slide, 7.0, 1.6, 5.8, 1.8, [
        "Define measurable targets (P95 < 200ms, 100 concurrent users)",
        "Use k6 or JMeter for load testing",
        "Monitor with OpenTelemetry / Prometheus",
        "Profile and optimize bottlenecks iteratively",
    ], font_size=13)

    perf_targets = [
        ("P95 Latency\n< 200ms", LIGHT_GREEN, ACCENT_GREEN),
        ("Throughput\n> 500 req/s", LIGHT_BLUE, ACCENT_BLUE),
        ("Concurrent\n100 users", LIGHT_ORANGE, ACCENT_ORANGE),
        ("Error Rate\n< 0.1%", LIGHT_PURPLE, ACCENT_PURPLE),
    ]
    for i, (lbl, bg, border) in enumerate(perf_targets):
        add_rounded_box(slide, 7.0 + i * 1.5, 3.5, 1.3, 0.75,
                        lbl, fill_color=bg, text_color=TEXT_DARK,
                        font_size=10, bold=True, border_color=border)

    add_textbox(slide, 0.6, 4.55, 12.0, 0.35, "Load Test Example (k6)", 14, True, ACCENT_TEAL)

    k6_code = ("import http from 'k6/http';\n"
               "export default function() {\n"
               "  http.post('http://localhost:8080/api/tasks',\n"
               "    JSON.stringify({title:'Test',priority:'HIGH'}),\n"
               "    {headers:{'Content-Type':'application/json'}});\n"
               "}\n"
               "export const options = { vus: 50, duration: '30s' };")
    add_code_box(slide, 0.6, 4.95, 7.0, 2.0, k6_code, font_size=11)

    add_textbox(slide, 8.0, 4.55, 4.8, 0.35, "Monitoring Stack", 14, True, ACCENT_ORANGE)
    monitor_items = [
        ("OpenTelemetry", "Distributed tracing &\nmetrics collection", LIGHT_BLUE, ACCENT_BLUE),
        ("Prometheus", "Time-series metrics\nstorage & alerting", LIGHT_ORANGE, ACCENT_ORANGE),
        ("Grafana", "Dashboards for\nreal-time visibility", LIGHT_GREEN, ACCENT_GREEN),
    ]
    for i, (title, desc, bg, border) in enumerate(monitor_items):
        add_rounded_box(slide, 8.0, 4.95 + i * 0.7, 4.8, 0.6,
                        f"{title}: {desc}", fill_color=bg, text_color=TEXT_DARK,
                        font_size=10, bold=True, border_color=border, alignment=PP_ALIGN.LEFT)

    add_notes(slide, """SPEAKER NOTES -- Slide 32: Performance & Scale Testing
--------------------------------------------------------
PERFORMANCE RISKS:
1. N+1 QUERIES: AI loops with individual DB queries. Fix: JOIN FETCH, @EntityGraph.
2. MISSING INDEXES: No @Index on queried columns. Performance: O(n) -> O(log n).
3. INEFFICIENT SERIALIZATION: Return entities directly, triggering lazy loads. Fix: Use DTOs.
4. OVER-FETCHING: findAll() with no pagination. Fix: Pageable, projections.
5. NO CACHING: Every request hits DB. Fix: @Cacheable, Redis/Caffeine.

K6 LOAD TEST: 50 virtual users for 30 seconds. Output: P50/P90/P95/P99, error rate.

MONITORING: OpenTelemetry for tracing, Prometheus for metrics, Grafana for dashboards.

EXERCISE: Run k6 against Task API, identify slow endpoints, add indexes, measure improvement.
""")
    n += 1

    return n

if __name__ == "__main__":
    prs = new_presentation()
    build(prs)
    save_deck(prs, "_part4_test_sec_cicd.pptx")
