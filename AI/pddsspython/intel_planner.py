import re


REQUIRED_KEYS = [
    "Project Size",
    "Project Complexity",
    "Requirements Clarity",
    "Team Size",
    "Stakeholder Involvement",
    "Budget",
    "Regulatory Compliance",
    "Innovation Level",
    "Risk Tolerance",
    "Urgency/Time-to-Market",
    "Project Type (Implicit)",
    "DevOps Implemented",
]


def _norm(text):
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def _contains_any(text, words):
    return any(w in text for w in words)


def _number_in_text(text):
    m = re.search(r"\b(\d{1,3})\b", text)
    return int(m.group(1)) if m else None


def infer_project_type(text):
    if _contains_any(text, ["mobile", "android", "ios", "flutter", "react native"]):
        return "Mobile App"
    if _contains_any(text, ["web app", "website", "web", "saas", "frontend", "backend"]):
        return "Web Application"
    if _contains_any(text, ["api", "backend", "microservice", "rest", "graphql"]):
        return "API/Backend Service"
    if _contains_any(text, ["ml", "machine learning", "ai", "model", "nlp"]):
        return "Machine Learning"
    if _contains_any(text, ["data science", "analytics", "data pipeline", "dashboard"]):
        return "Data Science"
    if _contains_any(text, ["desktop", "electron", "windows app", "mac app"]):
        return "Desktop App"
    if _contains_any(text, ["game", "unity", "unreal", "gamedev"]):
        return "Game Development"
    if _contains_any(text, ["embedded", "iot", "firmware", "microcontroller"]):
        return "Embedded System"
    if _contains_any(text, ["enterprise", "erp", "crm", "b2b"]):
        return "Enterprise Applications"
    if _contains_any(text, ["cross platform", "cross-platform"]):
        return "Cross Platform App"
    return "Other"


def infer_team_size(text):
    n = _number_in_text(text)
    if n is not None:
        if n <= 5:
            return "Small (1-5)"
        if n <= 20:
            return "Medium (6-20)"
        if n <= 50:
            return "Large (21-50)"
        return "Very Large (50+)"
    if _contains_any(text, ["solo", "single developer", "one person", "small team"]):
        return "Small (1-5)"
    if _contains_any(text, ["medium team", "team", "squad"]):
        return "Medium (6-20)"
    if _contains_any(text, ["large team", "enterprise team"]):
        return "Large (21-50)"
    if _contains_any(text, ["very large", "organization", "multiple teams"]):
        return "Very Large (50+)"
    return "Small (1-5)"


def infer_complexity(text):
    if _contains_any(text, ["very complex", "distributed", "enterprise", "multi-tenant", "high scale"]):
        return "Very High"
    if _contains_any(text, ["complex", "scalable", "high load", "real time", "real-time"]):
        return "High"
    if _contains_any(text, ["moderate", "medium", "standard"]):
        return "Medium"
    if _contains_any(text, ["simple", "mvp", "prototype", "basic"]):
        return "Low"
    return "Medium"


def infer_requirements_clarity(text):
    if _contains_any(text, ["not sure", "exploring", "idea", "vague", "unclear"]):
        return "Unclear"
    if _contains_any(text, ["iterative", "evolving", "changing", "flexible"]):
        return "Evolving"
    if _contains_any(text, ["fixed", "defined", "clear requirements", "spec"]):
        return "Clear"
    return "Evolving"


def infer_stakeholder_involvement(text):
    if _contains_any(text, ["stakeholder", "client", "customer review", "approval"]):
        return "High"
    if _contains_any(text, ["internal", "team only"]):
        return "Low"
    return "Medium"


def infer_budget(text):
    if _contains_any(text, ["bootstrap", "low budget", "no budget", "cheap"]):
        return "Low"
    if _contains_any(text, ["medium budget", "moderate budget"]):
        return "Medium"
    if _contains_any(text, ["high budget", "funded", "enterprise budget"]):
        return "High"
    return "Medium"


def infer_regulatory(text):
    if _contains_any(text, ["hipaa", "gdpr", "pci", "sox", "regulatory", "compliance"]):
        return "High"
    return "Low"


def infer_innovation(text):
    if _contains_any(text, ["novel", "research", "ai", "new", "innovative"]):
        return "High"
    return "Medium"


def infer_risk_tolerance(text):
    if _contains_any(text, ["mission critical", "safety", "risk averse", "conservative"]):
        return "Low"
    if _contains_any(text, ["risk", "experimental"]):
        return "High"
    return "Medium"


