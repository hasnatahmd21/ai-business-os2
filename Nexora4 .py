import streamlit as st

# ============================================================
# NEXORA
# AI SYSTEMS • DIGITAL INTELLIGENCE • SOFTWARE PRODUCTS
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

html {
    scroll-behavior: smooth;
}

* {
    font-family: 'Inter', sans-serif;
    box-sizing: border-box;
}

.stApp {
    background:
        radial-gradient(circle at 10% 5%, rgba(99,102,241,0.12), transparent 30%),
        radial-gradient(circle at 90% 15%, rgba(14,165,233,0.10), transparent 28%),
        #070a10;
    color: #f8fafc;
}

.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 5rem;
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

h1, h2, h3, h4, h5, h6 {
    color: #f8fafc !important;
}

p {
    color: #aab4c3;
    line-height: 1.75;
}

a {
    text-decoration: none !important;
}

/* ============================================================
   HEADER
   ============================================================ */

.nx-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0 25px 0;
    margin-bottom: 35px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

.nx-logo {
    font-size: 1.45rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: #ffffff;
}

.nx-logo span {
    color: #8b9cff;
}

.nx-badge {
    padding: 8px 14px;
    border-radius: 999px;
    border: 1px solid rgba(139,156,255,0.28);
    background: rgba(139,156,255,0.06);
    color: #cbd2ff;
    font-size: 0.76rem;
    font-weight: 600;
}

/* ============================================================
   HERO
   ============================================================ */

.nx-hero {
    text-align: center;
    padding: 60px 0 90px 0;
}

.nx-eyebrow {
    display: inline-block;
    padding: 8px 15px;
    margin-bottom: 25px;
    border-radius: 999px;
    border: 1px solid rgba(139,156,255,0.30);
    background: rgba(139,156,255,0.07);
    color: #b8c1ff;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.10em;
    text-transform: uppercase;
}

.nx-hero h1 {
    margin: 0 auto 25px auto;
    max-width: 1000px;
    font-size: clamp(3.2rem, 7vw, 6.3rem);
    line-height: 0.98;
    font-weight: 800;
    letter-spacing: -0.055em;
}

.nx-gradient {
    background: linear-gradient(
        100deg,
        #ffffff 10%,
        #9ca9ff 48%,
        #70d7ff 90%
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.nx-hero-copy {
    max-width: 790px;
    margin: 0 auto;
    color: #aeb8c8;
    font-size: 1.08rem;
    line-height: 1.8;
}

.nx-buttons {
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-top: 32px;
}

.nx-button-primary,
.nx-button-secondary {
    display: inline-block;
    padding: 14px 23px;
    border-radius: 10px;
    font-size: 0.88rem;
    font-weight: 700;
    transition: 0.2s ease;
}

.nx-button-primary {
    background: #f5f7fb;
    color: #071018 !important;
}

.nx-button-primary:hover {
    transform: translateY(-2px);
    background: #ffffff;
}

.nx-button-secondary {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.16);
    color: #e6eaff !important;
}

.nx-button-secondary:hover {
    transform: translateY(-2px);
    background: rgba(255,255,255,0.08);
}

/* ============================================================
   SECTIONS
   ============================================================ */

.nx-section {
    padding: 75px 0 25px 0;
}

.nx-label {
    color: #8d9cff;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    font-size: 0.72rem;
    font-weight: 800;
    margin-bottom: 10px;
}

.nx-title {
    color: #f8fafc;
    font-size: 2.35rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    margin-bottom: 14px;
}

.nx-copy {
    max-width: 730px;
    color: #aab4c3;
    line-height: 1.8;
}

/* ============================================================
   CARDS
   ============================================================ */

.nx-card {
    height: 100%;
    padding: 28px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.09);
    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.055),
            rgba(255,255,255,0.018)
        );
    box-shadow: 0 20px 60px rgba(0,0,0,0.13);
}

.nx-card-icon {
    font-size: 1.55rem;
    color: #9ba8ff;
    margin-bottom: 16px;
}

