import os
import streamlit as st
import pandas as pd

# Optional: import google.generativeai only when used to avoid import errors during demo
try:
    import google.generativeai as genai
except Exception:
    genai = None

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="AI Business OS™", page_icon="⚙️", layout="wide")

# Initialize Session State for Sales Pipeline Data
if "pipeline_data" not in st.session_state:
    st.session_state.pipeline_data = pd.DataFrame([
        {"Company": "TechFlow Inc", "Stage": "Negotiate", "Value ($)": 15000, "Next Action": "Send revised proposal"},
        {"Company": "ViralCart", "Stage": "Validate", "Value ($)": 8500, "Next Action": "Discovery Call"},
        {"Company": "Apex SaaS", "Stage": "Engage", "Value ($)": 22000, "Next Action": "Follow-up email"},
        {"Company": "Global Logistics", "Stage": "Unify", "Value ($)": 45000, "Next Action": "Contract signing"}
    ])

# ==========================================
# 2. SIDEBAR NAVIGATION & API CONFIG
# ==========================================
st.sidebar.title("⚙️ AI Business OS™")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Select Module",
    ["📊 Executive Dashboard", "📝 P.R.O.M.P.T. Engineer", "📈 Sales Pipeline"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔑 AI Settings")

# Prefill from environment variable if available
default_key = os.getenv("GEMINI_API_KEY", "")
api_key = st.sidebar.text_input(
    "Gemini API Key", 
    value=default_key,
    type="password", 
    help="Google AI Studio se free API key hasil karein (aistudio.google.com)"
)

st.sidebar.markdown("---")
st.sidebar.info("Built on the AI Business Operating Systems™ Framework.")

# ==========================================
# 3. MODULE 9: EXECUTIVE DASHBOARD
# ==========================================
if menu == "📊 Executive Dashboard":
    st.title("📊 Executive Decision System™")
    st.markdown("Track your E.X.E.C.U.T.E.™ Framework metrics.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Monthly Revenue", "$45,500", "+12% from last month")
    col2.metric("Active Clients", "124", "+4 new")
    col3.metric("Lead Conversion", "18%", "-2%")
    col4.metric("AI Hours Saved", "320 hrs", "+45 hrs")
    
    st.markdown("### 📈 Revenue Trends")
    chart_data = pd.DataFrame(
        {"Revenue": [30000, 32000, 38000, 41000, 45500],
         "Expenses": [15000, 16000, 18000, 19000, 21000]},
        index=["Jan", "Feb", "Mar", "Apr", "May"]
    )
    st.line_chart(chart_data)
    
    st.markdown("### 📋 Executive Task Action Items")
    tasks = pd.DataFrame([
        {"Task": "Review Q2 Marketing SOPs", "Assignee": "CMO", "Status": "Pending"},
        {"Task": "Approve new AI Tech Stack", "Assignee": "CEO", "Status": "In Progress"},
        {"Task": "Client Expansion Strategy", "Assignee": "Sales Head", "Status": "Completed"}
    ])
    st.dataframe(tasks, use_container_width=True)

# ==========================================
# 4. MODULE 5: P.R.O.M.P.T. ENGINEER
# ==========================================
elif menu == "📝 P.R.O.M.P.T. Engineer":
    st.title("📝 Premium Prompt Engineering System™")
    st.markdown("Design professional AI prompts using the **P.R.O.M.P.T.™ Framework**.")
    
    with st.form("prompt_builder"):
        p_purpose = st.text_input("**Purpose:** What is the business objective?", placeholder="e.g., Generate qualified leads for Shopify owners")
        r_role = st.text_input("**Role:** What expert role should AI take?", placeholder="e.g., Chief Marketing Officer")
        o_objective = st.text_input("**Objective:** What exactly needs to be produced?", placeholder="e.g., 5 Facebook Ad copy variations")
        m_market = st.text_area("**Market Context:** Industry, audience, budget?", placeholder="e.g., E-commerce owners, $5M+ revenue, struggling with ROAS")
        p_params = st.text_input("**Parameters:** Word count, tone, format?", placeholder="e.g., Professional tone, max 150 words per ad, bullet points")
        
        submitted = st.form_submit_button("Generate Consultant-Grade Prompt")
        
        if submitted:
            st.success("✅ Prompt Generated Successfully!")
            st.markdown("### Your Engineered Prompt:")
            
            final_prompt = (
                f"**Act As:** {r_role if r_role else '[Role]'}\n"
                f"**Business Objective:** {p_purpose if p_purpose else '[Purpose]'}\n\n"
                f"**Task:** {o_objective if o_objective else '[Objective]'}\n\n"
                f"**Context:**\n{m_market if m_market else '[Market Context]'}\n\n"
                f"**Constraints & Parameters:**\n{p_params if p_params else '[Parameters]'}\n\n"
                f"Please review this information and provide the output accordingly."
            )
            
            st.code(final_prompt, language="markdown")
            st.info("💡 Copy this prompt and paste it into ChatGPT, Claude, or Gemini.")

# ==========================================
# 5. MODULE 8: SALES PIPELINE (WITH LIVE AI)
# ==========================================
elif menu == "📈 Sales Pipeline":
    st.title("📈 AI Sales & Revenue Operating System™")
    st.markdown("Manage your **R.E.V.E.N.U.E.™ Framework** pipeline.")
    
    # Add New Lead Form
    with st.expander("➕ Add New Lead to Pipeline"):
        lead_name = st.text_input("Company Name")
        lead_stage = st.selectbox("Stage", ["Research", "Engage", "Validate", "Educate", "Negotiate", "Unify", "Expand"])
        lead_value = st.number_input("Estimated Value ($)", min_value=0)
        next_action = st.text_input("Next Action", placeholder="e.g., Follow-up call")
        
        if st.button("Add Lead"):
            if lead_name:
                new_lead = pd.DataFrame([{
                    "Company": lead_name,
                    "Stage": lead_stage,
                    "Value ($)": lead_value,
                    "Next Action": next_action if next_action else "N/A"
                }])
                st.session_state.pipeline_data = pd.concat([st.session_state.pipeline_data, new_lead], ignore_index=True)
                st.success(f"Added {lead_name} to the {lead_stage} stage!")
                st.experimental_rerun()
            else:
                st.warning("Please enter a Company Name.")

    st.markdown("### 📊 Active Pipeline")
    st.dataframe(st.session_state.pipeline_data, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 🤖 Live AI Sales Assistant")
    
    user_prompt = st.text_area(
        "Ask AI to research, draft emails, or prepare sales pitches:", 
        placeholder="e.g., Draft a follow-up email for ViralCart after our validation call..."
    )

    use_demo = st.checkbox("Use demo AI output (no API key)", value=False)
    
    if st.button("🚀 Generate Live Output"):
        if use_demo:
            # Provide a canned demo response so you can see output without an API key
            demo_response = (
                "Subject: Follow-up on Validation Call\n\n"
                "Hi [Name],\n\n"
                "Thanks for taking the time to validate the solution with us. Based on our discussion, "
                "I've outlined the next steps and a recommended approach to move forward: \n\n"
                "1) Pilot scope & goals\n2) Timeline & milestones\n3) Pricing overview\n\n"
                "Please let me know a good time this week to get the pilot started.\n\nBest,\n[Your Name]"
            )
            st.success("✅ Demo Response Generated:")
            st.markdown(demo_response)
        else:
            if not api_key:
                st.warning("⚠️ Please enter your Gemini API Key in the sidebar or use the demo option.")
            elif not user_prompt:
                st.warning("⚠️ Please enter a question or command for the AI.")
            else:
                if genai is None:
                    st.error("google-generativeai package not available. Install it or use the demo option.")
                else:
                    with st.spinner("AI Sales Engine is processing your request..."):
                        try:
                            # Configure Gemini API
                            genai.configure(api_key=api_key)
                            model = genai.GenerativeModel("gemini-1.5-flash")
                            
                            # Pass Pipeline Data as Context to AI
                            context = st.session_state.pipeline_data.to_string(index=False)
                            
                            system_instructions = f"""
You are an expert AI B2B Sales & Revenue Strategist working within the AI Business Operating Systems™ framework.

Here is the current real-time Sales Pipeline context:
{context}

Respond professionally, actionably, and concisely to the following user request.
If drafting an email or pitch, make it consultant-grade and ready to send.
"""
                            # Note: SDK method names can change; this is what your original code used.
                            response = model.generate_content(f"{system_instructions}\n\nUser Request: {user_prompt}")
                            
                            st.success("✅ Response Generated:")
                            st.markdown(response.text)
                            
                        except Exception as e:
                            st.error(f"❌ Error connecting to Gemini API: {str(e)}")