def infer_urgency(text):
    if _contains_any(text, ["asap", "urgent", "deadline", "fast", "quick"]):
        return "High"
    if _contains_any(text, ["no rush", "long term"]):
        return "Low"
    return "Medium"


def infer_devops(text):
    if _contains_any(text, ["ci", "cd", "cicd", "docker", "kubernetes", "devops"]):
        return "Yes"
    return "No"


def infer_scalability(text):
    if _contains_any(text, ["scale", "scalable", "millions", "high traffic"]):
        return "High"
    if _contains_any(text, ["some scale", "moderate traffic"]):
        return "Medium"
    return "Low"


def infer_realtime(text):
    if _contains_any(text, ["real time", "real-time", "streaming", "live", "low latency"]):
        return "Yes"
    return "No"


def prompt_to_pdss_input(prompt):
    text = _norm(prompt)
    characteristics = {
        "Project Size": "Small",
        "Project Complexity": infer_complexity(text),
        "Requirements Clarity": infer_requirements_clarity(text),
        "Team Size": infer_team_size(text),
        "Stakeholder Involvement": infer_stakeholder_involvement(text),
        "Budget": infer_budget(text),
        "Regulatory Compliance": infer_regulatory(text),
        "Innovation Level": infer_innovation(text),
        "Risk Tolerance": infer_risk_tolerance(text),
        "Urgency/Time-to-Market": infer_urgency(text),
        "Project Type (Implicit)": infer_project_type(text),
        "DevOps Implemented": infer_devops(text),
    }

    project_type = characteristics["Project Type (Implicit)"]
    if project_type in ["Web Application", "Mobile App", "Enterprise Applications", "API/Backend Service"]:
        characteristics["Scalability Needs"] = infer_scalability(text)
    if project_type in ["Data Science", "Machine Learning", "Embedded System"]:
        characteristics["Real-time Processing"] = infer_realtime(text)

    return characteristics


def _rec_first(recs, key, fallback=""):
    values = recs.get(key) or []
    return values[0] if values else fallback


