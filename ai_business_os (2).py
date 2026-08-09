import os
import json
import re
import time
import asyncio
import logging
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional
import pandas as pd
import streamlit as st
from pydantic import BaseModel, Field

# Optional Import for Google Gemini AI
try:
    import google.generativeai as genai
except ImportError:
    genai = None

# ===========================================================================
# LOGGING SETUP
# ===========================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("AIBusinessOS")


# ===========================================================================
# 1. CORE MONOLITH ENGINES (MARKETING, SALES, CONTENT, SUPPORT, KNOWLEDGE)
# ===========================================================================

class MarketingEngine:
    """Generates high-converting marketing frameworks, ad scripts, and briefs."""
    def __init__(self, brand_config: Dict[str, Any]):
        self.brand_name = brand_config.get("brand_name", "ViralCart")
        self.voice_tone = brand_config.get("voice_tone", ["Energetic", "Direct"])
        self.cta_templates = brand_config.get("cta_templates", [
            "Tap 'Shop Now' before stock runs out!",
            "Claim your discount today only."
        ])

    def generate_ad_campaign(self, product_name: str, key_feature: str, price: str) -> Dict[str, Any]:
        hooks = [
            f"Stop scrolling! If you hate wasting time, you need to see this {product_name}.",
            f"Why is everyone ordering the new {product_name} from {self.brand_name}?",
            f"This simple {product_name} hack will change your daily routine."
        ]
        
        script = {
            "00:00-00:03_Hook": hooks[0],
            "00:03-00:10_Problem": "Tired of dealing with messy, inefficient tools? Most options break in a week.",
            "00:10-00:20_Solution": f"The {product_name} features {key_feature}. Premium quality delivered to your door for just {price}.",
            "00:20-00:30_CTA": self.cta_templates[0]
        }
        
        return {
            "module": "MARKETING_OS",
            "brand": self.brand_name,
            "product": product_name,
            "tone_applied": ", ".join(self.voice_tone),
            "script_brief": script
        }

class SalesEngine:
    """Scores leads dynamically, routes them, and generates personalized outbound outreach."""
    def __init__(self):
        self.high_value_roles = ["CEO", "Founder", "CMO", "Owner", "E-commerce Manager"]

    def score_and_route_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        score = 0
        reasons = []

        budget = lead_data.get("monthly_budget", 0)
        if budget >= 5000:
            score += 40
            reasons.append("High Budget Priority (+40)")
        elif budget >= 1000:
            score += 20
            reasons.append("Medium Budget (+20)")
        else:
            score += 5
            reasons.append("Low Budget (+5)")

        role = lead_data.get("job_title", "")
        if any(r.lower() in role.lower() for r in self.high_value_roles):
            score += 30
            reasons.append("Decision Maker Role (+30)")
        else:
            score += 10
            reasons.append("Standard Staff Role (+10)")

        timeline = lead_data.get("timeline", "")
        if timeline == "Immediate":
            score += 30
            reasons.append("Urgent Timeline (+30)")
        elif timeline == "1-3 Months":
            score += 15
            reasons.append("Moderate Timeline (+15)")

        if score >= 70:
            action = "HOT_LEAD: Immediate Priority Call Assignment + Personal Email"
        elif score >= 40:
            action = "WARM_LEAD: Automated Nurture Sequence"
        else:
            action = "COLD_LEAD: Low-Touch Monthly Newsletter"

        return {
            "lead_name": lead_data.get("name"),
            "total_score": score,
            "routing_action": action,
            "audit_trail": reasons
        }

    def generate_outbound_email(self, lead_name: str, pain_point: str, offer: str) -> Dict[str, str]:
        subject = f"quick question re: {pain_point.lower()}"
        body = (
            f"Hi {lead_name},\n\n"
            f"Noticed a lot of teams struggle with {pain_point}.\n\n"
            f"We built {offer} specifically to eliminate that headache without the friction.\n\n"
            f"Worth a 2-minute look?\n\n"
            f"Best,\nSales Team"
        )
        return {"subject": subject, "body": body}

class ContentEngine:
    """Extracts key insights and repurposes content into social threads and video scripts."""
    def repurpose_transcript(self, raw_transcript: str) -> Dict[str, Any]:
        sentences = [s.strip() for s in re.split(r'(?<=[.!?]) +', raw_transcript) if len(s.strip()) > 0]
        takeaways = sentences[:3] if len(sentences) >= 3 else sentences

        tweet_thread = [
            f"🧵 Essential lesson on scaling:\n\n{takeaways[0] if len(takeaways) > 0 else ''}",
            f"2/ Key detail: {takeaways[1] if len(takeaways) > 1 else 'Focus on consistency.'}",
            f"3/ Takeaway: {takeaways[2] if len(takeaways) > 2 else 'Optimize daily.'}\n\nFollow for more tactics!"
        ]

        video_script = {
            "0-3s_Hook": f"Stop scrolling if you want to master this: {takeaways[0] if takeaways else ''}",
            "3-20s_Body": "Here is the exact breakdown of how this works in practice...",
            "20-30s_CTA": "Save this video and drop a comment below!"
        }

        return {
            "module": "CONTENT_OS",
            "extracted_points": takeaways,
            "tweet_thread": tweet_thread,
            "short_video_script": video_script
        }

