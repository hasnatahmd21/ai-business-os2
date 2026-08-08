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
        "⚡ AI Execution Systems™ (Systems 1-25)"
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
# 6. AI EXECUTION SYSTEMS™ (SYSTEMS 1 TO 25)
# ==========================================
elif menu == "⚡ AI Execution Systems™ (Systems 1-25)":
    st.title("⚡ Enterprise AI Execution Library™ (25 Systems)")
    st.caption("Complete Suite of Autonomous Business Operating Systems")
    
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
            "System 10 — AI Product & Innovation OS™ (I.N.N.O.V.A.T.E.™)",
            "System 11 — AI Knowledge Management OS™",
            "System 12 — AI Customer Intelligence OS™",
            "System 13 — AI Sales Optimization OS™",
            "System 14 — AI Marketing Intelligence OS™",
            "System 15 — AI Business Analytics & Decision Intelligence OS™",
            "System 16 — AI Automation & Workflow Optimization OS™",
            "System 17 — AI Financial Intelligence & Business Control OS™",
            "System 18 — AI Team Productivity & Collaboration OS™",
            "System 19 — AI Innovation & Product Development OS™",
            "System 20 — AI Business Growth & Scaling OS™",
            "System 21 — AI Competitive Intelligence & Market Dominance OS™",
            "System 22 — AI Executive Leadership & Business OS™",
            "System 23 — AI Customer Experience & Retention OS™",
            "System 24 — AI Business Security & Risk Management OS™",
            "System 25 — AI Future Business Transformation OS™"
        ]
    )
    
    st.markdown("---")
    
    # SYSTEM 1
    if "System 1 " in system_choice:
        st.subheader("System 1: AI Content Production System™")
        c_topic = st.text_input("Enter Content Topic/Product:", placeholder="e.g., AI Business Automation Tools")
        c_format = st.selectbox("Format:", ["Educational Post", "Product Launch Copy", "Case Study", "Video Script Narrative"])
        if st.button("Generate Content Asset"):
            if use_demo:
                st.success("✅ Demo Content Generated!")
            else:
                prompt = f"Act as AI Content Strategist. Create a high-converting {c_format} on '{c_topic}' using C.O.N.T.E.N.T.™ formula."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 2
    elif "System 2 " in system_choice:
        st.subheader("System 2: AI SEO Growth System™")
        s_keyword = st.text_input("Enter Focus Keyword:", placeholder="e.g., best AI software for e-commerce")
        if st.button("Generate SEO Brief"):
            if use_demo: st.success("✅ Demo SEO Brief Generated!")
            else:
                prompt = f"Act as AI SEO Strategist. Generate a complete SEO Brief for '{s_keyword}' following S.E.A.R.C.H.™."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 3
    elif "System 3 " in system_choice:
        st.subheader("System 3: AI Social Media OS™")
        sm_pillar = st.selectbox("Pillar:", ["Educational", "Authority", "Trust", "Engagement", "Offer"])
        sm_platform = st.selectbox("Platform:", ["LinkedIn", "Instagram Carousel", "X Thread", "TikTok Script"])
        if st.button("Generate Social Asset"):
            if use_demo: st.success("✅ Demo Social Asset Generated!")
            else:
                prompt = f"Act as Social Media Director. Create a high-engagement {sm_platform} asset for pillar '{sm_pillar}'."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 4
    elif "System 4 " in system_choice:
        st.subheader("System 4: AI Customer Support OS™")
        ticket_text = st.text_area("Paste Support Inquiry / Ticket:", placeholder="My order hasn't arrived yet...")
        if st.button("Generate Support Response"):
            if use_demo: st.success("✅ Demo Support Response Generated!")
            else:
                prompt = f"Act as AI Customer Care Specialist. Draft a response for: '{ticket_text}'"
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 5
    elif "System 5 " in system_choice:
        st.subheader("System 5: AI E-commerce Growth OS™")
        p_name = st.text_input("Product Name:", placeholder="e.g., Ergonomic Smart Desk Lamp")
        if st.button("Generate Product Page Copy"):
            if use_demo: st.success("✅ Demo Product Copy Generated!")
            else:
                prompt = f"Act as E-commerce Conversion Specialist. Create product description for '{p_name}'."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 6
    elif "System 6 " in system_choice:
        st.subheader("System 6: AI Agency Operating System™")
        client_type = st.text_input("Client Profile:", placeholder="e.g., E-commerce fashion brand doing $50k/mo")
        if st.button("Generate Proposal Structure"):
            if use_demo: st.success("✅ Demo Proposal Generated!")
            else:
                prompt = f"Act as Agency Founder. Create a proposal structure for target client '{client_type}'."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 7
    elif "System 7 " in system_choice:
        st.subheader("System 7: AI Executive Assistant OS™")
        meeting_notes = st.text_area("Paste Meeting Notes / Thoughts:", placeholder="Discussed campaign budget $10k, deadline Friday...")
        if st.button("Generate Executive Brief"):
            if use_demo: st.success("✅ Demo Executive Brief Generated!")
            else:
                prompt = f"Act as Executive Chief of Staff. Synthesize these notes into an Executive Brief: '{meeting_notes}'"
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 8
    elif "System 8 " in system_choice:
        st.subheader("System 8: AI HR & Recruitment OS™")
        job_role = st.text_input("Target Role:", placeholder="e.g., Senior AI Workflow Engineer")
        if st.button("Generate JD & Scorecard"):
            if use_demo: st.success("✅ Demo HR Framework Generated!")
            else:
                prompt = f"Act as Head of People. Generate a job description and evaluation scorecard for '{job_role}'."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 9
    elif "System 9 " in system_choice:
        st.subheader("System 9: AI Finance & BI OS™")
        fin_query = st.text_input("Financial Scenario Query:", placeholder="e.g., Impact of hiring $5,000/mo manager on $45k revenue")
        if st.button("Run Scenario Analysis"):
            if use_demo: st.success("✅ Demo Financial Analysis Generated!")
            else:
                prompt = f"Act as Virtual CFO. Provide a financial analysis for scenario: '{fin_query}'"
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 10
    elif "System 10 " in system_choice:
        st.subheader("System 10: AI Product Innovation OS™")
        prod_idea = st.text_input("Product Innovation Concept:", placeholder="e.g., AI WhatsApp support bot for e-commerce")
        if st.button("Generate Validation Plan"):
            if use_demo: st.success("✅ Demo Innovation Plan Generated!")
            else:
                prompt = f"Act as Chief Product Officer. Generate a product validation roadmap for concept: '{prod_idea}'."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 11
    elif "System 11 " in system_choice:
        st.subheader("System 11: AI Knowledge Management OS™")
        st.markdown("**Core Framework:** Capture → Organize → Analyze → Apply → Update")
        raw_info = st.text_area("Paste Raw Business Information / Conversations:", placeholder="Customer chat notes, team decisions, research notes...")
        if st.button("Organize Knowledge Asset"):
            if use_demo:
                st.success("✅ Knowledge Database Entry Created!")
                st.markdown("### Structured Knowledge Asset\n* **Category:** Customer Intelligence\n* **Summary:** Key buyer objections noted.\n* **Action Items:** Update FAQ & sales script.")
            else:
                prompt = f"Act as Knowledge Management System. Organize this information into a structured Business Knowledge Database with categories, key insights, and recommended actions: '{raw_info}'"
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 12
    elif "System 12 " in system_choice:
        st.subheader("System 12: AI Customer Intelligence OS™")
        cust_data = st.text_area("Paste Customer Data / Reviews / Chat Logs:", placeholder="Paste reviews, emails, or feedback here...")
        if st.button("Analyze Customer Intelligence"):
            if use_demo:
                st.success("✅ Customer Profile & Intelligence Report Created!")
                st.markdown("### Customer Intelligence Profile\n* **Main Pain Point:** Slow response time\n* **Buying Motivation:** Ease of use\n* **Recommended Angle:** Highlight fast setup in ads")
            else:
                prompt = f"Act as Customer Intelligence Director. Analyze this customer data and create 1. Customer profiles, 2. Main pain points, 3. Buying motivations, 4. Common objections, 5. Marketing opportunities: '{cust_data}'"
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 13
    elif "System 13 " in system_choice:
        st.subheader("System 13: AI Sales Optimization OS™")
        sales_convo = st.text_area("Paste Sales Conversation / Prospect Notes:", placeholder="Prospect mentioned price is high and wants to consult partner...")
        if st.button("Generate Sales Optimization Action"):
            if use_demo:
                st.success("✅ Sales Action Plan Generated!")
                st.markdown("### Sales Follow-up & Objection Strategy\n* **Objection:** Price & Authority\n* **Strategy:** Reframe ROI & provide partner summary PDF\n* **Recommended Email Draft:** Provided")
            else:
                prompt = f"Act as AI Sales Director. Analyze this sales conversation, identify objections, lead classification, and generate a personalized follow-up sequence: '{sales_convo}'"
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 14
    elif "System 14 " in system_choice:
        st.subheader("System 14: AI Marketing Intelligence OS™")
        mkt_context = st.text_input("Target Audience / Product / Campaign:", placeholder="e.g., Premium Gym Gear for Busy Executives")
        if st.button("Generate Marketing Intelligence Strategy"):
            if use_demo:
                st.success("✅ Marketing Strategy Generated!")
                st.markdown("### Intelligence Strategy\n* **Hook:** 15-min workout designed for CEOs\n* **Emotional Trigger:** Time efficiency & Status\n* **Recommended Channels:** LinkedIn + Meta Ads")
            else:
                prompt = f"Act as CMO. Analyze this market context '{mkt_context}' and generate customer messaging, high-performing content patterns, and campaign optimizations."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 15
    elif "System 15 " in system_choice:
        st.subheader("System 15: AI Business Analytics & Decision Intelligence OS™")
        biz_data = st.text_area("Input Business Performance Data:", placeholder="Q1 Revenue $120k, Ad spend $30k, Churn rate 8%, Conversion rate dropped 2%...")
        if st.button("Run Decision Intelligence Engine"):
            if use_demo:
                st.success("✅ Executive Decision Intelligence Analysis Complete!")
                st.markdown("### Decision Analysis\n* **Descriptive:** Conversion dropped 2%\n* **Diagnostic:** Landing page speed issue\n* **Prescriptive Action:** Re-allocate $5k from ads to UX optimization")
            else:
                prompt = f"Act as Chief Data Officer. Perform Descriptive, Diagnostic, Predictive, and Prescriptive analysis on this business data: '{biz_data}'"
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 16
    elif "System 16 " in system_choice:
        st.subheader("System 16: AI Automation & Workflow Optimization OS™")
        process_desc = st.text_area("Describe Current Manual Process:", placeholder="Every day we manually copy orders from email into Excel and send tracking manually...")
        if st.button("Generate Automation Blueprint"):
            if use_demo:
                st.success("✅ Automation Architecture Designed!")
                st.markdown("### Workflow Automation Blueprint\n* **Trigger:** New Order Email\n* **Automated Action:** Webhook to Google Sheets + WhatsApp API\n* **Time Saved:** ~15 hrs/week")
            else:
                prompt = f"Act as Automation Architect. Analyze this manual process and design a structured automated workflow with Trigger, Action, Decision points, and tool recommendations: '{process_desc}'"
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 17
    elif "System 17 " in system_choice:
        st.subheader("System 17: AI Financial Intelligence & Business Control OS™")
        fin_details = st.text_area("Financial Data / Budget Overview:", placeholder="Monthly revenue $50k, Software costs $4k, Team $20k, Ad spend $15k...")
        if st.button("Run Financial Control Analysis"):
            if use_demo:
                st.success("✅ Financial Health Report Generated!")
                st.markdown("### Financial Control Analysis\n* **Profit Margin:** 22%\n* **Cost Concern:** Software spend is high relative to team size\n* **Recommendation:** Consolidate tools to increase net margin to 28%")
            else:
                prompt = f"Act as Virtual CFO. Provide a comprehensive profitability, cash flow risk, and budget optimization analysis for: '{fin_details}'"
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 18
    elif "System 18 " in system_choice:
        st.subheader("System 18: AI Team Productivity & Collaboration OS™")
        team_issue = st.text_area("Describe Team Workflow / Meeting Transcript:", placeholder="Paste team discussion or describe bottlenecks in project delivery...")
        if st.button("Optimize Team Operations"):
            if use_demo:
                st.success("✅ Team Action Plan Generated!")
                st.markdown("### Team Optimization Plan\n* **Action Items:** 3 clear tasks assigned\n* **Process Bottleneck:** Approval delays\n* **SOP Recommendation:** Created standard review protocol")
            else:
                prompt = f"Act as VP of Operations. Analyze this team context and extract key decisions, action items, task assignments, and workflow improvements: '{team_issue}'"
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 19
    elif "System 19 " in system_choice:
        st.subheader("System 19: AI Innovation & Product Development OS™")
        market_signal = st.text_input("Market Signal / Customer Request:", placeholder="Customers keep asking for automated invoice generation inside CRM...")
        if st.button("Run Innovation Pipeline"):
            if use_demo:
                st.success("✅ Product Innovation Brief Generated!")
                st.markdown("### Innovation Concept\n* **Unmet Need:** Manual invoicing friction\n* **Proposed MVP:** One-click invoice button\n* **Validation Strategy:** Pre-announce to top 50 users")
            else:
                prompt = f"Act as Chief Product Officer. Evaluate this market signal '{market_signal}' and generate a product opportunity concept, validation plan, and launch strategy."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 20
    elif "System 20 " in system_choice:
        st.subheader("System 20: AI Business Growth & Scaling OS™")
        growth_stage = st.text_area("Current Scale & Bottlenecks:", placeholder="Doing $30k/mo in local market, want to expand nationally but support is overwhelmed...")
        if st.button("Generate Scaling Roadmap"):
            if use_demo:
                st.success("✅ Business Scaling Plan Generated!")
                st.markdown("### Business Scaling Blueprint\n* **Priority 1:** AI Support Automation\n* **Priority 2:** Localized Ad Channels\n* **Expected Impact:** 2.5x growth with zero team headcount increase")
            else:
                prompt = f"Act as Growth Strategist. Analyze this business state '{growth_stage}' and create a 7-layer growth scaling roadmap."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 21
    elif "System 21 " in system_choice:
        st.subheader("System 21: AI Competitive Intelligence & Market Dominance OS™")
        comp_name = st.text_input("Competitor Name or URL / Strategy:", placeholder="e.g., Competitor X charging $199/mo with 3-day support delay")
        if st.button("Run Competitive Analysis"):
            if use_demo:
                st.success("✅ Competitive Dominance Report Generated!")
                st.markdown("### Competitive Intelligence Report\n* **Competitor Weakness:** Slow support & high entry price\n* **Gap Opportunity:** Launch $99/mo tier with instant AI support\n* **Positioning Hook:** 'The 10x faster alternative'")
            else:
                prompt = f"Act as Competitive Intelligence Analyst. Analyze competitor '{comp_name}' and identify strengths, weaknesses, customer perception gaps, and positioning strategy."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 22
    elif "System 22 " in system_choice:
        st.subheader("System 22: AI Executive Leadership & Business OS™")
        strat_situation = st.text_area("Describe Strategic Situation / Dilemma:", placeholder="Should we pivot to enterprise B2B or keep scaling SMB product?")
        if st.button("Generate Executive Decision Brief"):
            if use_demo:
                st.success("✅ Executive Command Brief Generated!")
                st.markdown("### Executive Decision Support\n* **Option A (B2B):** Higher ACV, longer sales cycle\n* **Option B (SMB):** Fast volume, higher churn\n* **Strategic Recommendation:** Maintain SMB core while testing B2B with 2 pilot accounts")
            else:
                prompt = f"Act as Senior Executive Advisor. Evaluate this business dilemma and provide structured analysis including risk assessment, options, and strategic recommendation: '{strat_situation}'"
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 23
    elif "System 23 " in system_choice:
        st.subheader("System 23: AI Customer Experience & Retention OS™")
        retention_context = st.text_area("Customer Behavior / Feedback Data:", placeholder="Users drop off after day 14. Main feedback: 'Hard to configure rules'")
        if st.button("Generate Retention Strategy"):
            if use_demo:
                st.success("✅ Retention & CX Strategy Generated!")
                st.markdown("### Retention Strategy\n* **Root Cause:** Day 14 onboarding friction\n* **Solution:** Interactive setup wizard + AI auto-config\n* **Expected Result:** Churn reduced by 15%")
            else:
                prompt = f"Act as VP of Customer Experience. Analyze this retention context '{retention_context}' and generate customer journey fixes, churn risk mitigation, and advocacy programs."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 24
    elif "System 24 " in system_choice:
        st.subheader("System 24: AI Business Security & Risk Management OS™")
        risk_context = st.text_area("Business Operation / Asset Details:", placeholder="We store customer API keys and handle payment data on third-party servers...")
        if st.button("Run Risk Assessment Engine"):
            if use_demo:
                st.success("✅ Risk Assessment Report Generated!")
                st.markdown("### Risk Mitigation Report\n* **Operational Risk:** Medium (Third-party dependency)\n* **Security Action:** Implement end-to-end encryption & access control\n* **Continuity:** Daily automated backups to secure vault")
            else:
                prompt = f"Act as Chief Risk & Security Officer. Perform a risk assessment for: '{risk_context}'. Identify vulnerabilities, probability, impact, and prevention steps."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)

    # SYSTEM 25
    elif "System 25 " in system_choice:
        st.subheader("System 25: AI Future Business Transformation OS™")
        biz_model = st.text_area("Current Traditional Business Model:", placeholder="Traditional agency providing manual video editing services for e-commerce brands...")
        if st.button("Generate AI-Native Transformation Roadmap"):
            if use_demo:
                st.success("✅ AI-Native Transformation Roadmap Generated!")
                st.markdown("### AI-Native Business Architecture\n* **Phase 1:** Implement AI editing workflows (5x speed)\n* **Phase 2:** Launch self-serve client AI portal\n* **Phase 3:** Transition to high-margin recurring SaaS model")
            else:
                prompt = f"Act as AI Transformation Officer. Create an AI-native transformation roadmap for this business model: '{biz_model}' including operating model redesign, human-AI workforce plan, and autonomous systems architecture."
                out = run_ai_task(api_key, prompt)
                if out: st.markdown(out)
