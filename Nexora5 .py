import streamlit as st

# ============================================================
# NEXORA
# AI SYSTEMS • DIGITAL INTELLIGENCE • SOFTWARE PRODUCTS
# Native Streamlit Edition
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

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html {
    scroll-behavior: smooth;
}

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 5%,
            rgba(99, 102, 241, 0.12),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 15%,
            rgba(14, 165, 233, 0.10),
            transparent 28%
        ),
        #070a10;
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

/* Text */

h1, h2, h3, h4, h5, h6 {
    color: #f8fafc !important;
}

p {
    color: #aab4c3;
    line-height: 1.75;
}

/* Header */

.nexora-logo {
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: #ffffff;
}

.nexora-logo span {
    color: #8b9cff;
}

.nexora-badge {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 999px;
    border: 1px solid rgba(139,156,255,.30);
    background: rgba(139,156,255,.07);
    color: #cbd2ff;
    font-size: .75rem;
    font-weight: 600;
}

/* Hero */

.hero-title {
    text-align: center;
    font-size: clamp(3rem, 7vw, 6rem);
    line-height: 1;
    font-weight: 800;
    letter-spacing: -0.055em;
    margin-top: 35px;
}

.hero-gradient {
    background: linear-gradient(
        100deg,
        #ffffff 10%,
        #9ca9ff 48%,
        #70d7ff 90%
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    max-width: 800px;
    margin: 25px auto 0 auto;
    text-align: center;
    color: #aeb8c8;
    font-size: 1.08rem;
    line-height: 1.8;
}

/* Section */

.section-label {
    color: #8d9cff;
    text-transform: uppercase;
    letter-spacing: .13em;
    font-size: .72rem;
    font-weight: 800;
    margin-top: 70px;
    margin-bottom: 8px;
}

.section-title {
    color: #f8fafc;
    font-size: 2.3rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    margin-bottom: 12px;
}

.section-description {
    max-width: 750px;
    color: #aab4c3;
    line-height: 1.8;
    margin-bottom: 30px;
}

/* Cards */

.card {
    height: 100%;
    padding: 28px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,.09);
    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,.055),
            rgba(255,255,255,.018)
        );
    box-shadow: 0 20px 60px rgba(0,0,0,.12);
}

.card-number {
    color: #8997ff;
    font-size: .76rem;
    font-weight: 800;
    letter-spacing: .10em;
    margin-bottom: 10px;
}

.card-icon {
    color: #9ba8ff;
    font-size: 1.55rem;
    margin-bottom: 15px;
}

.card-title {
    color: #f8fafc;
    font-size: 1.12rem;
    font-weight: 700;
    margin-bottom: 10px;
}

.card-text {
    color: #aab4c3;
    font-size: .90rem;
    line-height: 1.7;
}

/* Flagship */

.flagship-box {
    padding: 42px;
    border-radius: 24px;
    border: 1px solid rgba(139,156,255,.25);
    background:
        radial-gradient(
            circle at 80% 10%,
            rgba(100,116,255,.14),
            transparent 38%
        ),
        rgba(255,255,255,.025);
}

.flagship-tag {
    color: #aeb8ff;
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .12em;
    text-transform: uppercase;
}

.flagship-title {
    color: #ffffff;
    font-size: 2.35rem;
    font-weight: 800;
    margin-top: 10px;
    margin-bottom: 15px;
}

/* Pills */

.pill {
    display: inline-block;
    padding: 7px 11px;
    margin: 4px;
    border-radius: 999px;
    border: 1px solid rgba(139,156,255,.18);
    background: rgba(139,156,255,.08);
    color: #cbd2ff;
    font-size: .73rem;
}

/* Business model */

.metric {
    height: 100%;
    padding: 24px 15px;
    text-align: center;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,.08);
    background: rgba(255,255,255,.025);
}

.metric-title {
    color: #ffffff;
    font-weight: 800;
    font-size: 1rem;
}

.metric-text {
    color: #8994a6;
    font-size: .75rem;
    line-height: 1.5;
    margin-top: 8px;
}

/* Acquisition */

.acquisition-box {
    padding: 42px;
    border-radius: 24px;
    border: 1px solid rgba(139,156,255,.28);
    background:
        linear-gradient(
            135deg,
            rgba(139,156,255,.10),
            rgba(0,0,0,.05)
        );
}

.price-card {
    height: 100%;
    padding: 24px;
    text-align: center;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,.12);
    background: rgba(0,0,0,.18);
}

.price-label {
    color: #9da8b9;
    font-size: .70rem;
    font-weight: 700;
    letter-spacing: .10em;
    text-transform: uppercase;
}

