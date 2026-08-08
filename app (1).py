import os
import streamlit as st
import pandas as pd

try:
    import google.generativeai as genai
except ImportError:
    genai = None

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="AI Business OS™", page_icon="⚙️", layout="wide")

# Initialize Session State for Pipeline Data
if "pipeline_data" not in st.session_state:
    st.session_state.pipeline_data = pd.DataFrame([
        {"Company": "TechFlow Inc", "Stage": "Negotiate", "Value ($)": 15000, "Next Action": "Send revised proposal"},
        {"Company": "ViralCart", "Stage": "Validate", "Value ($)": 8500, "Next Action": "Discovery Call"},
        {"Company": "Apex SaaS", "Stage": "Engage", "Value ($)": 22000, "Next Action": "Follow-up email"},
        {"Company": "Global Logistics", "Stage": "Unify", "Value ($)": 45000, "Next Action": "Contract signing"}
    ])

# Helper Function for Gemini AI Execution
def run_ai_task(api_key, prompt_text):
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API Key in the sidebar or check 'Use Demo Output'.")
        return None
    if genai is None:
        st.error("❌ google-generativeai library is missing. Please check requirements.txt.")
        return None
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None

# ==========================================
# 2. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("⚙️ AI Business OS™")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Select Module",
    [
        "📊 Executive Dashboard", 
        "📝 P.R.O.M.P.T. Engineer", 
        "📈 Sales Pipeline",
        "⚡ AI Execution Systems™ (Part 3)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔑 AI Settings")

default_key = os.getenv("GEMINI_API_KEY", "")
api_key = st.sidebar.text_input(
    "Gemini API Key", 
    value=default_key,
    type="password", 
    help="Google AI Studio se free API key (aistudio.google.com)"
)
use_demo = st.sidebar.checkbox("Use Demo Output (Without API Key)", value=False)

# ==========================================
# 3. EXECUTIVE DASHBOARD
# ==========================================
if menu == "📊 Executive Dashboard":
    st.title("📊 Executive Decision System™")
    st.caption("Track your E.X.E.C.U.T.E.™ Framework metrics.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Monthly Revenue", "$45,500", "+12%")
    col2.metric("Active Clients", "124", "+4 new")
    col3.metric("Lead Conversion", "18%", "-2%")
    col4.metric("AI Hours Saved", "320 hrs", "+45 hrs")
    
    st.markdown("### 📈 Revenue Trends")
    chart_data = pd.DataFrame(
        {"Revenue": [30000, 32000, 38000, 41000, 45500], "Expenses": [15000, 16000, 18000, 19000, 21000]},
        index=["Jan", "Feb", "Mar", "Apr", "May"]
    )
    st.line_chart(chart_data)

# ==========================================
# 4. P.R.O.M.P.T. ENGINEER
# ==========================================
elif menu == "📝 P.R.O.M.P.T. Engineer":
    st.title("📝 Premium Prompt Engineering System™")
    st.caption("Build strategic, context-aware prompts for enterprise workflows.")
    
    with st.form("prompt_builder"):
        p_purpose = st.text_input("Purpose / Business Objective", placeholder="e.g., Generate qualified B2B leads")
        r_role = st.text_input("Role", placeholder="e.g., Senior SaaS CMO")
        o_objective = st.text_input("Objective", placeholder="e.g., Write high-converting LinkedIn ad copy")
        submitted = st.form_submit_button("🚀 Generate Enterprise Prompt")
        
        if submitted:
            final_prompt = f"Act As: {r_role}\nBusiness Objective: {p_purpose}\nTask: {o_objective}\nProvide structured output with rationale."
            st.subheader("Generated Prompt Architecture:")
            st.code(final_prompt, language="markdown")

