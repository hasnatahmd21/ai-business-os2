import streamlit as st

# ============================================================
# NEXORA
# AI SYSTEMS • DIGITAL INTELLIGENCE • SOFTWARE PRODUCTS
# Professional Company Website
# ============================================================

st.set_page_config(
    page_title="Nexora | AI Systems & Digital Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(99,102,241,.10), transparent 28%),
        radial-gradient(circle at 85% 20%, rgba(14,165,233,.08), transparent 25%),
        #070a10;
    color: #f5f7fb;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 5rem;
}

h1, h2, h3, h4 {
    color: #f8fafc !important;
    letter-spacing: -0.035em;
}

p {
    color: #aab4c3;
    line-height: 1.75;
}

a {
    text-decoration: none !important;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* ============================================================
   HEADER
   ============================================================ */

.nexora-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0 28px 0;
    border-bottom: 1px solid rgba(255,255,255,.08);
    margin-bottom: 50px;
}

.brand {
    font-size: 1.45rem;
    font-weight: 800;
    letter-spacing: .08em;
    color: #ffffff;
}

.brand span {
    color: #8b9cff;
}

.header-badge {
    padding: 8px 14px;
    border: 1px solid rgba(139,156,255,.28);
    border-radius: 999px;
    color: #c9d1ff;
    font-size: .78rem;
    background: rgba(139,156,255,.06);
}

/* ============================================================
   HERO
   ============================================================ */

.hero {
    padding: 55px 0 75px 0;
    text-align: center;
}

.eyebrow {
    display: inline-block;
    padding: 8px 15px;
    border: 1px solid rgba(139,156,255,.30);
    background: rgba(139,156,255,.07);
    border-radius: 999px;
    color: #b8c1ff;
    font-size: .78rem;
    font-weight: 600;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin-bottom: 24px;
}

.hero h1 {
    font-size: clamp(3rem, 7vw, 6.2rem);
    line-height: .98;
    margin-bottom: 26px;
    font-weight: 800;
}

.hero h1 .gradient {
    background: linear-gradient(
        100deg,
        #ffffff 10%,
        #9ca9ff 48%,
        #70d7ff 90%
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-copy {
    max-width: 790px;
    margin: 0 auto;
    font-size: 1.13rem;
    color: #aeb8c8;
}

.cta-row {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 32px;
    flex-wrap: wrap;
}

.cta-primary,
.cta-secondary {
    display: inline-block;
    padding: 13px 23px;
    border-radius: 10px;
    font-weight: 700;
    font-size: .9rem;
}

.cta-primary {
    color: #071018 !important;
    background: #f5f7fb;
}

.cta-secondary {
    color: #e6eaff !important;
    border: 1px solid rgba(255,255,255,.16);
    background: rgba(255,255,255,.04);
}

/* ============================================================
   SECTIONS
   ============================================================ */

.section {
    padding: 80px 0 30px 0;
}

.section-label {
    color: #8d9cff;
    text-transform: uppercase;
    letter-spacing: .13em;
    font-size: .73rem;
    font-weight: 700;
    margin-bottom: 10px;
}

.section-title {
    font-size: 2.4rem;
    font-weight: 800;
    margin-bottom: 14px;
}

.section-copy {
    max-width: 720px;
    margin-bottom: 35px;
}

/* ============================================================
   CARDS
   ============================================================ */

.card {
    background: linear-gradient(
        145deg,
        rgba(255,255,255,.055),
        rgba(255,255,255,.018)
    );
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 18px;
    padding: 28px;
    height: 100%;
    box-shadow: 0 20px 60px rgba(0,0,0,.12);
}

.card-icon {
    font-size: 1.6rem;
    margin-bottom: 18px;
    color: #9ba8ff;
}

.card h3 {
    font-size: 1.18rem;
    margin-bottom: 10px;
}

.card p {
    font-size: .92rem;
    margin-bottom: 0;
}

/* ============================================================
   FLAGSHIP PRODUCT
   ============================================================ */

.flagship {
    border: 1px solid rgba(139,156,255,.24);
    background:
        radial-gradient(
            circle at 80% 10%,
            rgba(100,116,255,.13),
            transparent 35%
        ),
        rgba(255,255,255,.025);
    border-radius: 24px;
    padding: 42px;
    margin-top: 25px;
}

.flagship-tag {
    color: #aeb8ff;
    font-size: .75rem;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
}

.flagship h2 {
    font-size: 2.35rem;
    margin: 12px 0 15px;
}

.pill {
    display: inline-block;
    margin: 5px 5px 5px 0;
    padding: 7px 11px;
    border-radius: 999px;
    background: rgba(139,156,255,.08);
    border: 1px solid rgba(139,156,255,.17);
    color: #cbd2ff;
    font-size: .76rem;
}

/* ============================================================
   ACQUISITION
   ============================================================ */

.acquisition {
    background:
        linear-gradient(
            135deg,
            rgba(139,156,255,.10),
            rgba(0,0,0,.05)
        );
    border: 1px solid rgba(139,156,255,.28);
    border-radius: 24px;
    padding: 42px;
}

.acquisition h2 {
    font-size: 2.2rem;
}

.price-box {
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 16px;
    padding: 22px;
    background: rgba(0,0,0,.17);
    text-align: center;
}

.price-label {
    font-size: .73rem;
    text-transform: uppercase;
    letter-spacing: .11em;
    color: #9da8b9;
}

.price {
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
    margin-top: 6px;
}

/* ============================================================
   PROCESS
   ============================================================ */

.process-number {
    font-size: .78rem;
    font-weight: 800;
    color: #8997ff;
    letter-spacing: .1em;
}

/* ============================================================
   BUSINESS MODEL
   ============================================================ */

.metric-card {
    text-align: center;
    padding: 25px 15px;
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 16px;
    background: rgba(255,255,255,.025);
}

.metric-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: #ffffff;
}

.metric-label {
    color: #8994a6;
    font-size: .78rem;
    margin-top: 5px;
}

/* ============================================================
   CONTACT
   ============================================================ */

.contact-box {
    border: 1px solid rgba(255,255,255,.09);
    background: rgba(255,255,255,.025);
    border-radius: 22px;
    padding: 40px;
}

/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    border-top: 1px solid rgba(255,255,255,.08);
    margin-top: 90px;
    padding-top: 30px;
    color: #687386;
    font-size: .78rem;
}