.price-value {
    color: #ffffff;
    font-size: 1.9rem;
    font-weight: 800;
    margin: 7px 0;
}

.price-note {
    color: #727d8f;
    font-size: .73rem;
}

/* Contact */

.contact-box {
    padding: 35px;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,.09);
    background: rgba(255,255,255,.025);
}

/* Form */

div[data-testid="stForm"] {
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,.08);
    background: rgba(255,255,255,.018);
    padding: 25px;
}

div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stSelectbox"] label {
    color: #dce2ec !important;
}

div[data-baseweb="input"],
div[data-baseweb="textarea"],
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,.045) !important;
}

input,
textarea {
    color: #ffffff !important;
}

/* Button */

.stButton > button,
.stFormSubmitButton > button {
    border-radius: 10px !important;
    font-weight: 700 !important;
}

/* Footer */

.footer-line {
    margin-top: 80px;
    padding-top: 28px;
    border-top: 1px solid rgba(255,255,255,.08);
    color: #687386;
    font-size: .76rem;
    line-height: 1.7;
}

/* Mobile */

@media (max-width: 800px) {

    .hero-title {
        font-size: 3.1rem;
    }

    .section-title {
        font-size: 2rem;
    }

    .flagship-box,
    .acquisition-box,
    .contact-box {
        padding: 25px;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns([3, 1])

with header_left:
    st.markdown(
        """
        <div class="nexora-logo">
            NEX<span>ORA</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_right:
    st.markdown(
        """
        <div style="text-align:right;">
            <span class="nexora-badge">
                AI Systems • Digital Intelligence
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.divider()


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero-title">
        Build smarter.<br>
        <span class="hero-gradient">
            Operate intelligently.
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-description">
        Nexora builds AI-powered business systems, intelligent software
        products, and custom digital solutions designed to help
        organizations analyze, decide, automate, and execute with
        greater intelligence.
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

hero_a, hero_b, hero_c = st.columns([1, 1, 1])

with hero_b:

    button_a, button_b = st.columns(2)

    with button_a:
        if st.button(
            "Explore Flagship System",
            use_container_width=True,
        ):
            st.session_state["scroll_flagship"] = True

    with button_b:
        if st.button(
            "Work With Nexora",
            use_container_width=True,
        ):
            st.session_state["scroll_contact"] = True


# ============================================================
# WHAT NEXORA DOES
# ============================================================

st.markdown(
    '<div class="section-label">What Nexora Does</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">From business problems to intelligent systems.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        We combine artificial intelligence, software engineering,
        business intelligence, automation, and strategic system design
        to create practical technology for modern businesses.
    </div>
    """,
    unsafe_allow_html=True,
)


cards = [
    (
        "◈",
        "AI Systems",
        "Purpose-built AI systems designed around real business workflows and decision processes.",
    ),
    (
        "◇",
        "Custom Software",
        "Custom applications and business platforms built around specific client requirements.",
    ),
    (
        "△",
        "Digital Intelligence",
        "Systems for understanding markets, customers, competitors, operations, and business performance.",
    ),
    (
        "○",
        "AI Products",
        "Proprietary software products developed by Nexora for businesses and enterprise users.",
    ),
]

cols = st.columns(4)

for col, (icon, title, text) in zip(cols, cards):

    with col:

        st.markdown(
            f"""
            <div class="card">

                <div class="card-icon">
                    {icon}
                </div>

                <div class="card-title">
                    {title}
                </div>

                <div class="card-text">
                    {text}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# FLAGSHIP PRODUCT
# ============================================================

st.markdown(
    '<div id="flagship"></div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-label">Flagship Product</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="flagship-box">

        <div class="flagship-tag">
            Nexora Proprietary Technology
        </div>

        <div class="flagship-title">
            AI Business Operating System™
        </div>

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

        <div style="margin-top:20px;">

            <span class="pill">Business Intelligence</span>
            <span class="pill">Market Intelligence</span>
            <span class="pill">Customer Intelligence</span>
            <span class="pill">Competitive Intelligence</span>
            <span class="pill">Strategic Analysis</span>
            <span class="pill">Financial Analysis</span>
            <span class="pill">Risk Analysis</span>
            <span class="pill">Execution Planning</span>
            <span class="pill">AI Workflows</span>

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CORE CAPABILITIES
# ============================================================

st.markdown(
    '<div class="section-label">Core Capabilities</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">One system. Multiple layers of business intelligence.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        The platform is designed as a modular business intelligence
        and decision-support environment rather than a single-purpose
        AI tool.
    </div>
    """,
    unsafe_allow_html=True,
)


capabilities = [
    (
        "01",
        "Business DNA Analysis",
        "Analyze business identity, objectives, operating model, constraints, and strategic context.",
    ),
    (
        "02",
        "Market Intelligence",
        "Structure market, demand, opportunity, TAM/SAM/SOM, trends, and external intelligence.",
    ),
    (
        "03",
        "Customer Psychology",
        "Analyze customer needs, motivations, pain points, behavior, and buying dynamics.",
    ),
    (
        "04",
        "Competitive Intelligence",
        "Evaluate competitors, positioning, strengths, weaknesses, and market gaps.",
    ),
    (
        "05",
        "Opportunity Detection",
        "Identify strategic opportunities, gaps, threats, and potential growth directions.",
    ),
    (
        "06",
        "Financial Viability",
        "Evaluate economics, financial assumptions, viability, scenarios, and business risks.",
    ),
    (
        "07",
        "Risk Command",
        "Stress-test important assumptions and surface operational and strategic risks.",
    ),
    (
        "08",
        "Execution Blueprint",
        "Convert strategic conclusions into structured actions, priorities, and execution plans.",
    ),
]

cols = st.columns(4)

for i, (number, title, text) in enumerate(capabilities):

    with cols[i % 4]:

        st.markdown(
            f"""
            <div class="card" style="margin-bottom:18px;">

                <div class="card-number">
                    {number}
                </div>

                <div class="card-title">
                    {title}
                </div>

                <div class="card-text">
                    {text}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# OPERATING MODEL
# ============================================================

st.markdown(
    '<div class="section-label">Operating Model</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">From information to decisions.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        Nexora systems are designed around a structured progression
        from business context and evidence to analysis, validation,
        decisions, and execution.
    </div>
    """,
    unsafe_allow_html=True,
)


process = [
    (
        "01",
        "Understand",
        "Capture business context, objectives, constraints, and available evidence.",
    ),
    (
        "02",
        "Investigate",
        "Organize relevant business, market, customer, competitor, and financial intelligence.",
    ),
    (
        "03",
        "Analyze",
        "Evaluate available information through structured analytical frameworks.",
    ),
    (
        "04",
        "Validate",
        "Challenge assumptions, identify missing information, and stress-test conclusions.",
    ),
    (
        "05",
        "Decide",
        "Produce structured recommendations and decision-ready outputs.",
    ),
    (
        "06",
        "Execute",
        "Translate decisions into prioritized execution plans and measurable actions.",
    ),
]

cols = st.columns(3)

for i, (number, title, text) in enumerate(process):

    with cols[i % 3]:

        st.markdown(
            f"""
            <div class="card" style="margin-bottom:18px;">

                <div class="card-number">
                    {number}
                </div>

                <div class="card-title">
                    {title}
                </div>

                <div class="card-text">
                    {text}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# CUSTOM SOLUTIONS
# ============================================================

st.markdown(
    '<div class="section-label">Custom Solutions</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">Have a different problem?</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        Nexora also develops custom AI and software systems for
        organizations that need technology designed around their own
        workflows and requirements.
    </div>
    """,
    unsafe_allow_html=True,
)


services = [
    (
        "Custom AI Applications",
        "AI-powered applications designed for specific operational, analytical, or customer-facing requirements.",
    ),
    (
        "Business Automation",
        "Automate repetitive workflows, information processing, reporting, and internal business processes.",
    ),
    (
        "Decision Support Systems",
        "Build structured analytical systems that help teams evaluate complex business decisions.",
    ),
    (
        "Enterprise Dashboards",
        "Create intelligent dashboards and operational interfaces around business data and KPIs.",
    ),
    (
        "AI Agents & Workflows",
        "Design task-oriented AI workflows that connect reasoning with structured business processes.",
    ),
    (
        "Prototype to Product",
        "Transform a business concept or prototype into a deployable software product.",
    ),
]

cols = st.columns(3)

for i, (title, text) in enumerate(services):

    with cols[i % 3]:

        st.markdown(
            f"""
            <div class="card" style="margin-bottom:18px;">

                <div class="card-title">
                    {title}
                </div>

                <div class="card-text">
                    {text}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# BUSINESS MODEL
# ============================================================

st.markdown(
    '<div class="section-label">Nexora Business Model</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">Technology built for multiple commercial paths.</div>',
    unsafe_allow_html=True,
)

st.write("")


business_models = [
    (
        "Custom Projects",
        "Build systems for individual client requirements.",
    ),
    (
        "Ready-Made Products",
        "Sell proprietary systems developed by Nexora.",
    ),
    (
        "SaaS",
        "Offer products through recurring subscriptions.",
    ),
    (
        "Enterprise Licensing",
        "License technology to organizations.",
    ),
    (
        "IP Acquisition",
        "Transfer complete ownership of selected technology assets.",
    ),
]

cols = st.columns(5)

for col, (title, text) in zip(cols, business_models):

    with col:

        st.markdown(
            f"""
            <div class="metric">

                <div class="metric-title">
                    {title}
                </div>

                <div class="metric-text">
                    {text}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# STRATEGIC ACQUISITION
# ============================================================

st.markdown(
    '<div class="section-label">Strategic Acquisition</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="acquisition-box">

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
    """,
    unsafe_allow_html=True,
)


st.write("")

cols = st.columns(3)

with cols[0]:

    st.markdown(
        """
        <div class="price-card">

            <div class="price-label">
                Initial Asking Position
            </div>

            <div class="price-value">
                $150,000
            </div>

            <div class="price-note">
                USD · subject to negotiation and due diligence
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with cols[1]:

    st.markdown(
        """
        <div class="price-card">

            <div class="price-label">
                Transaction Scope
            </div>

            <div class="price-value">
                Full IP
            </div>

            <div class="price-note">
                Source code + proprietary technology + ownership
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with cols[2]:

    st.markdown(
        """
        <div class="price-card">

            <div class="price-label">
                Disclosure Model
            </div>

            <div class="price-value">
                NDA First
            </div>

            <div class="price-note">
                Detailed technical information provided during diligence
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


st.write("")

st.subheader("Why a strategic buyer may care")

st.write(
    "The system may be relevant to organizations looking to expand "
    "their enterprise AI, business intelligence, decision-support, "
    "automation, consulting, or software capabilities without "
    "developing an entire business-intelligence framework internally "
    "from the beginning."
)


# ============================================================
# TECHNOLOGY PHILOSOPHY
# ============================================================

st.markdown(
    '<div class="section-label">Technology Philosophy</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">Built around modular intelligence.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        Nexora products are designed to evolve through modular
        architecture, structured workflows, verification, knowledge
        integration, and continuous improvement.
    </div>
    """,
    unsafe_allow_html=True,
)


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
            <div class="card" style="margin-bottom:18px;padding:20px;">
                <div class="card-text" style="color:#d2d8e4;">
                    ✓ {item}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# ABOUT NEXORA
# ============================================================

st.markdown(
    '<div class="section-label">About Nexora</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">A product-driven technology company.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        Nexora is being developed around a simple idea:
        businesses should be able to access sophisticated technology
        without having to assemble every capability from scratch.
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="card">

        <p>
            Nexora combines custom software development with proprietary
            product development. The company is designed to serve
            organizations that need technology tailored to their
            specific business problems while also building reusable
            AI products that can operate independently at scale.
        </p>

        <p>
            Our long-term focus is on practical artificial intelligence:
            systems that help businesses understand information, make
            better decisions, automate work, and execute more effectively.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CONTACT
# ============================================================

st.markdown(
    '<div class="section-label">Contact Nexora</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="contact-box">

        <h2>
            Let's build something intelligent.
        </h2>

        <p>
            For custom software projects, enterprise AI solutions,
            product partnerships, or the strategic acquisition
            opportunity, contact Nexora.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CONTACT FORM
# ============================================================

with st.form("nexora_contact_form"):

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Name",
            placeholder="Your name",
        )

        company = st.text_input(
            "Company",
            placeholder="Company name",
        )

    with col2:

        email = st.text_input(
            "Business Email",
            placeholder="you@company.com",
        )

        inquiry_type = st.selectbox(
            "Inquiry Type",
            [
                "Custom AI / Software Project",
                "Enterprise Solution",
                "Product Partnership",
                "AI Business OS Acquisition",
                "Other",
            ],
        )

    message = st.text_area(
        "Message",
        height=150,
        placeholder="Tell us briefly what you are looking for.",
    )

    submitted = st.form_submit_button(
        "Submit Inquiry",
        type="primary",
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

st.markdown(
    """
    <div class="footer-line">

        <strong style="color:#dce2ec;">
            NEXORA
        </strong>

        <br>

        AI Systems • Digital Intelligence • Software Products

        <br><br>

        © 2026 Nexora. All rights reserved.

        <br><br>

        <strong>Important:</strong>
        Product capabilities, commercial terms, valuation,
        ownership, and acquisition information are subject to
        verification, due diligence, and definitive agreements.

    </div>
    """,
    unsafe_allow_html=True,
)