# ==========================================
# 5. SALES PIPELINE
# ==========================================
elif menu == "📈 Sales Pipeline":
    st.title("📈 AI Sales Operating System™")
    st.dataframe(st.session_state.pipeline_data, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 🤖 Live AI Sales Assistant")
    user_prompt = st.text_area("Ask AI to draft emails or research deals:", placeholder="Draft a follow-up email for ViralCart...")
    
    if st.button("🚀 Run Sales AI"):
        if use_demo:
            st.success("✅ Demo Response:")
            st.markdown("Subject: ViralCart Project Update\n\nHi ViralCart Team,\nFollowing up on our discovery call. Let's schedule a 15-min alignment session.")
        else:
            context = st.session_state.pipeline_data.to_string(index=False)
            full_query = f"Pipeline Context:\n{context}\n\nTask: {user_prompt}"
            output = run_ai_task(api_key, full_query)
            if output:
                st.success("✅ Output Generated:")
                st.markdown(output)

# ==========================================
# 6. AI EXECUTION SYSTEMS™ (PART 3)
# ==========================================
elif menu == "⚡ AI Execution Systems™ (Part 3)":
    st.title("⚡ AI Execution Systems Library™")
    st.caption("Practical operational systems to implement inside real businesses.")
    
    system_choice = st.selectbox(
        "Choose Execution System Module:",
        [
            "System 1 — AI Content Production System™ (C.O.N.T.E.N.T.™)",
            "System 2 — AI SEO Growth System™ (S.E.A.R.C.H.™)",
            "System 3 — AI Social Media OS™ (S.O.C.I.A.L.™)",
            "System 4 — AI Customer Support OS™ (C.A.R.E.™)",
            "System 5 — AI E-commerce Growth OS™ (S.H.O.P.™)",
            "System 6 — AI Agency Operating System™ (A.G.E.N.C.Y.™)",
            "System 7 — AI Executive Assistant OS™ (E.X.E.C.™)",
            "System 8 — AI HR & Recruitment OS™ (H.I.R.E.™)",
            "System 9 — AI Finance & BI OS™ (F.I.N.A.N.C.E.™)",
            "System 10 — AI Product & Innovation OS™ (I.N.N.O.V.A.T.E.™)"
        ]
    )
    
    st.markdown("---")
    
    # ----------------------------------------------------
    # SYSTEM 1: CONTENT PRODUCTION
    # ----------------------------------------------------
    if "System 1" in system_choice:
        st.subheader("System 1: AI Content Production System™")
        st.markdown("""
        **Framework:** `C.O.N.T.E.N.T.™`
        * **C**ustomer Intelligence | **O**bjective Definition | **N**arrative Development | **T**emplate Creation | **E**xecution Workflow | **N**etwork Distribution | **T**esting & Analytics
        """)
        
        st.markdown("#### 🤖 Run Content Engine")
        c_topic = st.text_input("Enter Content Topic/Product:", placeholder="e.g., AI Business Automation Tools")
        c_format = st.selectbox("Format:", ["Educational Post", "Product Launch Copy", "Case Study", "Video Script Narrative"])
        
        if st.button("Generate Content Asset"):
            if use_demo:
                st.success("✅ Demo Content Asset Generated:")
                st.markdown(f"**Hook:** Stop wasting 20+ hours on manual reporting.\n\n**Narrative:** Modern businesses use AI systems to streamline workflows...\n\n**Call to Action:** Try our AI Business OS today!")
            else:
                prompt = f"Act as AI Content Strategist. Create a high-converting {c_format} on '{c_topic}' using the C.O.N.T.E.N.T.™ narrative formula."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # ----------------------------------------------------
    # SYSTEM 2: SEO GROWTH
    # ----------------------------------------------------
    elif "System 2" in system_choice:
        st.subheader("System 2: AI SEO Growth System™")
        st.markdown("""
        **Framework:** `S.E.A.R.C.H.™`
        * **S**earch Intelligence | **E**valuate Intent | **A**rchitecture Planning | **R**esearch & Optimization | **C**ontent Pipeline | **H**olistic Loop
        """)
        
        s_keyword = st.text_input("Enter Focus Keyword:", placeholder="e.g., best AI software for e-commerce")
        if st.button("Generate SEO Content Brief"):
            if use_demo:
                st.success("✅ Demo SEO Brief Generated:")
                st.markdown("### Focus Keyword: best AI software for e-commerce\n* **Search Intent:** Commercial/Transactional\n* **Pillar Page:** Ultimate E-commerce AI Guide\n* **Recommended Headings:** H2 Key Features, H2 Cost Comparison, H2 ROI")
            else:
                prompt = f"Act as AI SEO Strategist. Generate a complete SEO Content Brief for keyword '{s_keyword}' following S.E.A.R.C.H.™ principles."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # ----------------------------------------------------
    # SYSTEM 3: SOCIAL MEDIA OS
    # ----------------------------------------------------
    elif "System 3" in system_choice:
        st.subheader("System 3: AI Social Media Operating System™")
        st.markdown("""
        **Framework:** `S.O.C.I.A.L.™`
        * **S**trategy Foundation | **O**bserve Audience | **C**ontent Pillar System | **I**ntelligent Production | **A**udience Engagement | **L**earning & Optimization
        """)
        
        sm_pillar = st.selectbox("Select Pillar:", ["Educational", "Authority", "Trust/Behind-Scenes", "Engagement/Poll", "Conversion Offer"])
        sm_platform = st.selectbox("Platform:", ["LinkedIn", "Instagram Carousel", "X (Twitter) Thread", "TikTok Script"])
        
        if st.button("Generate Social Campaign"):
            if use_demo:
                st.success("✅ Demo Campaign Output:")
                st.markdown(f"**[{sm_platform} - {sm_pillar}]**\n📌 *Slide 1:* 5 AI hacks every founder needs.\n📌 *Slide 2:* How ViralCart scaled 300%...\n📌 *CTA:* Comment 'SYSTEM' for access.")
            else:
                prompt = f"Act as Social Media Director. Create a high-engagement {sm_platform} asset for pillar '{sm_pillar}'."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # ----------------------------------------------------
    # SYSTEM 4: CUSTOMER SUPPORT OS
    # ----------------------------------------------------
    elif "System 4" in system_choice:
        st.subheader("System 4: AI Customer Support OS™")
        st.markdown("""
        **Framework:** `C.A.R.E.™`
        * **C**apture Knowledge | **A**ssist Customers | **R**esolve Issues | **E**nhance Experience
        """)
        
        ticket_text = st.text_area("Paste Support Inquiry / Ticket:", placeholder="My order hasn't arrived yet and I need a refund immediately...")
        if st.button("Generate Empathetic Resolution"):
            if use_demo:
                st.success("✅ Demo Support Response:")
                st.markdown("Hello! I deeply apologize for the shipping delay. I've checked your tracking and prioritized your ticket with dispatch. Here is your tracking link: ...")
            else:
                prompt = f"Act as AI Customer Care Specialist. Draft a empathetic, brand-aligned resolution response for this ticket: '{ticket_text}'"
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # ----------------------------------------------------
    # SYSTEM 5: E-COMMERCE GROWTH OS
    # ----------------------------------------------------
    elif "System 5" in system_choice:
        st.subheader("System 5: AI E-commerce Growth OS™")
        st.markdown("""
        **Framework:** `S.H.O.P.™`
        * **S**tore Intelligence | **H**igh-Value Product Strategy | **O**ptimization Engine | **P**erformance Scaling
        """)
        
        p_name = st.text_input("Product Name:", placeholder="e.g., Ergonomic Smart Desk Lamp")
        if st.button("Generate High-Converting Product Page Copy"):
            if use_demo:
                st.success("✅ Demo Product Copy:")
                st.markdown("### Ergonomic Smart Desk Lamp\n**Problem:** Eye strain during late-night work.\n**Solution:** Auto-adjusting natural circadian lighting.\n**Call To Action:** Order now for 20% off!")
            else:
                prompt = f"Act as E-commerce Conversion Specialist. Create a high-converting product description for '{p_name}' including Problem, Solution, Benefits, Trust, Action."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # ----------------------------------------------------
    # SYSTEM 6: AGENCY OS
    # ----------------------------------------------------
    elif "System 6" in system_choice:
        st.subheader("System 6: AI Agency Operating System™")
        st.markdown("""
        **Framework:** `A.G.E.N.C.Y.™`
        * **A**ttract | **G**enerate | **E**ngage & Close | **N**avigate Delivery | **C**reate Client Success | **Y**ield & Scale
        """)
        
        client_type = st.text_input("Client Industry / Profile:", placeholder="e.g., E-commerce fashion brand doing $50k/mo")
        if st.button("Generate Agency Proposal Outline"):
            if use_demo:
                st.success("✅ Demo Agency Proposal:")
                st.markdown("### Growth Proposal for E-commerce Partner\n* **Executive Summary:** Scaling through automated ad creation.\n* **Scope:** 30 Reels/month + AI Optimization.\n* **Investment:** $2,500/mo retainer.")
            else:
                prompt = f"Act as Agency Founder. Create a high-value proposal structure for target client '{client_type}' following A.G.E.N.C.Y.™ standards."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # ----------------------------------------------------
    # SYSTEM 7: EXECUTIVE ASSISTANT OS
    # ----------------------------------------------------
    elif "System 7" in system_choice:
        st.subheader("System 7: AI Executive Assistant OS™")
        st.markdown("""
        **Framework:** `E.X.E.C.™`
        * **E**xecute Info Management | **X**pedite Communication | **E**nhance Planning | **C**oordinate Decisions
        """)
        
        meeting_notes = st.text_area("Paste Raw Meeting Notes or Thoughts:", placeholder="Discussed ViralCart campaign, budget $10k, deadline Friday, need designer...")
        if st.button("Generate Executive Decision Brief"):
            if use_demo:
                st.success("✅ Demo Executive Brief:")
                st.markdown("### Executive Briefing\n* **Key Decisions:** Approved $10k ViralCart campaign budget.\n* **Action Items:** Assign designer by Wednesday.\n* **Deadline:** Friday launch.")
            else:
                prompt = f"Act as Executive Chief of Staff. Synthesize these notes into a structured Executive Briefing with Action Items and Key Decisions: '{meeting_notes}'"
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # ----------------------------------------------------
    # SYSTEM 8: HR & RECRUITMENT OS
    # ----------------------------------------------------
    elif "System 8" in system_choice:
        st.subheader("System 8: AI Human Resources & Recruitment OS™")
        st.markdown("""
        **Framework:** `H.I.R.E.™`
        * **H**iring Intelligence | **I**dentify Candidates | **R**etention & Dev | **E**mployee Experience
        """)
        
        job_role = st.text_input("Target Role:", placeholder="e.g., Senior AI Workflow Engineer")
        if st.button("Generate Job Description & Interview Framework"):
            if use_demo:
                st.success("✅ Demo HR Framework:")
                st.markdown(f"### Role: {job_role}\n* **Responsibilities:** Build custom AI apps, optimize workflows.\n* **Key Skills:** Python, Streamlit, Prompt Design.\n* **Interview Q1:** How do you handle AI hallucinations in production?")
            else:
                prompt = f"Act as Head of People. Generate a modern job description and candidate evaluation scorecard for '{job_role}'."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # ----------------------------------------------------
    # SYSTEM 9: FINANCE & BI OS
    # ----------------------------------------------------
    elif "System 9" in system_choice:
        st.subheader("System 9: AI Finance & Business Intelligence OS™")
        st.markdown("""
        **Framework:** `F.I.N.A.N.C.E.™`
        * **F**oundation | **I**ntelligence Reporting | **N**umber Analysis | **A**ssessment & Forecast | **N**avigation | **C**ontrol | **E**volution
        """)
        
        fin_query = st.text_input("Financial Scenario Query:", placeholder="e.g., Should we hire a $5,000/mo manager if revenue is $45,000/mo?")
        if st.button("Run Financial Intelligence Analysis"):
            if use_demo:
                st.success("✅ Demo Financial Analysis:")
                st.markdown("### Scenario Assessment\n* **Current Net Margin:** ~30%\n* **Impact of Hire:** Reduces net profit margin by 11%.\n* **Recommendation:** Proceed if hire generates at least $12,000 in additional revenue.")
            else:
                prompt = f"Act as Virtual CFO. Provide a financial analysis and risk evaluation for scenario: '{fin_query}'"
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # ----------------------------------------------------
    # SYSTEM 10: PRODUCT INNOVATION OS
    # ----------------------------------------------------
    elif "System 10" in system_choice:
        st.subheader("System 10: AI Product Development & Innovation OS™")
        st.markdown("""
        **Framework:** `I.N.N.O.V.A.T.E.™`
        * **I**dentify Opportunities | **N**avigate Needs | **N**ame Concepts | **O**utline Requirements | **V**alidate | **A**ssemble Workflow | **T**est | **E**xpand
        """)
        
        prod_idea = st.text_input("Product Innovation Concept:", placeholder="e.g., AI-powered WhatsApp customer support bot for dropshipping")
        if st.button("Generate Product Validation Roadmap"):
            if use_demo:
                st.success("✅ Demo Innovation Roadmap:")
                st.markdown(f"### Validation Plan for: {prod_idea}\n1. **Unmet Need:** Slow customer support leads to high refunds.\n2. **MVP Feature:** Instant tracking number lookup.\n3. **Validation Metric:** Pre-launch waitlist signups.")
            else:
                prompt = f"Act as Chief Product Officer. Generate a complete product validation roadmap for concept: '{prod_idea}' using I.N.N.O.V.A.T.E.™ framework."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)