def _listify(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _explain_recommendation(label, value):
    if not value:
        return ""
    return f"{label}: {value} helps align the team on a proven approach for this project profile."


def _build_rationales(characteristics, recommendations):
    items = []
    life_cycle = _rec_first(recommendations, "Life Cycle")
    methodology = _rec_first(recommendations, "Methodology")
    language = _rec_first(recommendations, "Language")
    arch = _rec_first(recommendations, "Model (Architectural)")
    testing = _rec_first(recommendations, "Testing Strategy")
    deployment = _rec_first(recommendations, "Deployment")
    risk = _rec_first(recommendations, "Risk Management")
    docs = _rec_first(recommendations, "Documentation")
    tools = _rec_first(recommendations, "Collaboration Tools")

    if life_cycle:
        items.append(
            f"Life cycle: {life_cycle} suits "
            f"{characteristics.get('Requirements Clarity').lower()} requirements and "
            f"{characteristics.get('Project Complexity').lower()} complexity by enabling the right cadence of feedback."
        )
    if methodology:
        items.append(
            f"Methodology: {methodology} improves delivery flow and coordination given "
            f"team size {characteristics.get('Team Size')} and "
            f"{characteristics.get('Urgency/Time-to-Market').lower()} urgency."
        )
    if language:
        items.append(
            f"Language: {language} balances development speed with maintainability for a "
            f"{characteristics.get('Project Type (Implicit)')}."
        )
    if arch:
        items.append(
            f"Architecture: {arch} reduces coupling and supports scaling as the project grows."
        )
    if testing:
        items.append(
            f"Testing: {testing} mitigates risk and keeps quality stable as features expand."
        )
    if deployment:
        items.append(
            f"Deployment: {deployment} reduces rollout risk and supports fast iteration."
        )
    if risk:
        items.append(
            f"Risk management: {risk} is critical for "
            f"{characteristics.get('Risk Tolerance').lower()} risk tolerance."
        )
    if docs:
        items.append(
            f"Documentation: {docs} keeps knowledge shared across stakeholders and new team members."
        )
    if tools:
        items.append(
            f"Collaboration tools: {tools} help maintain alignment and traceability."
        )
    return items


def _feature_hints(prompt):
    text = _norm(prompt)
    return {
        "auth": _contains_any(text, ["login", "auth", "authentication", "oauth", "sso"]),
        "payments": _contains_any(text, ["payment", "billing", "subscription", "stripe", "paypal"]),
        "notifications": _contains_any(text, ["email", "sms", "push", "notification", "alerts"]),
        "chat": _contains_any(text, ["chat", "messaging", "real-time", "realtime"]),
        "search": _contains_any(text, ["search", "filter", "query"]),
        "analytics": _contains_any(text, ["analytics", "dashboard", "metrics", "reports"]),
        "admin": _contains_any(text, ["admin", "moderation", "backoffice"]),
        "uploads": _contains_any(text, ["upload", "file", "media", "image", "video", "document"]),
        "ai": _contains_any(text, ["ai", "ml", "machine learning", "nlp", "vision"]),
        "integrations": _contains_any(text, ["integration", "webhook", "third party", "third-party"]),
        "compliance": _contains_any(text, ["hipaa", "gdpr", "pci", "sox", "compliance"]),
        "multi_tenant": _contains_any(text, ["multi-tenant", "multitenant", "enterprise"]),
        "realtime": _contains_any(text, ["realtime", "real-time", "live", "streaming"]),
        "offline": _contains_any(text, ["offline", "sync"]),
        "geolocation": _contains_any(text, ["gps", "geolocation", "location", "maps"]),
        "marketplace": _contains_any(text, ["marketplace", "buyers", "sellers", "two-sided"]),
        "mobile": _contains_any(text, ["mobile", "android", "ios", "flutter", "react native"]),
        "accessibility": _contains_any(text, ["accessibility", "a11y", "wcag"]),
        "education": _contains_any(text, ["education", "school", "student", "teacher", "tutor", "course", "lms"]),
        "healthcare": _contains_any(text, ["healthcare", "hospital", "clinic", "patient", "doctor", "medical"]),
        "fintech": _contains_any(text, ["fintech", "finance", "bank", "wallet", "payment", "billing"]),
        "logistics": _contains_any(text, ["logistics", "delivery", "fleet", "warehouse", "route", "shipping"]),
        "ecommerce": _contains_any(text, ["ecommerce", "store", "cart", "checkout", "product", "inventory"]),
        "hr": _contains_any(text, ["hr", "recruiting", "hiring", "payroll", "employee"]),
    }


def _narrative_sections(prompt, characteristics, recommendations):
    project_type = characteristics.get("Project Type (Implicit)")
    complexity = characteristics.get("Project Complexity")
    urgency = characteristics.get("Urgency/Time-to-Market")
    clarity = characteristics.get("Requirements Clarity")
    team_size = characteristics.get("Team Size")
    budget = characteristics.get("Budget")
    regulatory = characteristics.get("Regulatory Compliance")
    innovation = characteristics.get("Innovation Level")

    life_cycle = _rec_first(recommendations, "Life Cycle", "Iterative")
    methodology = _rec_first(recommendations, "Methodology", "Agile")
    language = _rec_first(recommendations, "Language", "Python")
    arch = _rec_first(recommendations, "Model (Architectural)", "Layered")
    testing = _rec_first(recommendations, "Testing Strategy", "Automated testing with CI")
    deployment = _rec_first(recommendations, "Deployment", "Staged rollout")

    summary = (
        f"This {project_type} project targets {urgency.lower()} delivery with "
        f"{complexity.lower()} complexity and {clarity.lower()} requirements. "
        f"A {life_cycle} life cycle and {methodology} workflow will keep the team aligned "
        f"and reduce rework. {language} is recommended to maximize delivery speed, "
        f"while a {arch} architecture keeps long-term maintainability strong."
    )

    scope = (
        f"Scope should prioritize the critical user journeys for a {project_type}, "
        f"define the data model early, and lock down API contracts before scaling. "
        f"Given a {budget.lower()} budget and {team_size.lower()} team size, "
        f"the MVP should be tight and measurable."
    )

    risks = (
        f"Key risks include requirement shifts ({clarity.lower()}), "
        f"delivery pressure ({urgency.lower()} urgency), and integration complexity. "
        f"{testing} and {deployment} reduce regression and rollout risk."
    )

    compliance = ""
    if regulatory in ["High", "Very High"]:
        compliance = (
            "Compliance is a major constraint. Build security, auditability, and "
            "data minimization into the core design to avoid costly rework."
        )
    elif regulatory == "Medium":
        compliance = (
            "Compliance should be addressed early with data handling policies and logging."
        )
    else:
        compliance = (
            "Compliance risk is low, so focus on reliability and user experience first."
        )

    innovation_note = ""
    if innovation in ["High", "Very High"]:
        innovation_note = (
            "Innovation is high, so prototype uncertain components early and validate "
            "with quick experiments before committing to the full build."
        )
    else:
        innovation_note = (
            "Innovation level is moderate, so focus on execution quality and stable delivery."
        )

    rationales = _build_rationales(characteristics, recommendations)

    sections = [
        ("Summary", summary),
        ("Prompt Understanding", prompt or "N/A"),
        ("Scope and Requirements", scope),
        ("Risks and Mitigations", risks),
        ("Compliance and Security", compliance),
        ("Innovation Strategy", innovation_note),
        ("Recommendation Rationale", "\n".join(rationales) if rationales else "No specific rationale available."),
    ]
    return sections


def _tech_stack_suggestions(characteristics, recommendations):
    project_type = characteristics.get("Project Type (Implicit)")
    language = _rec_first(recommendations, "Language", "Python")
    arch = _rec_first(recommendations, "Model (Architectural)", "Layered")
    items = []

    if project_type in ["Web Application", "API/Backend Service"]:
        items.append(f"Backend: {language} with a modular service layout to support {arch} patterns.")
        items.append("API: REST or GraphQL with explicit versioning and contract tests.")
        items.append("Storage: relational DB for core entities and a cache for hot paths.")
    elif project_type in ["Mobile App", "Cross Platform App"]:
        items.append("Client: cross-platform UI framework with offline-safe state management.")
        items.append("Sync: background sync jobs and conflict resolution policy.")
    elif project_type in ["Machine Learning", "Data Science"]:
        items.append(f"Modeling: {language} pipelines with reproducible experiments and dataset versioning.")
        items.append("Serving: API wrapper with model monitoring and drift detection.")
    elif project_type == "Enterprise Applications":
        items.append("Integration: enterprise SSO, audit logging, and role-based access control.")

    return items


def _industry_hints(features):
    industries = []
    if features.get("education"):
        industries.append("Education")
    if features.get("healthcare"):
        industries.append("Healthcare")
    if features.get("fintech"):
        industries.append("Fintech")
    if features.get("logistics"):
        industries.append("Logistics")
    if features.get("ecommerce"):
        industries.append("E-commerce")
    if features.get("hr"):
        industries.append("HR/Recruiting")
    return industries or ["General"]


def _architecture_patterns(characteristics, features):
    complexity = characteristics.get("Project Complexity", "Medium")
    realtime = features.get("realtime") or features.get("chat")
    multi_tenant = features.get("multi_tenant")
    patterns = []

    if complexity in ["Low", "Medium"]:
        patterns.append({
            "pattern": "Layered (Modular Monolith)",
            "why": "Faster delivery with clear boundaries and lower operational overhead.",
        })
    if complexity in ["High", "Very High"]:
        patterns.append({
            "pattern": "Service-Oriented / Modular Services",
            "why": "Reduces coupling and enables scaling of hot paths independently.",
        })
    if realtime:
        patterns.append({
            "pattern": "Event-Driven Components",
            "why": "Supports low-latency updates and decouples producers/consumers.",
        })
    if multi_tenant:
        patterns.append({
            "pattern": "Tenant-Isolated Architecture",
            "why": "Protects data boundaries and simplifies enterprise onboarding.",
        })
    return patterns


def _architecture_components(features, characteristics):
    components = [
        {"component": "API layer", "reason": "Defines stable contracts between clients and services."},
        {"component": "Database", "reason": "Source of truth for core domain data."},
    ]
    if features.get("auth"):
        components.append({"component": "Auth service", "reason": "Centralizes identity, roles, and permissions."})
    if features.get("payments"):
        components.append({"component": "Payments service", "reason": "Isolates billing logic and retries safely."})
    if features.get("notifications"):
        components.append({"component": "Notification service", "reason": "Decouples delivery channels and retries."})
    if features.get("search"):
        components.append({"component": "Search index", "reason": "Enables fast filtering and discovery."})
    if features.get("uploads"):
        components.append({"component": "Object storage", "reason": "Handles media at scale with CDN support."})
    if features.get("analytics"):
        components.append({"component": "Analytics pipeline", "reason": "Provides product insights and KPI tracking."})
    if features.get("realtime") or features.get("chat"):
        components.append({"component": "Realtime gateway", "reason": "Maintains low-latency updates and presence."})
    if features.get("ai"):
        components.append({"component": "ML service", "reason": "Separates model inference and monitoring."})
    if characteristics.get("Regulatory Compliance") in ["High", "Very High"]:
        components.append({"component": "Audit log", "reason": "Provides traceability for compliance."})
    return components


def _quality_strategy(characteristics, recommendations):
    risk = characteristics.get("Risk Tolerance")
    testing = _rec_first(recommendations, "Testing Strategy", "Automated testing")
    strategy = [
        f"Testing approach: {testing} aligned to critical user journeys.",
        "Code quality gates: linting, type checks, and mandatory reviews.",
    ]
    if risk == "Low":
        strategy.append("Add staged rollouts, canary tests, and strict regression suites.")
    return strategy


def _data_strategy(characteristics, features):
    strategy = [
        "Define a canonical data model and data ownership boundaries early.",
        "Track data lineage for critical entities.",
    ]
    if features.get("analytics"):
        strategy.append("Instrument event tracking and define KPI dashboards.")
    if characteristics.get("Regulatory Compliance") in ["High", "Very High"]:
        strategy.append("Implement data minimization, retention policies, and access auditing.")
    return strategy


def _risk_register(characteristics, features):
    risks = [
        {
            "risk": "Scope creep",
            "impact": "Delays and quality regression",
            "mitigation": "MVP enforcement and change control",
        },
        {
            "risk": "Integration failures",
            "impact": "Unstable releases",
            "mitigation": "Contract tests and sandbox environments",
        },
    ]
    if features.get("payments"):
        risks.append({
            "risk": "Payment edge cases",
            "impact": "Revenue loss or user churn",
            "mitigation": "Idempotent billing and reconciliation workflows",
        })
    if characteristics.get("Regulatory Compliance") in ["High", "Very High"]:
        risks.append({
            "risk": "Compliance gaps",
            "impact": "Legal exposure and rework",
            "mitigation": "Security review and audit logging from day one",
        })
    if characteristics.get("Project Complexity") in ["High", "Very High"]:
        risks.append({
            "risk": "Architecture bottlenecks",
            "impact": "Scaling failures",
            "mitigation": "Performance testing and capacity planning",
        })
    return risks


def _success_metrics(characteristics, features):
    project_type = characteristics.get("Project Type (Implicit)")
    metrics = ["User activation rate", "Weekly active users", "Retention"]
    if project_type in ["API/Backend Service"]:
        metrics.extend(["p95 latency", "Error rate", "Availability"])
    if features.get("payments"):
        metrics.append("Conversion rate to paid")
    if features.get("marketplace"):
        metrics.append("Match rate between supply and demand")
    return metrics


def _market_analogs(characteristics, features):
    project_type = characteristics.get("Project Type (Implicit)", "Other")
    analogs = []
    if project_type == "Web Application":
        analogs.append({
            "type": "SaaS analytics platform",
            "why": "Common web app pattern with dashboards and admin controls",
        })
    if project_type == "Mobile App":
        analogs.append({
            "type": "On-demand mobile service",
            "why": "Mobile UX, notifications, and real-time updates",
        })
    if project_type == "API/Backend Service":
        analogs.append({
            "type": "Integration API platform",
            "why": "Contract stability, rate limits, partner onboarding",
        })
    if features.get("marketplace"):
        analogs.append({
            "type": "Two-sided marketplace",
            "why": "Requires trust, matching, and dispute flows",
        })
    if features.get("fintech"):
        analogs.append({
            "type": "Payments-enabled product",
            "why": "Needs idempotency, reconciliation, and fraud checks",
        })
    return analogs


def _dependency_map(phases):
    deps = []
    for i, phase in enumerate(phases):
        if i == 0:
            deps.append({"phase": phase["phase"], "depends_on": []})
        else:
            deps.append({"phase": phase["phase"], "depends_on": [phases[i - 1]["phase"]]})
    return deps


def _critical_path(phases):
    # Simple linear critical path based on phase order
    return [phase["phase"] for phase in phases]


def _release_train(characteristics, features):
    urgency = characteristics.get("Urgency/Time-to-Market", "Medium")
    complexity = characteristics.get("Project Complexity", "Medium")

    if urgency == "High":
        cadence_weeks = 2
    elif urgency == "Low":
        cadence_weeks = 4
    else:
        cadence_weeks = 3

    iterations = []
    total_iterations = 4 if complexity in ["Low", "Medium"] else 6
    for i in range(1, total_iterations + 1):
        goals = ["Ship a tested increment", "Collect feedback and update backlog"]
        if i == 1:
            goals.insert(0, "Foundational architecture and core entities")
        if features.get("payments") and i == 2:
            goals.append("Payments flow with retry and reconciliation")
        if features.get("realtime") and i == 3:
            goals.append("Realtime gateway and load test baseline")
        iterations.append({"iteration": f"Sprint {i}", "cadence_weeks": cadence_weeks, "goals": goals})
    return {"cadence_weeks": cadence_weeks, "iterations": iterations}


def _stakeholder_comms(characteristics):
    involvement = characteristics.get("Stakeholder Involvement", "Medium")
    if involvement == "High":
        return [
            "Weekly stakeholder demo with decision log",
            "Mid-sprint alignment check-ins",
            "Monthly roadmap review and KPI update",
        ]
    if involvement == "Low":
        return [
            "Bi-weekly updates with progress summary",
            "Monthly roadmap review",
        ]
    return [
        "Bi-weekly demos with feedback capture",
        "Monthly roadmap review",
    ]


def _acceptance_criteria(features):
    criteria = {
        "core": [
            "Key user journey completes without errors",
            "Data integrity checks pass for critical entities",
            "Performance baseline meets p95 latency targets",
        ]
    }
    if features.get("auth"):
        criteria["auth"] = [
            "Users can sign in and sign out reliably",
            "Role-based permissions enforced across endpoints",
        ]
    if features.get("payments"):
        criteria["payments"] = [
            "Payment is idempotent and resilient to retries",
            "Refund and reconciliation paths tested",
        ]
    if features.get("realtime"):
        criteria["realtime"] = [
            "Realtime updates delivered within latency budget",
            "Backpressure and reconnection flows handled",
        ]
    if features.get("offline"):
        criteria["offline"] = [
            "Offline changes sync correctly without data loss",
            "Conflicts are resolved predictably",
        ]
    if features.get("uploads"):
        criteria["uploads"] = [
            "Uploads are validated and virus-scanned where applicable",
            "Large file uploads resume safely",
        ]
    return criteria


def _similar_projects(characteristics, features, recommendations):
    project_type = characteristics.get("Project Type (Implicit)", "Other")
    urgency = characteristics.get("Urgency/Time-to-Market", "Medium")
    complexity = characteristics.get("Project Complexity", "Medium")
    examples = []

    if project_type == "Web Application":
        examples.append({
            "example": "SaaS dashboard for business operations",
            "why_similar": "Web-based product with analytics and admin workflows",
            "result": "Prioritizes role-based access, dashboards, and audit trails",
        })
        if features.get("payments"):
            examples.append({
                "example": "Subscription billing web app",
                "why_similar": "Recurring revenue model with payment flows",
                "result": "Requires idempotent billing, retries, and reconciliation",
            })
    elif project_type == "Mobile App":
        examples.append({
            "example": "On-demand service booking app",
            "why_similar": "Mobile-first UX with notifications and real-time updates",
            "result": "Focus on latency, push reliability, and offline handling",
        })
    elif project_type == "API/Backend Service":
        examples.append({
            "example": "Public API platform for third-party integrations",
            "why_similar": "API contracts and partner integration needs",
            "result": "Emphasizes versioning, rate limits, and observability",
        })
    elif project_type == "Machine Learning":
        examples.append({
            "example": "ML inference service with monitoring",
            "why_similar": "Model lifecycle management and prediction serving",
            "result": "Requires dataset versioning and drift monitoring",
        })
    elif project_type == "Data Science":
        examples.append({
            "example": "Analytics pipeline with KPI dashboards",
            "why_similar": "Data ingestion, transformations, and reporting",
            "result": "Needs data quality checks and lineage tracking",
        })
    elif project_type == "Enterprise Applications":
        examples.append({
            "example": "Internal workflow automation system",
            "why_similar": "Large-team collaboration with compliance",
            "result": "Requires strong RBAC, audit logs, and SLAs",
        })
    elif project_type == "Embedded System":
        examples.append({
            "example": "IoT device monitoring platform",
            "why_similar": "Hardware integration and reliability constraints",
            "result": "Prioritizes telemetry, fail-safes, and firmware update flows",
        })
    elif project_type == "Game Development":
        examples.append({
            "example": "Multiplayer game backend",
            "why_similar": "Realtime interaction and session management",
            "result": "Requires low-latency transport and anti-abuse controls",
        })

    if urgency == "High":
        examples.append({
            "example": "MVP-first delivery pattern",
            "why_similar": "High urgency with evolving requirements",
            "result": "Favors rapid iteration and tight scope control",
        })
    if complexity in ["High", "Very High"]:
        examples.append({
            "example": "Phased delivery for complex systems",
            "why_similar": "Multi-component architecture and integration risk",
            "result": "Needs architecture review gates and staged rollouts",
        })
    return examples


def _project_category_overview(characteristics, recommendations):
    project_type = characteristics.get("Project Type (Implicit)", "Other")
    life_cycle = _rec_first(recommendations, "Life Cycle", "Iterative")
    methodology = _rec_first(recommendations, "Methodology", "Agile")
    return {
        "category": project_type,
        "delivery_style": f"{life_cycle} + {methodology}",
        "notes": "Category summarizes the dominant project style and delivery cadence.",
    }


def describe_project(prompt, characteristics, recommendations):
    sections = _narrative_sections(prompt, characteristics, recommendations)
    parts = []
    for title, content in sections:
        parts.append(f"{title}:\n{content}")
    return "\n\n".join(parts)


def build_plan(characteristics, recommendations, prompt):
    features = _feature_hints(prompt)
    complexity = characteristics.get("Project Complexity", "Medium")
    urgency = characteristics.get("Urgency/Time-to-Market", "Medium")
    regulatory = characteristics.get("Regulatory Compliance", "Low")
    methodology = _rec_first(recommendations, "Methodology", "Agile")
    testing = _rec_first(recommendations, "Testing Strategy", "Automated testing with CI")
    deployment = _rec_first(recommendations, "Deployment", "Staged rollout")
    docs = _rec_first(recommendations, "Documentation", "Living documentation")

    discovery_goals = [
        "Clarify target users, success metrics, and constraints",
        "Convert the prompt into validated requirements and user journeys",
        f"Define MVP scope aligned to {urgency.lower()} delivery",
    ]
    if regulatory in ["High", "Very High"]:
        discovery_goals.append("Identify compliance requirements and data handling policies")
    if features.get("ai"):
        discovery_goals.append("Validate AI feasibility and data availability")

    design_goals = [
        f"Choose a {methodology} delivery cadence and project structure",
        "Define system architecture, data model, and API contracts",
        "Design UX flows and error-handling paths",
    ]
    if features.get("payments"):
        design_goals.append("Design payment flows and failure recovery paths")
    if features.get("multi_tenant"):
        design_goals.append("Define tenant isolation and authorization boundaries")

    build_goals = [
        "Implement core services, UI, and data pipelines",
        "Integrate authentication, authorization, and audit logging",
        "Iterate in short cycles with stakeholder feedback",
    ]
    if features.get("analytics"):
        build_goals.append("Implement analytics events and reporting pipelines")
    if features.get("notifications"):
        build_goals.append("Build notification delivery with retries and fallback channels")

    harden_goals = [
        f"Execute {testing} focused on regression and critical paths",
        "Performance profiling and reliability improvements",
        f"Finalize {docs} for onboarding and operations",
    ]
    if regulatory in ["High", "Very High"]:
        harden_goals.append("Complete compliance validation and security review")

    launch_goals = [
        f"Deploy using {deployment} with rollback readiness",
        "Monitor KPIs, errors, and user behavior",
        "Plan next iteration based on feedback and metrics",
    ]

    phases = [
        {"phase": "Discovery", "goals": discovery_goals, "outputs": ["PRD", "MVP scope", "Project timeline"]},
        {"phase": "Design", "goals": design_goals, "outputs": ["Architecture diagram", "Data schema", "API spec"]},
        {"phase": "Implementation", "goals": build_goals, "outputs": ["Working MVP", "Integration tests"]},
        {"phase": "Hardening", "goals": harden_goals, "outputs": ["Release candidate", "Runbooks"]},
        {"phase": "Launch", "goals": launch_goals, "outputs": ["Production release", "Post-launch report"]},
    ]

    if complexity in ["High", "Very High"]:
        phases.insert(2, {
            "phase": "Architecture Review",
            "goals": [
                "Validate scalability assumptions and failure modes",
                "Stress-test design decisions with realistic workloads",
            ],
            "outputs": ["Architecture review notes", "Risk register update"],
        })

    return phases


def _dynamic_deliverables(characteristics, recommendations, prompt):
    features = _feature_hints(prompt)
    deliverables = [
        "MVP release aligned to core user journeys",
        "Architecture and API documentation tied to system boundaries",
    ]
    if features.get("auth"):
        deliverables.append("Authentication and authorization spec with role matrix")
    if features.get("payments"):
        deliverables.append("Billing flows with failure handling and reconciliation guide")
    if features.get("analytics"):
        deliverables.append("Analytics event taxonomy and dashboard definitions")
    if features.get("ai"):
        deliverables.append("Model evaluation report and data quality checklist")
    testing = _rec_first(recommendations, "Testing Strategy", "")
    if testing:
        deliverables.append(f"{testing} suite with CI gates for critical paths")
    deployment = _rec_first(recommendations, "Deployment", "")
    if deployment:
        deliverables.append(f"{deployment} playbook and rollback procedure")
    if characteristics.get("Regulatory Compliance") in ["High", "Very High"]:
        deliverables.append("Compliance checklist and audit evidence pack")
    if _feature_hints(prompt).get("accessibility"):
        deliverables.append("Accessibility review report and WCAG compliance checks")
    if _feature_hints(prompt).get("realtime"):
        deliverables.append("Realtime performance budget and load test report")
    if _feature_hints(prompt).get("offline"):
        deliverables.append("Offline sync strategy and conflict resolution policy")
    return deliverables


def _dynamic_considerations(characteristics, recommendations, prompt):
    considerations = []
    regulatory = characteristics.get("Regulatory Compliance")
    risk = characteristics.get("Risk Tolerance")
    urgency = characteristics.get("Urgency/Time-to-Market")
    team = characteristics.get("Team Size")
    complexity = characteristics.get("Project Complexity")

    if regulatory in ["High", "Very High"]:
        considerations.append("Compliance-first delivery: threat modeling, audit logs, and data retention policies.")
    if risk == "Low":
        considerations.append("Risk-averse approach: smaller releases, stronger QA gates, and rollback drills.")
    if urgency == "High":
        considerations.append("Time-to-market focus: strict MVP scope and aggressive prioritization.")
    if team in ["Small (1-5)"] and complexity in ["High", "Very High"]:
        considerations.append("Scope control is critical due to limited team capacity vs. high complexity.")
    if _feature_hints(prompt).get("integrations"):
        considerations.append("Integration risk: validate third-party limits, SLAs, and fallback paths early.")
    if _feature_hints(prompt).get("realtime"):
        considerations.append("Realtime features need backpressure and latency budgets to avoid cascading failures.")
    if _feature_hints(prompt).get("offline"):
        considerations.append("Offline mode needs conflict resolution and clear user messaging.")
    if _feature_hints(prompt).get("ecommerce"):
        considerations.append("Inventory consistency and order state transitions must be resilient to failures.")
    if _feature_hints(prompt).get("healthcare"):
        considerations.append("Healthcare workflows need strict access controls and auditability.")
    if _feature_hints(prompt).get("education"):
        considerations.append("Education workflows benefit from role-based views for teachers, students, and admins.")

    recs = _build_rationales(characteristics, recommendations)
    for r in recs:
        if r:
            considerations.append(r)
    return considerations


def advanced_project_plan(prompt, characteristics, recommendations):
    narrative = describe_project(prompt, characteristics, recommendations)
    plan = build_plan(characteristics, recommendations, prompt)
    deliverables = _dynamic_deliverables(characteristics, recommendations, prompt)
    considerations = _dynamic_considerations(characteristics, recommendations, prompt)
    features = _feature_hints(prompt)
    release_train = _release_train(characteristics, features)

    return {
        "narrative": narrative,
        "plan": plan,
        "architecture_components": _architecture_components(features, characteristics),
        "architecture_patterns": _architecture_patterns(characteristics, features),
        "tech_stack_suggestions": _tech_stack_suggestions(characteristics, recommendations),
        "quality_strategy": _quality_strategy(characteristics, recommendations),
        "data_strategy": _data_strategy(characteristics, features),
        "risk_register": _risk_register(characteristics, features),
        "success_metrics": _success_metrics(characteristics, features),
        "project_category_overview": _project_category_overview(characteristics, recommendations),
        "similar_project_examples": _similar_projects(characteristics, features, recommendations),
        "market_analogs": _market_analogs(characteristics, features),
        "industry_context": _industry_hints(features),
        "dependency_map": _dependency_map(plan),
        "critical_path": _critical_path(plan),
        "release_train": release_train,
        "stakeholder_communications": _stakeholder_comms(characteristics),
        "acceptance_criteria": _acceptance_criteria(features),
        "deliverables": deliverables,
        "real_world_considerations": considerations,
    }


def super_planner(prompt, pdss_characteristics, recommendations):
    return advanced_project_plan(prompt, pdss_characteristics, recommendations)
