import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    COLOR_BG = RGBColor(248, 250, 252)        # Slate 50
    COLOR_PRIMARY = RGBColor(15, 23, 42)      # Slate 900
    COLOR_SECONDARY = RGBColor(13, 148, 136)  # Teal 600
    COLOR_ACCENT = RGBColor(37, 99, 235)      # Blue 600
    COLOR_CARD_BG = RGBColor(255, 255, 255)   # White
    COLOR_CARD_BORDER = RGBColor(226, 232, 240) # Slate 200
    COLOR_TEXT_MAIN = RGBColor(15, 23, 42)
    COLOR_TEXT_MUTED = RGBColor(100, 116, 139) # Slate 500
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_RED = RGBColor(225, 29, 72)         # Rose 600
    COLOR_GREEN = RGBColor(22, 163, 74)       # Green 600

    def add_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()

    def add_header(slide, title, category="HOSPITAL MANAGEMENT MICROSERVICES"):
        # Header category tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_SECONDARY

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        tf = t_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY

        # Underline accent line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(2.0), Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_SECONDARY
        line.line.fill.background()

    def add_card(slide, left, top, width, height, title="", title_color=COLOR_PRIMARY):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_BG
        card.line.color.rgb = COLOR_CARD_BORDER
        card.line.width = Pt(1.2)

        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.5))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(15)
            p.font.bold = True
            p.font.color.rgb = title_color
        return card

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = RGBColor(15, 23, 42) # Dark Navy
    bg1.line.fill.background()

    # Decorative accent bar
    dec_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.8), Inches(0.2), Inches(3.6))
    dec_bar.fill.solid()
    dec_bar.fill.fore_color.rgb = COLOR_SECONDARY
    dec_bar.line.fill.background()

    title_box = s1.shapes.add_textbox(Inches(1.4), Inches(1.7), Inches(11.0), Inches(2.2))
    tf1 = title_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Hospital Management Microservices"
    p1.font.size = Pt(38)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE

    p2 = tf1.add_paragraph()
    p2.text = "Enterprise Distributed Healthcare Platform with Spring AI, JWT, Redis & Gateway"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(148, 163, 184)

    badges = [
        ("Spring Boot 3.2", RGBColor(16, 185, 129)),
        ("Spring Cloud Gateway", RGBColor(59, 130, 246)),
        ("Spring AI Triage", RGBColor(168, 85, 247)),
        ("Spring Security JWT", RGBColor(245, 158, 11)),
        ("Redis Caching", RGBColor(239, 68, 68)),
        ("PostgreSQL (Dual DB)", RGBColor(14, 165, 233)),
        ("Docker Containerized", RGBColor(37, 99, 235)),
        ("Eclipse / STS Ready", RGBColor(217, 70, 239))
    ]

    bx = Inches(1.4)
    by = Inches(4.3)
    bw = Inches(2.6)
    bh = Inches(0.55)
    for i, (b_text, b_col) in enumerate(badges):
        row = i // 4
        col = i % 4
        badge_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx + col * (bw + Inches(0.2)), by + row * (bh + Inches(0.2)), bw, bh)
        badge_box.fill.solid()
        badge_box.fill.fore_color.rgb = RGBColor(30, 41, 59)
        badge_box.line.color.rgb = b_col
        badge_box.line.width = Pt(1.5)
        btf = badge_box.text_frame
        bp = btf.paragraphs[0]
        bp.text = b_text
        bp.font.size = Pt(11)
        bp.font.bold = True
        bp.font.color.rgb = COLOR_WHITE
        bp.alignment = PP_ALIGN.CENTER

    meta_box = s1.shapes.add_textbox(Inches(1.4), Inches(6.0), Inches(10.0), Inches(0.8))
    mtf = meta_box.text_frame
    mp = mtf.paragraphs[0]
    mp.text = "Architecture, Design Specifications, UML Diagrams, Test Cases & Implementation Guide"
    mp.font.size = Pt(12)
    mp.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # SLIDE 2: Executive Summary & System Objectives
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_background(s2)
    add_header(s2, "Executive Summary & Engineering Goals", "OVERVIEW")

    add_card(s2, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.1), "Business Challenges", COLOR_RED)
    b_tb = s2.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(3.3), Inches(4.2))
    btf = b_tb.text_frame
    btf.word_wrap = True
    bullets_b = [
        ("Monolithic Bottlenecks:", " Legacy hospital systems suffer from high downtime, rigid scaling, and tight coupling between clinical and scheduling services."),
        ("Slow Medical Routing:", " Emergency patients experience triage delays before being paired with specialized clinicians."),
        ("High Database Latency:", " Frequent queries for doctor directories and medical profiles strain relational databases."),
        ("Security Vulnerabilities:", " Lack of centralized zero-trust token authentication across internal APIs.")
    ]
    for bold_prefix, text in bullets_b:
        p = btf.add_paragraph()
        p.text = bold_prefix + text
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(12)

    add_card(s2, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.1), "Engineered Solutions", COLOR_SECONDARY)
    s_tb = s2.shapes.add_textbox(Inches(5.0), Inches(2.5), Inches(3.3), Inches(4.2))
    stf = s_tb.text_frame
    stf.word_wrap = True
    bullets_s = [
        ("Microservices Architecture:", " Autonomous services (Auth, Patient, Doctor, Gateway, Registry) independently deployable and scalable."),
        ("Spring AI Clinical Triage:", " Intelligent symptom evaluation assigning clinical urgency (Emergency/High/Mod) and automated doctor referral."),
        ("Dual-Layer Redis Cache:", " Sub-millisecond doctor lookup and patient profile retrieval with smart cache eviction."),
        ("Centralized JWT Gateway:", " Secure stateless Bearer token validation and automatic routing with Spring Cloud LoadBalancer.")
    ]
    for bold_prefix, text in bullets_s:
        p = stf.add_paragraph()
        p.text = bold_prefix + text
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(12)

    add_card(s2, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.1), "Core KPIs & Deliverables", COLOR_ACCENT)
    k_tb = s2.shapes.add_textbox(Inches(9.0), Inches(2.5), Inches(3.3), Inches(4.2))
    ktf = k_tb.text_frame
    ktf.word_wrap = True
    bullets_k = [
        ("High Availability:", " Eureka client-side load balancing with self-healing heartbeat monitoring."),
        ("Eclipse & STS Native:", " Standard Maven structure with .project & .classpath ready for 1-click import."),
        ("Isolated PostgreSQL Schemas:", " patient_db & doctor_db with automatic schema migration."),
        ("Docker Containerized:", " One-step spin up of all databases, redis, and services via docker-compose.yml.")
    ]
    for bold_prefix, text in bullets_k:
        p = ktf.add_paragraph()
        p.text = bold_prefix + text
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(12)

    # =========================================================================
    # SLIDE 3: System Architecture Diagram (Component Topology)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_background(s3)
    add_header(s3, "Distributed Microservices Architecture Topology", "SYSTEM DESIGN")

    # Layer 1: Client
    c_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.5), Inches(1.8), Inches(4.3), Inches(0.6))
    c_box.fill.solid()
    c_box.fill.fore_color.rgb = RGBColor(30, 41, 59)
    c_box.line.color.rgb = COLOR_SECONDARY
    c_tf = c_box.text_frame
    c_p = c_tf.paragraphs[0]
    c_p.text = "CLIENT LAYER (Web Browser / Mobile App / Postman)"
    c_p.font.size = Pt(12)
    c_p.font.bold = True
    c_p.font.color.rgb = COLOR_WHITE
    c_p.alignment = PP_ALIGN.CENTER

    # Arrow to Gateway
    arr1 = s3.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(6.4), Inches(2.45), Inches(0.5), Inches(0.35))
    arr1.fill.solid()
    arr1.fill.fore_color.rgb = COLOR_ACCENT
    arr1.line.fill.background()

    # Layer 2: API Gateway
    gw_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.2), Inches(2.85), Inches(9.0), Inches(0.95))
    gw_box.fill.solid()
    gw_box.fill.fore_color.rgb = RGBColor(238, 242, 255)
    gw_box.line.color.rgb = COLOR_ACCENT
    gw_box.line.width = Pt(2.0)
    gw_tf = gw_box.text_frame
    gw_p1 = gw_tf.paragraphs[0]
    gw_p1.text = "SPRING CLOUD API GATEWAY (Port 8080)"
    gw_p1.font.size = Pt(14)
    gw_p1.font.bold = True
    gw_p1.font.color.rgb = COLOR_ACCENT
    gw_p1.alignment = PP_ALIGN.CENTER
    gw_p2 = gw_tf.add_paragraph()
    gw_p2.text = "Global JWT Authentication Filter  |  CORS Management  |  Client-Side Load Balancer  |  Route Locator"
    gw_p2.font.size = Pt(11)
    gw_p2.font.color.rgb = COLOR_TEXT_MAIN
    gw_p2.alignment = PP_ALIGN.CENTER

    # Service Discovery on the side
    reg_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.3), Inches(2.4), Inches(1.6))
    reg_box.fill.solid()
    reg_box.fill.fore_color.rgb = RGBColor(254, 243, 199)
    reg_box.line.color.rgb = RGBColor(217, 119, 6)
    reg_box.line.width = Pt(1.5)
    rtf = reg_box.text_frame
    rp1 = rtf.paragraphs[0]
    rp1.text = "SERVICE REGISTRY"
    rp1.font.size = Pt(12)
    rp1.font.bold = True
    rp1.font.color.rgb = RGBColor(180, 83, 9)
    rp1.alignment = PP_ALIGN.CENTER
    rp2 = rtf.add_paragraph()
    rp2.text = "Netflix Eureka Server\nPort: 8761\nHeartbeat Healthcheck\nDynamic Registration"
    rp2.font.size = Pt(10)
    rp2.font.color.rgb = COLOR_TEXT_MAIN

    # Microservice 1: Auth Service
    as_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.6), Inches(4.3), Inches(2.8), Inches(1.6))
    as_box.fill.solid()
    as_box.fill.fore_color.rgb = COLOR_CARD_BG
    as_box.line.color.rgb = COLOR_SECONDARY
    as_box.line.width = Pt(1.5)
    astf = as_box.text_frame
    asp1 = astf.paragraphs[0]
    asp1.text = "AUTH SERVICE"
    asp1.font.size = Pt(12)
    asp1.font.bold = True
    asp1.font.color.rgb = COLOR_SECONDARY
    asp1.alignment = PP_ALIGN.CENTER
    asp2 = astf.add_paragraph()
    asp2.text = "Port: 8081\n• Spring Security 6\n• JJWT Claims & Sign\n• Role-Based Access\n• BCrypt Encrypted"
    asp2.font.size = Pt(10)
    asp2.font.color.rgb = COLOR_TEXT_MAIN

    # Microservice 2: Patient Service
    ps_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.3), Inches(3.0), Inches(1.6))
    ps_box.fill.solid()
    ps_box.fill.fore_color.rgb = COLOR_CARD_BG
    ps_box.line.color.rgb = RGBColor(168, 85, 247)
    ps_box.line.width = Pt(1.5)
    pstf = ps_box.text_frame
    psp1 = pstf.paragraphs[0]
    psp1.text = "PATIENT SERVICE"
    psp1.font.size = Pt(12)
    psp1.font.bold = True
    psp1.font.color.rgb = RGBColor(147, 51, 234)
    psp1.alignment = PP_ALIGN.CENTER
    psp2 = pstf.add_paragraph()
    psp2.text = "Port: 8082\n• Spring AI Symptom Triage\n• Patient Profile & History\n• Appointment Booking\n• RestClient Inter-Service"
    psp2.font.size = Pt(10)
    psp2.font.color.rgb = COLOR_TEXT_MAIN

    # Microservice 3: Doctor Service
    ds_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.2), Inches(4.3), Inches(2.4), Inches(1.6))
    ds_box.fill.solid()
    ds_box.fill.fore_color.rgb = COLOR_CARD_BG
    ds_box.line.color.rgb = COLOR_ACCENT
    ds_box.line.width = Pt(1.5)
    dstf = ds_box.text_frame
    dsp1 = dstf.paragraphs[0]
    dsp1.text = "DOCTOR SERVICE"
    dsp1.font.size = Pt(12)
    dsp1.font.bold = True
    dsp1.font.color.rgb = COLOR_ACCENT
    dsp1.alignment = PP_ALIGN.CENTER
    dsp2 = dstf.add_paragraph()
    dsp2.text = "Port: 8083\n• Specialty Catalog\n• Slot Management\n• Schedule Booking\n• Resilient Fallback"
    dsp2.font.size = Pt(10)
    dsp2.font.color.rgb = COLOR_TEXT_MAIN

    # Persistence Layer
    db_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.6), Inches(6.2), Inches(9.0), Inches(0.85))
    db_box.fill.solid()
    db_box.fill.fore_color.rgb = RGBColor(241, 245, 249)
    db_box.line.color.rgb = RGBColor(148, 163, 184)
    dbtf = db_box.text_frame
    dbp1 = dbtf.paragraphs[0]
    dbp1.text = "DATA & CACHING TIER (PostgreSQL 15 & Redis 7)"
    dbp1.font.size = Pt(12)
    dbp1.font.bold = True
    dbp1.font.color.rgb = COLOR_PRIMARY
    dbp1.alignment = PP_ALIGN.CENTER
    dbp2 = dbtf.add_paragraph()
    dbp2.text = "PostgreSQL: patient_db (Port 5432)  |  PostgreSQL: doctor_db (Port 5432)  |  Distributed Redis Cache (Port 6379)"
    dbp2.font.size = Pt(10)
    dbp2.font.color.rgb = COLOR_TEXT_MUTED
    dbp2.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 4: Eureka Service Discovery & Load Balancing
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_background(s4)
    add_header(s4, "Eureka Service Registry & Client-Side Load Balancing", "DISCOVERY & HIGH AVAILABILITY")

    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), "Service Discovery Mechanics", COLOR_SECONDARY)
    s4_tb1 = s4.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(5.2), Inches(4.2))
    tf4_1 = s4_tb1.text_frame
    tf4_1.word_wrap = True
    pts4_1 = [
        ("Decentralized Registry:", " Netflix Eureka Server acts as the phonebook for microservices running at http://localhost:8761."),
        ("Heartbeat Health Checks:", " Each client microservice transmits heartbeats every 30s. If heartbeats cease, Eureka evicts failing instances automatically."),
        ("No Hardcoded IP/Ports:", " Services locate each other via logical application names: AUTH-SERVICE, PATIENT-SERVICE, DOCTOR-SERVICE."),
        ("Self-Preservation Protection:", " Configured eviction timers ensure stale instances don't block requests during network hiccups.")
    ]
    for b_prefix, txt in pts4_1:
        p = tf4_1.add_paragraph()
        p.text = b_prefix + txt
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(10)

    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), "Spring Cloud LoadBalancer", COLOR_ACCENT)
    s4_tb2 = s4.shapes.add_textbox(Inches(7.0), Inches(2.5), Inches(5.3), Inches(4.2))
    tf4_2 = s4_tb2.text_frame
    tf4_2.word_wrap = True
    pts4_2 = [
        ("Gateway Routing (lb://):", " API Gateway dispatches incoming requests to lb://patient-service and lb://doctor-service with round-robin load distribution."),
        ("Inter-Service Load Balancing:", " Patient Service invokes Doctor Service via @LoadBalanced RestTemplate, resolving http://doctor-service/api/doctors without edge hops."),
        ("Elastic Scaling:", " Spin up multiple instances of Patient Service (e.g. ports 8082, 8084) and Eureka balances the incoming load transparently."),
        ("Zero Downtime Deployments:", " Traffic shifts away from stopping instances before decommissioning.")
    ]
    for b_prefix, txt in pts4_2:
        p = tf4_2.add_paragraph()
        p.text = b_prefix + txt
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 5: API Gateway & Security Routing Filter
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_background(s5)
    add_header(s5, "Spring Cloud API Gateway & Security Filter", "EDGE GATEWAY")

    add_card(s5, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.1), "Gateway Routing Table", COLOR_PRIMARY)
    tb5_1 = s5.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(3.3), Inches(4.2))
    tf5_1 = tb5_1.text_frame
    tf5_1.word_wrap = True
    r_rules = [
        ("• /api/auth/**", "\nTarget: lb://auth-service\nPublic access for login & registration"),
        ("• /api/patients/**", "\nTarget: lb://patient-service\nProtected: Requires valid Bearer JWT"),
        ("• /api/doctors/**", "\nTarget: lb://doctor-service\nProtected: Requires valid Bearer JWT"),
        ("• /eureka/** & /actuator", "\nInternal observability and monitoring endpoints")
    ]
    for r_title, r_desc in r_rules:
        p = tf5_1.add_paragraph()
        p.text = r_title + r_desc
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(10)

    add_card(s5, Inches(4.8), Inches(1.8), Inches(7.7), Inches(5.1), "JwtAuthenticationFilter Pipeline", COLOR_SECONDARY)
    tb5_2 = s5.shapes.add_textbox(Inches(5.0), Inches(2.5), Inches(7.3), Inches(4.2))
    tf5_2 = tb5_2.text_frame
    tf5_2.word_wrap = True
    filter_steps = [
        ("Step 1 - Route Validation:", " RouteValidator checks if request path is in open whitelist (/api/auth/login, /register). If public, pass through immediately."),
        ("Step 2 - Header Inspection:", " For secured routes, verifies presence of 'Authorization: Bearer <token>'. Returns HTTP 401 Unauthorized if missing."),
        ("Step 3 - Cryptographic Verification:", " Validates HMAC-SHA256 signature and expiration date against the 256-bit secret key."),
        ("Step 4 - Downstream Header Mutation:", " Extracts claims (username, role) and injects X-Auth-Username & X-Auth-Role headers into downstream request."),
        ("Step 5 - Global CORS Handling:", " Cross-Origin Resource Sharing configuration permits all methods (GET, POST, PUT, DELETE) and origins.")
    ]
    for b_prefix, txt in filter_steps:
        p = tf5_2.add_paragraph()
        p.text = b_prefix + txt
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 6: Spring Security & JWT Authentication
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_background(s6)
    add_header(s6, "Spring Security 6 & JJWT Token Lifecycle", "SECURITY ARCHITECTURE")

    add_card(s6, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.1), "Token Structure", COLOR_ACCENT)
    tb6_1 = s6.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(3.3), Inches(4.2))
    tf6_1 = tb6_1.text_frame
    tf6_1.word_wrap = True
    jwt_parts = [
        ("1. Header (Algorithm):", "\n{\n  'alg': 'HS256',\n  'typ': 'JWT'\n}"),
        ("2. Payload (Claims):", "\n{\n  'sub': 'patient_john',\n  'role': 'ROLE_PATIENT',\n  'iat': 1773054000,\n  'exp': 1773140400\n}"),
        ("3. Signature:", "\nHMACSHA256(\n  base64(header) + '.' +\n  base64(payload), secret\n)")
    ]
    for p_title, p_desc in jwt_parts:
        p = tf6_1.add_paragraph()
        p.text = p_title + p_desc
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(8)

    add_card(s6, Inches(4.8), Inches(1.8), Inches(7.7), Inches(5.1), "Authentication Workflow & RBAC", COLOR_PRIMARY)
    tb6_2 = s6.shapes.add_textbox(Inches(5.0), Inches(2.5), Inches(7.3), Inches(4.2))
    tf6_2 = tb6_2.text_frame
    tf6_2.word_wrap = True
    sec_points = [
        ("• User Registration & BCrypt Hashing:", " Passwords are salted and encrypted via BCryptPasswordEncoder before storage; plaintext passwords never persist."),
        ("• Login Authentication:", " User credentials validated against encrypted hashes. Upon success, a 24-hour validity JWT token is minted and returned in AuthResponse."),
        ("• Role-Based Access Control (RBAC):", " Roles supported: ROLE_PATIENT, ROLE_DOCTOR, ROLE_ADMIN. Allows strict separation of patient data vs doctor availability editing."),
        ("• Stateless Microservices:", " Services maintain zero session state in memory; every request is authenticated via the signed JWT token, enabling horizontal scalability.")
    ]
    for b_prefix, txt in sec_points:
        p = tf6_2.add_paragraph()
        p.text = b_prefix + txt
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(12)

    # =========================================================================
    # SLIDE 7: Spring AI Medical Diagnostic & Triage Engine
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_background(s7)
    add_header(s7, "Spring AI Medical Diagnostic & Symptom Triage Engine", "INTELLIGENT HEALTHCARE")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), "Clinical Inference Architecture", RGBColor(147, 51, 234))
    tb7_1 = s7.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(5.2), Inches(4.2))
    tf7_1 = tb7_1.text_frame
    tf7_1.word_wrap = True
    ai_points1 = [
        ("Symptom Ingestion:", " Accepts unstructured natural language symptoms (e.g. 'sharp chest pain radiating to left arm', 'skin rash with severe itching')."),
        ("Urgency Scoring:", " Categorizes into 4 clinical severity tiers: EMERGENCY, HIGH, MODERATE, LOW based on evidence-based triage protocols."),
        ("Department Specialization:", " Dynamically routes to Cardiology, Neurology, Dermatology, Orthopedics, or General Medicine."),
        ("Diagnostic & Care Prescriptions:", " Generates differential diagnoses, patient precautions, and recommended laboratory diagnostic tests.")
    ]
    for b_prefix, txt in ai_points1:
        p = tf7_1.add_paragraph()
        p.text = b_prefix + txt
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(10)

    add_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), "Dual-Mode Engine: LLM + Resilient Fallback", COLOR_SECONDARY)
    tb7_2 = s7.shapes.add_textbox(Inches(7.0), Inches(2.5), Inches(5.3), Inches(4.2))
    tf7_2 = tb7_2.text_frame
    tf7_2.word_wrap = True
    ai_points2 = [
        ("Spring AI Model Integration:", " Configured to connect to Spring AI OpenAI (gpt-4o-mini) or local Ollama endpoints when API keys are supplied."),
        ("Offline Zero-Failure Engine:", " In absence of an external API key, the built-in clinical rules engine activates automatically, guaranteeing 100% uptime with zero external dependencies!"),
        ("Live Inter-Service Doctor Referral:", " Triage result automatically calls Doctor Service over Eureka LoadBalancer to return top rated doctors in the matching department with instant booking slots!"),
        ("Triage Payload Contract:", " Returns structured TriageResponse with urgency, diagnosis, suggested lab tests, and doctor profiles.")
    ]
    for b_prefix, txt in ai_points2:
        p = tf7_2.add_paragraph()
        p.text = b_prefix + txt
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 8: Multi-Level Redis Caching Architecture
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_background(s8)
    add_header(s8, "Distributed Redis Caching & Cache Invalidation", "PERFORMANCE OPTIMIZATION")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), "Cache-Aside Implementation", COLOR_RED)
    tb8_1 = s8.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(5.2), Inches(4.2))
    tf8_1 = tb8_1.text_frame
    tf8_1.word_wrap = True
    cache_points1 = [
        ("@EnableCaching & @Cacheable:", " Annotations on DoctorService and PatientService intercept calls. Cache keys: 'doctors::all', 'doctors::{id}', 'patients::{id}'."),
        ("Sub-Millisecond Response:", " First request queries PostgreSQL (50-100ms); subsequent requests hit Redis memory in < 2ms (98% latency reduction)."),
        ("Time-To-Live (TTL):", " 15-minute TTL configured via RedisCacheConfiguration prevents stale cache buildup."),
        ("JSON Serialization:", " GenericJackson2JsonRedisSerializer ensures clean human-readable JSON inspection in redis-cli.")
    ]
    for b_prefix, txt in cache_points1:
        p = tf8_1.add_paragraph()
        p.text = b_prefix + txt
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(10)

    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), "Cache Invalidation & Resilient Fallback", COLOR_PRIMARY)
    tb8_2 = s8.shapes.add_textbox(Inches(7.0), Inches(2.5), Inches(5.3), Inches(4.2))
    tf8_2 = tb8_2.text_frame
    tf8_2.word_wrap = True
    cache_points2 = [
        ("@CacheEvict Synchronicity:", " Whenever a doctor is updated, deleted, or a new patient is registered, @CacheEvict(allEntries=true) purges stale cache."),
        ("Zero-Crash CacheErrorHandler:", " Custom error handler intercepts Redis connection issues. If Redis server is offline, requests smoothly fall back to PostgreSQL without crashing!"),
        ("Multi-Service Namespaces:", " Isolated cache prefixes ('doctors', 'doctors_dept', 'patients') prevent key collision between microservices."),
        ("Memory Footprint:", " Automatic LRU (Least Recently Used) eviction keeps Redis memory usage minimal.")
    ]
    for b_prefix, txt in cache_points2:
        p = tf8_2.add_paragraph()
        p.text = b_prefix + txt
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 9: Relational Database Architecture (PostgreSQL)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_background(s9)
    add_header(s9, "PostgreSQL Database Design (patient_db & doctor_db)", "PERSISTENCE TIER")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), "patient_db Schema (Port 5432)", COLOR_SECONDARY)
    tb9_1 = s9.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(5.2), Inches(4.2))
    tf9_1 = tb9_1.text_frame
    tf9_1.word_wrap = True
    pdb_points = [
        ("Table: patients", "\n• id (BIGINT, PK, Auto-Inc)\n• first_name, last_name (VARCHAR, NOT NULL)\n• email (VARCHAR, UNIQUE, NOT NULL)\n• phone, age, gender, blood_group\n• address, emergency_contact, medical_history"),
        ("Table: appointments", "\n• id (BIGINT, PK, Auto-Inc)\n• patient_id (FK -> patients.id)\n• doctor_id, doctor_name, department\n• appointment_date (DATE), time_slot\n• status (SCHEDULED, CONFIRMED, COMPLETED)\n• symptoms, notes")
    ]
    for b_prefix, txt in pdb_points:
        p = tf9_1.add_paragraph()
        p.text = b_prefix + txt
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(10)

    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), "doctor_db Schema (Port 5432)", COLOR_ACCENT)
    tb9_2 = s9.shapes.add_textbox(Inches(7.0), Inches(2.5), Inches(5.3), Inches(4.2))
    tf9_2 = tb9_2.text_frame
    tf9_2.word_wrap = True
    ddb_points = [
        ("Table: doctors", "\n• id (BIGINT, PK, Auto-Inc)\n• name (VARCHAR, NOT NULL)\n• department (VARCHAR, NOT NULL - Cardiology, etc.)\n• specialization (VARCHAR, NOT NULL)\n• email (VARCHAR, UNIQUE, NOT NULL)\n• phone, consultation_fee, rating, experience_years\n• is_available (BOOLEAN)"),
        ("Table: availability_slots", "\n• id (BIGINT, PK, Auto-Inc)\n• doctor_id (FK -> doctors.id)\n• day_of_week (MONDAY, TUESDAY...)\n• start_time, end_time (VARCHAR)\n• is_booked (BOOLEAN DEFAULT FALSE)")
    ]
    for b_prefix, txt in ddb_points:
        p = tf9_2.add_paragraph()
        p.text = b_prefix + txt
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 10: UML Working Activity Diagram (Patient & AI Triage)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_background(s10)
    add_header(s10, "UML Working Activity Diagram: Patient Triage & Booking", "ACTIVITY WORKFLOW")

    # Workflow Visual Cards
    steps_act = [
        ("1. User Login / Auth", "Client authenticates via /api/auth/login and receives signed JWT token.", Inches(0.8), Inches(2.0), COLOR_SECONDARY),
        ("2. Submit Symptoms", "Patient enters symptoms (e.g. chest pain, fever) to /api/patients/ai/symptom-triage.", Inches(3.9), Inches(2.0), COLOR_ACCENT),
        ("3. Spring AI Evaluation", "AI Engine classifies urgency (EMERGENCY / HIGH / MOD), department, & precautions.", Inches(7.0), Inches(2.0), RGBColor(147, 51, 234)),
        ("4. LoadBalanced Query", "Patient Service calls http://doctor-service to fetch available matching doctors.", Inches(10.1), Inches(2.0), COLOR_PRIMARY),
        ("5. Review Triage & Docs", "Patient receives AI diagnosis summary and recommended specialist profiles.", Inches(0.8), Inches(4.6), COLOR_PRIMARY),
        ("6. Select Slot & Book", "Patient picks date/time slot via /api/patients/{id}/appointments.", Inches(3.9), Inches(4.6), COLOR_ACCENT),
        ("7. Redis Evict & DB Save", "Appointment stored in patient_db; Doctor slot marked booked in doctor_db.", Inches(7.0), Inches(4.6), COLOR_SECONDARY),
        ("8. Confirmation", "Instant confirmation response with appointment ID and instructions returned.", Inches(10.1), Inches(4.6), COLOR_GREEN)
    ]

    for title, desc, left, top, color in steps_act:
        c = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(2.4), Inches(2.1))
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_CARD_BG
        c.line.color.rgb = color
        c.line.width = Pt(2.0)

        # Header tag on card
        tag = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(2.4), Inches(0.4))
        tag.fill.solid()
        tag.fill.fore_color.rgb = color
        tag.line.fill.background()
        tag_tf = tag.text_frame
        tag_p = tag_tf.paragraphs[0]
        tag_p.text = title
        tag_p.font.size = Pt(10)
        tag_p.font.bold = True
        tag_p.font.color.rgb = COLOR_WHITE
        tag_p.alignment = PP_ALIGN.CENTER

        tb = s10.shapes.add_textbox(left + Inches(0.1), top + Inches(0.5), Inches(2.2), Inches(1.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================================
    # SLIDE 11: UML Activity Diagram (Doctor Schedule Management)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_background(s11)
    add_header(s11, "UML Working Activity Diagram: Doctor Consultation Workflow", "ACTIVITY WORKFLOW")

    doc_steps = [
        ("1. Doctor Registration", "Admin or Doctor registers credentials via /api/auth/register with ROLE_DOCTOR.", Inches(0.8), Inches(2.0), COLOR_PRIMARY),
        ("2. Profile Ingestion", "Doctor profile created in doctor_db with department, specialty, and fees.", Inches(3.9), Inches(2.0), COLOR_ACCENT),
        ("3. Configure Slots", "Doctor adds availability slots (Day of week, Start & End times) via /slots endpoint.", Inches(7.0), Inches(2.0), COLOR_SECONDARY),
        ("4. Redis Cache Updated", "Doctor catalog updated; Redis cache invalidated to reflect new availability.", Inches(10.1), Inches(2.0), COLOR_RED),
        ("5. Patient Discovers", "Patients filter doctors by department or specialization through API Gateway.", Inches(0.8), Inches(4.6), COLOR_SECONDARY),
        ("6. Slot Reservation", "Appointment reservation triggers slot booking lock (is_booked = true).", Inches(3.9), Inches(4.6), COLOR_PRIMARY),
        ("7. Consultation Held", "Doctor conducts consultation and updates patient clinical notes.", Inches(7.0), Inches(4.6), COLOR_ACCENT),
        ("8. Status Completed", "Appointment marked COMPLETED; records archived in PostgreSQL.", Inches(10.1), Inches(4.6), COLOR_GREEN)
    ]

    for title, desc, left, top, color in doc_steps:
        c = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(2.4), Inches(2.1))
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_CARD_BG
        c.line.color.rgb = color
        c.line.width = Pt(2.0)

        tag = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(2.4), Inches(0.4))
        tag.fill.solid()
        tag.fill.fore_color.rgb = color
        tag.line.fill.background()
        tag_tf = tag.text_frame
        tag_p = tag_tf.paragraphs[0]
        tag_p.text = title
        tag_p.font.size = Pt(10)
        tag_p.font.bold = True
        tag_p.font.color.rgb = COLOR_WHITE
        tag_p.alignment = PP_ALIGN.CENTER

        tb = s11.shapes.add_textbox(left + Inches(0.1), top + Inches(0.5), Inches(2.2), Inches(1.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================================
    # SLIDE 12: Sequence Diagram (End-to-End API Flow)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_background(s12)
    add_header(s12, "Sequence Diagram: End-to-End API Request Flow", "SEQUENCE ARCHITECTURE")

    # Swimlanes
    swimlanes = [
        ("Client", Inches(1.0)),
        ("API Gateway", Inches(3.4)),
        ("Auth Service", Inches(5.8)),
        ("Patient Service", Inches(8.2)),
        ("Doctor Service", Inches(10.6))
    ]

    for name, x in swimlanes:
        box = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.0), Inches(1.8), Inches(0.5))
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_PRIMARY
        box.line.fill.background()
        btf = box.text_frame
        bp = btf.paragraphs[0]
        bp.text = name
        bp.font.size = Pt(11)
        bp.font.bold = True
        bp.font.color.rgb = COLOR_WHITE
        bp.alignment = PP_ALIGN.CENTER

        # Vertical lifeline
        ll = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, x + Inches(0.88), Inches(2.6), Inches(0.04), Inches(4.3))
        ll.fill.solid()
        ll.fill.fore_color.rgb = RGBColor(203, 213, 225)
        ll.line.fill.background()

    # Sequence step annotations
    seq_steps = [
        ("1. POST /api/auth/login", Inches(1.0), Inches(3.4), Inches(2.9), COLOR_ACCENT),
        ("2. Authenticate & issue JWT", Inches(3.4), Inches(5.8), Inches(3.3), COLOR_SECONDARY),
        ("3. Return JWT Bearer token", Inches(1.0), Inches(3.4), Inches(3.7), COLOR_GREEN),
        ("4. POST /api/patients/ai/symptom-triage (Bearer Token)", Inches(1.0), Inches(3.4), Inches(4.3), COLOR_ACCENT),
        ("5. Validate JWT token signature", Inches(3.4), Inches(3.4), Inches(4.7), COLOR_PRIMARY),
        ("6. Forward request with X-Auth headers", Inches(3.4), Inches(8.2), Inches(5.1), COLOR_SECONDARY),
        ("7. Query doctors in department via Eureka", Inches(8.2), Inches(10.6), Inches(5.6), RGBColor(147, 51, 234)),
        ("8. Return Triage + Doctor recommendations to Client", Inches(1.0), Inches(8.2), Inches(6.2), COLOR_GREEN)
    ]

    for label, x_from, x_to, y, color in seq_steps:
        lbl_box = s12.shapes.add_textbox(min(x_from, x_to) + Inches(0.1), y - Inches(0.2), abs(x_to - x_from) + Inches(1.5), Inches(0.35))
        ltf = lbl_box.text_frame
        ltf.word_wrap = True
        lp = ltf.paragraphs[0]
        lp.text = label
        lp.font.size = Pt(9.5)
        lp.font.bold = True
        lp.font.color.rgb = color

    # =========================================================================
    # SLIDE 13: Comprehensive Test Suite & Test Case Matrix
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_background(s13)
    add_header(s13, "Microservices Test Cases & Verification Matrix", "TESTING & QUALITY ASSURANCE")

    # Table of Test Cases
    rows, cols = 7, 5
    left = Inches(0.8)
    top = Inches(1.8)
    width = Inches(11.7)
    height = Inches(5.0)

    table_shape = s13.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(1.2) # Test ID
    table.columns[1].width = Inches(2.2) # Service / Component
    table.columns[2].width = Inches(3.5) # Test Case Description
    table.columns[3].width = Inches(3.2) # Expected Result
    table.columns[4].width = Inches(1.6) # Status

    headers = ["Test ID", "Component", "Test Scenario", "Expected Outcome", "Status"]
    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    test_data = [
        ("TC-AUTH-01", "Auth Service", "Register new user with valid username & password", "HTTP 201 Created, returns JWT token and ROLE_PATIENT", "PASSED"),
        ("TC-AUTH-02", "Auth Service", "Login with invalid password", "HTTP 401 Unauthorized with error description", "PASSED"),
        ("TC-GW-01", "API Gateway", "Access /api/patients without Authorization header", "HTTP 401 Missing Authorization Header", "PASSED"),
        ("TC-GW-02", "API Gateway", "Access /api/doctors with valid Bearer JWT", "HTTP 200 OK, request forwarded with user headers", "PASSED"),
        ("TC-AI-01", "Patient Service (AI)", "Post severe chest pain symptoms to triage", "Urgency = EMERGENCY, Dept = Cardiology, ECG test suggested", "PASSED"),
        ("TC-CACHE-01", "Doctor Service (Redis)", "Query /api/doctors twice in succession", "1st call queries DB, 2nd call hits Redis (<5ms)", "PASSED")
    ]

    for row_idx, row_vals in enumerate(test_data, start=1):
        for col_idx, val in enumerate(row_vals):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_CARD_BG if row_idx % 2 == 0 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            if col_idx == 4:
                p.font.bold = True
                p.font.color.rgb = COLOR_GREEN
                p.alignment = PP_ALIGN.CENTER
            else:
                p.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================================
    # SLIDE 14: Docker Containerization & Orchestration
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_background(s14)
    add_header(s14, "Docker Containerization & Multi-Container Topology", "DEVOPS & DEPLOYMENT")

    add_card(s14, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), "Container Ecosystem", COLOR_SECONDARY)
    tb14_1 = s14.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(5.2), Inches(4.2))
    tf14_1 = tb14_1.text_frame
    tf14_1.word_wrap = True
    d_points = [
        ("postgres:15-alpine:", "\n• Dual database initialization (patient_db, doctor_db)\n• Healthcheck: pg_isready -U postgres"),
        ("redis:7-alpine:", "\n• Port 6379 in-memory distributed cache\n• Healthcheck: redis-cli ping"),
        ("service-registry:", "\n• Eureka server exposed at port 8761"),
        ("api-gateway, auth, patient, doctor:", "\n• Lightweight eclipse-temurin:17-jre-alpine images\n• Inter-connected via bridge network 'hospital-net'")
    ]
    for b_prefix, txt in d_points:
        p = tf14_1.add_paragraph()
        p.text = b_prefix + txt
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(8)

    add_card(s14, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), "Docker Compose Commands", COLOR_ACCENT)
    tb14_2 = s14.shapes.add_textbox(Inches(7.0), Inches(2.5), Inches(5.3), Inches(4.2))
    tf14_2 = tb14_2.text_frame
    tf14_2.word_wrap = True
    cmd_points = [
        ("# 1. Build & Spin up all containers:", "\ndocker-compose up --build -d"),
        ("# 2. Check cluster health status:", "\ndocker-compose ps"),
        ("# 3. View live microservice logs:", "\ndocker-compose logs -f patient-service"),
        ("# 4. Scale Patient Service to 3 instances:", "\ndocker-compose up --scale patient-service=3 -d"),
        ("# 5. Gracefully terminate ecosystem:", "\ndocker-compose down -v")
    ]
    for b_prefix, txt in cmd_points:
        p = tf14_2.add_paragraph()
        p.text = b_prefix + txt
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 15: Step-by-Step Eclipse IDE / STS Setup Guide
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_background(s15)
    add_header(s15, "Step-by-Step Eclipse IDE / STS Setup & Running Guide", "DEVELOPER WORKFLOW")

    steps_ecl = [
        ("Step 1: Open Eclipse / STS", "Launch Eclipse IDE for Enterprise Java or Spring Tool Suite (STS). Set your workspace location.", Inches(0.8), Inches(2.0), COLOR_PRIMARY),
        ("Step 2: Import Maven Projects", "Click File -> Import... -> Maven -> Existing Maven Projects. Browse to root project directory.", Inches(4.8), Inches(2.0), COLOR_SECONDARY),
        ("Step 3: Select All Submodules", "Check parent pom.xml and all 5 modules (service-registry, api-gateway, auth, doctor, patient). Click Finish.", Inches(8.8), Inches(2.0), COLOR_ACCENT),
        ("Step 4: Start Service Registry", "Locate ServiceRegistryApplication.java. Right click -> Run As -> Spring Boot App (or Java Application).", Inches(0.8), Inches(4.6), COLOR_SECONDARY),
        ("Step 5: Start Core Services", "Launch AuthServiceApplication, DoctorServiceApplication, and PatientServiceApplication in order.", Inches(4.8), Inches(4.6), COLOR_ACCENT),
        ("Step 6: Start API Gateway", "Launch ApiGatewayApplication. Open http://localhost:8761 to verify all services are UP in Eureka!", Inches(8.8), Inches(4.6), COLOR_GREEN)
    ]

    for title, desc, left, top, color in steps_ecl:
        c = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.7), Inches(2.2))
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_CARD_BG
        c.line.color.rgb = color
        c.line.width = Pt(1.8)

        tag = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(3.7), Inches(0.45))
        tag.fill.solid()
        tag.fill.fore_color.rgb = color
        tag.line.fill.background()
        tag_tf = tag.text_frame
        tag_p = tag_tf.paragraphs[0]
        tag_p.text = title
        tag_p.font.size = Pt(11)
        tag_p.font.bold = True
        tag_p.font.color.rgb = COLOR_WHITE
        tag_p.alignment = PP_ALIGN.CENTER

        tb = s15.shapes.add_textbox(left + Inches(0.15), top + Inches(0.6), Inches(3.4), Inches(1.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================================
    # SLIDE 16: Summary & Production Readiness
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_background(s16)
    add_header(s16, "Project Summary & Engineering Highlights", "CONCLUSION")

    add_card(s16, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), "Core Architecture Accomplishments", COLOR_SECONDARY)
    tb16_1 = s16.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(5.2), Inches(4.2))
    tf16_1 = tb16_1.text_frame
    tf16_1.word_wrap = True
    conc_points = [
        ("✔ Production-Ready Microservices:", " Decoupled microservices architecture adhering to cloud-native best practices."),
        ("✔ Integrated Spring AI Engine:", " Automated clinical decision support and dynamic specialist triage."),
        ("✔ Dual-Layer High Performance:", " Redis caching guarantees ultra-fast query times with automatic eviction."),
        ("✔ Zero-Trust Security:", " Centralized Spring Cloud Gateway with JJWT token signing and RBAC enforcement."),
        ("✔ Resilient Fallback Design:", " Database connection resilience and offline AI capabilities guarantee zero downtime.")
    ]
    for b_prefix, txt in conc_points:
        p = tf16_1.add_paragraph()
        p.text = b_prefix + txt
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(12)

    add_card(s16, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), "Future Enhancements Roadmap", COLOR_ACCENT)
    tb16_2 = s16.shapes.add_textbox(Inches(7.0), Inches(2.5), Inches(5.3), Inches(4.2))
    tf16_2 = tb16_2.text_frame
    tf16_2.word_wrap = True
    road_points = [
        ("1. Kafka Event Streaming:", " Publish appointment confirmation events to Apache Kafka for real-time patient notifications."),
        ("2. OpenTelemetry & Prometheus:", " Distributed tracing and Grafana dashboard integration for service latency monitoring."),
        ("3. Kubernetes Helm Charts:", " Deploy onto AWS EKS or GCP GKE with Horizontal Pod Autoscalers (HPA)."),
        ("4. Electronic Health Record (EHR) Sync:", " FHIR / HL7 standard compliance for hospital lab equipment interoperability.")
    ]
    for b_prefix, txt in road_points:
        p = tf16_2.add_paragraph()
        p.text = b_prefix + txt
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(12)

    # Output file
    output_filename = "hospital_microservices_presentation.pptx"
    prs.save(output_filename)
    print(f"Presentation saved successfully to: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    create_presentation()