.nx-card h3 {
    font-size: 1.12rem;
    margin-bottom: 10px;
}

.nx-card p {
    font-size: 0.90rem;
    margin: 0;
}

/* ============================================================
   FLAGSHIP
   ============================================================ */

.nx-flagship {
    padding: 43px;
    margin-top: 25px;
    border-radius: 24px;
    border: 1px solid rgba(139,156,255,0.25);
    background:
        radial-gradient(
            circle at 80% 10%,
            rgba(100,116,255,0.14),
            transparent 36%
        ),
        rgba(255,255,255,0.025);
}

.nx-flagship-tag {
    color: #aeb8ff;
    font-size: 0.73rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.nx-flagship h2 {
    margin: 12px 0 15px 0;
    font-size: 2.35rem;
}

.nx-pill {
    display: inline-block;
    margin: 5px 5px 5px 0;
    padding: 7px 11px;
    border-radius: 999px;
    border: 1px solid rgba(139,156,255,0.18);
    background: rgba(139,156,255,0.08);
    color: #cbd2ff;
    font-size: 0.74rem;
}

/* ============================================================
   NUMBER
   ============================================================ */

.nx-number {
    color: #8997ff;
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    margin-bottom: 10px;
}

/* ============================================================
   BUSINESS MODEL
   ============================================================ */

.nx-metric {
    height: 100%;
    padding: 25px 16px;
    text-align: center;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.025);
}

.nx-metric-title {
    color: #ffffff;
    font-size: 1rem;
    font-weight: 800;
}

.nx-metric-text {
    color: #8994a6;
    font-size: 0.76rem;
    line-height: 1.5;
    margin-top: 7px;
}

/* ============================================================
   ACQUISITION
   ============================================================ */

.nx-acquisition {
    padding: 43px;
    border-radius: 24px;
    border: 1px solid rgba(139,156,255,0.28);
    background:
        linear-gradient(
            135deg,
            rgba(139,156,255,0.10),
            rgba(0,0,0,0.05)
        );
}

.nx-acquisition h2 {
    font-size: 2.2rem;
}

.nx-price {
    height: 100%;
    padding: 23px;
    text-align: center;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.12);
    background: rgba(0,0,0,0.18);
}

.nx-price-label {
    color: #9da8b9;
    font-size: 0.70rem;
    font-weight: 700;
    letter-spacing: 0.10em;
    text-transform: uppercase;
}

.nx-price-value {
    color: #ffffff;
    font-size: 1.9rem;
    font-weight: 800;
    margin: 6px 0;
}

.nx-price-note {
    color: #727d8f;
    font-size: 0.73rem;
}

/* ============================================================
   CONTACT
   ============================================================ */

.nx-contact {
    padding: 40px;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.09);
    background: rgba(255,255,255,0.025);
}

/* ============================================================
   STREAMLIT FORM
   ============================================================ */

div[data-testid="stForm"] {
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.018);
}

div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stSelectbox"] label {
    color: #dce2ec !important;
}

div[data-baseweb="input"],
div[data-baseweb="textarea"],
div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.045) !important;
    border-color: rgba(255,255,255,0.12) !important;
}

input,
textarea {
    color: #ffffff !important;
}

button[kind="primary"] {
    background: #f5f7fb !important;
    color: #071018 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
}

/* ============================================================
   FOOTER
   ============================================================ */

.nx-footer {
    margin-top: 90px;
    padding-top: 30px;
    border-top: 1px solid rgba(255,255,255,0.08);
    color: #687386;
    font-size: 0.76rem;
    line-height: 1.7;
}

