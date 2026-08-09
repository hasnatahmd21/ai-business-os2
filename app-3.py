import os
import json
import re
import time
import uuid
import math
import random
import asyncio
import logging
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
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
# 🌟 VOLUME 2.0: MLOPS & INFRASTRUCTURE MODELS
# ===========================================================================

class ModelStatus(str, Enum):
    STAGING = "Staging"
    PRODUCTION = "Production"
    ARCHIVED = "Archived"

class AIModelMetadata(BaseModel):
    model_id: str
    name: str
    version: str
    accuracy_score: float = Field(..., ge=0.0, le=1.0)
    latency_ms: float
    status: ModelStatus

class MLOpsPipeline:
    """Volume 2.0: Model Deployment, Health Monitoring & Infrastructure Orchestration"""
    
    def __init__(self):
        self.registry: Dict[str, AIModelMetadata] = {
            "M-101": AIModelMetadata(
                model_id="M-101", 
                name="EnterpriseFinanceNet", 
                version="2.4.0", 
                accuracy_score=0.96, 
                latency_ms=42.5, 
                status=ModelStatus.PRODUCTION
            ),
            "M-102": AIModelMetadata(
                model_id="M-102", 
                name="ClinicalTriageModel", 
                version="1.8.1", 
                accuracy_score=0.94, 
                latency_ms=65.0, 
                status=ModelStatus.PRODUCTION
            )
        }

    def register_model(self, model: AIModelMetadata) -> Dict[str, Any]:
        self.registry[model.model_id] = model
        return {"status": "SUCCESS", "message": f"Model {model.name} (v{model.version}) registered successfully."}

    def evaluate_telemetry(self, model_id: str) -> Dict[str, Any]:
        model = self.registry.get(model_id)
        if not model:
            return {"error": "Model not found."}
        
        health = "HEALTHY" if model.latency_ms < 200 and model.accuracy_score >= 0.90 else "DEGRADED"
        return {
            "model_id": model.model_id,
            "model_name": model.name,
            "system_health": health,
            "latency": f"{model.latency_ms}ms",
            "accuracy": f"{model.accuracy_score * 100}%",
            "status": model.status.value
        }


# ===========================================================================
# 🛡️ VOLUME 3.0: AI SECURITY & ZERO-TRUST GOVERNANCE
# ===========================================================================

class SecurityGuardrail:
    """Volume 3.0: Data Anonymization, RBAC, and PII Protection Engine"""

    @staticmethod
    def sanitize_input(prompt_text: str) -> str:
        sensitive_keywords = ["SSN", "CreditCard", "Password", "CNIC", "API_KEY"]
        sanitized = prompt_text
        for kw in sensitive_keywords:
            if kw in sanitized:
                sanitized = re.sub(rf"\b{kw}\b", "[REDACTED_SENSITIVE_DATA]", sanitized, flags=re.IGNORECASE)
        return sanitized

    @staticmethod
    def verify_access_control(user_role: str, resource: str) -> bool:
        allowed_roles = {
            "Admin": ["ALL"], 
            "Clinician": ["HEALTHCARE", "SUPPORT"], 
            "FinanceOfficer": ["FINANCE", "SALES"],
            "Marketer": ["MARKETING", "CONTENT"],
            "Executive": ["STRATEGY", "GOVERNANCE", "ALL"]
        }
        permissions = allowed_roles.get(user_role, [])
        return "ALL" in permissions or resource.upper() in permissions


# ===========================================================================
# 1. CORE MONOLITH ENGINES (MARKETING, SALES, CONTENT, SUPPORT, KNOWLEDGE)
# ===========================================================================

class MarketingEngine:
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
# 2. CUSTOMER SUCCESS OS, HEALTHCARE OS & UNIFIED FINANCE ENGINE (CH 9-12)
# ===========================================================================

class CustomerSuccessEngine:
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

        usage_score = license_util * 0.35
        activity_score = min(100.0, (login_freq / 50.0) * 100.0) * 0.25
        support_score = max(0.0, 100.0 - (open_tickets * 25.0)) * 0.20
        sentiment_score = (nps / 10.0) * 100.0 * 0.20
        
        health_score = round(usage_score + activity_score + support_score + sentiment_score, 2)
        if not ebr_attended:
            health_score = max(0.0, health_score - 10.0)
        churn_risk = round(100.0 - health_score, 2)

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

        propensity_score = round((health_score * 0.6) + (license_util * 0.4), 2) if health_score >= 65 else 20.0
        expansion_type = "Seat Addition"
        estimated_upside = arr * 0.15
        if license_util >= 85.0:
            expansion_type = "Enterprise Tier Upgrade"
            estimated_upside = arr * 0.30

        advocate_score = round((health_score * 0.5) + ((nps / 10.0) * 50.0), 2)
        is_advocate = advocate_score >= 80.0 and ebr_attended
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

class HealthcareEngine:
    """
    NOTE — SAFETY DISCLAIMER:
    This module intentionally does NOT perform, simulate, or output clinical
    triage, diagnosis, urgency classification, or treatment/prescription
    content. Earlier drafts of this file included keyword-matching logic
    dressed up as clinical decision support (e.g. classifying "emergency"
    priority from a symptom checklist, or auto-generating a treatment plan).
    That is not real medical AI, and presenting it as such in a real product
    could cause a buyer or their staff to rely on it for actual patient care
    decisions — which is dangerous regardless of how the underlying code
    works. This stub exists so the rest of the app's navigation still runs;
    it deliberately refuses to produce anything that looks like clinical
    guidance. Any real healthcare workflow tooling needs to be built with
    licensed clinical input, validated data, and regulatory review — not
    as a demo feature in a general business toolkit.
    """
    @staticmethod
    def process_patient_triage(patient_id: str, symptoms: List[str], vitals: Dict[str, str]) -> Dict[str, Any]:
        return {
            "patient_id": patient_id,
            "status": "NOT_AVAILABLE",
            "message": (
                "Automated clinical triage has been intentionally disabled in this build. "
                "Symptom- or vitals-based urgency classification is a medical decision and "
                "must be made by a licensed clinician, not by this software."
            ),
        }

    @staticmethod
    def generate_clinical_soap(patient_id: str, symptoms: List[str], clinical_notes: str) -> Dict[str, Any]:
        return {
            "patient_id": patient_id,
            "status": "NOT_AVAILABLE",
            "message": (
                "Automated clinical documentation / treatment planning has been intentionally "
                "disabled in this build. Assessment and treatment plans must be written and "
                "signed by a licensed clinician, not generated by this software."
            ),
        }