.small-note {
    color: #727d8f;
    font-size: .76rem;
}

/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 800px) {

    .hero h1 {
        font-size: 3.1rem;
    }

    .flagship,
    .acquisition,
    .contact-box {
        padding: 25px;
    }

    .nexora-header {
        align-items: flex-start;
        gap: 15px;
        flex-direction: column;
    }
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="nexora-header">

    <div class="brand">
        NEX<span>ORA</span>
    </div>

    <div class="header-badge">
        AI Systems • Digital Intelligence
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown("""
<section class="hero">

    <div class="eyebrow">
        AI Systems & Digital Intelligence
    </div>

    <h1>
        Build smarter.<br>
        <span class="gradient">
            Operate intelligently.
        </span>
    </h1>

    <div class="hero-copy">
        Nexora builds AI-powered business systems, intelligent software
        products, and custom digital solutions designed to help organizations
        analyze, decide, automate, and execute with greater intelligence.
    </div>

    <div class="cta-row">

        <a class="cta-primary" href="#flagship">
            Explore Our Flagship System
        </a>

        <a class="cta-secondary" href="#contact">
            Work With Nexora
        </a>

    </div>

</section>
""", unsafe_allow_html=True)


# ============================================================
# WHAT NEXORA DOES
# ============================================================

st.markdown("""
<div class="section">

    <div class="section-label">
        What Nexora Does
    </div>

    <div class="section-title">
        From business problems to intelligent systems.
    </div>

    <div class="section-copy">
        We combine artificial intelligence, software engineering,
        business intelligence, automation, and strategic system design
        to create practical technology for modern businesses.
    </div>

</div>
""", unsafe_allow_html=True)


cols = st.columns(4)

cards = [
    (
        "◈",
        "AI Systems",
        "Purpose-built AI systems designed around real business workflows and decision processes."
    ),
    (
        "◇",
        "Custom Software",
        "Custom applications and business platforms built around specific client requirements."
    ),
    (
        "△",
        "Digital Intelligence",
        "Systems for understanding markets, customers, competitors, operations, and business performance."
    ),
    (
        "○",
        "AI Products",
        "Proprietary software products developed by Nexora for businesses and enterprise users."
    ),
]

for col, (icon, title, text) in zip(cols, cards):

    with col:

        st.markdown(
            f"""
            <div class="card">

                <div class="card-icon">
                    {icon}
                </div>

                <h3>
                    {title}
                </h3>

                <p>
                    {text}
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# FLAGSHIP PRODUCT
# ============================================================

st.markdown("""
<div class="section" id="flagship">

    <div class="section-label">
        Flagship Product
    </div>

    <div class="flagship">

        <div class="flagship-tag">
            Nexora Proprietary Technology
        </div>

        <h2>
            AI Business Operating System™
        </h2>

        <p>
            An integrated business intelligence and decision-support system
            designed to help organizations understand their business
            environment, evaluate opportunities, analyze customers and
            competitors, assess financial and operational factors, and turn
            analysis into structured strategic action.
        </p>

        <p>
            The system is designed as a modular business intelligence
            environment rather than a single-purpose AI tool, bringing
            multiple analytical and strategic capabilities into one
            operating framework.
        </p>

        <div style="margin-top:22px;">

            <span class="pill">
                Business Intelligence
            </span>

            <span class="pill">
                Market Intelligence
            </span>

            <span class="pill">
                Customer Intelligence
            </span>

            <span class="pill">
                Competitive Intelligence
            </span>

            <span class="pill">
                Strategic Analysis
            </span>

            <span class="pill">
                Financial Analysis
            </span>

            <span class="pill">
                Risk Analysis
            </span>

            <span class="pill">
                Execution Planning
            </span>

            <span class="pill">
                AI Workflows
            </span>

        </div>

    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# CORE CAPABILITIES
# ============================================================

st.markdown("""
<div class="section">

    <div class="section-label">
        Core Capabilities
    </div>

    <div class="section-title">
        One system. Multiple layers of business intelligence.
    </div>

    <div class="section-copy">
        The platform is designed as a modular business intelligence
        and decision-support environment rather than a single-purpose
        AI tool.
    </div>

</div>
""", unsafe_allow_html=True)


capabilities = [

    (
        "01",
        "Business DNA Analysis",
        "Analyze business identity, objectives, operating model, constraints, and strategic context."
    ),

    (
        "02",
        "Market Intelligence",
        "Structure market, demand, opportunity, TAM/SAM/SOM, trends, and external intelligence."
    ),

    (
        "03",
        "Customer Psychology",
        "Analyze customer needs, motivations, pain points, behavior, and buying dynamics."
    ),

    (
        "04",
        "Competitive Intelligence",
        "Evaluate competitors, positioning, strengths, weaknesses, and market gaps."
    ),

    (
        "05",
        "Opportunity Detection",
        "Identify strategic opportunities, gaps, threats, and potential growth directions."
    ),

    (
        "06",
        "Financial Viability",
        "Evaluate economics, financial assumptions, viability, scenarios, and business risks."
    ),

    (
        "07",
        "Risk Command",
        "Stress-test important assumptions and surface operational and strategic risks."
    ),

    (
        "08",
        "Execution Blueprint",
        "Convert strategic conclusions into structured actions, priorities, and execution plans."
    ),
]


cols = st.columns(4)

for i, (num, title, text) in enumerate(capabilities):

    with cols[i % 4]:

        st.markdown(
            f"""
            <div class="card" style="margin-bottom:18px;">

                <div class="process-number">
                    {num}
                </div>

                <h3>
                    {title}
                </h3>

                <p>
                    {text}
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# OPERATING MODEL
# ============================================================

st.markdown("""
<div class="section">

    <div class="section-label">
        Operating Model
    </div>

    <div class="section-title">
        From information to decisions.
    </div>

    <div class="section-copy">
        Nexora systems are designed around a structured progression from
        business context and evidence to analysis, validation, decisions,
        and execution.
    </div>

</div>
""", unsafe_allow_html=True)


process = [

    (
        "01",
        "Understand",
        "Capture business context, objectives, constraints, and available evidence."
    ),

    (
        "02",
        "Investigate",
        "Organize relevant business, market, customer, competitor, and financial intelligence."
    ),

    (
        "03",
        "Analyze",
        "Evaluate the available information through structured analytical frameworks."
    ),

    (
        "04",
        "Validate",
        "Challenge assumptions, identify missing information, and stress-test conclusions."
    ),

    (
        "05",
        "Decide",
        "Produce structured recommendations and decision-ready outputs."
    ),

    (
        "06",
        "Execute",
        "Translate decisions into prioritized execution plans and measurable actions."
    ),
]


cols = st.columns(3)

for i, (num, title, text) in enumerate(process):

    with cols[i % 3]:

        st.markdown(
            f"""
            <div class="card" style="margin-bottom:18px;">

                <div class="process-number">
                    {num}
                </div>

                <h3>
                    {title}
                </h3>

                <p>
                    {text}
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# CUSTOM SOLUTIONS
# ============================================================

st.markdown("""
<div class="section">

    <div class="section-label">
        Custom Solutions
    </div>

    <div class="section-title">
        Have a different problem?
    </div>

    <div class="section-copy">
        Nexora also develops custom AI and software systems for organizations
        that need technology designed around their own workflows and
        requirements.
    </div>

</div>
""", unsafe_allow_html=True)


services = [

    (
        "Custom AI Applications",
        "AI-powered applications designed for specific operational, analytical, or customer-facing requirements."
    ),

    (
        "Business Automation",
        "Automate repetitive workflows, information processing, reporting, and internal business processes."
    ),

    (
        "Decision Support Systems",
        "Build structured analytical systems that help teams evaluate complex business decisions."
    ),

    (
        "Enterprise Dashboards",
        "Create intelligent dashboards and operational interfaces around business data and KPIs."
    ),

    (
        "AI Agents & Workflows",
        "Design task-oriented AI workflows that connect reasoning with structured business processes."
    ),

    (
        "Prototype to Product",
        "Transform a business concept or prototype into a deployable software product."
    ),
]


cols = st.columns(3)

for i, (title, text) in enumerate(services):

    with cols[i % 3]:

        st.markdown(
            f"""
            <div class="card" style="margin-bottom:18px;">

                <h3>
                    {title}
                </h3>

                <p>
                    {text}
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# NEXORA BUSINESS MODEL
# ============================================================

st.markdown("""
<div class="section">

    <div class="section-label">
        Nexora Business Model
    </div>

    <div class="section-title">
        Technology built for multiple commercial paths.
    </div>

</div>
""", unsafe_allow_html=True)


cols = st.columns(5)

business_models = [

    (
        "Custom Projects",
        "Build systems for individual client requirements."
    ),

    (
        "Ready-Made Products",
        "Sell proprietary systems developed by Nexora."
    ),

    (
        "SaaS",
        "Offer products through recurring subscriptions."
    ),

    (
        "Enterprise Licensing",
        "License technology to organizations."
    ),

    (
        "IP Acquisition",
        "Transfer complete ownership of selected technology assets."
    ),
]


for col, (title, text) in zip(cols, business_models):

    with col:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-value"
                     style="font-size:1.05rem;">
                    {title}
                </div>

                <div class="metric-label">
                    {text}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# STRATEGIC ACQUISITION
# ============================================================

st.markdown("""
<div class="section" id="acquisition">

    <div class="section-label">
        Strategic Acquisition
    </div>

    <div class="acquisition">

        <h2>
            AI Business Operating System™
        </h2>

        <p>
            Nexora is open to discussing a strategic acquisition of the
            AI Business Operating System™ with a qualified technology
            company, enterprise software provider, AI organization,
            consulting group, or strategic investor.
        </p>

        <p>
            The contemplated transaction can include the complete software
            source code, associated intellectual property, documentation,
            deployment materials, and exclusive commercial ownership rights,
            subject to definitive agreements and due diligence.
        </p>

        <p>
            Detailed technical and proprietary information is not publicly
            disclosed and can be made available to qualified parties during
            an appropriate due-diligence process.
        </p>

    </div>

</div>
""", unsafe_allow_html=True)


cols = st.columns(3)

with cols[0]:

    st.markdown("""
    <div class="price-box">

        <div class="price-label">
            Initial Asking Position
        </div>

        <div class="price">
            $150,000
        </div>

        <div class="small-note">
            USD · subject to negotiation and due diligence
        </div>

    </div>
    """, unsafe_allow_html=True)


with cols[1]:

    st.markdown("""
    <div class="price-box">

        <div class="price-label">
            Transaction Scope
        </div>

        <div class="price">
            Full IP
        </div>

        <div class="small-note">
            Source code + proprietary technology + ownership
        </div>

    </div>
    """, unsafe_allow_html=True)


with cols[2]:

    st.markdown("""
    <div class="price-box">

        <div class="price-label">
            Disclosure Model
        </div>

        <div class="price">
            NDA First
        </div>

        <div class="small-note">
            Detailed technical information provided during diligence
        </div>

    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div style="margin-top:35px;">

<h3>
Why a strategic buyer may care
</h3>

<p>
The system may be relevant to organizations looking to expand their
enterprise AI, business intelligence, decision-support, automation,
consulting, or software capabilities without developing an entire
business-intelligence framework internally from the beginning.
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# TECHNOLOGY PHILOSOPHY
# ============================================================

st.markdown("""
<div class="section">

    <div class="section-label">
        Technology Philosophy
    </div>

    <div class="section-title">
        Built around modular intelligence.
    </div>

    <div class="section-copy">
        Nexora products are designed to evolve through modular architecture,
        structured workflows, verification, knowledge integration, and
        continuous improvement.
    </div>

</div>
""", unsafe_allow_html=True)


tech_items = [

    "Modular software architecture",
    "Structured AI workflows",
    "Business intelligence frameworks",
    "Verification and quality-control layers",
    "Knowledge and retrieval components",
    "Data-driven analysis",
    "Security and governance considerations",
    "Deployable application interfaces",

]


cols = st.columns(4)

for i, item in enumerate(tech_items):

    with cols[i % 4]:

        st.markdown(
            f"""
            <div class="card"
                 style="margin-bottom:18px; padding:20px;">

                <p style="margin:0; color:#d2d8e4;">
                    ✓ {item}
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# ABOUT NEXORA
# ============================================================

st.markdown("""
<div class="section">

    <div class="section-label">
        About Nexora
    </div>

    <div class="section-title">
        A product-driven technology company.
    </div>

    <div class="section-copy">
        Nexora is being developed around a simple idea:
        businesses should be able to access sophisticated technology
        without having to assemble every capability from scratch.
    </div>

</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="card">

    <p>
        Nexora combines custom software development with proprietary
        product development. The company is designed to serve organizations
        that need technology tailored to their specific business problems
        while also building reusable AI products that can operate
        independently at scale.
    </p>

    <p>
        Our long-term focus is on practical artificial intelligence:
        systems that help businesses understand information, make better
        decisions, automate work, and execute more effectively.
    </p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# CONTACT
# ============================================================

st.markdown("""
<div class="section" id="contact">

    <div class="section-label">
        Contact Nexora
    </div>

    <div class="contact-box">

        <h2>
            Let's build something intelligent.
        </h2>

        <p>
            For custom software projects, enterprise AI solutions,
            product partnerships, or the strategic acquisition opportunity,
            contact Nexora.
        </p>

    </div>

</div>
""", unsafe_allow_html=True)


with st.form("contact_form"):

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Name"
        )

        company = st.text_input(
            "Company"
        )

    with col2:

        email = st.text_input(
            "Business Email"
        )

        inquiry_type = st.selectbox(
            "Inquiry Type",
            [
                "Custom AI / Software Project",
                "Enterprise Solution",
                "Product Partnership",
                "AI Business OS Acquisition",
                "Other"
            ]
        )

    message = st.text_area(
        "Message",
        height=140,
        placeholder="Tell us briefly what you are looking for."
    )

    submitted = st.form_submit_button(
        "Submit Inquiry"
    )

    if submitted:

        if not name or not email or not message:

            st.warning(
                "Please complete your name, email, and message."
            )

        else:

            st.success(
                "Thank you. Your inquiry has been received. "
                "Connect this form to your preferred email or CRM "
                "backend before publishing the website publicly."
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

    <div style="
        display:flex;
        justify-content:space-between;
        gap:20px;
        flex-wrap:wrap;
    ">

        <div>
            <strong style="color:#dce2ec;">
                NEXORA
            </strong>
            <br>
            AI Systems • Digital Intelligence • Software Products
        </div>

        <div>
            © 2026 Nexora. All rights reserved.
        </div>

    </div>

    <div style="margin-top:20px;">

        <strong>Important:</strong>
        Product capabilities, commercial terms, valuation,
        ownership, and acquisition information are subject to
        verification, due diligence, and definitive agreements.

    </div>

</div>
""", unsafe_allow_html=True)