class SupportEngine:
    """Triages support tickets by urgency and drafts automated empathetic responses."""
    def __init__(self):
        self.urgent_keywords = ["broken", "refund", "stolen", "scam", "defective", "missing", "cancel"]

    def triage_and_resolve(self, customer_name: str, message: str) -> Dict[str, Any]:
        msg_lower = message.lower()
        urgency_score = sum(1 for word in self.urgent_keywords if word in msg_lower)

        if urgency_score >= 2 or "refund" in msg_lower:
            priority = "HIGH"
            action = "Route to Senior Specialist + Issue Auto-Acknowledge"
        elif urgency_score == 1:
            priority = "MEDIUM"
            action = "AI Draft Auto-Response + Human Approval"
        else:
            priority = "LOW"
            action = "Fully Automated AI Resolution"

        response_body = (
            f"Hi {customer_name},\n\n"
            f"Thank you for reaching out. We are so sorry to hear about the issue with your order.\n"
            f"Our team has prioritized your request ({priority} Priority) and is taking immediate action to make this right.\n\n"
            f"Best regards,\nCustomer Support Team"
        )

        return {
            "module": "SUPPORT_OS",
            "priority": priority,
            "routing_action": action,
            "generated_response": response_body
        }

class KnowledgeEngine:
    """Simulates internal document retrieval (RAG) and operational QA."""
    def __init__(self):
        self.knowledge_base = {
            "shipping_policy": "Standard delivery takes 2-3 business days. Free shipping applies to orders over $50.",
            "refund_policy": "Full refunds are accepted within 30 days of item delivery in original condition.",
            "fulfillment_sop": "Orders received before 2 PM PKT are processed and dispatched on the same day."
        }

    def query_knowledge_base(self, query: str) -> Dict[str, Any]:
        query_lower = query.lower()
        matched_results = []

        for key, text in self.knowledge_base.items():
            if any(word in query_lower for word in key.split("_")):
                matched_results.append({"topic": key, "policy_snippet": text})

        if not matched_results:
            return {
                "query": query,
                "found": False,
                "answer": "Information not found in internal knowledge base."
            }

        return {
            "query": query,
            "found": True,
            "matches": matched_results
        }


# ===========================================================================
# 2. NEW ENGINES ADDED: CUSTOMER SUCCESS OS & AI FINANCE OS
# ===========================================================================

class CustomerSuccessEngine:
    """Enterprise AI CS OS (Chapters 5-8): Churn, Health Scoring, Expansion, Advocacy & Governance."""
    
    def analyze_customer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        license_util = data.get("license_utilization_pct", 50.0)
        login_freq = data.get("login_frequency_per_week", 10)
        open_tickets = data.get("open_high_priority_tickets", 0)
        nps = data.get("nps_score", 7)
        ebr_attended = data.get("executive_ebr_attended", True)
        days_to_renewal = data.get("days_until_renewal", 180)
        arr = data.get("arr_usd", 10000.0)
        contacts = data.get("contact_count_last_week", 2)
        privacy = data.get("privacy_consent", True)

        # 1. Churn & Health Score Calculation
        usage_score = license_util * 0.35
        activity_score = min(100.0, (login_freq / 50.0) * 100.0) * 0.25
        support_score = max(0.0, 100.0 - (open_tickets * 25.0)) * 0.20
        sentiment_score = (nps / 10.0) * 100.0 * 0.20
        
        health_score = round(usage_score + activity_score + support_score + sentiment_score, 2)
        if not ebr_attended:
            health_score = max(0.0, health_score - 10.0)
        churn_risk = round(100.0 - health_score, 2)

        # Health Tier & Playbook
        actions = []
        if health_score >= 75:
            tier = "GREEN"
            playbook = "Expansion & Loyalty Acceleration"
            actions = ["Identify seat expansion opportunities", "Engage for executive referral"]
        elif 50 <= health_score < 75:
            tier = "YELLOW"
            playbook = "Adoption & Intervention Acceleration"
            actions = ["Schedule CSM usage audit", "Deploy feature training module"]
        else:
            tier = "RED"
            playbook = "Executive Crisis & Risk Mitigation"
            actions = ["Alert CS Leadership", "Assign Solutions Architect for tickets", "Schedule Emergency EBR"]

        if days_to_renewal <= 60 and churn_risk > 35:
            actions.insert(0, "URGENT: Renewal at risk within 60 days!")

        # 2. Account Expansion Potential
        propensity_score = round((health_score * 0.6) + (license_util * 0.4), 2) if health_score >= 65 else 20.0
        expansion_type = "Seat Addition"
        estimated_upside = arr * 0.15
        if license_util >= 85.0:
            expansion_type = "Enterprise Tier Upgrade"
            estimated_upside = arr * 0.30

        # 3. Advocacy & VoC
        advocate_score = round((health_score * 0.5) + ((nps / 10.0) * 50.0), 2)
        is_advocate = advocate_score >= 80.0 and ebr_attended

        # 4. Governance & Audit Checks
        contact_flag = contacts > 4
        compliance_passed = privacy and not contact_flag

        return {
            "module": "CUSTOMER_SUCCESS_OS",
            "customer_id": data.get("customer_id", "CUST-001"),
            "health_summary": {
                "health_score": health_score,
                "health_tier": tier,
                "churn_risk_pct": churn_risk,
                "playbook": playbook,
                "actions": actions
            },
            "expansion_summary": {
                "propensity_score": propensity_score,
                "recommended_expansion": expansion_type,
                "estimated_arr_upside": round(estimated_upside, 2)
            },
            "advocacy_summary": {
                "advocate_score": advocate_score,
                "is_eligible_for_case_study": is_advocate
            },
            "governance_summary": {
                "compliance_passed": compliance_passed,
                "spam_warning_flag": contact_flag,
                "privacy_valid": privacy
            }
        }