class UnifiedFinanceEngine:
    def analyze_finance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        mrr = data.get("mrr_usd", 50000.0)
        opex = data.get("opex_usd", 40000.0)
        cash_res = data.get("cash_reserve_usd", 200000.0)
        ar = data.get("accounts_receivable_usd", 15000.0)
        ap = data.get("accounts_payable_usd", 8000.0)
        margin = data.get("gross_margin_pct", 75.0)
        overdue = data.get("overdue_invoices_count", 1)
        audit_approved = data.get("audit_approved", True)

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

        anomalies = []
        if margin < 65.0:
            anomalies.append("Gross Margin is below recommended 65% benchmark.")
        if mrr > 0 and (opex / mrr) > 0.8:
            anomalies.append(f"High OpEx Ratio: Expenses eat {round((opex/mrr)*100,1)}% of MRR.")

        credit_risk = "LOW_RISK"
        if overdue > 10 or margin < 50.0:
            credit_risk = "HIGH_RISK"
        elif overdue > 3:
            credit_risk = "MODERATE_RISK"

        return {
            "module": "FINANCE_OS_RUNWAY",
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

    def run_fpa_analysis(self, actual_rev: float, budget_rev: float, growth_pct: float) -> Dict[str, Any]:
        variance = actual_rev - budget_rev
        var_pct = (variance / budget_rev) * 100 if budget_rev > 0 else 0.0
        projected_next_q = actual_rev * (1 + (growth_pct / 100.0))

        return {
            "chapter": "CH_9_FPA_PREDICTIVE",
            "revenue_variance": round(variance, 2),
            "variance_percentage": f"{round(var_pct, 2)}%",
            "performance_status": "AHEAD_OF_BUDGET" if variance >= 0 else "BELOW_BUDGET",
            "projected_next_quarter_revenue": round(projected_next_q, 2)
        }

    def screen_transactions(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        flagged = []
        for tx in transactions:
            risk_score = tx.get("risk_score", 0.0)
            amount = tx.get("amount", 0.0)
            if risk_score > 0.75 or amount > 50000.0:
                flagged.append({
                    "tx_id": tx.get("tx_id"),
                    "amount": amount,
                    "reason": "High Anomaly Score (>0.75)" if risk_score > 0.75 else "Large Transaction Threshold Exceeded ($50k+)"
                })

        return {
            "chapter": "CH_10_FRAUD_RISK",
            "total_screened": len(transactions),
            "flagged_count": len(flagged),
            "flagged_details": flagged,
            "status": "CRITICAL_ATTENTION" if len(flagged) > 0 else "CLEAN"
        }

    def reconcile_ledger(self, bank_balance: float, ledger_balance: float) -> Dict[str, Any]:
        diff = abs(bank_balance - ledger_balance)
        return {
            "chapter": "CH_11_LEDGER_RECONCILIATION",
            "bank_balance": bank_balance,
            "ledger_balance": ledger_balance,
            "discrepancy": round(diff, 2),
            "reconciliation_status": "BALANCED" if diff == 0 else "DISCREPANCY_DETECTED"
        }


# ===========================================================================
# 🌐 CHAPTER 30.9: AI ENTERPRISE STRATEGY INTELLIGENCE & TRANSFORMATION ENGINE
# ===========================================================================

@dataclass
class StrategicInitiativeData:
    id: str
    name: str
    department: str
    budget: float
    target_roi: float
    current_progress: float
    risk_score: float
    status: str = "PLANNED"

@dataclass
class CompetitorProfileData:
    name: str
    market_share: float
    pricing_index: float
    tech_capability_score: float
    recent_launches: List[str]

@dataclass
class MATargetData:
    company_name: str
    valuation: float
    annual_revenue: float
    synergy_score: float
    cultural_fit: float
    tech_debt_score: float

@dataclass
class BusinessUnitData:
    name: str
    current_capital: float
    projected_growth: float
    risk_level: float

class TransformationIntelligenceModule:
    def plan_modernization_roadmap(self, legacy_systems: List[str], readiness_score: float) -> Dict[str, Any]:
        phases = []
        phase_count = 3 if readiness_score > 7.0 else 5
        for i in range(1, phase_count + 1):
            phases.append({
                "phase": f"Phase {i}",
                "target_systems": legacy_systems[(i-1)*len(legacy_systems)//phase_count : i*len(legacy_systems)//phase_count],
                "estimated_months": round(12 / phase_count, 1)
            })
        return {"readiness_score": readiness_score, "roadmap": phases}

    def change_management_analytics(self, total_workforce: int, trained_workforce: int, sentiment_index: float) -> Dict[str, Any]:
        adoption_rate = round((trained_workforce / total_workforce) * 100, 2)
        return {
            "workforce_adoption_rate": f"{adoption_rate}%",
            "sentiment_score": f"{sentiment_index}/10.0",
            "change_management_risk": "HIGH" if adoption_rate < 50.0 or sentiment_index < 5.0 else "OPTIMAL"
        }

class CompetitiveIndustryIntelligenceSystem:
    def __init__(self):
        self.competitors: List[CompetitorProfileData] = []

    def register_competitor(self, comp: CompetitorProfileData):
        self.competitors.append(comp)

    def analyze_market_landscape(self) -> Dict[str, Any]:
        if not self.competitors:
            return {"status": "NO_COMPETITOR_DATA"}
        avg_share = sum(c.market_share for c in self.competitors) / len(self.competitors)
        high_threats = [c.name for c in self.competitors if c.tech_capability_score > 8.0 and c.market_share > avg_share]
        return {
            "total_competitors_monitored": len(self.competitors),
            "threat_status": "HIGH ALERT" if high_threats else "STABLE",
            "top_threat_actors": high_threats,
            "strategic_recommendation": "Accelerate Product R&D & Dynamic Pricing" if high_threats else "Protect Core Share"
        }

class StrategicScenarioSimulationEngine:
    def simulate_product_launch_impact(self, market_size: float, investment: float, competition_factor: float) -> Dict[str, Any]:
        simulations = 1000
        successful_outcomes = 0
        total_projected_revenue = 0.0

        for _ in range(simulations):
            adoption_rate = random.uniform(0.01, 0.12) / (competition_factor * 0.5)
            market_volatility = random.uniform(0.8, 1.2)
            revenue = (market_size * adoption_rate) * market_volatility
            
            roi = ((revenue - investment) / investment) * 100
            if roi > 20.0:
                successful_outcomes += 1
            total_projected_revenue += revenue

        avg_revenue = total_projected_revenue / simulations
        return {
            "success_probability_pct": round((successful_outcomes / simulations) * 100, 2),
            "projected_avg_revenue": round(avg_revenue, 2),
            "expected_avg_roi_pct": round(((avg_revenue - investment) / investment) * 100, 2)
        }

class InnovationProductStrategyModule:
    def prioritize_rd_pipeline(self, project_proposals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for proj in project_proposals:
            score = (proj["unmet_need_score"] * proj["market_gap_score"]) / (proj["cost"] / 100000)
            proj["priority_score"] = round(score, 2)
        return sorted(project_proposals, key=lambda x: x["priority_score"], reverse=True)

class AutonomousExecutionEngine:
    def execute_and_detect_bottlenecks(self, initiatives: List[StrategicInitiativeData]) -> Dict[str, Any]:
        delayed = []
        active = 0
        for init in initiatives:
            if init.status == "EXECUTING":
                active += 1
                if init.current_progress < 30.0 and init.risk_score > 0.6:
                    init.status = "BLOCKED"
                    delayed.append(init.name)
        return {
            "active_initiatives": active,
            "blocked_initiatives": delayed,
            "auto_correction_triggered": True if delayed else False
        }

class TransformationCommandDashboard:
    def generate_dashboard(self, initiatives: List[StrategicInitiativeData], health_score: float) -> Dict[str, Any]:
        risk_map = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
        for init in initiatives:
            if init.risk_score < 0.35:
                risk_map["LOW"] += 1
            elif init.risk_score < 0.70:
                risk_map["MEDIUM"] += 1
            else:
                risk_map["HIGH"] += 1
        return {
            "transformation_health_score": f"{health_score} / 100",
            "strategic_risk_heat_map": risk_map,
            "total_initiatives": len(initiatives),
            "status": "HEALTHY" if health_score >= 70.0 else "INTERVENTION_REQUIRED"
        }

class BusinessImpactAnalyzer:
    def calculate_impact(self, capital_saved: float, speedup_ratio: float, error_reduction: float) -> Dict[str, Any]:
        return {
            "total_capital_optimized": f"${capital_saved:,.2f}",
            "execution_velocity_increase": f"{speedup_ratio}x faster",
            "operational_error_reduction": f"{error_reduction}%",
            "sustainable_growth_index": "STRONG"
        }

class MAAndPartnershipIntelligenceSystem:
    def evaluate_ma_candidate(self, target: MATargetData) -> Dict[str, Any]:
        overall_score = (target.synergy_score * 0.4) + (target.cultural_fit * 0.3) + ((10.0 - target.tech_debt_score) * 0.3)
        adjusted_val = target.valuation * (1.0 - (target.tech_debt_score * 0.03))
        return {
            "target_company": target.company_name,
            "due_diligence_score": round(overall_score, 2),
            "tech_adjusted_valuation": f"${adjusted_val:,.2f}",
            "recommendation": "PROCEED WITH ACQUISITION" if overall_score >= 6.8 else "REJECT OR RE-NEGOTIATE"
        }

class BusinessModelMonetizationEngine:
    def model_subscription_transition(self, one_time_revenue: float, monthly_user_value: float, users: int) -> Dict[str, Any]:
        arr = users * monthly_user_value * 12
        break_even = one_time_revenue / (arr / 12) if arr > 0 else 0
        return {
            "projected_ARR": round(arr, 2),
            "break_even_months": round(break_even, 1),
            "strategy": "Transition to ARR Recommended" if arr > one_time_revenue else "Maintain Hybrid Model"
        }

class CapitalAllocationEngine:
    def reallocate_capital(self, total_budget: float, business_units: List[BusinessUnitData]) -> Dict[str, Any]:
        total_score = sum(bu.projected_growth / (bu.risk_level if bu.risk_level > 0 else 0.1) for bu in business_units)
        plan = {}
        for bu in business_units:
            score = bu.projected_growth / (bu.risk_level if bu.risk_level > 0 else 0.1)
            share = score / total_score
            allocated = total_budget * share
            plan[bu.name] = {
                "allocated_capital": round(allocated, 2),
                "delta": round(allocated - bu.current_capital, 2)
            }
        return plan

class EnterpriseDigitalTwin:
    def simulate_org_restructuring(self, current_latency: float, current_layers: int, target_layers: int) -> Dict[str, Any]:
        latency_reduction = (current_layers - target_layers) * 15.0
        new_latency = max(current_latency * (1 - (latency_reduction / 100)), 10.0)
        return {
            "simulated_domain": "Organizational Restructuring",
            "previous_latency_ms": current_latency,
            "optimized_latency_ms": round(new_latency, 2),
            "productivity_gain_pct": round((current_layers - target_layers) * 8.5, 2)
        }

class RiskGovernanceLayer:
    def audit_initiative(self, initiative: StrategicInitiativeData, max_budget: float) -> Dict[str, Any]:
        reg_pass = initiative.risk_score < 0.80
        brand_pass = initiative.risk_score < 0.65
        budget_pass = initiative.budget <= max_budget
        passed = reg_pass and brand_pass and budget_pass
        return {
            "initiative_id": initiative.id,
            "governance_status": "APPROVED" if passed else "REJECTED_BY_GOVERNANCE",
            "regulatory_pass": reg_pass,
            "brand_safety_pass": brand_pass,
            "budget_pass": budget_pass
        }

class EnterpriseStrategyOrchestrator:
    def __init__(self, enterprise_name: str = "ViralCart Enterprise Systems"):
        self.enterprise_name = enterprise_name
        self.trans_intel = TransformationIntelligenceModule()
        self.comp_intel = CompetitiveIndustryIntelligenceSystem()
        self.sim_engine = StrategicScenarioSimulationEngine()
        self.innov_engine = InnovationProductStrategyModule()
        self.exec_engine = AutonomousExecutionEngine()
        self.dashboard = TransformationCommandDashboard()
        self.impact_analyzer = BusinessImpactAnalyzer()
        self.ma_engine = MAAndPartnershipIntelligenceSystem()
        self.monetization_engine = BusinessModelMonetizationEngine()
        self.capital_engine = CapitalAllocationEngine()
        self.digital_twin = EnterpriseDigitalTwin()
        self.governance = RiskGovernanceLayer()


# ===========================================================================
# 🎛️ MASTER MONOLITH + ENTERPRISE AI BUSINESS OS ORCHESTRATOR
# ===========================================================================

class AIBusinessOS:
    """Master Monolithic Orchestrator Engine combining all Volumes and Systems."""
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
        self.healthcare = HealthcareEngine()
        self.finance = UnifiedFinanceEngine()
        self.mlops = MLOpsPipeline()
        self.strategy_orchestrator = EnterpriseStrategyOrchestrator()

# Singleton Monolith Instance
os_core = AIBusinessOS()


# ===========================================================================
# 3. SHARED INTELLIGENCE MEMORY & MULTI-AGENT ARCHITECTURE (VOL 4.0)
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

st.set_page_config(page_title="AI Business OS™ Enterprise Suite v4.0", page_icon="⚙️", layout="wide")

# ===========================================================================
# 0. LANDING PAGE (embedded) — shown first, then gates into the app below
# ===========================================================================
import streamlit.components.v1 as components

_LANDING_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Enterprise Operating System™ — The Intelligence Layer For Modern Business</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root{
    --bg: #0A0C10;
    --bg-2: #0F1219;
    --panel: #141821;
    --panel-2: #1A1F2B;
    --line: rgba(230,235,245,0.09);
    --ink: #EAEEF6;
    --ink-dim: #8C93A6;
    --signal: #5B8DEF;      /* intelligence / data blue */
    --signal-2: #7C9CF6;
    --insight: #F0A93E;     /* recommendation / action amber */
    --violet: #8B7CF6;      /* architecture accent */
    --ok: #3FBF8F;
  }
  *{margin:0;padding:0;box-sizing:border-box;}
  html{scroll-behavior:smooth;}
  body{background:var(--bg); color:var(--ink); font-family:'Inter',sans-serif; -webkit-font-smoothing:antialiased; overflow-x:hidden;}
  h1,h2,h3{font-family:'Space Grotesk',sans-serif; letter-spacing:-0.01em;}
  .mono{font-family:'IBM Plex Mono',monospace;}
  a{text-decoration:none; color:inherit;}
  .wrap{max-width:1180px; margin:0 auto; padding:0 32px;}
  a:focus-visible, button:focus-visible{outline:2px solid var(--signal-2); outline-offset:3px;}
  @media (prefers-reduced-motion: reduce){
    *{animation-duration:0.01ms !important; animation-iteration-count:1 !important; transition-duration:0.01ms !important; scroll-behavior:auto !important;}
  }
  ::selection{background:rgba(91,141,239,0.35);}

  /* NAV */
  nav{position:fixed; top:0; left:0; right:0; z-index:60; background:rgba(10,12,16,0.75); backdrop-filter:blur(16px); border-bottom:1px solid var(--line);}
  nav .wrap{display:flex; align-items:center; justify-content:space-between; height:74px;}
  .logo{display:flex; align-items:center; gap:10px; font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:16.5px;}
  .logo-mark{width:26px; height:26px;}
  .navlinks{display:flex; gap:32px; font-size:13.5px; font-weight:500; color:var(--ink-dim);}
  .navlinks a:hover{color:var(--ink);}
  .nav-cta{background:var(--signal); color:#fff; font-weight:600; font-size:13.5px; padding:10px 18px; border-radius:7px; transition:background .2s;}
  .nav-cta:hover{background:var(--signal-2);}
  @media (max-width:900px){ .navlinks{display:none;} }

  /* HERO */
  header.hero{
    position:relative; padding:172px 0 120px; overflow:hidden;
    background:
      radial-gradient(900px 420px at 20% -10%, rgba(91,141,239,0.14), transparent 60%),
      radial-gradient(700px 400px at 100% 0%, rgba(139,124,246,0.10), transparent 60%),
      var(--bg);
    border-bottom:1px solid var(--line);
  }
  #net{position:absolute; inset:0; width:100%; height:100%; opacity:0.55; pointer-events:none;}
  .hero-inner{position:relative; z-index:2; text-align:center; max-width:840px; margin:0 auto;}
  .eyebrow{
    display:inline-flex; align-items:center; gap:8px; font-family:'IBM Plex Mono',monospace; font-size:12px;
    letter-spacing:0.07em; color:var(--signal-2); background:rgba(91,141,239,0.08);
    border:1px solid rgba(91,141,239,0.25); padding:7px 16px; border-radius:100px; margin-bottom:30px;
  }
  .eyebrow .dot{width:6px; height:6px; border-radius:50%; background:var(--signal-2); box-shadow:0 0 8px var(--signal-2);}
  h1.headline{font-size:clamp(32px,5vw,58px); font-weight:700; line-height:1.1; color:#fff;}
  h1.headline .grad{background:linear-gradient(90deg, var(--signal-2), var(--violet)); -webkit-background-clip:text; background-clip:text; color:transparent;}
  .sub{margin:26px auto 0; font-size:18px; line-height:1.7; color:var(--ink-dim); max-width:620px;}
  .hero-actions{display:flex; align-items:center; justify-content:center; gap:18px; margin-top:40px; flex-wrap:wrap;}
  .btn-primary{
    background:var(--signal); color:#fff; font-weight:600; font-size:15px; padding:15px 28px; border-radius:9px; border:none; cursor:pointer;
    box-shadow:0 10px 28px rgba(91,141,239,0.28); transition:transform .18s ease, background .18s ease;
  }
  .btn-primary:hover{background:var(--signal-2); transform:translateY(-2px);}
  .btn-secondary{
    color:var(--ink); font-weight:600; font-size:15px; padding:15px 26px; border-radius:9px; border:1px solid var(--line);
    transition:border-color .18s ease, background .18s ease;
  }
  .btn-secondary:hover{border-color:rgba(230,235,245,0.3); background:rgba(255,255,255,0.03);}

  /* TRUST STRIP */
  .trust{padding:44px 0; border-bottom:1px solid var(--line); background:var(--bg-2);}
  .trust .wrap{display:flex; align-items:center; justify-content:center; gap:52px; flex-wrap:wrap;}
  .trust-item{display:flex; align-items:center; gap:9px; font-size:13.5px; font-weight:500; color:var(--ink-dim);}
  .trust-item svg{flex-shrink:0; color:var(--signal-2);}
  .trust-line{text-align:center; font-family:'IBM Plex Mono',monospace; font-size:12px; letter-spacing:0.06em; color:var(--ink-dim); margin-bottom:26px; text-transform:uppercase;}

  /* SECTION generic */
  section{padding:112px 0;}
  .section-head{max-width:660px; margin-bottom:56px;}
  .section-head.center{margin-left:auto; margin-right:auto; text-align:center;}
  .kicker{font-family:'IBM Plex Mono',monospace; font-size:12px; letter-spacing:0.08em; color:var(--signal-2); text-transform:uppercase; margin-bottom:14px;}
  h2.section-title{font-size:clamp(26px,3.4vw,40px); font-weight:700; color:#fff; line-height:1.18;}
  .section-body{margin-top:16px; font-size:16px; color:var(--ink-dim); line-height:1.75;}

  /* PROBLEM / SOLUTION */
  .ps-grid{display:grid; grid-template-columns:1fr 1fr; gap:24px;}
  @media (max-width:860px){ .ps-grid{grid-template-columns:1fr;} }
  .ps-card{border:1px solid var(--line); border-radius:16px; padding:36px;}
  .ps-card.before{background:var(--panel);}
  .ps-card.after{background:linear-gradient(180deg, rgba(91,141,239,0.08), var(--panel)); border-color:rgba(91,141,239,0.3);}
  .ps-card h3{font-size:18px; font-weight:600; color:#fff; margin-bottom:22px;}
  .ps-list{list-style:none; display:flex; flex-direction:column; gap:14px;}
  .ps-list li{display:flex; gap:12px; font-size:14.5px; color:var(--ink-dim); line-height:1.5; align-items:flex-start;}
  .ps-list .x{color:#E0637A; flex-shrink:0; margin-top:2px;}
  .ps-list .ok{color:var(--ok); flex-shrink:0; margin-top:2px;}
  .ps-note{margin-top:28px; font-size:15px; color:var(--ink-dim); line-height:1.6; text-align:center;}
  .ps-note strong{color:var(--ink); font-weight:600;}

  /* ARCHITECTURE — signature element */
  .arch-section{background:var(--bg-2); border-top:1px solid var(--line); border-bottom:1px solid var(--line);}
  .arch-wrap{display:flex; justify-content:center;}
  .arch-stack{display:flex; flex-direction:column; align-items:center; position:relative; padding:20px 0;}
  .arch-line{position:absolute; top:36px; bottom:36px; left:50%; width:2px; background:linear-gradient(180deg, var(--signal), var(--violet), var(--signal)); opacity:0.35; transform:translateX(-50%);}
  .arch-pulse-track{position:absolute; top:36px; bottom:36px; left:50%; width:2px; transform:translateX(-50%);}
  .arch-node{
    position:relative; z-index:2; width:min(480px, 88vw); background:var(--panel); border:1px solid var(--line); border-radius:12px;
    padding:16px 22px; margin:9px 0; display:flex; align-items:center; justify-content:space-between; gap:14px;
    transition:border-color .2s, background .2s;
  }
  .arch-node.top{background:linear-gradient(135deg, rgba(91,141,239,0.16), rgba(139,124,246,0.12)); border-color:rgba(91,141,239,0.4);}
  .arch-node:not(.top):hover{border-color:rgba(91,141,239,0.4); background:var(--panel-2);}
  .arch-node .name{font-weight:600; font-size:14.5px; color:var(--ink);}
  .arch-node.top .name{font-size:16px; color:#fff;}
  .arch-node .tag{font-family:'IBM Plex Mono',monospace; font-size:10.5px; color:var(--ink-dim); letter-spacing:0.04em;}
  .arch-chevron{color:var(--ink-dim); opacity:0.5; margin:2px 0;}

  /* FEATURE MODULES */
  .mod-grid{display:grid; grid-template-columns:repeat(4,1fr); gap:1px; background:var(--line); border:1px solid var(--line); border-radius:16px; overflow:hidden;}
  @media (max-width:980px){ .mod-grid{grid-template-columns:repeat(2,1fr);} }
  @media (max-width:600px){ .mod-grid{grid-template-columns:1fr;} }
  .mod{background:var(--bg); padding:30px 26px; transition:background .2s;}
  .mod:hover{background:var(--panel);}
  .mod-icon{width:38px; height:38px; border-radius:9px; background:rgba(91,141,239,0.10); border:1px solid rgba(91,141,239,0.25); display:flex; align-items:center; justify-content:center; margin-bottom:18px; color:var(--signal-2);}
  .mod h3{font-size:15.5px; font-weight:600; color:#fff; margin-bottom:9px;}
  .mod p{font-size:13.5px; color:var(--ink-dim); line-height:1.6;}

  /* DASHBOARD PREVIEW */
  .dash-section{background:var(--bg-2); border-top:1px solid var(--line); border-bottom:1px solid var(--line);}
  .dash-frame{
    background:var(--panel); border:1px solid var(--line); border-radius:18px; padding:24px; box-shadow:0 40px 80px -40px rgba(0,0,0,0.6);
  }
  .dash-topbar{display:flex; align-items:center; justify-content:space-between; margin-bottom:22px; padding-bottom:18px; border-bottom:1px solid var(--line);}
  .dash-topbar .l{font-family:'IBM Plex Mono',monospace; font-size:12px; color:var(--ink-dim); letter-spacing:0.04em;}
  .dash-dots{display:flex; gap:6px;}
  .dash-dots span{width:8px; height:8px; border-radius:50%; background:var(--line);}
  .dash-grid{display:grid; grid-template-columns:1.2fr 1fr; gap:18px;}
  @media (max-width:860px){ .dash-grid{grid-template-columns:1fr;} }
  .dash-col{display:flex; flex-direction:column; gap:18px;}
  .dcard{background:var(--panel-2); border:1px solid var(--line); border-radius:12px; padding:20px;}
  .dcard .lbl{font-family:'IBM Plex Mono',monospace; font-size:11px; color:var(--ink-dim); letter-spacing:0.05em; text-transform:uppercase; margin-bottom:12px;}
  .health-ring{display:flex; align-items:center; gap:20px;}
  .health-num{font-family:'Space Grotesk',sans-serif; font-size:40px; font-weight:700; color:#fff;}
  .health-num span{font-size:15px; color:var(--ink-dim); font-weight:500;}
  .health-bar{flex:1; height:6px; background:var(--line); border-radius:100px; overflow:hidden;}
  .health-fill{width:92%; height:100%; background:linear-gradient(90deg, var(--signal), var(--ok));}
  .chart-bars{display:flex; align-items:flex-end; gap:6px; height:70px; margin-top:14px;}
  .chart-bars div{flex:1; background:linear-gradient(180deg, var(--signal-2), rgba(91,141,239,0.25)); border-radius:3px 3px 0 0;}
  .rec-card{border-left:3px solid var(--insight); background:rgba(240,169,62,0.06);}
  .rec-card .lbl{color:var(--insight);}
  .rec-card p{font-size:13.5px; color:var(--ink); line-height:1.6;}
  .sec-status{display:flex; align-items:center; gap:10px; font-size:13.5px; color:var(--ink);}
  .sec-status .ok-dot{width:8px; height:8px; border-radius:50%; background:var(--ok); box-shadow:0 0 8px var(--ok);}
  .alert-list{display:flex; flex-direction:column; gap:10px;}
  .alert-list li{list-style:none; font-size:12.5px; color:var(--ink-dim); display:flex; gap:8px; align-items:flex-start;}
  .alert-list li::before{content:''; width:5px; height:5px; border-radius:50%; background:var(--signal-2); margin-top:6px; flex-shrink:0;}

  /* WORKFLOW */
  .flow-row{display:flex; align-items:stretch; gap:0; overflow-x:auto; padding-bottom:8px;}
  .flow-step{flex:1; min-width:170px; padding:26px 20px; position:relative;}
  .flow-step .num{font-family:'IBM Plex Mono',monospace; font-size:12px; color:var(--signal-2); margin-bottom:14px;}
  .flow-step h3{font-size:15.5px; font-weight:600; color:#fff; margin-bottom:8px;}
  .flow-step p{font-size:13px; color:var(--ink-dim); line-height:1.55;}
  .flow-arrow{display:flex; align-items:center; color:var(--ink-dim); opacity:0.4; padding:0 4px;}
  @media (max-width:860px){ .flow-row{flex-direction:column;} .flow-arrow{display:none;} .flow-step{border-bottom:1px solid var(--line); padding:20px 0;} }

  /* INDUSTRIES */
  .ind-grid{display:grid; grid-template-columns:repeat(4,1fr); gap:20px;}
  @media (max-width:980px){ .ind-grid{grid-template-columns:1fr 1fr;} }
  @media (max-width:560px){ .ind-grid{grid-template-columns:1fr;} }
  .ind-card{background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:26px;}
  .ind-card h3{font-size:16px; font-weight:600; color:#fff; margin-bottom:14px;}
  .ind-card ul{list-style:none; display:flex; flex-direction:column; gap:8px;}
  .ind-card li{font-size:13px; color:var(--ink-dim); padding-left:14px; position:relative;}
  .ind-card li::before{content:'—'; position:absolute; left:0; color:var(--signal-2);}

  /* PRICING */
  .price-grid{display:grid; grid-template-columns:repeat(3,1fr); gap:20px;}
  @media (max-width:900px){ .price-grid{grid-template-columns:1fr;} }
  .price-card{border:1px solid var(--line); border-radius:16px; padding:34px 28px; background:var(--panel); display:flex; flex-direction:column; position:relative;}
  .price-card.hi{border-color:rgba(91,141,239,0.5); background:linear-gradient(180deg, rgba(91,141,239,0.08), var(--panel));}
  .price-tag{position:absolute; top:-13px; left:28px; background:var(--signal); color:#fff; font-size:10.5px; font-weight:700; padding:5px 12px; border-radius:100px; letter-spacing:0.03em;}
  .price-card h3{font-size:20px; font-weight:700; color:#fff; margin-bottom:6px;}
  .price-for{font-size:13px; color:var(--ink-dim); margin-bottom:24px;}
  .price-feats{list-style:none; display:flex; flex-direction:column; gap:12px; margin-bottom:28px; flex:1;}
  .price-feats li{display:flex; gap:10px; font-size:13.5px; color:var(--ink); align-items:flex-start;}
  .price-feats li svg{flex-shrink:0; margin-top:3px; color:var(--signal-2);}
  .price-btn{text-align:center; padding:13px; border-radius:9px; font-weight:600; font-size:14px; border:1px solid var(--line); color:var(--ink);}
  .price-card.hi .price-btn{background:var(--signal); color:#fff; border:none;}

  /* FAQ */
  .faq-list{display:flex; flex-direction:column;}
  .faq-item{border-top:1px solid var(--line);}
  .faq-item:last-child{border-bottom:1px solid var(--line);}
  .faq-q{width:100%; text-align:left; background:none; border:none; padding:24px 0; display:flex; justify-content:space-between; align-items:center; gap:20px; cursor:pointer; color:var(--ink); font-family:'Space Grotesk',sans-serif; font-size:16px; font-weight:600;}
  .faq-q .plus{flex-shrink:0; color:var(--signal-2); transition:transform .25s ease;}
  .faq-item.open .plus{transform:rotate(45deg);}
  .faq-a{max-height:0; overflow:hidden; transition:max-height .3s ease;}
  .faq-a p{padding-bottom:24px; font-size:14.5px; color:var(--ink-dim); line-height:1.7; max-width:760px;}
  .faq-item.open .faq-a{max-height:300px;}

  /* CTA band */
  .cta-band{background:radial-gradient(700px 340px at 50% 0%, rgba(91,141,239,0.14), transparent 60%), var(--bg-2); border-top:1px solid var(--line); border-bottom:1px solid var(--line); padding:104px 0; text-align:center;}
  .cta-band h2{font-size:clamp(28px,4.2vw,44px); color:#fff; max-width:680px; margin:0 auto;}
  .cta-band p{color:var(--ink-dim); margin-top:18px; font-size:16px; max-width:560px; margin-left:auto; margin-right:auto;}
  .cta-band .hero-actions{justify-content:center; margin-top:36px;}

  /* FOOTER */
  footer{padding:56px 0 40px;}
  .foot-grid{display:flex; justify-content:space-between; align-items:flex-start; gap:40px; flex-wrap:wrap; padding-bottom:36px; border-bottom:1px solid var(--line);}
  .foot-cols{display:flex; gap:60px; flex-wrap:wrap;}
  .foot-col h4{font-size:12.5px; color:var(--ink); margin-bottom:14px; text-transform:uppercase; letter-spacing:0.04em;}
  .foot-col a{display:block; font-size:13.5px; color:var(--ink-dim); margin-bottom:10px;}
  .foot-col a:hover{color:var(--ink);}
  .foot-bottom{display:flex; justify-content:space-between; align-items:center; padding-top:26px; font-size:12px; color:var(--ink-dim); flex-wrap:wrap; gap:12px;}

  .reveal{opacity:0; transform:translateY(18px); transition:opacity .7s ease, transform .7s ease;}
  .reveal.in{opacity:1; transform:translateY(0);}
</style>
</head>
<body>

<nav>
  <div class="wrap">
    <div class="logo">
      <svg class="logo-mark" viewBox="0 0 26 26" fill="none"><rect width="26" height="26" rx="6" fill="url(#g1)"/><path d="M7 17.5V8.5L13 14L19 8.5V17.5" stroke="#0A0C10" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><defs><linearGradient id="g1" x1="0" y1="0" x2="26" y2="26"><stop stop-color="#5B8DEF"/><stop offset="1" stop-color="#8B7CF6"/></linearGradient></defs></svg>
      AI Enterprise OS™
    </div>
    <div class="navlinks">
      <a href="#architecture">Architecture</a>
      <a href="#modules">Modules</a>
      <a href="#dashboard">Dashboard</a>
      <a href="#pricing">Pricing</a>
      <a href="#faq">FAQ</a>
    </div>
    <a href="#pricing" class="nav-cta">Request Early Access</a>
  </div>
</nav>

<header class="hero">
  <canvas id="net"></canvas>
  <div class="wrap hero-inner">
    <div class="eyebrow"><span class="dot"></span> AI ENTERPRISE OPERATING SYSTEM™</div>
    <h1 class="headline">The Intelligent Operating System <span class="grad">Built For The Future of Business</span></h1>
    <p class="sub">One AI layer that connects revenue, customers, marketing, sales, operations, and security — turning scattered business data into understanding, recommendations, and automated action.</p>
    <div class="hero-actions">
      <button class="btn-primary">Request Early Access</button>
      <a href="#modules" class="btn-secondary">Explore AI Capabilities</a>
    </div>
  </div>
</header>

<div class="trust">
  <div class="wrap" style="flex-direction:column; gap:20px;">
    <div class="trust-line">Built for the next generation of intelligent businesses</div>
    <div style="display:flex; justify-content:center; gap:52px; flex-wrap:wrap;">
      <div class="trust-item"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 1L9.8 6.2L15 8L9.8 9.8L8 15L6.2 9.8L1 8L6.2 6.2L8 1Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg> AI Intelligence</div>
      <div class="trust-item"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 1.5L14 4V8C14 11.5 11.5 13.8 8 14.5C4.5 13.8 2 11.5 2 8V4L8 1.5Z" stroke="currentColor" stroke-width="1.4"/></svg> Enterprise Security</div>
      <div class="trust-item"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6.2" stroke="currentColor" stroke-width="1.4"/><path d="M8 5V8L10 9.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg> Automation</div>
      <div class="trust-item"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M2 14V9M7 14V2M12 14V6" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg> Data Analytics</div>
      <div class="trust-item"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M1.5 12.5L6 8L9 11L14.5 4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg> Growth Optimization</div>
    </div>
  </div>
</div>

<section id="problem-solution">
  <div class="wrap">
    <div class="section-head center reveal">
      <div class="kicker">The Shift</div>
      <h2 class="section-title">Businesses have more data than ever. Most still lack intelligence.</h2>
      <p class="section-body">Traditional software stores information. AI Enterprise Operating System™ transforms it into decisions.</p>
    </div>
    <div class="ps-grid reveal">
      <div class="ps-card before">
        <h3>Before AI Enterprise OS™</h3>
        <ul class="ps-list">
          <li><span class="x">✕</span> Data scattered across disconnected platforms</li>
          <li><span class="x">✕</span> Manual decision-making and slow reporting</li>
          <li><span class="x">✕</span> Missed revenue and growth opportunities</li>
          <li><span class="x">✕</span> Repetitive tasks consuming team time</li>
          <li><span class="x">✕</span> Rising, unmonitored security risks</li>
        </ul>
      </div>
      <div class="ps-card after">
        <h3>After AI Enterprise OS™</h3>
        <ul class="ps-list">
          <li><span class="ok">✓</span> One unified intelligence layer across the business</li>
          <li><span class="ok">✓</span> Real-time insights instead of manual analysis</li>
          <li><span class="ok">✓</span> AI-surfaced revenue and growth opportunities</li>
          <li><span class="ok">✓</span> Automated workflows handling routine work</li>
          <li><span class="ok">✓</span> Continuous digital protection and risk alerts</li>
        </ul>
      </div>
    </div>
    <p class="ps-note reveal">Traditional software: <strong>Data → Reports → Human Analysis → Decision.</strong><br>AI Enterprise Operating System™: <strong>Data → AI Understanding → Recommendation → Automated Action.</strong></p>
  </div>
</section>

<section id="architecture" class="arch-section">
  <div class="wrap">
    <div class="section-head center reveal">
      <div class="kicker">System Architecture</div>
      <h2 class="section-title">One operating system. Eight intelligence layers.</h2>
      <p class="section-body">Every layer runs independently, but reports into the same intelligence core — so the business is understood as one connected system, not a set of separate tools.</p>
    </div>
    <div class="arch-wrap reveal">
      <div class="arch-stack">
        <div class="arch-line"></div>
        <div class="arch-node top"><span class="name">AI Enterprise Operating System™</span><span class="tag">CORE</span></div>
        <svg class="arch-chevron" width="14" height="8" viewBox="0 0 14 8" fill="none"><path d="M1 1L7 7L13 1" stroke="currentColor" stroke-width="1.4"/></svg>
        <div class="arch-node"><span class="name">AI Executive Decision Intelligence™</span><span class="tag">LAYER 01</span></div>
        <svg class="arch-chevron" width="14" height="8" viewBox="0 0 14 8" fill="none"><path d="M1 1L7 7L13 1" stroke="currentColor" stroke-width="1.4"/></svg>
        <div class="arch-node"><span class="name">AI Revenue Intelligence™</span><span class="tag">LAYER 02</span></div>
        <svg class="arch-chevron" width="14" height="8" viewBox="0 0 14 8" fill="none"><path d="M1 1L7 7L13 1" stroke="currentColor" stroke-width="1.4"/></svg>
        <div class="arch-node"><span class="name">AI Customer Intelligence™</span><span class="tag">LAYER 03</span></div>
        <svg class="arch-chevron" width="14" height="8" viewBox="0 0 14 8" fill="none"><path d="M1 1L7 7L13 1" stroke="currentColor" stroke-width="1.4"/></svg>
        <div class="arch-node"><span class="name">AI Marketing Intelligence™</span><span class="tag">LAYER 04</span></div>
        <svg class="arch-chevron" width="14" height="8" viewBox="0 0 14 8" fill="none"><path d="M1 1L7 7L13 1" stroke="currentColor" stroke-width="1.4"/></svg>
        <div class="arch-node"><span class="name">AI Sales Intelligence™</span><span class="tag">LAYER 05</span></div>
        <svg class="arch-chevron" width="14" height="8" viewBox="0 0 14 8" fill="none"><path d="M1 1L7 7L13 1" stroke="currentColor" stroke-width="1.4"/></svg>
        <div class="arch-node"><span class="name">AI Operations Intelligence™</span><span class="tag">LAYER 06</span></div>
        <svg class="arch-chevron" width="14" height="8" viewBox="0 0 14 8" fill="none"><path d="M1 1L7 7L13 1" stroke="currentColor" stroke-width="1.4"/></svg>
        <div class="arch-node"><span class="name">AI Cybersecurity &amp; Digital Trust Intelligence™</span><span class="tag">LAYER 07</span></div>
      </div>
    </div>
  </div>
</section>

<section id="modules">
  <div class="wrap">
    <div class="section-head reveal">
      <div class="kicker">Capabilities</div>
      <h2 class="section-title">Every business function, understood by AI.</h2>
      <p class="section-body">Each module works on its own, or together as one connected ecosystem — from a single dashboard.</p>
    </div>
    <div class="mod-grid reveal">
      <div class="mod">
        <div class="mod-icon"><svg width="18" height="18" viewBox="0 0 18 18" fill="none"><rect x="2" y="2" width="14" height="14" rx="3" stroke="currentColor" stroke-width="1.5"/><path d="M6 9H12M9 6V12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
        <h3>Business Intelligence Core™</h3>
        <p>Unifies revenue, customer, marketing, operations, and security data into one intelligence engine with a single Business Health Score.</p>
      </div>
      <div class="mod">
        <div class="mod-icon"><svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M2 15L7 9L10.5 12L16 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
        <h3>Revenue Intelligence™</h3>
        <p>Tracks revenue performance, forecasts future sales, and surfaces upsell, cross-sell, and pricing opportunities automatically.</p>
      </div>
      <div class="mod">
        <div class="mod-icon"><svg width="18" height="18" viewBox="0 0 18 18" fill="none"><circle cx="9" cy="6.5" r="3" stroke="currentColor" stroke-width="1.5"/><path d="M3.5 15C3.5 12 6 10 9 10C12 10 14.5 12 14.5 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
        <h3>Customer Intelligence™</h3>
        <p>Segments customers by value and behavior, and predicts lifetime value and repeat-purchase probability.</p>
      </div>
      <div class="mod">
        <div class="mod-icon"><svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M2 9C2 5.7 5 3 9 3C13 3 16 5.7 16 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M4.5 9C4.5 6.8 6.5 5 9 5C11.5 5 13.5 6.8 13.5 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><circle cx="9" cy="9" r="1.6" fill="currentColor"/></svg></div>
        <h3>Marketing Intelligence™</h3>
        <p>Analyzes campaign performance, discovers ideal audiences, and recommends content and channel improvements.</p>
      </div>
      <div class="mod">
        <div class="mod-icon"><svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M3 15L8 10L11 13L15 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M11 6H15V10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
        <h3>Sales Intelligence™</h3>
        <p>Scores and ranks leads by purchase probability, and gives sales teams AI-generated follow-up guidance.</p>
      </div>
      <div class="mod">
        <div class="mod-icon"><svg width="18" height="18" viewBox="0 0 18 18" fill="none"><rect x="2.5" y="4" width="13" height="10" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M5.5 7.5H12.5M5.5 10.5H9.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
        <h3>Operations Intelligence™</h3>
        <p>Finds workflow bottlenecks, automates routine tasks, and lets teams build custom AI-powered workflows.</p>
      </div>
      <div class="mod">
        <div class="mod-icon"><svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M9 2L15 4.5V9C15 12.5 12.5 15 9 15.8C5.5 15 3 12.5 3 9V4.5L9 2Z" stroke="currentColor" stroke-width="1.5"/></svg></div>
        <h3>Cybersecurity &amp; Digital Trust™</h3>
        <p>Continuously monitors for threats, access anomalies, and compliance risk — with early, proactive alerts.</p>
      </div>
      <div class="mod">
        <div class="mod-icon"><svg width="18" height="18" viewBox="0 0 18 18" fill="none"><rect x="2" y="3" width="14" height="9" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M6 15.5H12M9 12V15.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
        <h3>Executive Decision Intelligence™</h3>
        <p>Gives leadership a single business overview, strategic recommendations, and an AI advisor for direct questions.</p>
      </div>
    </div>
  </div>
</section>

<section id="dashboard" class="dash-section">
  <div class="wrap">
    <div class="section-head reveal">
      <div class="kicker">Business Command Center™</div>
      <h2 class="section-title">Everything your business needs, in one intelligent dashboard.</h2>
      <p class="section-body">Not a wall of charts — a command center built to turn business information into clear, ranked decisions.</p>
    </div>
    <div class="dash-frame reveal">
      <div class="dash-topbar">
        <span class="l">OVERVIEW · Business Command Center™</span>
        <div class="dash-dots"><span></span><span></span><span></span></div>
      </div>
      <div class="dash-grid">
        <div class="dash-col">
          <div class="dcard">
            <div class="lbl">Business Health Score</div>
            <div class="health-ring">
              <div class="health-num">92<span>/100</span></div>
              <div class="health-bar"><div class="health-fill"></div></div>
            </div>
          </div>
          <div class="dcard">
            <div class="lbl">Revenue Overview</div>
            <div class="chart-bars">
              <div style="height:35%"></div><div style="height:48%"></div><div style="height:40%"></div>
              <div style="height:62%"></div><div style="height:55%"></div><div style="height:78%"></div>
              <div style="height:70%"></div><div style="height:92%"></div>
            </div>
          </div>
          <div class="dcard rec-card">
            <div class="lbl">AI Recommendation</div>
            <p>"Customer retention decreased by 8%. Launch a re-engagement campaign for inactive high-value customers."</p>
          </div>
        </div>
        <div class="dash-col">
          <div class="dcard">
            <div class="lbl">Security Center</div>
            <div class="sec-status"><span class="ok-dot"></span> All systems protected</div>
          </div>
          <div class="dcard">
            <div class="lbl">Business Alerts</div>
            <ul class="alert-list">
              <li>New growth opportunity identified in Product A segment</li>
              <li>Checkout conversion dropped 4% this week</li>
              <li>Marketing campaign #3 outperforming benchmark by 22%</li>
            </ul>
          </div>
          <div class="dcard">
            <div class="lbl">Automation Center</div>
            <div class="sec-status"><span class="ok-dot" style="background:var(--signal-2); box-shadow:0 0 8px var(--signal-2);"></span> 14 workflows active · 3 pending review</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="workflow">
  <div class="wrap">
    <div class="section-head center reveal">
      <div class="kicker">How It Works</div>
      <h2 class="section-title">From business data to intelligent action.</h2>
    </div>
    <div class="flow-row reveal">
      <div class="flow-step"><div class="num">01</div><h3>Connect</h3><p>Link your existing business systems and data sources — no migration required.</p></div>
      <div class="flow-arrow"><svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M2 9H16M16 9L11 4M16 9L11 14" stroke="currentColor" stroke-width="1.5"/></svg></div>
      <div class="flow-step"><div class="num">02</div><h3>Understand</h3><p>AI analyzes performance, customers, and operations to learn how your business actually runs.</p></div>
      <div class="flow-arrow"><svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M2 9H16M16 9L11 4M16 9L11 14" stroke="currentColor" stroke-width="1.5"/></svg></div>
      <div class="flow-step"><div class="num">03</div><h3>Recommend</h3><p>Receive prioritized, plain-language recommendations grounded in your real data.</p></div>
      <div class="flow-arrow"><svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M2 9H16M16 9L11 4M16 9L11 14" stroke="currentColor" stroke-width="1.5"/></svg></div>
      <div class="flow-step"><div class="num">04</div><h3>Automate</h3><p>Turn recommendations into AI-powered workflows that run without manual work.</p></div>
      <div class="flow-arrow"><svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M2 9H16M16 9L11 4M16 9L11 14" stroke="currentColor" stroke-width="1.5"/></svg></div>
      <div class="flow-step"><div class="num">05</div><h3>Grow</h3><p>Use continuous intelligence to improve decisions and scale with confidence.</p></div>
    </div>
  </div>
</section>

<section id="industries" style="background:var(--bg-2); border-top:1px solid var(--line); border-bottom:1px solid var(--line);">
  <div class="wrap">
    <div class="section-head reveal">
      <div class="kicker">Built For</div>
      <h2 class="section-title">Every growth stage, one operating system.</h2>
    </div>
    <div class="ind-grid reveal">
      <div class="ind-card">
        <h3>E-commerce</h3>
        <ul><li>Sales &amp; conversion optimization</li><li>Customer retention</li><li>Product-level intelligence</li></ul>
      </div>
      <div class="ind-card">
        <h3>SMEs &amp; Startups</h3>
        <ul><li>Affordable business intelligence</li><li>Workflow automation</li><li>Growth &amp; scaling guidance</li></ul>
      </div>
      <div class="ind-card">
        <h3>SaaS Companies</h3>
        <ul><li>Customer retention analytics</li><li>Growth &amp; churn intelligence</li><li>Revenue forecasting</li></ul>
      </div>
      <div class="ind-card">
        <h3>Enterprise</h3>
        <ul><li>Multi-department intelligence</li><li>Advanced security &amp; compliance</li><li>Executive decision support</li></ul>
      </div>
    </div>
  </div>
</section>

<section id="pricing">
  <div class="wrap">
    <div class="section-head center reveal">
      <div class="kicker">Pricing</div>
      <h2 class="section-title">Plans that scale with your business.</h2>
      <p class="section-body">Every plan starts with early access onboarding. Enterprise pricing is custom.</p>
    </div>
    <div class="price-grid reveal">
      <div class="price-card">
        <h3>Starter</h3>
        <div class="price-for">For small businesses starting with AI</div>
        <ul class="price-feats">
          <li><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L5.5 10.5L12 3.5" stroke="currentColor" stroke-width="1.6"/></svg> AI Business Intelligence Core</li>
          <li><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L5.5 10.5L12 3.5" stroke="currentColor" stroke-width="1.6"/></svg> Business Health Dashboard</li>
          <li><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L5.5 10.5L12 3.5" stroke="currentColor" stroke-width="1.6"/></svg> Basic analytics &amp; AI reports</li>
          <li><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L5.5 10.5L12 3.5" stroke="currentColor" stroke-width="1.6"/></svg> Core recommendations</li>
        </ul>
        <a href="#" class="price-btn">Request Early Access</a>
      </div>
      <div class="price-card hi">
        <div class="price-tag">MOST POPULAR</div>
        <h3>Growth</h3>
        <div class="price-for">For businesses focused on scaling</div>
        <ul class="price-feats">
          <li><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L5.5 10.5L12 3.5" stroke="currentColor" stroke-width="1.6"/></svg> Everything in Starter</li>
          <li><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L5.5 10.5L12 3.5" stroke="currentColor" stroke-width="1.6"/></svg> Revenue &amp; Customer Intelligence</li>
          <li><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L5.5 10.5L12 3.5" stroke="currentColor" stroke-width="1.6"/></svg> Marketing &amp; Sales Intelligence</li>
          <li><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L5.5 10.5L12 3.5" stroke="currentColor" stroke-width="1.6"/></svg> Advanced automation</li>
        </ul>
        <a href="#" class="price-btn">Request Early Access</a>
      </div>
      <div class="price-card">
        <h3>Enterprise</h3>
        <div class="price-for">For large organizations</div>
        <ul class="price-feats">
          <li><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L5.5 10.5L12 3.5" stroke="currentColor" stroke-width="1.6"/></svg> Everything in Growth</li>
          <li><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L5.5 10.5L12 3.5" stroke="currentColor" stroke-width="1.6"/></svg> Cybersecurity Intelligence</li>
          <li><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L5.5 10.5L12 3.5" stroke="currentColor" stroke-width="1.6"/></svg> Custom AI workflows &amp; integrations</li>
          <li><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L5.5 10.5L12 3.5" stroke="currentColor" stroke-width="1.6"/></svg> Dedicated enterprise support</li>
        </ul>
        <a href="#" class="price-btn">Talk to Sales</a>
      </div>
    </div>
  </div>
</section>

<section id="faq" style="background:var(--bg-2); border-top:1px solid var(--line); border-bottom:1px solid var(--line);">
  <div class="wrap">
    <div class="section-head reveal">
      <div class="kicker">FAQ</div>
      <h2 class="section-title">Common questions</h2>
    </div>
    <div class="faq-list reveal">
      <div class="faq-item">
        <button class="faq-q">Is this an AI chatbot, or something more?<span class="plus"><svg width="16" height="16" viewBox="0 0 16 16"><path d="M8 2V14M2 8H14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></span></button>
        <div class="faq-a"><p>AI Enterprise Operating System™ is a full business operating layer, not a single chatbot. It connects revenue, customer, marketing, sales, operations, and security intelligence into one system, with an AI advisor as just one part of it.</p></div>
      </div>
      <div class="faq-item">
        <button class="faq-q">What do I need to connect to get started?<span class="plus"><svg width="16" height="16" viewBox="0 0 16 16"><path d="M8 2V14M2 8H14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></span></button>
        <div class="faq-a"><p>You connect your existing business systems — e-commerce platforms, CRM, marketing tools, or analytics platforms. There's no need to migrate data; the AI reads what you already have.</p></div>
      </div>
      <div class="faq-item">
        <button class="faq-q">How long before I see AI recommendations?<span class="plus"><svg width="16" height="16" viewBox="0 0 16 16"><path d="M8 2V14M2 8H14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></span></button>
        <div class="faq-a"><p>After connecting your data, the AI Learning Phase analyzes your business and generates your first Business Intelligence Report, covering revenue, customers, operations, and security.</p></div>
      </div>
      <div class="faq-item">
        <button class="faq-q">Does it replace my existing tools?<span class="plus"><svg width="16" height="16" viewBox="0 0 16 16"><path d="M8 2V14M2 8H14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></span></button>
        <div class="faq-a"><p>No — it sits above your existing systems as an intelligence and automation layer, so you keep the tools you already use while gaining a unified, AI-powered view across all of them.</p></div>
      </div>
      <div class="faq-item">
        <button class="faq-q">Is my business data secure?<span class="plus"><svg width="16" height="16" viewBox="0 0 16 16"><path d="M8 2V14M2 8H14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></span></button>
        <div class="faq-a"><p>Enterprise trust is a core principle of the platform. The Cybersecurity &amp; Digital Trust Intelligence layer continuously monitors access, activity, and risk across your connected systems.</p></div>
      </div>
      <div class="faq-item">
        <button class="faq-q">Can the platform grow with my business?<span class="plus"><svg width="16" height="16" viewBox="0 0 16 16"><path d="M8 2V14M2 8H14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></span></button>
        <div class="faq-a"><p>Yes. It's designed to scale from small businesses to large enterprises — from the Starter plan through custom Enterprise deployments with advanced integrations and dedicated support.</p></div>
      </div>
    </div>
  </div>
</section>

<div class="cta-band">
  <div class="wrap">
    <h2 class="reveal">Build the future of your business with AI intelligence.</h2>
    <p class="reveal">Move beyond disconnected tools. Deploy one intelligent operating system designed for modern business growth.</p>
    <div class="hero-actions reveal">
      <button class="btn-primary">Request Early Access</button>
    </div>
  </div>
</div>

<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div class="logo">
        <svg class="logo-mark" viewBox="0 0 26 26" fill="none"><rect width="26" height="26" rx="6" fill="url(#g2)"/><path d="M7 17.5V8.5L13 14L19 8.5V17.5" stroke="#0A0C10" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><defs><linearGradient id="g2" x1="0" y1="0" x2="26" y2="26"><stop stop-color="#5B8DEF"/><stop offset="1" stop-color="#8B7CF6"/></linearGradient></defs></svg>
        AI Enterprise OS™
      </div>
      <div class="foot-cols">
        <div class="foot-col">
          <h4>Platform</h4>
          <a href="#architecture">Architecture</a>
          <a href="#modules">Modules</a>
          <a href="#dashboard">Dashboard</a>
          <a href="#pricing">Pricing</a>
        </div>
        <div class="foot-col">
          <h4>Company</h4>
          <a href="#">About</a>
          <a href="#">Contact</a>
          <a href="#">Careers</a>
        </div>
        <div class="foot-col">
          <h4>Legal</h4>
          <a href="#">Privacy</a>
          <a href="#">Terms</a>
        </div>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© 2026 AI Enterprise Operating System™. All rights reserved.</span>
      <span>The intelligence layer behind modern business.</span>
    </div>
  </div>
</footer>

<script>
  // reveal on scroll
  const io = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('in'); } });
  }, {threshold:0.12});
  document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

  // FAQ accordion
  document.querySelectorAll('.faq-item').forEach(item=>{
    item.querySelector('.faq-q').addEventListener('click', ()=>{
      const isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(o=>o.classList.remove('open'));
      if(!isOpen) item.classList.add('open');
    });
  });

  // Ambient network canvas in hero
  const canvas = document.getElementById('net');
  const ctx = canvas.getContext('2d');
  let w, h, points;
  function resize(){
    w = canvas.width = canvas.offsetWidth;
    h = canvas.height = canvas.offsetHeight;
  }
  function initPoints(){
    const count = Math.min(46, Math.floor(w/28));
    points = Array.from({length:count}, ()=>({
      x: Math.random()*w, y: Math.random()*h,
      vx:(Math.random()-0.5)*0.25, vy:(Math.random()-0.5)*0.25
    }));
  }
  function step(){
    if(!document.body.contains(canvas)) return;
    ctx.clearRect(0,0,w,h);
    for(const p of points){
      p.x += p.vx; p.y += p.vy;
      if(p.x<0||p.x>w) p.vx*=-1;
      if(p.y<0||p.y>h) p.vy*=-1;
    }
    for(let i=0;i<points.length;i++){
      for(let j=i+1;j<points.length;j++){
        const dx=points[i].x-points[j].x, dy=points[i].y-points[j].y;
        const dist=Math.sqrt(dx*dx+dy*dy);
        if(dist<120){
          ctx.strokeStyle = `rgba(91,141,239,${0.14*(1-dist/120)})`;
          ctx.lineWidth=1;
          ctx.beginPath(); ctx.moveTo(points[i].x,points[i].y); ctx.lineTo(points[j].x,points[j].y); ctx.stroke();
        }
      }
    }
    for(const p of points){
      ctx.fillStyle='rgba(124,156,246,0.55)';
      ctx.beginPath(); ctx.arc(p.x,p.y,1.6,0,Math.PI*2); ctx.fill();
    }
    requestAnimationFrame(step);
  }
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  window.addEventListener('resize', ()=>{ resize(); initPoints(); });
  resize(); initPoints();
  if(!reduceMotion) requestAnimationFrame(step);

  // ---- App launch wiring ----
  // These CTA buttons break out of this embedded frame and reload the
  // real Streamlit app with ?entered_app=true, which the Python side
  // reads to unlock the dashboard.
  document.querySelectorAll('.btn-primary, .price-btn, .btn-secondary, .nav-cta').forEach(el => {
    el.style.cursor = 'pointer';
    el.addEventListener('click', (e) => {
      e.preventDefault();
      const target = window.top || window.parent;
      const base = target.location.href.split('?')[0].split('#')[0];
      target.location.href = base + '?entered_app=true';
    });
  });
</script>

</body>
</html>
"""

if "entered_app" not in st.session_state:
    st.session_state.entered_app = False

def _get_query_params():
    try:
        return dict(st.query_params)
    except Exception:
        try:
            return st.experimental_get_query_params()
        except Exception:
            return {}

def _clear_query_params():
    try:
        st.query_params.clear()
    except Exception:
        try:
            st.experimental_set_query_params()
        except Exception:
            pass

_qp = _get_query_params()
_qp_val = _qp.get("entered_app")
if isinstance(_qp_val, list):
    _qp_val = _qp_val[0] if _qp_val else None
if _qp_val == "true":
    st.session_state.entered_app = True
    _clear_query_params()

def _enter_app_cb():
    st.session_state.entered_app = True

def _back_to_landing_cb():
    st.session_state.entered_app = False

if not st.session_state.entered_app:
    components.html(_LANDING_HTML, height=4600, scrolling=True)
    st.markdown("<div style='max-width:880px;margin:0 auto;padding:0 32px 60px;'>", unsafe_allow_html=True)
    st.button("🚀 Enter the App", use_container_width=True, type="primary", on_click=_enter_app_cb, key="enter_app_btn")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

st.sidebar.button("← Back to landing page", on_click=_back_to_landing_cb, key="back_to_landing_btn")
st.sidebar.markdown("---")



if "pipeline_data" not in st.session_state:
    st.session_state.pipeline_data = pd.DataFrame([
        {"Company": "TechFlow Inc", "Stage": "Negotiate", "Value ($)": 15000, "Next Action": "Send revised proposal"},
        {"Company": "ViralCart", "Stage": "Validate", "Value ($)": 8500, "Next Action": "Discovery Call"},
        {"Company": "Apex SaaS", "Stage": "Engage", "Value ($)": 22000, "Next Action": "Follow-up email"},
        {"Company": "Global Logistics", "Stage": "Unify", "Value ($)": 45000, "Next Action": "Contract signing"}
    ])

def run_ai_task(api_key: str, prompt_text: str):
    """Executes Gemini AI task or warns if missing API Key."""
    sanitized_prompt = SecurityGuardrail.sanitize_input(prompt_text)
    
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API Key in the sidebar or check 'Use Demo Mode'.")
        return None
    if genai is None:
        st.error("❌ google-generativeai library is missing. Install via `pip install google-generativeai`.")
        return None
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(sanitized_prompt)
        return response.text
    except Exception as e:
        st.error(f"❌ Gemini API Error: {str(e)}")
        return None


# ===========================================================================
# 5. SIDEBAR NAVIGATION
# ===========================================================================

st.sidebar.title("⚙️ AI Business OS™")
st.sidebar.caption("Master Enterprise Autonomous Infrastructure")
st.sidebar.caption("⚠️ Business planning & automation toolkit. Not licensed medical, legal, financial, or accounting advice.")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Select System Module",
    [
        "📊 Executive Dashboard",
        "🌐 Chapter 30.9: Enterprise Strategy OS™",
        "🤖 Core Monolith Engines (Ch 1-5)",
        "🎯 AI Customer Success OS (Ch 5-8)",
        "💰 AI Finance OS (Ch 9-12 Complete)",
        "🏥 AI Healthcare OS (Vol 5.0)",
        "🛠️ MLOps & Telemetry (Vol 2.0)",
        "🛡️ AI Security & Governance (Vol 3.0)",
        "🐝 Multi-Agent Orchestrator (Vol 4.0)",
        "📝 P.R.O.M.P.T. Engineer",
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
    help="Get free key from Google AI Studio"
)
use_demo = st.sidebar.checkbox("Use Demo Mode (Without API Key)", value=False)


# ===========================================================================
# 6. MODULE: EXECUTIVE DASHBOARD
# ===========================================================================

if menu == "📊 Executive Dashboard":
    st.title("📊 Executive Decision System™")
    st.caption("Track your E.X.E.C.U.T.E.™ Framework core business metrics.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Monthly Revenue", "$125,500", "+18%")
    col2.metric("Active Clients", "142", "+8 new")
    col3.metric("Lead Conversion", "22%", "+4%")
    col4.metric("AI Hours Saved", "480 hrs", "+65 hrs")
    
    st.markdown("### 📈 Revenue Trends & Financial Forecast")
    chart_data = pd.DataFrame(
        {"Revenue": [80000, 92000, 105000, 118000, 125500], "Expenses": [35000, 38000, 42000, 45000, 48000]},
        index=["Jan", "Feb", "Mar", "Apr", "May"]
    )
    st.line_chart(chart_data)

    st.markdown("### 📋 Active Executive Tasks & Action Items")
    tasks = pd.DataFrame([
        {"Task": "Review Q3 FP&A Variance Analysis", "Assignee": "CFO", "Status": "In Progress"},
        {"Task": "Review Q3 Customer Success Health Scores", "Assignee": "VP Customer Success", "Status": "Pending"},
        {"Task": "Execute Multi-Agent Marketing Launch", "Assignee": "CMO", "Status": "Completed"}
    ])
    st.dataframe(tasks, use_container_width=True)


# ===========================================================================
# 🌐 MODULE: CHAPTER 30.9 ENTERPRISE STRATEGY OS™
# ===========================================================================

elif menu == "🌐 Chapter 30.9: Enterprise Strategy OS™":
    st.title("🌐 Chapter 30.9 — AI Enterprise Strategy Intelligence™")
    st.caption("Autonomous Business Transformation, Scenario Simulation, Digital Twin & Governance Framework.")

    strat_tab = st.tabs([
        "🚀 Strategic Scenario Twin", 
        "📊 Capital Allocation", 
        "🔍 Competitor & M&A Intelligence", 
        "⚙️ Autonomous Execution & Risk"
    ])

    # 1. Scenario Twin & Simulation
    with strat_tab[0]:
        st.subheader("30.9.6 & 30.9.14 — Digital Twin & Market Scenario Engine")
        col1, col2 = st.columns(2)
        with col1:
            m_size = st.number_input("Target Market Size ($)", value=10000000.0)
            invest = st.number_input("R&D / Expansion Budget ($)", value=500000.0)
            comp_idx = st.slider("Competitor Resistance Index (1-10)", 1.0, 10.0, 6.5)
        with col2:
            current_lat = st.number_input("Current Org Latency (ms)", value=120.0)
            cur_layers = st.slider("Current Org Layers", 3, 10, 7)
            tar_layers = st.slider("Target Org Layers", 2, 8, 4)

        if st.button("🚀 Run Monte Carlo Launch & Digital Twin Sim"):
            sim_res = os_core.strategy_orchestrator.sim_engine.simulate_product_launch_impact(m_size, invest, comp_idx)
            twin_res = os_core.strategy_orchestrator.digital_twin.simulate_org_restructuring(current_lat, cur_layers, tar_layers)
            
            st.success("✅ Simulation Completed Successfully!")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("### Market Launch Probabilities")
                st.json(sim_res)
            with c2:
                st.markdown("### Digital Twin Org Impact")
                st.json(twin_res)

    # 2. Capital Allocation Engine
    with strat_tab[1]:
        st.subheader("30.9.13 — Strategic Portfolio & Capital Allocation Engine")
        tot_budget = st.number_input("Total Reallocation Budget ($)", value=1000000.0)
        
        st.markdown("#### Business Unit Vectors")
        bu1_name = st.text_input("Unit 1 Name", value="Digital E-Commerce")
        bu1_cap = st.number_input("Unit 1 Capital ($)", value=300000.0)
        bu1_gr = st.number_input("Unit 1 Growth Rate %", value=35.0)
        bu1_risk = st.slider("Unit 1 Risk (0-1)", 0.0, 1.0, 0.25)
        
        bu2_name = st.text_input("Unit 2 Name", value="Legacy Wholesale")
        bu2_cap = st.number_input("Unit 2 Capital ($)", value=400000.0)
        bu2_gr = st.number_input("Unit 2 Growth Rate %", value=8.0)
        bu2_risk = st.slider("Unit 2 Risk (0-1)", 0.0, 1.0, 0.65)

        if st.button("⚖️ Optimize Risk-Adjusted Capital Split"):
            units = [
                BusinessUnitData(bu1_name, bu1_cap, bu1_gr, bu1_risk),
                BusinessUnitData(bu2_name, bu2_cap, bu2_gr, bu2_risk)
            ]
            alloc_res = os_core.strategy_orchestrator.capital_engine.reallocate_capital(tot_budget, units)
            st.json(alloc_res)

    # 3. Competitor & M&A Intelligence
    with strat_tab[2]:
        st.subheader("30.9.5 & 30.9.11 — Market Threats & M&A Valuation")
        sub_c1, sub_c2 = st.columns(2)
        with sub_c1:
            st.markdown("#### Competitor Threat Check")
            c_name = st.text_input("Competitor Name", value="Alpha Tech Ltd")
            c_share = st.number_input("Market Share %", value=32.0)
            c_tech = st.slider("Tech Score", 1.0, 10.0, 8.8)
            if st.button("Evaluate Threat Level"):
                os_core.strategy_orchestrator.comp_intel.register_competitor(
                    CompetitorProfileData(c_name, c_share, 1.0, c_tech, ["AI Core"])
                )
                st.json(os_core.strategy_orchestrator.comp_intel.analyze_market_landscape())

        with sub_c2:
            st.markdown("#### M&A Target Due Diligence")
            target_co = st.text_input("Target Company", value="CloudCore Software")
            val = st.number_input("Valuation ($)", value=3000000.0)
            syn = st.slider("Synergy Score", 1.0, 10.0, 8.5)
            tech_debt = st.slider("Tech Debt Score (Lower is better)", 1.0, 10.0, 3.0)
            if st.button("Run M&A Due Diligence"):
                ma_target = MATargetData(target_co, val, val*0.3, syn, 7.5, tech_debt)
                st.json(os_core.strategy_orchestrator.ma_engine.evaluate_ma_candidate(ma_target))

    # 4. Autonomous Execution & Risk
    with strat_tab[3]:
        st.subheader("30.9.8 & 30.9.15 — Execution Bottlenecks & Governance")
        init_name = st.text_input("Initiative Name", value="Autonomous Supply Chain AI")
        init_budget = st.number_input("Initiative Budget ($)", value=450000.0)
        init_prog = st.slider("Current Progress %", 0.0, 100.0, 20.0)
        init_risk = st.slider("Initiative Risk Index", 0.0, 1.0, 0.75)

        if st.button("⚡ Audit Risk & Check Execution Status"):
            init_obj = StrategicInitiativeData("INIT-101", init_name, "Ops", init_budget, 30.0, init_prog, init_risk, "EXECUTING")
            gov_res = os_core.strategy_orchestrator.governance.audit_initiative(init_obj, max_budget=500000.0)
            exec_res = os_core.strategy_orchestrator.exec_engine.execute_and_detect_bottlenecks([init_obj])
            
            st.json({"governance_audit": gov_res, "execution_pipeline": exec_res})


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
# 9. MODULE: AI FINANCE OS (CHAPTERS 9-12 COMPLETE)
# ===========================================================================

elif menu == "💰 AI Finance OS (Ch 9-12 Complete)":
    st.title("💰 AI Finance Operating System™ (Chapters 9 - 12)")
    st.caption("FP&A Predictive Forecasting, Fraud Screening, Smart Reconciliation & Runway Engine.")
    st.info("ℹ️ These are transparent, rule-based calculators for planning purposes — not licensed accounting, audit, or fraud-detection software.")

    fin_sub_tab = st.tabs(["📊 Runway & Cashflow", "📈 Chapter 9: FP&A Variance", "🛡️ Chapter 10: Fraud Screening", "⚖️ Chapter 11: Ledger Reconciliation"])

    with fin_sub_tab[0]:
        col1, col2 = st.columns(2)
        with col1:
            mrr = st.number_input("Monthly Revenue ($)", value=150000.0)
            opex = st.number_input("Operating Costs ($)", value=95000.0)
            cash_res = st.number_input("Cash Reserves ($)", value=500000.0)
        with col2:
            ar = st.number_input("Accounts Receivable ($)", value=45000.0)
            ap = st.number_input("Accounts Payable ($)", value=20000.0)
            margin = st.slider("Gross Margin %", 0.0, 100.0, 78.0)

        if st.button("🚀 Run Cashflow & Runway Analysis"):
            res = os_core.finance.analyze_finance({
                "mrr_usd": mrr, "opex_usd": opex, "cash_reserve_usd": cash_res,
                "accounts_receivable_usd": ar, "accounts_payable_usd": ap, "gross_margin_pct": margin
            })
            st.json(res)

    with fin_sub_tab[1]:
        st.subheader("Chapter 9: Predictive FP&A Engine")
        act_rev = st.number_input("Actual Revenue ($)", value=1250000.0)
        bud_rev = st.number_input("Budgeted Revenue ($)", value=1100000.0)
        growth_p = st.number_input("Projected Growth Rate %", value=12.5)
        if st.button("Calculate FP&A Variance"):
            fpa_res = os_core.finance.run_fpa_analysis(act_rev, bud_rev, growth_p)
            st.json(fpa_res)

    with fin_sub_tab[2]:
        st.subheader("Chapter 10: Algorithmic Fraud & Risk Screening")
        tx_id = st.text_input("Transaction ID", value="TX-9902")
        tx_amt = st.number_input("Transaction Amount ($)", value=65000.0)
        tx_risk = st.slider("Risk Anomaly Score (0=Low, 1=High)", 0.0, 1.0, 0.88)
        if st.button("Screen Transaction Risk"):
            tx_data = [{"tx_id": tx_id, "amount": tx_amt, "risk_score": tx_risk}]
            fraud_res = os_core.finance.screen_transactions(tx_data)
            st.json(fraud_res)

    with fin_sub_tab[3]:
        st.subheader("Chapter 11: Automated Ledger Reconciliation")
        bank_b = st.number_input("Bank Statement Balance ($)", value=250000.0)
        ledger_b = st.number_input("Internal Ledger Balance ($)", value=250000.0)
        if st.button("Reconcile Ledger"):
            rec_res = os_core.finance.reconcile_ledger(bank_b, ledger_b)
            st.json(rec_res)


# ===========================================================================
# 10. MODULE: AI HEALTHCARE OS (VOLUME 5.0)
# ===========================================================================

elif menu == "🏥 AI Healthcare OS (Vol 5.0)":
    st.title("🏥 Healthcare Module")
    st.error(
        "⚠️ Disabled by design. Automated clinical triage and treatment/documentation "
        "generation are not offered in this product. Classifying patient urgency or "
        "drafting treatment plans is a licensed clinical judgment — software that does "
        "this without a real clinician and regulatory oversight can cause real harm. "
        "If you need clinical decision-support tooling, it should be built separately "
        "with licensed medical professionals and proper validation, not as a demo "
        "feature in a general business toolkit."
    )
    st.caption("The buttons below are left in place only to show where this would sit in the navigation.")

    h_tab1, h_tab2 = st.tabs(["🚑 Clinical Triage", "📋 SOAP Note Generator"])

    with h_tab1:
        st.subheader("Automated Patient Triage Evaluation")
        pt_id = st.text_input("Patient ID", value="PT-8821")
        pt_symptoms = st.multiselect("Symptoms", ["Chest Pain", "Shortness of breath", "High Fever", "Headache", "Cough"], default=["Chest Pain", "Shortness of breath"])
        bp = st.text_input("Blood Pressure", value="140/90")
        pulse = st.text_input("Pulse Rate", value="102 bpm")
        
        if st.button("Evaluate Triage Urgency"):
            triage_res = os_core.healthcare.process_patient_triage(pt_id, pt_symptoms, {"BP": bp, "Pulse": pulse})
            st.json(triage_res)

    with h_tab2:
        st.subheader("AI-Assisted SOAP Clinical Note")
        pt_notes = st.text_area("Doctor/Clinician Observation Notes:", value="Patient reports acute discomfort in the chest occurring after moderate activity.")
        if st.button("Generate SOAP Documentation"):
            soap_res = os_core.healthcare.generate_clinical_soap(pt_id, pt_symptoms, pt_notes)
            st.json(soap_res)


# ===========================================================================
# 11. MODULE: MLOPS & TELEMETRY (VOLUME 2.0)
# ===========================================================================

elif menu == "🛠️ MLOps & Telemetry (Vol 2.0)":
    st.title("🛠️ MLOps & Model Infrastructure Registry™")
    st.caption("Monitor deployed AI models, latency telemetry, and system degradation.")
    st.info("ℹ️ Sample/demo data — this registry is preloaded with illustrative model entries, not live production models.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Deployed Models Registry")
        for m_id, m_data in os_core.mlops.registry.items():
            st.info(f"**Model:** {m_data.name} (v{m_data.version})\n- **Latency:** {m_data.latency_ms}ms\n- **Accuracy:** {m_data.accuracy_score*100}%\n- **Status:** {m_data.status.value}")

    with col2:
        st.subheader("Evaluate Telemetry Health")
        selected_m = st.selectbox("Select Model ID", list(os_core.mlops.registry.keys()))
        if st.button("Run Telemetry Diagnostic"):
            diag = os_core.mlops.evaluate_telemetry(selected_m)
            st.json(diag)


# ===========================================================================
# 12. MODULE: AI SECURITY & GOVERNANCE (VOLUME 3.0)
# ===========================================================================

elif menu == "🛡️ AI Security & Governance (Vol 3.0)":
    st.title("🛡️ Zero-Trust AI Security & Data Anonymization™")
    st.caption("Test Zero-Trust RBAC Access Controls and PII Prompt Masking.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔒 PII Data Masking Tester")
        test_prompt = st.text_area("Input Prompt with Sensitive Data:", value="User SSN is 123-45-6789 and Password is MySecretPassword123.")
        if st.button("Sanitize Prompt"):
            sanitized = SecurityGuardrail.sanitize_input(test_prompt)
            st.success("Sanitized Result:")
            st.code(sanitized)

    with col2:
        st.subheader("🔑 Role-Based Access Control (RBAC)")
        u_role = st.selectbox("Select User Role", ["Admin", "Clinician", "FinanceOfficer", "Marketer", "Executive"])
        target_res = st.selectbox("Target Domain Resource", ["HEALTHCARE", "FINANCE", "MARKETING", "STRATEGY"])
        if st.button("Check Access Rights"):
            is_allowed = SecurityGuardrail.verify_access_control(u_role, target_res)
            if is_allowed:
                st.success(f"✅ Access GRANTED for {u_role} to access {target_res}.")
            else:
                st.error(f"❌ Access DENIED for {u_role} to access {target_res}.")


# ===========================================================================
# 13. MODULE: MULTI-AGENT ORCHESTRATOR (VOLUME 4.0)
# ===========================================================================

elif menu == "🐝 Multi-Agent Orchestrator (Vol 4.0)":
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
# 14. MODULE: P.R.O.M.P.T. ENGINEER
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
# 15. MODULE: SALES PIPELINE
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
# 16. MODULE: 25 AI EXECUTION SYSTEMS SUITE
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
            "System 25 — AI Business Transformation OS™ (Ch 30.9 Integrated)"
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
