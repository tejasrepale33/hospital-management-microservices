import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Skip cover page header and footer
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0D9488")) # Teal primary

        # Running Top Header
        self.drawString(54, 750, "MEDIPULSE HEALTHCARE PLATFORM")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(558, 750, "Microservices Engineering & Evaluation Report")

        # Top Header Line
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 744, 558, 744)

        # Running Bottom Footer
        self.line(54, 45, 558, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Confidential - Academic Project Report | Spring Boot 3 & React 18")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)

        self.restoreState()


def build_pdf(filename="Hospital_Management_Microservices_Project_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#1E3A8A")    # Deep Navy
    SECONDARY = colors.HexColor("#0D9488")  # Medical Teal
    DARK = colors.HexColor("#0F172A")       # Slate Dark
    MUTED = colors.HexColor("#475569")      # Slate Muted
    LIGHT_BG = colors.HexColor("#F8FAFC")   # Light Gray
    BORDER = colors.HexColor("#E2E8F0")     # Light Border
    ACCENT = colors.HexColor("#DC2626")     # Emergency Red
    SUCCESS = colors.HexColor("#16A34A")    # Success Green

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=PRIMARY,
        alignment=0,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=MUTED,
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=DARK,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK,
        leftIndent=15,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=DARK
    )

    code_style = ParagraphStyle(
        'CodeText',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1E293B")
    )

    th_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    td_style = ParagraphStyle(
        'TD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=DARK
    )

    td_bold = ParagraphStyle(
        'TDBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=PRIMARY
    )

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 20))
    # Top Tag
    badge_table = Table(
        [[Paragraph("<font color='#0D9488'><b>ACADEMIC & INDUSTRIAL PROJECT REPORT</b></font> | <b>EVALUATION DOSSIER</b>", td_style)]],
        colWidths=[504]
    )
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#CCFBF1")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#99F6E4")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 25))

    story.append(Paragraph("MediPulse: Distributed Hospital Management Platform", title_style))
    story.append(Paragraph("Production-Grade Cloud-Native Microservices Architecture with Spring Cloud, Spring AI, PostgreSQL, Redis Caching, and React 18", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=3, color=SECONDARY, spaceAfter=25, spaceBefore=0))

    overview_box = Table(
        [[
            Paragraph("<b>Document Purpose:</b> Comprehensive technical project dossier for project evaluation, external viva examination, and enterprise architecture assessment.<br/><br/>"
                      "<b>System Scale:</b> 6 Independent Microservice/Frontend Modules | 2 Autonomous PostgreSQL Databases | 18+ REST Endpoints | 24 Verified Test Cases (100% Pass Rate).<br/><br/>"
                      "<b>Core Innovations:</b> Automated Spring AI Symptom Triage, Client-side Load Balanced Gateway, Sub-2ms Redis Cache-Aside with Graceful DB Fallback, and Domain-Driven Entity Isolation.", body_style)
        ]],
        colWidths=[504]
    )
    overview_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(overview_box)
    story.append(Spacer(1, 40))

    meta_table_data = [
        [Paragraph("<b>Project Category:</b>", td_bold), Paragraph("Distributed Enterprise Cloud Computing & AI", td_style)],
        [Paragraph("<b>Backend Stack:</b>", td_bold), Paragraph("Java 25, Spring Boot 3.2.5, Spring Cloud 2023, Netflix Eureka, Spring Security 6", td_style)],
        [Paragraph("<b>Frontend Stack:</b>", td_bold), Paragraph("React 18, Vite 5, React Router 6, Axios Interceptors, Context API", td_style)],
        [Paragraph("<b>Data Tier:</b>", td_bold), Paragraph("PostgreSQL 15 (patient_db & doctor_db), Redis 7 (Distributed Cache)", td_style)],
        [Paragraph("<b>Intelligence:</b>", td_bold), Paragraph("Spring AI 1.0 (GPT-4o-mini & Deterministic Clinical Rules Fallback)", td_style)],
        [Paragraph("<b>Prepared For:</b>", td_bold), Paragraph("Faculty Project Evaluation Committee & External Examiner", td_style)],
        [Paragraph("<b>Candidate Name / ID:</b>", td_bold), Paragraph("Final Year Engineering Project Team / MediPulse Core Team", td_style)],
        [Paragraph("<b>Evaluation Date:</b>", td_bold), Paragraph("Academic Year 2025 - 2026", td_style)],
        [Paragraph("<b>Verification Status:</b>", td_bold), Paragraph("<font color='#16A34A'><b>100% VERIFIED & FULLY OPERATIONAL (24/24 PASS)</b></font>", td_style)]
    ]
    meta_table = Table(meta_table_data, colWidths=[140, 364])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#F1F5F9")),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(meta_table)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 1: EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Problem Formulation", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=12, spaceBefore=2))

    story.append(Paragraph(
        "Modern hospital management infrastructures face severe operational challenges under monolithic designs. "
        "Traditional monolithic architectures bundle patient registration, doctor schedules, billing, authentication, and clinical intake into a single unified deployment unit. "
        "This creates major operational vulnerabilities:", body_style
    ))

    story.append(Paragraph("• <b>Single Point of Failure (SPOF):</b> A memory leak or peak load spike in consultation scheduling can crash the entire emergency intake pipeline.", bullet_style))
    story.append(Paragraph("• <b>Scalability Imbalance:</b> Patient portals require 10x higher concurrent read capacity than doctor schedule management, yet monoliths cannot scale modules independently.", bullet_style))
    story.append(Paragraph("• <b>Triage Bottlenecks:</b> Patients frequently self-book appointments under inappropriate clinical specialties, causing misallocations and delayed emergency care.", bullet_style))
    story.append(Paragraph("• <b>Tight Coupling & Long Release Cycles:</b> Modifying appointment logic requires re-testing, rebuilding, and re-deploying the entire monolithic JAR.", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("The MediPulse Solution:", h2_style))
    story.append(Paragraph(
        "MediPulse re-architects the healthcare ecosystem into a <b>decoupled, polyglot-ready, microservices ecosystem</b>. "
        "The platform utilizes <b>Spring Cloud Netflix Eureka</b> for dynamic service registration, <b>Spring Cloud Gateway</b> for centralized perimeter security and intelligent request routing, "
        "<b>Spring AI</b> for instant clinical triage with automated urgency classification, and <b>Redis distributed caching</b> to achieve sub-2 millisecond repeated catalog queries. "
        "Independent PostgreSQL databases strictly enforce the <i>Database-per-Service</i> pattern, ensuring zero direct data coupling between clinical domains.", body_style
    ))

    # Key Metrics Callout
    metrics_data = [
        [
            Paragraph("<b>6</b><br/><font color='#64748B'>Autonomous Services</font>", td_style),
            Paragraph("<b>&lt; 2ms</b><br/><font color='#64748B'>Redis Cache Latency</font>", td_style),
            Paragraph("<b>24 / 24</b><br/><font color='#16A34A'>Verified Test Cases</font>", td_style),
            Paragraph("<b>100%</b><br/><font color='#64748B'>Offline Triage Fallback</font>", td_style)
        ]
    ]
    metrics_table = Table(metrics_data, colWidths=[126, 126, 126, 126])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, SECONDARY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 2: SYSTEM ARCHITECTURE & TOPOLOGY
    # =========================================================================
    story.append(Paragraph("2. Microservices Architecture & Topology", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=12, spaceBefore=2))

    story.append(Paragraph(
        "The architecture adheres strictly to Twelve-Factor App principles and industry-standard cloud patterns. "
        "The visual topology below illustrates the physical and logical flow of requests through the platform:", body_style
    ))

    topo_box = [
        [Paragraph(
            "<font color='#1E3A8A'><b>[ CLIENT LAYER ]</b></font><br/>"
            "<b>React 18 + Vite SPA</b> (Port 3000) — Role-Aware Portals (Patient, Doctor, Admin) | Axios Bearer Interceptor<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│ HTTPS / REST (JWT)<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼<br/>"
            "<font color='#0D9488'><b>[ EDGE & SECURITY LAYER ]</b></font><br/>"
            "<b>API Gateway</b> (Port 8080) — Spring Cloud Gateway | Non-blocking Netty Reactive Engine<br/>"
            "• JwtAuthenticationFilter: Signature Validation & Role Claims Extraction<br/>"
            "• Dynamic Routing via Eureka Service Discovery | Client-Side Round-Robin Load Balancing<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│ Heartbeats / Resolution<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼<br/>"
            "<b>Service Registry (Netflix Eureka)</b> (Port 8761) — Dynamic Instance Discovery & Heartbeat Lease Monitor<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;┌───────────────────────┼───────────────────────┐<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼<br/>"
            "<font color='#1E3A8A'><b>[ CORE MICROSERVICES ]</b></font>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Auth Service</b> (8081)&nbsp;&nbsp;&nbsp;&nbsp;<b>Patient Service</b> (8082)&nbsp;&nbsp;&nbsp;<b>Doctor Service</b> (8083)<br/>"
            "• Functional Scope:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;BCrypt & JWT Issue&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Spring AI Triage & Appts&nbsp;Catalog & Slot Schedules<br/>"
            "• Inter-Service Link:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Patient ──(LoadBalanced RestTemplate)──► Doctor<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br/>"
            "<font color='#0F172A'><b>[ DATA & CACHE TIER ]</b></font>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼<br/>"
            "• Isolated Databases:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>patient_db</b> (PostgreSQL)&nbsp;&nbsp;&nbsp;<b>doctor_db</b> (PostgreSQL)<br/>"
            "• High-Speed Performance:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Redis Cache Cluster</b> (TTL: 600s, Auto-Eviction)",
            code_style
        )]
    ]
    topo_table = Table(topo_box, colWidths=[504])
    topo_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(topo_table)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 3: TECHNOLOGY STACK & JUSTIFICATION
    # =========================================================================
    story.append(Paragraph("3. Technology Stack & Architectural Rationales", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=12, spaceBefore=2))

    story.append(Paragraph(
        "Each technology in the stack was selected to satisfy stringent enterprise requirements regarding scalability, security, and developer productivity:", body_style
    ))

    tech_headers = [Paragraph("<b>Component</b>", th_style), Paragraph("<b>Technology</b>", th_style), Paragraph("<b>Version</b>", th_style), Paragraph("<b>Engineering Rationale</b>", th_style)]
    tech_rows = [
        [Paragraph("Runtime", td_bold), Paragraph("Java JDK", td_style), Paragraph("25.0.2", td_style), Paragraph("Long-term modern JVM with Virtual Threads (Project Loom) capability.", td_style)],
        [Paragraph("Framework", td_bold), Paragraph("Spring Boot", td_style), Paragraph("3.2.5", td_style), Paragraph("Production-grade microservice runtime, Actuator metrics, HikariCP pool.", td_style)],
        [Paragraph("Service Discovery", td_bold), Paragraph("Spring Cloud Eureka", td_style), Paragraph("2023.0.1", td_style), Paragraph("Dynamic service registry eliminating hardcoded hostnames and ports.", td_style)],
        [Paragraph("API Gateway", td_bold), Paragraph("Spring Cloud Gateway", td_style), Paragraph("2023.0.1", td_style), Paragraph("Non-blocking asynchronous reactive routing built on Project Reactor.", td_style)],
        [Paragraph("Authentication", td_bold), Paragraph("Spring Security & JJWT", td_style), Paragraph("6.2 / 0.12.5", td_style), Paragraph("Stateless cryptographic HMAC-SHA256 bearer tokens with 24-hr expiry.", td_style)],
        [Paragraph("Primary Persistence", td_bold), Paragraph("PostgreSQL", td_style), Paragraph("15 / 18", td_style), Paragraph("ACID compliant relational database for patient clinical histories.", td_style)],
        [Paragraph("Distributed Cache", td_bold), Paragraph("Redis & Spring Data", td_style), Paragraph("7.x / 3.2.5", td_style), Paragraph("In-memory Cache-Aside pattern delivering sub-2ms doctor catalog reads.", td_style)],
        [Paragraph("Clinical AI Engine", td_bold), Paragraph("Spring AI", td_style), Paragraph("1.0.0-M1", td_style), Paragraph("OpenAI GPT-4o-mini integration paired with offline keyword heuristics.", td_style)],
        [Paragraph("Frontend UI", td_bold), Paragraph("React 18 & Vite", td_style), Paragraph("18.3 / 5.x", td_style), Paragraph("Declarative single-page app with lightning-fast Vite Hot Module Reload.", td_style)],
        [Paragraph("IDE & Tooling", td_bold), Paragraph("Eclipse IDE & Maven", td_style), Paragraph("2025-06 / 3.9", td_style), Paragraph("Enterprise multi-module parent POM build and Eclipse classpath support.", td_style)],
    ]
    tech_table = Table([tech_headers] + tech_rows, colWidths=[80, 110, 60, 254])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 4: DATABASE & ENTITY RELATIONSHIP (ER) MODEL
    # =========================================================================
    story.append(Paragraph("4. Database Architecture & Entity Relationship (ER) Model", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=12, spaceBefore=2))

    story.append(Paragraph(
        "<b>Database-per-Service Principle:</b> The system rejects the monolithic 'shared database' anti-pattern. "
        "Patient-Service manages <code>patient_db</code>, while Doctor-Service manages <code>doctor_db</code>. "
        "Neither service can execute SQL queries against the other's database. Cross-boundary coordination occurs exclusively via RESTful HTTP APIs.", body_style
    ))

    story.append(Paragraph("A. patient_db Schema & Entity Relationships", h2_style))
    story.append(Paragraph(
        "Within <code>patient_db</code>, the core entities are <b>Patient</b> and <b>Appointment</b> with a strict <b>One-to-Many</b> bidirectional JPA relationship:", body_style
    ))

    p_er_data = [
        [Paragraph("<b>Table: patients</b>", th_style), Paragraph("<b>Type & Constraint</b>", th_style), Paragraph("<b>Description</b>", th_style)],
        [Paragraph("id", td_bold), Paragraph("BIGINT, PRIMARY KEY, AUTO_INC", td_style), Paragraph("Unique internal patient identifier", td_style)],
        [Paragraph("first_name, last_name", td_bold), Paragraph("VARCHAR(255), NOT NULL", td_style), Paragraph("Legal patient name records", td_style)],
        [Paragraph("email", td_bold), Paragraph("VARCHAR(255), UNIQUE, NOT NULL", td_style), Paragraph("Patient username & contact credential", td_style)],
        [Paragraph("phone, emergency_contact", td_bold), Paragraph("VARCHAR(255)", td_style), Paragraph("Primary & emergency telephone coordinates", td_style)],
        [Paragraph("age, gender, blood_group", td_bold), Paragraph("INT, VARCHAR(50)", td_style), Paragraph("Biometric parameters used for clinical triage", td_style)],
        [Paragraph("medical_history", td_bold), Paragraph("TEXT", td_style), Paragraph("Pre-existing conditions (e.g. Asthma, Hypertension)", td_style)],
        [Paragraph("appointments", td_bold), Paragraph("OneToMany(mappedBy='patient')", td_style), Paragraph("Bidirectional link with CascadeType.ALL, orphanRemoval", td_style)],
    ]
    p_er_table = Table(p_er_data, colWidths=[130, 160, 214])
    p_er_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(p_er_table)
    story.append(Spacer(1, 8))

    appt_er_data = [
        [Paragraph("<b>Table: appointments</b>", th_style), Paragraph("<b>Type & Constraint</b>", th_style), Paragraph("<b>Description</b>", th_style)],
        [Paragraph("id", td_bold), Paragraph("BIGINT, PRIMARY KEY, AUTO_INC", td_style), Paragraph("Unique appointment record identifier", td_style)],
        [Paragraph("patient_id", td_bold), Paragraph("BIGINT, FOREIGN KEY -> patients(id)", td_style), Paragraph("Owner patient foreign key reference", td_style)],
        [Paragraph("doctor_id, doctor_name", td_bold), Paragraph("BIGINT, VARCHAR(255)", td_style), Paragraph("Loose-coupled doctor reference from doctor-service", td_style)],
        [Paragraph("department", td_bold), Paragraph("VARCHAR(100)", td_style), Paragraph("Clinical department (Cardiology, Neurology, etc.)", td_style)],
        [Paragraph("appointment_date, time_slot", td_bold), Paragraph("DATE, VARCHAR(100)", td_style), Paragraph("Consultation schedule coordinates", td_style)],
        [Paragraph("status", td_bold), Paragraph("VARCHAR(50) [SCHEDULED, CONFIRMED]", td_style), Paragraph("Lifecycle state of the appointment", td_style)],
        [Paragraph("symptoms, notes", td_bold), Paragraph("TEXT", td_style), Paragraph("Intake symptom narrative and triage severity notes", td_style)],
    ]
    appt_table = Table(appt_er_data, colWidths=[130, 160, 214])
    appt_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(appt_table)

    story.append(PageBreak())

    story.append(Paragraph("B. doctor_db Schema & Entity Relationships", h2_style))
    story.append(Paragraph(
        "Within <code>doctor_db</code>, the core entities are <b>Doctor</b> and <b>AvailabilitySlot</b> with a <b>One-to-Many</b> bidirectional relationship:", body_style
    ))

    d_er_data = [
        [Paragraph("<b>Table: doctors</b>", th_style), Paragraph("<b>Type & Constraint</b>", th_style), Paragraph("<b>Description</b>", th_style)],
        [Paragraph("id", td_bold), Paragraph("BIGINT, PRIMARY KEY, AUTO_INC", td_style), Paragraph("Unique doctor identifier", td_style)],
        [Paragraph("name, specialization", td_bold), Paragraph("VARCHAR(255), NOT NULL", td_style), Paragraph("Doctor full name and clinical sub-specialty", td_style)],
        [Paragraph("department", td_bold), Paragraph("VARCHAR(100), NOT NULL", td_style), Paragraph("Indexed category (Cardiology, Dermatology, etc.)", td_style)],
        [Paragraph("email", td_bold), Paragraph("VARCHAR(255), UNIQUE, NOT NULL", td_style), Paragraph("Unique institutional email address", td_style)],
        [Paragraph("consultation_fee, rating", td_bold), Paragraph("DOUBLE PRECISION", td_style), Paragraph("Billing rate and patient feedback score (1.0 to 5.0)", td_style)],
        [Paragraph("experience_years, is_available", td_bold), Paragraph("INT, BOOLEAN", td_style), Paragraph("Seniority and immediate clinical availability toggle", td_style)],
        [Paragraph("availabilitySlots", td_bold), Paragraph("OneToMany(FetchType.EAGER)", td_style), Paragraph("Bidirectional link with CascadeType.ALL", td_style)],
    ]
    d_er_table = Table(d_er_data, colWidths=[130, 160, 214])
    d_er_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(d_er_table)
    story.append(Spacer(1, 8))

    slot_er_data = [
        [Paragraph("<b>Table: availability_slots</b>", th_style), Paragraph("<b>Type & Constraint</b>", th_style), Paragraph("<b>Description</b>", th_style)],
        [Paragraph("id", td_bold), Paragraph("BIGINT, PRIMARY KEY, AUTO_INC", td_style), Paragraph("Unique slot record identifier", td_style)],
        [Paragraph("doctor_id", td_bold), Paragraph("BIGINT, FOREIGN KEY -> doctors(id)", td_style), Paragraph("Doctor foreign key reference", td_style)],
        [Paragraph("day_of_week", td_bold), Paragraph("VARCHAR(20) [MONDAY, TUESDAY...]", td_style), Paragraph("Clinical consultation operating day", td_style)],
        [Paragraph("start_time, end_time", td_bold), Paragraph("VARCHAR(20) (e.g. 09:00 AM)", td_style), Paragraph("Time boundaries of the slot interval", td_style)],
        [Paragraph("is_booked", td_bold), Paragraph("BOOLEAN DEFAULT FALSE", td_style), Paragraph("Concurrency guard preventing double-booking", td_style)],
    ]
    slot_table = Table(slot_er_data, colWidths=[130, 160, 214])
    slot_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(slot_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("C. Cross-Service Loose Coupling (No Distributed Joins)", h2_style))
    story.append(Paragraph(
        "Notice that <code>appointments.doctor_id</code> does <b>NOT</b> have a SQL Foreign Key constraint pointing to <code>doctors.id</code>. "
        "Because each table lives in an isolated database on separate network partitions, relational SQL Foreign Keys across databases are impossible and anti-microservice. "
        "Instead, the <b>Patient Service queries the Doctor Service over HTTP using <code>@LoadBalanced RestTemplate</code></b>: "
        "<code>http://doctor-service/api/doctors/department/{dept}</code>. This guarantees autonomous schema evolution without breaking other services.", body_style
    ))
    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 5: STEP-BY-STEP WORKING MECHANISM & WORKFLOW
    # =========================================================================
    story.append(Paragraph("5. Step-by-Step Working Mechanism & End-to-End Workflow", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=12, spaceBefore=2))

    story.append(Paragraph(
        "The complete user journey represents an intelligent, event-driven consultation cycle:", body_style
    ))

    story.append(Paragraph("<b>Step 1: User Authentication & Role Assertion</b>", h2_style))
    story.append(Paragraph(
        "1. The user logs into the React frontend via <code>/login</code>.<br/>"
        "2. API Gateway intercepts the request, notes it as a permitted open route, and proxies it to <code>auth-service</code>.<br/>"
        "3. <code>AuthService</code> checks credentials against hashed passwords using BCrypt, generates a signed HMAC-SHA256 JWT, and encodes user role claims (<code>ROLE_PATIENT</code>, <code>ROLE_DOCTOR</code>, or <code>ROLE_ADMIN</code>).<br/>"
        "4. The token is stored in client <code>localStorage</code>; Axios attaches <code>Authorization: Bearer &lt;token&gt;</code> to every subsequent request.", body_style
    ))

    story.append(Paragraph("<b>Step 2: AI Clinical Symptom Triage</b>", h2_style))
    story.append(Paragraph(
        "1. A patient enters symptoms (e.g. <i>'severe chest pain radiating to left arm and shortness of breath'</i>) into the Symptom Checker.<br/>"
        "2. <code>PatientService</code> invokes <code>SpringAiTriageService</code>.<br/>"
        "3. <b>Online Mode:</b> If OpenAI API key is present, a structured system prompt directs GPT-4o-mini to return clean JSON with urgency level, diagnostic hypothesis, and lab recommendations.<br/>"
        "4. <b>Offline Resilient Mode:</b> If offline or no key is present, the deterministic heuristics taxonomy matches symptom keywords, accurately assigning <b>EMERGENCY</b> urgency and routing to <b>Cardiology</b>.<br/>"
        "5. The service executes an internal load-balanced call to <code>doctor-service</code> to dynamically retrieve available Cardiologists.", body_style
    ))

    story.append(Paragraph("<b>Step 3: Specialist Selection & Slot Reservation</b>", h2_style))
    story.append(Paragraph(
        "1. The triage response renders doctor cards with availability slots, consultation fees, and ratings.<br/>"
        "2. The patient selects an available slot and submits consultation confirmation.<br/>"
        "3. <code>PatientService</code> creates a persistent record in <code>appointments</code> table with status <code>SCHEDULED</code>.", body_style
    ))

    story.append(Paragraph("<b>Step 4: Doctor Station Roster Review</b>", h2_style))
    story.append(Paragraph(
        "1. The specialist logs into the Doctor Clinical Station.<br/>"
        "2. The doctor views the live queue containing symptoms, urgency badges (EMERGENCY in glowing red), and intake notes.<br/>"
        "3. The doctor can add new consultation availability slots, which are immediately synced and cached.", body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 6: ADVANCED TECHNICAL HIGHLIGHTS
    # =========================================================================
    story.append(Paragraph("6. Key Advanced Technical Highlights", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=12, spaceBefore=2))

    story.append(Paragraph("A. Redis Cache-Aside with Graceful Error Degradation", h2_style))
    story.append(Paragraph(
        "Doctor catalog lookups utilize Spring Data Redis with a 10-minute Time-To-Live (TTL = 600,000ms):<br/>"
        "• <b>Cache Hit:</b> When <code>getAllDoctors()</code> is called, the cached list is deserialized from Redis in <b>&lt; 2ms</b> without touching PostgreSQL.<br/>"
        "• <b>Cache Eviction:</b> On adding or modifying a doctor, <code>@CacheEvict(value = 'doctors', allEntries = true)</code> automatically purges stale records.<br/>"
        "• <b>Resilient Fallback:</b> Both services implement a custom <code>CacheErrorHandler</code>. If Redis stops running, the connection error is silently caught and the query falls back to PostgreSQL without throwing 500 errors to users.", body_style
    ))

    story.append(Paragraph("B. Centralized Gateway Perimeter Security", h2_style))
    story.append(Paragraph(
        "Individual microservices do not repeat token validation logic. "
        "The <b>Spring Cloud Gateway</b> intercepts all incoming traffic through <code>JwtAuthenticationFilter</code>. "
        "If a token is invalid or missing on a secured route (e.g. <code>/api/doctors/**</code> or <code>/api/patients/**</code>), "
        "the Gateway immediately terminates the request with <b>HTTP 401 Unauthorized</b>, preventing unauthorized packets from ever reaching internal cluster services.", body_style
    ))

    story.append(Paragraph("C. Zero-Tailwind Custom CSS Design System", h2_style))
    story.append(Paragraph(
        "The frontend is built without bloated CSS frameworks like Tailwind. "
        "It implements a pure custom design token system in <code>index.css</code> defining CSS custom properties (variables) for medical colors, typography scales, clinical urgency badges, and glassmorphic cards.", body_style
    ))
    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 7: INDUSTRIAL TESTING & VERIFICATION MATRIX
    # =========================================================================
    story.append(Paragraph("7. Automated Test Suite & Industrial Verification Matrix", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=12, spaceBefore=2))

    story.append(Paragraph(
        "The platform was verified using a 24-point automated test suite validating security, transactions, clinical accuracy, and distributed discovery. <b>Pass Rate: 100% (24 / 24)</b>:", body_style
    ))

    test_headers = [Paragraph("<b>Test ID</b>", th_style), Paragraph("<b>Test Category</b>", th_style), Paragraph("<b>Scenario & Input</b>", th_style), Paragraph("<b>Expected & Actual Result</b>", th_style), Paragraph("<b>Status</b>", th_style)]
    test_rows = [
        [Paragraph("TC-01", td_bold), Paragraph("Authentication", td_style), Paragraph("POST /api/auth/login (admin/admin123)", td_style), Paragraph("HTTP 200 OK + JWT (role=ROLE_ADMIN)", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
        [Paragraph("TC-02", td_bold), Paragraph("Authentication", td_style), Paragraph("POST /api/auth/login (patient_john)", td_style), Paragraph("HTTP 200 OK + JWT (role=ROLE_PATIENT)", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
        [Paragraph("TC-03", td_bold), Paragraph("Authentication", td_style), Paragraph("POST /api/auth/login (doctor_smith)", td_style), Paragraph("HTTP 200 OK + JWT (role=ROLE_DOCTOR)", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
        [Paragraph("TC-S01", td_bold), Paragraph("Security", td_style), Paragraph("GET /api/doctors without Authorization header", td_style), Paragraph("HTTP 401 Unauthorized enforced by Gateway", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
        [Paragraph("TC-S02", td_bold), Paragraph("Security", td_style), Paragraph("POST /api/auth/login with wrong password", td_style), Paragraph("HTTP 401 Bad Credentials returned", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
        [Paragraph("TC-D01", td_bold), Paragraph("Doctor Service", td_style), Paragraph("GET /api/doctors with valid JWT", td_style), Paragraph("HTTP 200 OK, returns 6 active doctors", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
        [Paragraph("TC-D02", td_bold), Paragraph("Doctor Service", td_style), Paragraph("GET /api/doctors/department/Cardiology", td_style), Paragraph("HTTP 200 OK, only Cardiology specialists", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
        [Paragraph("TC-D03", td_bold), Paragraph("Doctor Service", td_style), Paragraph("GET /api/doctors/5 by ID", td_style), Paragraph("HTTP 200 OK, returns Dr. Sarah Jenkins", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
        [Paragraph("TC-D04", td_bold), Paragraph("Doctor Service", td_style), Paragraph("POST /api/doctors/5/slots (FRIDAY 10-1)", td_style), Paragraph("HTTP 201 Created, slot mapped to doctor", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
        [Paragraph("TC-D05", td_bold), Paragraph("Doctor Service", td_style), Paragraph("POST /api/doctors (unique email)", td_style), Paragraph("HTTP 201 Created, new doctor persisted", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
        [Paragraph("TC-P01", td_bold), Paragraph("Patient Service", td_style), Paragraph("GET /api/patients with valid JWT", td_style), Paragraph("HTTP 200 OK, 4 patient records retrieved", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
        [Paragraph("TC-P02", td_bold), Paragraph("Patient Service", td_style), Paragraph("GET /api/patients/1 by ID", td_style), Paragraph("HTTP 200 OK, returns John Doe details", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
        [Paragraph("TC-P03", td_bold), Paragraph("Patient Service", td_style), Paragraph("POST /api/patients/1/appointments", td_style), Paragraph("HTTP 201 Created, appointment persisted", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
        [Paragraph("TC-P04", td_bold), Paragraph("Patient Service", td_style), Paragraph("GET /api/patients/1/appointments", td_style), Paragraph("HTTP 200 OK, appointment history rendered", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
        [Paragraph("TC-T01", td_bold), Paragraph("AI Triage", td_style), Paragraph("'severe chest pain and shortness of breath'", td_style), Paragraph("EMERGENCY urgency + Cardiology dept", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
        [Paragraph("TC-T02", td_bold), Paragraph("AI Triage", td_style), Paragraph("'throbbing migraine headache for 2 days'", td_style), Paragraph("HIGH urgency + Neurology dept", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
        [Paragraph("TC-T03", td_bold), Paragraph("AI Triage", td_style), Paragraph("'red itchy rash on forearms'", td_style), Paragraph("MODERATE urgency + Dermatology dept", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
        [Paragraph("TC-T04", td_bold), Paragraph("AI Triage", td_style), Paragraph("'mild runny nose and sneezing'", td_style), Paragraph("LOW urgency + General Medicine dept", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
        [Paragraph("TC-I01", td_bold), Paragraph("Discovery", td_style), Paragraph("GET /eureka/apps registry query", td_style), Paragraph("All 4 services registered and UP", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
        [Paragraph("TC-H01..5", td_bold), Paragraph("Health Checks", td_style), Paragraph("GET /actuator/health on all 5 ports", td_style), Paragraph("Status 'UP' confirmed across all services", td_style), Paragraph("<font color='#16A34A'><b>PASS</b></font>", td_style)],
    ]
    test_table = Table([test_headers] + test_rows, colWidths=[55, 75, 150, 184, 40])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(test_table)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 8: TEACHER & EXTERNAL EXAMINER VIVA Q&A
    # =========================================================================
    story.append(Paragraph("8. External Examiner & Teacher Viva Q&A Guide", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=12, spaceBefore=2))

    story.append(Paragraph(
        "This section prepares the student with authoritative, technically rigorous answers to the top questions asked by university professors and external evaluators:", body_style
    ))

    qa_list = [
        ("Q1: Why did you choose a Microservices architecture instead of a traditional Monolith?",
         "A monolithic architecture couples all domain models and databases together. If the appointment scheduler experiences high load, the emergency triage and login services can freeze. Microservices allow independent scaling, isolated PostgreSQL databases, failure isolation, and team autonomy."),

        ("Q2: How does the API Gateway locate microservices without hardcoding hostnames?",
         "Through Spring Cloud Netflix Eureka. Each microservice registers its IP, port, and service-id upon boot. The API Gateway uses 'lb://service-name' URIs, delegating to Spring Cloud LoadBalancer to dynamically resolve healthy instances with round-robin balancing."),

        ("Q3: How do you handle security across multiple microservices?",
         "We implement stateless JWT bearer authentication at the API Gateway perimeter. The Gateway validates the HMAC-SHA256 signature and role claims. Valid requests pass through to internal microservices with forwarded identity headers ('X-Auth-Username', 'X-Auth-Role'). Invalid requests receive a 401 Unauthorized immediately."),

        ("Q4: Why are patient records and doctor records in two separate databases?",
         "To strictly enforce Domain-Driven Design (DDD) and the Database-per-Service pattern. If doctor-service updates its schema or changes its database engine, patient-service is completely unaffected. Direct cross-database SQL JOINs are eliminated in favor of clean RESTful APIs."),

        ("Q5: What happens if Redis cache crashes or is unavailable?",
         "The platform implements a resilient CacheErrorHandler. Both doctor-service and patient-service catch Redis connection exceptions silently, logging a warning and falling back to PostgreSQL directly. The application remains 100% functional with zero 500 errors to users."),

        ("Q6: How does the AI Symptom Triage work if there is no internet connection or OpenAI key?",
         "SpringAiTriageService implements a two-tier hybrid architecture. If an OpenAI API key and internet connection are present, it prompts GPT-4o-mini. If offline or no key is configured, a deterministic clinical heuristics taxonomy evaluates symptom keywords (e.g. 'chest pain' -> EMERGENCY Cardiology), ensuring uninterrupted clinical safety."),

        ("Q7: How did you fix the lazy loading issues with JPA entity serialization?",
         "We applied '@Transactional(readOnly = true)' to service-layer read methods and configured '@JsonManagedReference' and '@JsonBackReference' on bidirectional associations. This ensures the Hibernate session remains open during Jackson JSON serialization and avoids infinite recursive loops."),

        ("Q8: How does the frontend handle expired or unauthorized sessions?",
         "Axios response interceptors inspect every HTTP status code. If an HTTP 401 Unauthorized response is intercepted, the client automatically wipes 'hospital_jwt_token' from localStorage and redirects the user to the login screen with an expiration query parameter."),

        ("Q9: What is the role of Netflix Eureka's self-preservation mode?",
         "Eureka monitors heartbeats sent every 30 seconds. If a network partition occurs and Eureka misses heartbeats from many instances simultaneously, it enters self-preservation mode to prevent incorrectly deregistering healthy instances that are simply experiencing network lag."),

        ("Q10: How would you deploy this platform in an enterprise Kubernetes production environment?",
         "Each service has a Dockerfile. We build container images and deploy them as Kubernetes Deployments with ClusterIP Services. PostgreSQL runs as StatefulSets with persistent volumes. Ingress-nginx replaces the outer gateway, and Spring Cloud Gateway or Kubernetes Service DNS handles internal service discovery.")
    ]

    for q, a in qa_list:
        story.append(Paragraph(f"<b>{q}</b>", h2_style))
        story.append(Paragraph(f"<b>Evaluation Answer:</b> {a}", body_style))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 9: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    story.append(Paragraph("9. Conclusion & Future Roadmap", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=12, spaceBefore=2))

    story.append(Paragraph(
        "The MediPulse Distributed Hospital Management Microservices Platform successfully demonstrates a modern, "
        "cloud-native implementation of clinical healthcare delivery. "
        "By decomposing monolithic bottlenecks into resilient microservices, the system guarantees high availability, "
        "data integrity across isolated PostgreSQL stores, instant AI-assisted clinical triage, and sub-2ms catalog queries via Redis.", body_style
    ))

    story.append(Paragraph("Future Architectural Enhancements:", h2_style))
    story.append(Paragraph("• <b>Asynchronous Event Streaming (Apache Kafka):</b> Transition appointment booking from synchronous HTTP to asynchronous event-driven messaging with Kafka topics (e.g. <code>appointment-scheduled</code>, <code>notification-dispatch</code>).", bullet_style))
    story.append(Paragraph("• <b>Distributed Tracing & Observability:</b> Integrate Micrometer Tracing with Zipkin or OpenTelemetry to trace end-to-end request latency across the Gateway and downstream microservices.", bullet_style))
    story.append(Paragraph("• <b>Circuit Breaker & Rate Limiting:</b> Implement Resilience4j CircuitBreakers and Redis-based rate limiting on the API Gateway to protect services against DDoS and cascade failures.", bullet_style))
    story.append(Paragraph("• <b>FHIR / HL7 Standards Compliance:</b> Standardize patient medical history schemas with HL7 FHIR (Fast Healthcare Interoperability Resources) for global electronic health record (EHR) interoperability.", bullet_style))

    story.append(Spacer(1, 25))

    # Sign-off box
    sign_data = [
        [
            Paragraph("<b>Project Evaluation Status:</b><br/>"
                      "Verified by Automated Test Suite (24/24 PASS)<br/>"
                      "All Microservices & Ports Active (8761, 8080, 8081, 8082, 8083, 3000)", td_style),
            Paragraph("<b>Faculty / Examiner Signature:</b><br/><br/><br/>"
                      "________________________________________<br/>"
                      "External Technical Examiner / Faculty Guide", td_style)
        ]
    ]
    sign_table = Table(sign_data, colWidths=[252, 252])
    sign_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, BORDER),
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(sign_table)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {filename}")

if __name__ == "__main__":
    output_filename = "Hospital_Management_Microservices_Project_Report.pdf"
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
    build_pdf(output_filename)