class FinanceEngine:
    """Enterprise AI Finance OS: Cash Flow, Runway Forecasting, OpEx & Credit Risk Governance."""
    
    def analyze_finance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        mrr = data.get("mrr_usd", 50000.0)
        opex = data.get("opex_usd", 40000.0)
        cash_res = data.get("cash_reserve_usd", 200000.0)
        ar = data.get("accounts_receivable_usd", 15000.0)
        ap = data.get("accounts_payable_usd", 8000.0)
        margin = data.get("gross_margin_pct", 75.0)
        overdue = data.get("overdue_invoices_count", 1)
        audit_approved = data.get("audit_approved", True)

        # 1. Cashflow & Runway
        monthly_net = mrr - opex
        if monthly_net < 0:
            burn_rate = abs(monthly_net)
            runway_months = round(cash_res / burn_rate, 1) if burn_rate > 0 else 999.0
        else:
            burn_rate = 0.0
            runway_months = 999.0

        projected_60_day = cash_res + (monthly_net * 2) + (ar * 0.85) - ap

        cash_tier = "HEALTHY_GREEN"
        if runway_months < 6.0 and monthly_net < 0:
            cash_tier = "CRITICAL_RED"
        elif 6.0 <= runway_months < 12.0 and monthly_net < 0:
            cash_tier = "WARNING_YELLOW"

        # 2. Expense & Pricing Intelligence
        anomalies = []
        if margin < 65.0:
            anomalies.append("Gross Margin is below recommended 65% benchmark.")
        if mrr > 0 and (opex / mrr) > 0.8:
            anomalies.append(f"High OpEx Ratio: Expenses eat {round((opex/mrr)*100,1)}% of MRR.")

        # 3. Credit Risk & Governance
        credit_risk = "LOW_RISK"
        if overdue > 10 or margin < 50.0:
            credit_risk = "HIGH_RISK"
        elif overdue > 3:
            credit_risk = "MODERATE_RISK"

        return {
            "module": "FINANCE_OS",
            "cashflow_summary": {
                "monthly_net_cashflow_usd": round(monthly_net, 2),
                "monthly_burn_rate_usd": round(burn_rate, 2),
                "runway_months": runway_months,
                "projected_60_day_cash": round(projected_60_day, 2),
                "cash_tier": cash_tier
            },
            "expense_pricing_summary": {
                "gross_margin_pct": margin,
                "anomalies_detected": anomalies if anomalies else ["None. Expenses within limits."]
            },
            "risk_governance_summary": {
                "credit_risk_tier": credit_risk,
                "audit_passed": audit_approved
            }
        }

class AIBusinessOS:
    """Master Monolithic Orchestrator Engine containing all systems."""
    def __init__(self, brand_vault: Optional[Dict[str, Any]] = None):
        if not brand_vault:
            brand_vault = {
                "brand_name": "ViralCart",
                "voice_tone": ["Energetic", "Direct", "Value-Driven"],
                "cta_templates": ["Tap 'Shop Now' before stock runs out!"]
            }
        self.marketing = MarketingEngine(brand_vault)
        self.sales = SalesEngine()
        self.content = ContentEngine()
        self.support = SupportEngine()
        self.knowledge = KnowledgeEngine()
        self.customer_success = CustomerSuccessEngine()
        self.finance = FinanceEngine()

# Global Singleton Monolith Instance
os_core = AIBusinessOS()


# ===========================================================================
# 3. SHARED INTELLIGENCE MEMORY & MULTI-AGENT ARCHITECTURE
# ===========================================================================