/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 800px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .nx-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 14px;
    }

    .nx-hero {
        padding: 35px 0 60px 0;
    }

    .nx-hero h1 {
        font-size: 3.15rem;
    }

    .nx-hero-copy {
        font-size: 0.98rem;
    }

    .nx-title {
        font-size: 2rem;
    }

    .nx-flagship,
    .nx-acquisition,
    .nx-contact {
        padding: 25px;
    }

    .nx-flagship h2,
    .nx-acquisition h2 {
        font-size: 1.8rem;
    }

    .nx-button-primary,
    .nx-button-secondary {
        width: 100%;
        text-align: center;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="nx-header">
    <div class="nx-logo">
        NEX<span>ORA</span>
    </div>

    <div class="nx-badge">
        AI Systems • Digital Intelligence
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="nx-hero">

    <div class="nx-eyebrow">
        AI Systems & Digital Intelligence
    </div>

    <h1>
        Build smarter.<br>
        <span class="nx-gradient">
            Operate intelligently.
        </span>
    </h1>

    <div class="nx-hero-copy">
        Nexora builds AI-powered business systems, intelligent software
        products, and custom digital solutions designed to help
        organizations analyze, decide, automate, and execute with
        greater intelligence.
    </div>

    <div class="nx-buttons">
        <a class="nx-button-primary" href="#flagship">
            Explore Our Flagship System
        </a>

        <a class="nx-button-secondary" href="#contact">
            Work With Nexora
        </a>
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# WHAT NEXORA DOES
# ============================================================

st.markdown("""
<div class="nx-section">

    <div class="nx-label">
        What Nexora Does
    </div>

    <div class="nx-title">
        From business problems to intelligent systems.
    </div>

    <div class="nx-copy">
        We combine artificial intelligence, software engineering,
        business intelligence, automation, and strategic system design
        to create practical technology for modern businesses.
    </div>

</div>
""", unsafe_allow_html=True)


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

cols = st.columns(4)

for col, (icon, title, text) in zip(cols, cards):

    with col:
        st.markdown(f"""
        <div class="nx-card">
            <div class="nx-card-icon">{icon}</div>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# FLAGSHIP PRODUCT
# ============================================================

st.markdown("""
<div class="nx-section" id="flagship">

    <div class="nx-label">
        Flagship Product
    </div>

    <div class="nx-flagship">

        <div class="nx-flagship-tag">
            Nexora Proprietary Technology
        </div>

        <h2>
            AI Business Operating System™
        </h2>

        <p>
            An integrated business intelligence and decision-support
            system designed to help organizations understand their
            business environment, evaluate opportunities, analyze
            customers and competitors, assess financial and operational
            factors, and turn analysis into structured strategic action.
        </p>

        <p>
            The system is designed as a modular business intelligence
            environment rather than a single-purpose AI tool, bringing
            multiple analytical and strategic capabilities into one
            operating framework.
        </p>

        <div style="margin-top:22px;">
            <span class="nx-pill">Business Intelligence</span>
            <span class="nx-pill">Market Intelligence</span>
            <span class="nx-pill">Customer Intelligence</span>
            <span class="nx-pill">Competitive Intelligence</span>
            <span class="nx-pill">Strategic Analysis</span>
            <span class="nx-pill">Financial Analysis</span>
            <span class="nx-pill">Risk Analysis</span>
            <span class="nx-pill">Execution Planning</span>
            <span class="nx-pill">AI Workflows</span>
        </div>

    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# CORE CAPABILITIES
# ============================================================

st.markdown("""
<div class="nx-section">

    <div class="nx-label">
        Core Capabilities
    </div>

    <div class="nx-title">
        One system. Multiple layers of business intelligence.
    </div>

    <div class="nx-copy">
        The platform is designed as a modular business intelligence
        and decision-support environment rather than a single-purpose
        AI tool.
    </div>

</div>
""", unsafe_allow_html=True)


capabilities = [
    ("01", "Business DNA Analysis",
     "Analyze business identity, objectives, operating model, constraints, and strategic context."),

    ("02", "Market Intelligence",
     "Structure market, demand, opportunity, TAM/SAM/SOM, trends, and external intelligence."),

    ("03", "Customer Psychology",
     "Analyze customer needs, motivations, pain points, behavior, and buying dynamics."),

    ("04", "Competitive Intelligence",
     "Evaluate competitors, positioning, strengths, weaknesses, and market gaps."),

    ("05", "Opportunity Detection",
     "Identify strategic opportunities, gaps, threats, and potential growth directions."),

    ("06", "Financial Viability",
     "Evaluate economics, financial assumptions, viability, scenarios, and business risks."),

    ("07", "Risk Command",
     "Stress-test important assumptions and surface operational and strategic risks."),

    ("08", "Execution Blueprint",
     "Convert strategic conclusions into structured actions, priorities, and execution plans."),
]

cols = st.columns(4)

for i, (num, title, text) in enumerate(capabilities):

    with cols[i % 4]:
        st.markdown(f"""
        <div class="nx-card" style="margin-bottom:18px;">
            <div class="nx-number">{num}</div>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# OPERATING MODEL
# ============================================================

st.markdown("""
<div class="nx-section">

    <div class="nx-label">
        Operating Model
    </div>

    <div class="nx-title">
        From information to decisions.
    </div>

    <div class="nx-copy">
        Nexora systems are designed around a structured progression
        from business context and evidence to analysis, validation,
        decisions, and execution.
    </div>

</div>
""", unsafe_allow_html=True)


process = [
    ("01", "Understand",
     "Capture business context, objectives, constraints, and available evidence."),

    ("02", "Investigate",
     "Organize relevant business, market, customer, competitor, and financial intelligence."),

    ("03", "Analyze",
     "Evaluate the available information through structured analytical frameworks."),

    ("04", "Validate",
     "Challenge assumptions, identify missing information, and stress-test conclusions."),

    ("05", "Decide",
     "Produce structured recommendations and decision-ready outputs."),

    ("06", "Execute",
     "Translate decisions into prioritized execution plans and measurable actions."),
]

cols = st.columns(3)

for i, (num, title, text) in enumerate(process):

    with cols[i % 3]:
        st.markdown(f"""
        <div class="nx-card" style="margin-bottom:18px;">
            <div class="nx-number">{num}</div>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# CUSTOM SOLUTIONS
# ============================================================

st.markdown("""
<div class="nx-section">

    <div class="nx-label">
        Custom Solutions
    </div>

    <div class="nx-title">
        Have a different problem?
    </div>

    <div class="nx-copy">
        Nexora also develops custom AI and software systems for
        organizations that need technology designed around their own
        workflows and requirements.
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
        st.markdown(f"""
        <div class="nx-card" style="margin-bottom:18px;">
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# BUSINESS MODEL
# ============================================================

st.markdown("""
<div class="nx-section">

    <div class="nx-label">
        Nexora Business Model
    </div>

    <div class="nx-title">
        Technology built for multiple commercial paths.
    </div>

</div>
""", unsafe_allow_html=True)


business_models = [
    ("Custom Projects",
     "Build systems for individual client requirements."),

    ("Ready-Made Products",
     "Sell proprietary systems developed by Nexora."),

    ("SaaS",
     "Offer products through recurring subscriptions."),

    ("Enterprise Licensing",
     "License technology to organizations."),

    ("IP Acquisition",
     "Transfer complete ownership of selected technology assets."),
]

cols = st.columns(5)

for col, (title, text) in zip(cols, business_models):

    with col:
        st.markdown(f"""
        <div class="nx-metric">
            <div class="nx-metric-title">{title}</div>
            <div class="nx-metric-text">{text}</div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# STRATEGIC ACQUISITION
# ============================================================

st.markdown("""
<div class="nx-section" id="acquisition">

    <div class="nx-label">
        Strategic Acquisition
    </div>

    <div class="nx-acquisition">

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
            The contemplated transaction can include the complete
            software source code, associated intellectual property,
            documentation, deployment materials, and exclusive
            commercial ownership rights, subject to definitive
            agreements and due diligence.
        </p>

        <p>
            Detailed technical and proprietary information is not
            publicly disclosed and can be made available to qualified
            parties during an appropriate due-diligence process.
        </p>

    </div>

</div>
""", unsafe_allow_html=True)


cols = st.columns(3)

with cols[0]:
    st.markdown("""
    <div class="nx-price">
        <div class="nx-price-label">
            Initial Asking Position
        </div>

        <div class="nx-price-value">
            $150,000
        </div>

        <div class="nx-price-note">
            USD · subject to negotiation and due diligence
        </div>
    </div>
    """, unsafe_allow_html=True)

with cols[1]:
    st.markdown("""
    <div class="nx-price">
        <div class="nx-price-label">
            Transaction Scope
        </div>

        <div class="nx-price-value">
            Full IP
        </div>

        <div class="nx-price-note">
            Source code + proprietary technology + ownership
        </div>
    </div>
    """, unsafe_allow_html=True)

with cols[2]:
    st.markdown("""
    <div class="nx-price">
        <div class="nx-price-label">
            Disclosure Model
        </div>

        <div class="nx-price-value">
            NDA First
        </div>

        <div class="nx-price-note">
            Detailed technical information provided during diligence
        </div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div style="margin-top:40px;">

    <h3>
        Why a strategic buyer may care
    </h3>

    <p>
        The system may be relevant to organizations looking to expand
        their enterprise AI, business intelligence, decision-support,
        automation, consulting, or software capabilities without
        developing an entire business-intelligence framework internally
        from the beginning.
    </p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# TECHNOLOGY PHILOSOPHY
# ============================================================

st.markdown("""
<div class="nx-section">

    <div class="nx-label">
        Technology Philosophy
    </div>

    <div class="nx-title">
        Built around modular intelligence.
    </div>

    <div class="nx-copy">
        Nexora products are designed to evolve through modular
        architecture, structured workflows, verification, knowledge
        integration, and continuous improvement.
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
        st.markdown(f"""
        <div class="nx-card" style="margin-bottom:18px;padding:20px;">
            <p style="margin:0;color:#d2d8e4;">
                ✓ {item}
            </p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# ABOUT
# ============================================================

st.markdown("""
<div class="nx-section">

    <div class="nx-label">
        About Nexora
    </div>

    <div class="nx-title">
        A product-driven technology company.
    </div>

    <div class="nx-copy">
        Nexora is being developed around a simple idea:
        businesses should be able to access sophisticated technology
        without having to assemble every capability from scratch.
    </div>

</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="nx-card">

    <p>
        Nexora combines custom software development with proprietary
        product development. The company is designed to serve
        organizations that need technology tailored to their specific
        business problems while also building reusable AI products
        that can operate independently at scale.
    </p>

    <p>
        Our long-term focus is on practical artificial intelligence:
        systems that help businesses understand information, make
        better decisions, automate work, and execute more effectively.
    </p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# CONTACT
# ============================================================

st.markdown("""
<div class="nx-section" id="contact">

    <div class="nx-label">
        Contact Nexora
    </div>

    <div class="nx-contact">

        <h2>
            Let's build something intelligent.
        </h2>

        <p>
            For custom software projects, enterprise AI solutions,
            product partnerships, or the strategic acquisition
            opportunity, contact Nexora.
        </p>

    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# CONTACT FORM
# ============================================================

with st.form("nexora_contact_form"):

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Name",
            placeholder="Your name"
        )

        company = st.text_input(
            "Company",
            placeholder="Company name"
        )

    with col2:

        email = st.text_input(
            "Business Email",
            placeholder="you@company.com"
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
        height=150,
        placeholder="Tell us briefly what you are looking for."
    )

    submitted = st.form_submit_button(
        "Submit Inquiry",
        type="primary"
    )

    if submitted:

        if not name.strip() or not email.strip() or not message.strip():

            st.warning(
                "Please complete your name, business email, and message."
            )

        else:

            st.success(
                "Thank you. Your inquiry has been received."
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="nx-footer">

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