class AgentTask(BaseModel):
    task_id: str
    assigned_agent: str
    target_channel: Optional[str] = "All"
    payload: Dict[str, Any]
    status: str = "PENDING"
    result: Optional[Dict[str, Any]] = None

class SystemEvent(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    sender: str
    event_type: str
    data: Dict[str, Any]

class SharedIntelligenceMemory:
    """Centralized, real-time memory layer for all agents."""
    def __init__(self):
        self._memory_store: Dict[str, Any] = {}
        self._audit_log: List[SystemEvent] = []

    def set_context(self, key: str, value: Any) -> None:
        self._memory_store[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        return self._memory_store.get(key, default)

    def log_event(self, sender: str, event_type: str, data: Dict[str, Any]) -> None:
        event = SystemEvent(sender=sender, event_type=event_type, data=data)
        self._audit_log.append(event)

    def get_audit_trail(self) -> List[Dict[str, Any]]:
        return [e.model_dump() for e in self._audit_log]

class BaseAgent:
    def __init__(self, agent_name: str, memory: SharedIntelligenceMemory):
        self.agent_name = agent_name
        self.memory = memory

    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        raise NotImplementedError()

class ExecutiveStrategyAgent(BaseAgent):
    def __init__(self, memory: SharedIntelligenceMemory):
        super().__init__("ExecutiveStrategyAgent", memory)

    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        goal = task.payload.get("goal", "Maximize Revenue")
        budget = task.payload.get("allocated_budget", 5000.0)
        
        directives = [
            AgentTask(
                task_id="TASK-CREATIVE-01",
                assigned_agent="CreativeProductionAgent",
                payload={"product": "Viral Smart Bottle", "feature": "UV Sterilization", "price": "$49.99"}
            ),
            AgentTask(
                task_id="TASK-EXECUTION-01",
                assigned_agent="CampaignExecutionAgent",
                payload={"channels": ["Meta Ads", "TikTok Ads", "Google Search"], "allocated_budget": budget}
            ),
            AgentTask(
                task_id="TASK-CUSTOMER-01",
                assigned_agent="CustomerIntelligenceAgent",
                payload={"name": "Sarah Khan", "job_title": "CEO", "monthly_budget": budget, "timeline": "Immediate"}
            )
        ]
        
        self.memory.set_context("active_directives", [t.model_dump() for t in directives])
        self.memory.log_event(self.agent_name, "DIRECTIVES_GENERATED", {"goal": goal, "count": len(directives)})
        return {"status": "SUCCESS", "sub_tasks": directives}

class CreativeProductionAgent(BaseAgent):
    def __init__(self, memory: SharedIntelligenceMemory):
        super().__init__("CreativeProductionAgent", memory)

    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        prod = task.payload.get("product", "Smart Device")
        feat = task.payload.get("feature", "High Performance")
        price = task.payload.get("price", "$29.99")
        
        script_data = os_core.marketing.generate_ad_campaign(prod, feat, price)
        self.memory.set_context("latest_creatives", script_data)
        self.memory.log_event(self.agent_name, "CREATIVES_PRODUCED", script_data)
        return {"status": "SUCCESS", "assets": script_data}

class CampaignExecutionAgent(BaseAgent):
    def __init__(self, memory: SharedIntelligenceMemory):
        super().__init__("CampaignExecutionAgent", memory)

    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        channels = task.payload.get("channels", ["Meta"])
        budget = task.payload.get("allocated_budget", 1000)
        
        deployments = {}
        for ch in channels:
            deployments[ch] = {
                "status": "ACTIVE_RUNNING",
                "allocated_budget": budget / len(channels),
                "optimization": "Auto-Bidding ROI Max"
            }
            
        self.memory.set_context("live_campaigns", deployments)
        self.memory.log_event(self.agent_name, "CAMPAIGNS_DEPLOYED", deployments)
        return {"status": "SUCCESS", "deployments": deployments}

class CustomerIntelligenceAgent(BaseAgent):
    def __init__(self, memory: SharedIntelligenceMemory):
        super().__init__("CustomerIntelligenceAgent", memory)

    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        lead_score = os_core.sales.score_and_route_lead(task.payload)
        self.memory.set_context("active_persona", lead_score)
        self.memory.log_event(self.agent_name, "PERSONA_EVALUATED", lead_score)
        return {"status": "SUCCESS", "lead_score": lead_score}

class AnalyticsAgent(BaseAgent):
    def __init__(self, memory: SharedIntelligenceMemory):
        super().__init__("AnalyticsAgent", memory)

    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        live_campaigns = self.memory.get_context("live_campaigns", {})
        report = {
            "overall_roas": 4.25,
            "conversions": 189,
            "live_channels_count": len(live_campaigns),
            "status": "HEALTHY_OPTIMAL"
        }
        self.memory.set_context("analytics_report", report)
        self.memory.log_event(self.agent_name, "ANALYTICS_GENERATED", report)
        return {"status": "SUCCESS", "metrics": report}

class MultiAgentCoordinator:
    def __init__(self):
        self.memory = SharedIntelligenceMemory()
        self.agents: Dict[str, BaseAgent] = {
            "ExecutiveStrategyAgent": ExecutiveStrategyAgent(self.memory),
            "CreativeProductionAgent": CreativeProductionAgent(self.memory),
            "CampaignExecutionAgent": CampaignExecutionAgent(self.memory),
            "CustomerIntelligenceAgent": CustomerIntelligenceAgent(self.memory),
            "AnalyticsAgent": AnalyticsAgent(self.memory),
        }

    async def run_enterprise_workflow(self, strategic_goal: str, budget: float) -> Dict[str, Any]:
        strategy_task = AgentTask(
            task_id="TASK-STRAT-001",
            assigned_agent="ExecutiveStrategyAgent",
            payload={"goal": strategic_goal, "allocated_budget": budget}
        )
        strat_res = await self.agents["ExecutiveStrategyAgent"].execute_task(strategy_task)
        
        sub_tasks: List[AgentTask] = strat_res.get("sub_tasks", [])
        tasks_to_run = []
        for t in sub_tasks:
            agent = self.agents.get(t.assigned_agent)
            if agent:
                tasks_to_run.append(agent.execute_task(t))
                
        await asyncio.gather(*tasks_to_run)
        
        analytics_task = AgentTask(
            task_id="TASK-ANALYTICS-001",
            assigned_agent="AnalyticsAgent",
            payload={}
        )
        analytics_res = await self.agents["AnalyticsAgent"].execute_task(analytics_task)
        
        return {
            "report_title": "Multi-Agent Operational Log Report™",
            "timestamp": datetime.utcnow().isoformat(),
            "shared_memory_snapshot": {
                "active_persona": self.memory.get_context("active_persona"),
                "latest_creatives": self.memory.get_context("latest_creatives"),
                "live_campaigns": self.memory.get_context("live_campaigns"),
            },
            "performance_summary": analytics_res.get("metrics"),
            "full_audit_trail": self.memory.get_audit_trail()
        }


# ===========================================================================
# 4. STREAMLIT PAGE CONFIGURATION & UTILS
# ===========================================================================

st.set_page_config(page_title="AI Business OS™ Master Suite", page_icon="⚙️", layout="wide")

if "pipeline_data" not in st.session_state:
    st.session_state.pipeline_data = pd.DataFrame([
        {"Company": "TechFlow Inc", "Stage": "Negotiate", "Value ($)": 15000, "Next Action": "Send revised proposal"},
        {"Company": "ViralCart", "Stage": "Validate", "Value ($)": 8500, "Next Action": "Discovery Call"},
        {"Company": "Apex SaaS", "Stage": "Engage", "Value ($)": 22000, "Next Action": "Follow-up email"},
        {"Company": "Global Logistics", "Stage": "Unify", "Value ($)": 45000, "Next Action": "Contract signing"}
    ])

def run_ai_task(api_key: str, prompt_text: str):
    """Executes Gemini 1.5 Flash AI task or warns if missing API Key."""
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API Key in the sidebar or check 'Use Demo Mode'.")
        return None
    if genai is None:
        st.error("❌ google-generativeai library is missing. Install via `pip install google-generativeai`.")
        return None
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        st.error(f"❌ Gemini API Error: {str(e)}")
        return None


# ===========================================================================
# 5. SIDEBAR NAVIGATION
# ===========================================================================

st.sidebar.title("⚙️ AI Business OS™")
st.sidebar.caption("Unified Autonomous Operating Infrastructure")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Select System Module",
    [
        "📊 Executive Dashboard",
        "🤖 Core Monolith Engines (Ch 1-5)",
        "🎯 AI Customer Success OS (Ch 5-8)",
        "💰 AI Finance Operating System",
        "🐝 Multi-Agent Orchestrator",
        "📝 P.R.O.M.P. Engineer",
        "📈 Sales Pipeline",
        "⚡ AI Execution Systems™ (Systems 1-25)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔑 AI & Key Settings")

default_key = os.getenv("GEMINI_API_KEY", "")
api_key = st.sidebar.text_input(
    "Gemini API Key", 
    value=default_key,
    type="password", 
    help="Get free key from Google AI Studio (aistudio.google.com)"
)
use_demo = st.sidebar.checkbox("Use Demo Mode (Without API Key)", value=False)


# ===========================================================================
# 6. MODULE: EXECUTIVE DASHBOARD
# ===========================================================================

if menu == "📊 Executive Dashboard":
    st.title("📊 Executive Decision System™")
    st.caption("Track your E.X.E.C.U.T.E.™ Framework core business metrics.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Monthly Revenue", "$45,500", "+12%")
    col2.metric("Active Clients", "124", "+4 new")
    col3.metric("Lead Conversion", "18%", "-2%")
    col4.metric("AI Hours Saved", "320 hrs", "+45 hrs")
    
    st.markdown("### 📈 Revenue Trends & Financial Forecast")
    chart_data = pd.DataFrame(
        {"Revenue": [30000, 32000, 38000, 41000, 45500], "Expenses": [15000, 16000, 18000, 19000, 21000]},
        index=["Jan", "Feb", "Mar", "Apr", "May"]
    )
    st.line_chart(chart_data)

    st.markdown("### 📋 Active Executive Tasks & Action Items")
    tasks = pd.DataFrame([
        {"Task": "Review Q2 Marketing SOPs", "Assignee": "CMO", "Status": "Pending"},
        {"Task": "Approve new AI Tech Stack", "Assignee": "CEO", "Status": "In Progress"},
        {"Task": "Client Expansion Strategy", "Assignee": "Sales Head", "Status": "Completed"}
    ])
    st.dataframe(tasks, use_container_width=True)


# ===========================================================================
# 7. MODULE: CORE MONOLITH ENGINES (CH 1-5)
# ===========================================================================

elif menu == "🤖 Core Monolith Engines (Ch 1-5)":
    st.title("🤖 Core Business Python Engines (Local Execution)")
    st.caption("Run rule-based internal business algorithms built directly into the Monolith.")

    engine_tab = st.selectbox("Select Engine to Execute:", [
        "Chapter 1: Marketing Engine",
        "Chapter 2: Sales Scoring Engine",
        "Chapter 3: Content Repurposing Engine",
        "Chapter 4: Customer Support Triage Engine",
        "Chapter 5: Internal Knowledge Engine"
    ])

    if engine_tab == "Chapter 1: Marketing Engine":
        st.subheader("📢 Marketing Campaign Script Generator")
        p_name = st.text_input("Product Name", value="UltraClean Pro")
        p_feat = st.text_input("Key Feature", value="Sonic Vibration Cleaning")
        p_price = st.text_input("Price Point", value="$29.99")
        if st.button("Generate Script Brief"):
            res = os_core.marketing.generate_ad_campaign(p_name, p_feat, p_price)
            st.json(res)

    elif engine_tab == "Chapter 2: Sales Scoring Engine":
        st.subheader("🎯 Lead Qualifier & Router")
        l_name = st.text_input("Lead Name", value="Sarah Khan")
        l_role = st.selectbox("Job Title", ["Founder", "CEO", "CMO", "Manager", "Developer"])
        l_budget = st.number_input("Monthly Budget ($)", value=5000)
        l_time = st.selectbox("Timeline", ["Immediate", "1-3 Months", "Flexible"])
        if st.button("Evaluate Lead"):
            res = os_core.sales.score_and_route_lead({
                "name": l_name, "job_title": l_role, "monthly_budget": l_budget, "timeline": l_time
            })
            st.json(res)

    elif engine_tab == "Chapter 3: Content Repurposing Engine":
        st.subheader("📲 Transcript to Social Media Bundle")
        raw_text = st.text_area("Paste Raw Transcript or Thought:", value="Testing video hooks in the first 3 seconds is critical. Most ad spend is wasted on bad opening frames. Always optimize visual interrupts.")
        if st.button("Repurpose Content"):
            res = os_core.content.repurpose_transcript(raw_text)
            st.json(res)

    elif engine_tab == "Chapter 4: Customer Support Triage Engine":
        st.subheader("🎧 Support Urgency Triage & Resolver")
        c_name = st.text_input("Customer Name", value="Ali Raza")
        c_msg = st.text_area("Customer Complaint / Message:", value="My package arrived broken and I want a full refund immediately!")
        if st.button("Triage Ticket"):
            res = os_core.support.triage_and_resolve(c_name, c_msg)
            st.json(res)

    elif engine_tab == "Chapter 5: Internal Knowledge Engine":
        st.subheader("🔍 Internal SOP Knowledge Query")
        query = st.text_input("Search Policy or SOP:", value="What is our refund policy?")
        if st.button("Query Knowledge Base"):
            res = os_core.knowledge.query_knowledge_base(query)
            st.json(res)


# ===========================================================================
# 8. MODULE: AI CUSTOMER SUCCESS OS (CHAPTERS 5-8 INTEGRATED)
# ===========================================================================

elif menu == "🎯 AI Customer Success OS (Ch 5-8)":
    st.title("🎯 AI Customer Success Operating System™")
    st.caption("Automated Health Scoring, Churn Mitigation, Account Expansion, and CS Governance.")

    col1, col2 = st.columns(2)
    with col1:
        cust_id = st.text_input("Customer ID", value="CUST-1024")
        company_name = st.text_input("Company Name", value="Global Tech Logistics")
        lic_util = st.slider("License Utilization %", 0.0, 100.0, 88.5)
        login_freq = st.number_input("Logins per Week", value=42)
        open_tickets = st.number_input("Open High-Priority Tickets", value=0)
    with col2:
        nps = st.slider("NPS Score", 0, 10, 9)
        ebr = st.checkbox("Executive EBR Attended", value=True)
        renewal_days = st.number_input("Days Until Renewal", value=90)
        arr = st.number_input("Annual Recurring Revenue ($)", value=50000.0)
        contacts = st.number_input("Contact Count Last Week", value=2)

    if st.button("🚀 Analyze Customer Health & Expansion"):
        cust_data = {
            "customer_id": cust_id,
            "company_name": company_name,
            "license_utilization_pct": lic_util,
            "login_frequency_per_week": login_freq,
            "open_high_priority_tickets": open_tickets,
            "nps_score": nps,
            "executive_ebr_attended": ebr,
            "days_until_renewal": renewal_days,
            "arr_usd": arr,
            "contact_count_last_week": contacts,
            "privacy_consent": True
        }
        res = os_core.customer_success.analyze_customer(cust_data)
        st.success("✅ Customer Success Analysis Complete!")
        st.json(res)


# ===========================================================================
# 9. MODULE: AI FINANCE OPERATING SYSTEM (INTEGRATED)
# ===========================================================================

elif menu == "💰 AI Finance Operating System":
    st.title("💰 AI Finance Operating System™")
    st.caption("Cash Flow Forecasting, Expense Optimization, Pricing Engine, and Risk Governance.")

    col1, col2 = st.columns(2)
    with col1:
        mrr = st.number_input("Monthly Recurring Revenue ($)", value=120000.0)
        opex = st.number_input("Monthly Operating Expenses ($)", value=95000.0)
        cash_res = st.number_input("Current Cash Reserve ($)", value=450000.0)
    with col2:
        ar = st.number_input("Accounts Receivable ($)", value=35000.0)
        ap = st.number_input("Accounts Payable ($)", value=18000.0)
        margin = st.slider("Gross Margin %", 0.0, 100.0, 74.5)
        overdue = st.number_input("Overdue Invoices Count", value=2)

    if st.button("🚀 Run Financial Audit & Cashflow Forecast"):
        fin_data = {
            "mrr_usd": mrr,
            "opex_usd": opex,
            "cash_reserve_usd": cash_res,
            "accounts_receivable_usd": ar,
            "accounts_payable_usd": ap,
            "gross_margin_pct": margin,
            "overdue_invoices_count": overdue,
            "audit_approved": True
        }
        res = os_core.finance.analyze_finance(fin_data)
        st.success("✅ Financial Analysis & Runway Forecast Generated!")
        st.json(res)


# ===========================================================================
# 10. MODULE: MULTI-AGENT ORCHESTRATOR
# ===========================================================================

elif menu == "🐝 Multi-Agent Orchestrator":
    st.title("🐝 AI Multi-Agent Coordination Network™")
    st.caption("Autonomous workforce coordinating Strategy, Creative, Campaigns, Customer Data, and Analytics.")
    
    col1, col2 = st.columns(2)
    with col1:
        campaign_goal = st.text_input("Strategic Campaign Goal", value="ViralCart Scale Launch 2026")
    with col2:
        campaign_budget = st.number_input("Budget Allocation ($)", value=10000.0, step=1000.0)

    if st.button("🚀 Trigger Autonomous Multi-Agent Execution"):
        with st.spinner("Multi-Agent Workforce in action... Coordinating Shared Memory and Tasks."):
            coordinator = MultiAgentCoordinator()
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            agent_report = loop.run_until_complete(
                coordinator.run_enterprise_workflow(campaign_goal, campaign_budget)
            )
            
            st.success("✅ Multi-Agent Workflow Execution Complete!")
            
            t1, t2, t3 = st.tabs(["📊 Performance & Memory Snapshot", "📜 Full Audit Trail Log", "🧱 Raw JSON Output"])
            
            with t1:
                st.subheader("Shared Memory Snapshot")
                st.json(agent_report["shared_memory_snapshot"])
                st.subheader("Analytics Summary")
                st.json(agent_report["performance_summary"])
                
            with t2:
                st.subheader("System Event & Audit Trail")
                st.dataframe(pd.DataFrame(agent_report["full_audit_trail"]), use_container_width=True)
                
            with t3:
                st.json(agent_report)


# ===========================================================================
# 11. MODULE: P.R.O.M.P.T. ENGINEER
# ===========================================================================

elif menu == "📝 P.R.O.M.P.T. Engineer":
    st.title("📝 Premium Prompt Engineering System™")
    st.caption("Design enterprise-grade AI prompts using the **P.R.O.M.P.T.™ Framework**.")
    
    with st.form("prompt_builder"):
        p_purpose = st.text_input("Purpose / Business Objective", placeholder="e.g., Generate qualified B2B leads")
        r_role = st.text_input("Role", placeholder="e.g., Senior SaaS CMO")
        o_objective = st.text_input("Objective", placeholder="e.g., Write high-converting LinkedIn ad copy")
        m_market = st.text_area("Market Context", placeholder="e.g., Target audience $5M+ revenue e-commerce owners")
        p_params = st.text_input("Parameters / Constraints", placeholder="e.g., Professional tone, max 150 words, markdown format")
        
        submitted = st.form_submit_button("🚀 Generate Enterprise Prompt")
        
        if submitted:
            final_prompt = (
                f"**Act As:** {r_role if r_role else '[Role]'}\n"
                f"**Business Objective:** {p_purpose if p_purpose else '[Purpose]'}\n\n"
                f"**Task:** {o_objective if o_objective else '[Objective]'}\n\n"
                f"**Context:**\n{m_market if m_market else '[Market Context]'}\n\n"
                f"**Constraints & Parameters:**\n{p_params if p_params else '[Parameters]'}\n"
            )
            st.subheader("Generated Prompt Architecture:")
            st.code(final_prompt, language="markdown")


# ===========================================================================
# 12. MODULE: SALES PIPELINE
# ===========================================================================

elif menu == "📈 Sales Pipeline":
    st.title("📈 AI Sales & Revenue Operating System™")
    st.caption("Manage pipeline deals and trigger AI outreach.")
    
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
                st.success(f"Added {lead_name} to pipeline!")
                st.rerun()

    st.markdown("### 📊 Active Pipeline Data")
    st.dataframe(st.session_state.pipeline_data, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 🤖 Live AI Sales Assistant")
    user_prompt = st.text_area("Ask AI to draft emails or research deals:", placeholder="Draft a follow-up email for ViralCart after our validation call...")
    
    if st.button("🚀 Run Sales AI Assistant"):
        if use_demo:
            st.success("✅ Demo Response:")
            st.markdown("Subject: ViralCart Project Follow-up\n\nHi ViralCart Team,\nGreat connecting on our call today. Here is the revised proposal link...")
        else:
            context = st.session_state.pipeline_data.to_string(index=False)
            full_query = f"Pipeline Context:\n{context}\n\nUser Request: {user_prompt}"
            output = run_ai_task(api_key, full_query)
            if output:
                st.success("✅ AI Response:")
                st.markdown(output)


# ===========================================================================
# 13. MODULE: 25 AI EXECUTION SYSTEMS SUITE
# ===========================================================================

elif menu == "⚡ AI Execution Systems™ (Systems 1-25)":
    st.title("⚡ Enterprise AI Execution Library™ (Systems 1 - 25)")
    st.caption("Autonomous Operations Infrastructure Suite")
    
    system_choice = st.selectbox(
        "Select Execution Module:",
        [
            "System 1 — AI Content Production System™",
            "System 2 — AI SEO Growth System™",
            "System 3 — AI Social Media OS™",
            "System 4 — AI Customer Support OS™",
            "System 5 — AI E-commerce Growth OS™",
            "System 6 — AI Agency Operating System™",
            "System 7 — AI Executive Assistant OS™",
            "System 8 — AI HR & Recruitment OS™",
            "System 9 — AI Finance & BI OS™",
            "System 10 — AI Product & Innovation OS™",
            "System 11 — AI Knowledge Management OS™",
            "System 12 — AI Customer Intelligence OS™",
            "System 13 — AI Sales Optimization OS™",
            "System 14 — AI Marketing Intelligence OS™",
            "System 15 — AI Business Analytics OS™",
            "System 16 — AI Automation & Workflow OS™",
            "System 17 — AI Financial Intelligence OS™",
            "System 18 — AI Team Productivity OS™",
            "System 19 — AI Innovation Pipeline OS™",
            "System 20 — AI Business Scaling OS™",
            "System 21 — AI Competitive Intelligence OS™",
            "System 22 — AI Executive Leadership OS™",
            "System 23 — AI CX & Retention OS™",
            "System 24 — AI Business Security & Risk OS™",
            "System 25 — AI Business Transformation OS™"
        ]
    )
    
    st.markdown("---")
    
    sys_num = system_choice.split(" — ")[0]
    sys_title = system_choice.split(" — ")[1]
    
    st.subheader(f"{sys_num}: {sys_title}")
    input_text = st.text_area(f"Input Context / Data for {sys_title}:", placeholder="Enter specific topic, data, or objective here...")
    
    if st.button(f"Run {sys_num} Engine"):
        if use_demo:
            st.success(f"✅ Demo Output generated for {sys_title}!")
            st.markdown(f"**Status:** Successfully processed input context.\n\n**Actionable Result:** Generated optimized operational workflow using the corresponding framework.")
        else:
            prompt = f"Act as Chief Specialist for '{sys_title}'. Process the following input context and generate a complete, structured, highly actionable business execution plan: '{input_text}'"
            out = run_ai_task(api_key, prompt)
            if out:
                st.success("✅ Output Generated:")
                st.markdown(out)

if __name__ == "__main__":
    pass