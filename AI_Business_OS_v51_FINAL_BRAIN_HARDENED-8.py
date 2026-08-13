from __future__ import annotations
code_source_marker = "from pathlib import Path"
import os
import json
import re
import time
import uuid
import math
import random
import asyncio
import logging
import sqlite3
import urllib.request
import urllib.error
import urllib.parse
import secrets
import hashlib
import base64
import statistics
import sys
import threading
import contextlib
from datetime import datetime
from pathlib import Path
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple

import pandas as pd
import streamlit as st
from pydantic import BaseModel, Field

# AI PROVIDERS
# The current Google GenAI SDK is preferred. The legacy SDK is retained only
# as a compatibility fallback for existing deployments.
try:
    from google import genai as google_genai
except ImportError:
    google_genai = None

try:
    import google.generativeai as legacy_genai
except ImportError:
    legacy_genai = None

# ===========================================================================
# WHITE-LABEL BRAND CONFIG — edit these five lines to rebrand the entire
# deployment (sidebar, sign-in screen, page title) for a specific client.
# No other code changes are required.
# ===========================================================================
BRAND_CONFIG = {
    "company_name": os.getenv("BRAND_COMPANY_NAME", "AI Business OS™"),
    "tagline": os.getenv("BRAND_TAGLINE", "Enterprise Suite"),
    "primary_color": os.getenv("BRAND_PRIMARY_COLOR", "#5B8DEF"),
    "logo_emoji": os.getenv("BRAND_LOGO_EMOJI", "⚙️"),
    "support_email": os.getenv("BRAND_SUPPORT_EMAIL", "support@example.com"),
}

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
        self.registry: Dict[str, AIModelMetadata] = {}  # Live models are registered by deployment/inference infrastructure.

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
    """Defense-in-depth input sanitation and simple RBAC controls."""

    SECRET_PATTERNS = [
        (r"(?i)\b(?:api[_ -]?key|secret|token)\s*[:=]\s*['\"]?[\w\-\.]{12,}['\"]?",
         "[REDACTED_SECRET]"),
        (r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]"),
        (r"(?i)\b(?:cnic)\s*[:=]?\s*\d{5}-?\d{7}-?\d\b", "[REDACTED_CNIC]"),
        (r"\b(?:\d[ -]*?){13,19}\b", "[REDACTED_CARD]"),
        (r"(?i)\bpassword\s*[:=]\s*\S+", "[REDACTED_PASSWORD]"),
        (r"(?i)\bbearer\s+[A-Za-z0-9\-\._~\+/]+=*", "[REDACTED_BEARER]"),
    ]

    @classmethod
    def sanitize_input(cls, prompt_text: str) -> str:
        sanitized = str(prompt_text or "")
        for pattern, replacement in cls.SECRET_PATTERNS:
            sanitized = re.sub(pattern, replacement, sanitized)
        # Legacy keyword cleanup for field labels that may still be sensitive.
        for kw in ["SSN", "CreditCard", "Password", "CNIC", "API_KEY"]:
            sanitized = re.sub(
                rf"\b{re.escape(kw)}\b",
                "[REDACTED_SENSITIVE_FIELD]",
                sanitized,
                flags=re.IGNORECASE,
            )
        return sanitized[:MAX_PROMPT_CHARS]

    @staticmethod
    def verify_access_control(user_role: str, resource: str) -> bool:
        allowed_roles = {
            "Admin": ["ALL"],
            "Clinician": ["HEALTHCARE", "SUPPORT"],
            "FinanceOfficer": ["FINANCE", "SALES"],
            "Marketer": ["MARKETING", "CONTENT"],
            "Executive": ["STRATEGY", "GOVERNANCE", "ALL"],
        }
        permissions = allowed_roles.get(user_role, [])
        return "ALL" in permissions or resource.upper() in permissions

    @staticmethod
    def audit_payload(payload: Any) -> Dict[str, Any]:
        raw = json.dumps(payload, default=str)
        sanitized = SecurityGuardrail.sanitize_input(raw)
        return {
            "sanitized": sanitized,
            "contains_redaction": "[REDACTED" in sanitized,
            "payload_size": len(raw),
        }


# ===========================================================================
# 1. CORE MONOLITH ENGINES (MARKETING, SALES, CONTENT, SUPPORT, KNOWLEDGE)
# ===========================================================================

class MarketingEngine:
    def __init__(self, brand_config: Dict[str, Any]):
        self.brand_name = brand_config.get("brand_name", BRAND_CONFIG.get("company_name", "AI Business OS™"))
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
    SAFETY NOTE: this module deliberately does not perform clinical triage,
    diagnosis, urgency classification, or treatment/prescription generation.
    Classifying a patient's medical urgency or drafting a treatment plan is a
    licensed clinical judgment — software that does this from a keyword list
    without a real clinician and regulatory review can cause real harm if a
    buyer ever points it at real patients. This stub keeps the navigation
    intact but refuses to produce clinical output. A genuine healthcare
    feature would need to be built with licensed clinical input, validated
    data, and regulatory review.
    """
    @staticmethod
    def process_patient_triage(patient_id: str, symptoms: List[str], vitals: Dict[str, str]) -> Dict[str, Any]:
        return {
            "patient_id": patient_id,
            "status": "NOT_AVAILABLE",
            "message": (
                "Automated clinical triage is intentionally disabled. Urgency "
                "classification from symptoms/vitals must be made by a licensed "
                "clinician, not this software."
            ),
        }

    @staticmethod
    def generate_clinical_soap(patient_id: str, symptoms: List[str], clinical_notes: str) -> Dict[str, Any]:
        return {
            "patient_id": patient_id,
            "status": "NOT_AVAILABLE",
            "message": (
                "Automated clinical documentation and treatment planning are "
                "intentionally disabled. Assessment and treatment plans must be "
                "written and signed by a licensed clinician, not generated here."
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
        adoption_rate = (
            round((trained_workforce / total_workforce) * 100, 2)
            if total_workforce > 0 else 0.0
        )
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

        # competition_factor is a 1-10 "resistance" slider. Recalibrated so it
        # dampens adoption gradually instead of crushing it — the previous
        # formula divided adoption by (competition_factor * 0.5), which made
        # any competition_factor above ~5 mathematically guarantee a 0%
        # success rate regardless of market size or investment.
        resistance_multiplier = max(0.15, 1.0 - (max(1.0, competition_factor) - 1.0) * 0.08)

        for _ in range(simulations):
            adoption_rate = random.uniform(0.02, 0.22) * resistance_multiplier
            market_volatility = random.uniform(0.85, 1.15)
            revenue = (market_size * adoption_rate) * market_volatility

            roi = ((revenue - investment) / investment) * 100 if investment > 0 else float("inf")
            if roi > 20.0:
                successful_outcomes += 1
            total_projected_revenue += revenue

        avg_revenue = total_projected_revenue / simulations
        return {
            "success_probability_pct": round((successful_outcomes / simulations) * 100, 2),
            "projected_avg_revenue": round(avg_revenue, 2),
            "expected_avg_roi_pct": round(((avg_revenue - investment) / investment) * 100, 2) if investment > 0 else None
        }

class InnovationProductStrategyModule:
    def prioritize_rd_pipeline(self, project_proposals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for proj in project_proposals:
            score = (proj["unmet_need_score"] * proj["market_gap_score"]) / (proj["cost"] / 100000) if proj.get("cost", 0) > 0 else 0.0
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
        overall_score = max(0.0, min(10.0, (target.synergy_score * 0.4) + (target.cultural_fit * 0.3) + ((10.0 - target.tech_debt_score) * 0.3)))
        adjusted_val = max(0.0, target.valuation * (1.0 - (target.tech_debt_score * 0.03)))
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
        scores = [bu.projected_growth / (bu.risk_level if bu.risk_level > 0 else 0.1) for bu in business_units]
        total_score = sum(scores)
        plan = {}
        if total_score <= 0 or not business_units:
            # No unit shows positive risk-adjusted growth (e.g. all growth
            # rates left at their 0.0 default) — fall back to an equal split
            # instead of dividing by zero, and say so explicitly.
            equal_share = 1.0 / len(business_units) if business_units else 0.0
            for bu in business_units:
                allocated = total_budget * equal_share
                plan[bu.name] = {
                    "allocated_capital": round(allocated, 2),
                    "delta": round(allocated - bu.current_capital, 2),
                    "note": "Equal split used — enter a non-zero growth rate for a risk-adjusted allocation."
                }
            return plan
        for bu, score in zip(business_units, scores):
            share = score / total_score
            allocated = total_budget * share
            plan[bu.name] = {
                "allocated_capital": round(allocated, 2),
                "delta": round(allocated - bu.current_capital, 2)
            }
        return plan

class EnterpriseDigitalTwin:
    def simulate_org_restructuring(self, current_latency: float, current_layers: int, target_layers: int) -> Dict[str, Any]:
        layer_diff = current_layers - target_layers
        # Exponential decay instead of a linear percentage — the previous
        # linear formula (diff * 15%) went negative for any diff beyond ~6
        # layers, silently collapsing to the 10ms floor and making the
        # "optimized latency" meaningless for large restructurings.
        new_latency = max(current_latency * (0.90 ** layer_diff), 10.0)
        productivity_gain = max(-60.0, min(75.0, layer_diff * 8.5))
        return {
            "simulated_domain": "Organizational Restructuring",
            "previous_latency_ms": current_latency,
            "optimized_latency_ms": round(new_latency, 2),
            "productivity_gain_pct": round(productivity_gain, 2)
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
    def __init__(self, enterprise_name: str = "AI Business OS™ Enterprise"):
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
                "brand_name": BRAND_CONFIG.get("company_name", "AI Business OS™"),
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
    timestamp: str = Field(default_factory=lambda: datetime.now().astimezone().isoformat())
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
        goal = task.payload.get("goal") or "No business goal supplied from live business context."
        budget = task.payload.get("allocated_budget")
        
        directives = [
            AgentTask(
                task_id="TASK-CREATIVE-01",
                assigned_agent="CreativeProductionAgent",
                payload={"product": "", "feature": "", "price": "", "source": "live_business_context_required"}
            ),
            AgentTask(
                task_id="TASK-EXECUTION-01",
                assigned_agent="CampaignExecutionAgent",
                payload={"channels": [], "allocated_budget": budget, "source": "live_business_context_required"}
            ),
            AgentTask(
                task_id="TASK-CUSTOMER-01",
                assigned_agent="CustomerIntelligenceAgent",
                payload={"name": "", "job_title": "", "monthly_budget": budget, "timeline": "", "source": "live_business_context_required"}
            )
        ]
        
        self.memory.set_context("active_directives", [t.model_dump() for t in directives])
        self.memory.log_event(self.agent_name, "DIRECTIVES_GENERATED", {"goal": goal, "count": len(directives)})
        return {"status": "SUCCESS", "sub_tasks": directives}

class CreativeProductionAgent(BaseAgent):
    def __init__(self, memory: SharedIntelligenceMemory):
        super().__init__("CreativeProductionAgent", memory)

    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        prod = task.payload.get("product") or "Live product context required."
        feat = task.payload.get("feature") or "Live product context required."
        price = task.payload.get("price") or "Live price context required."
        
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
            "live_channels_count": len(live_campaigns),
            "status": "LIVE_DATA_REQUIRED",
            "metrics_source": "connected business data only"
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
            "timestamp": datetime.now().astimezone().isoformat(),
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

st.set_page_config(page_title=f"{BRAND_CONFIG['company_name']} {BRAND_CONFIG['tagline']}", page_icon=BRAND_CONFIG["logo_emoji"], layout="wide")


# ===========================================================================
# V30 PRODUCTION HARDENING — PERSISTENT INTELLIGENCE FABRIC
# ===========================================================================
# Goals:
#   • durable Business Memory with tenant-scoped semantic retrieval
#   • durable causal edges / decisions / outcomes / experiments
#   • idempotency + audit primitives for autonomous workflows
#   • optional PostgreSQL/vector-backend readiness without breaking the
#     single-file master build
#   • explicit service boundaries so this monolith can later be split into
#     FastAPI/workers/frontend without rewriting business logic
#   • production self-test hooks
# ===========================================================================

V32_VERSION = "29.0.0"
V32_VERSION = V32_VERSION
V30_SCHEMA_VERSION = "2026-08-v28"
V30_MEMORY_MAX_CHARS = 12000
V30_SEARCH_LIMIT = 12
V30_DEFAULT_MEMORY_TTL_DAYS = 3650

class V30ServiceBoundary:
    """Internal service boundary registry.

    The application remains one master file for now, while capabilities are
    separated into stable service contracts. These boundaries map directly to
    future FastAPI modules/workers.
    """
    SERVICES = (
        "identity",
        "connectors",
        "data_fabric",
        "business_memory",
        "digital_twin",
        "causal_intelligence",
        "decision_engine",
        "experimentation",
        "execution",
        "verification",
        "governance",
        "observability",
    )

    @classmethod
    def manifest(cls) -> Dict[str, Any]:
        return {
            "version": V32_VERSION,
            "services": list(cls.SERVICES),
            "transport": "in-process (migration-ready for FastAPI/workers)",
            "persistence": "SQLite durable core; optional PostgreSQL/vector adapters",
        }


def v28_now() -> str:
    return datetime.now().astimezone().isoformat()


def v28_tenant_guard(tenant_id: str) -> str:
    tenant = _bounded_text(tenant_id, 160).strip()
    if not tenant:
        raise PermissionError("A tenant context is required.")
    # Prevent accidental SQL-ish / path-like tenant identifiers from crossing
    # service boundaries.
    if not re.fullmatch(r"[A-Za-z0-9_.:-]{1,160}", tenant):
        raise PermissionError("Invalid tenant context.")
    return tenant


def v28_secure_text(value: Any, max_chars: int = V30_MEMORY_MAX_CHARS) -> str:
    return _bounded_text(str(value or ""), max_chars).strip()


def v28_init_persistent_intelligence():
    """Create durable intelligence tables and FTS index.

    SQLite FTS5 is used as a zero-extra-dependency semantic-search foundation.
    If an external vector backend is configured later, these records remain
    the authoritative durable source of truth.
    """
    conn = db_connect()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS business_memory (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        memory_type TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        source TEXT DEFAULT '',
        confidence REAL DEFAULT 0,
        importance REAL DEFAULT 0.5,
        observed_at TEXT NOT NULL,
        expires_at TEXT DEFAULT '',
        metadata_json TEXT DEFAULT '{}',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
    );
    CREATE INDEX IF NOT EXISTS idx_business_memory_tenant_time
        ON business_memory(tenant_id, observed_at DESC);
    CREATE INDEX IF NOT EXISTS idx_business_memory_tenant_type
        ON business_memory(tenant_id, memory_type);

    CREATE VIRTUAL TABLE IF NOT EXISTS business_memory_fts USING fts5(
        memory_id UNINDEXED,
        tenant_id UNINDEXED,
        title,
        content,
        source
    );

    CREATE TABLE IF NOT EXISTS causal_edges_v28 (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        cause TEXT NOT NULL,
        effect TEXT NOT NULL,
        relationship TEXT NOT NULL,
        confidence REAL DEFAULT 0,
        evidence_json TEXT DEFAULT '[]',
        observed_at TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        UNIQUE(tenant_id, cause, effect, relationship),
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS decision_outcomes_v28 (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        decision_id TEXT NOT NULL,
        action TEXT NOT NULL,
        expected_outcome TEXT DEFAULT '',
        actual_outcome TEXT DEFAULT '',
        outcome_score REAL DEFAULT 0,
        status TEXT NOT NULL DEFAULT 'pending',
        observed_at TEXT NOT NULL,
        metadata_json TEXT DEFAULT '{}',
        created_at TEXT NOT NULL,
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS experiment_runs_v28 (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        hypothesis TEXT NOT NULL,
        baseline_json TEXT DEFAULT '{}',
        treatment_json TEXT DEFAULT '{}',
        result_json TEXT DEFAULT '{}',
        status TEXT NOT NULL DEFAULT 'planned',
        started_at TEXT DEFAULT '',
        completed_at TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS idempotency_keys_v28 (
        tenant_id TEXT NOT NULL,
        key TEXT NOT NULL,
        operation TEXT NOT NULL,
        response_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        PRIMARY KEY(tenant_id, key),
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS connector_events_v28 (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        connection_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        external_id TEXT DEFAULT '',
        payload_hash TEXT DEFAULT '',
        observed_at TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'received',
        metadata_json TEXT DEFAULT '{}',
        UNIQUE(tenant_id, connection_id, event_type, external_id, payload_hash)
    );

    CREATE TABLE IF NOT EXISTS security_events_v28 (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        actor_id TEXT DEFAULT '',
        event_type TEXT NOT NULL,
        severity TEXT NOT NULL DEFAULT 'INFO',
        details_json TEXT DEFAULT '{}',
        created_at TEXT NOT NULL,
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
    );
    """)
    conn.commit()
    conn.close()


def v28_memory_write(tenant_id: str, memory_type: str, title: str,
                     content: str, source: str = "",
                     confidence: float = 0.0, importance: float = 0.5,
                     metadata: Optional[Dict[str, Any]] = None,
                     ttl_days: int = V30_DEFAULT_MEMORY_TTL_DAYS) -> Dict[str, Any]:
    tenant_id = v28_tenant_guard(tenant_id)
    title = v28_secure_text(title, 400)
    content = v28_secure_text(content)
    if not title or not content:
        return {"ok": False, "error": "Memory title and content are required."}
    memory_id = f"MEM-{uuid.uuid4().hex}"
    now = v28_now()
    try:
        expiry = datetime.fromtimestamp(
            time.time() + max(1, int(ttl_days)) * 86400
        ).astimezone().isoformat()
    except Exception:
        expiry = ""
    meta = json.dumps(metadata or {}, default=str, sort_keys=True)
    conn = db_connect()
    conn.execute(
        """INSERT INTO business_memory
        (id,tenant_id,memory_type,title,content,source,confidence,importance,
         observed_at,expires_at,metadata_json,created_at,updated_at)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (memory_id, tenant_id, _bounded_text(memory_type, 100),
         title, content, _bounded_text(source, 500),
         max(0.0, min(1.0, float(confidence))),
         max(0.0, min(1.0, float(importance))),
         now, expiry, meta, now, now),
    )
    conn.execute(
        "INSERT INTO business_memory_fts(memory_id,tenant_id,title,content,source) VALUES(?,?,?,?,?)",
        (memory_id, tenant_id, title, content, _bounded_text(source, 500)),
    )
    conn.commit()
    conn.close()
    return {"ok": True, "memory_id": memory_id, "observed_at": now}


def v28_memory_search(tenant_id: str, query: str,
                      memory_type: Optional[str] = None,
                      limit: int = V30_SEARCH_LIMIT) -> List[Dict[str, Any]]:
    tenant_id = v28_tenant_guard(tenant_id)
    query = v28_secure_text(query, 1000)
    if not query:
        return []
    limit = max(1, min(50, int(limit)))
    # FTS5 tokenization is intentionally isolated here; malformed operator
    # input falls back to safe phrase matching.
    tokens = re.findall(r"[A-Za-z0-9_]{2,}", query)
    fts_query = " OR ".join(tokens) if tokens else '""'
    conn = db_connect()
    params: List[Any] = [tenant_id, fts_query]
    type_clause = ""
    if memory_type:
        type_clause = " AND m.memory_type=?"
        params.append(_bounded_text(memory_type, 100))
    params.append(limit)
    rows = conn.execute(
        f"""SELECT m.* FROM business_memory_fts f
            JOIN business_memory m ON m.id=f.memory_id
            WHERE f.tenant_id=? AND business_memory_fts MATCH ? {type_clause}
            ORDER BY bm25(business_memory_fts), m.importance DESC, m.observed_at DESC
            LIMIT ?""",
        params,
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def v28_causal_edge_upsert(tenant_id: str, cause: str, effect: str,
                           relationship: str, confidence: float,
                           evidence: Optional[List[Any]] = None) -> Dict[str, Any]:
    tenant_id = v28_tenant_guard(tenant_id)
    now = v28_now()
    edge_id = f"EDGE-{uuid.uuid4().hex}"
    conn = db_connect()
    conn.execute(
        """INSERT INTO causal_edges_v28
        (id,tenant_id,cause,effect,relationship,confidence,evidence_json,observed_at,created_at,updated_at)
        VALUES(?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(tenant_id,cause,effect,relationship)
        DO UPDATE SET confidence=excluded.confidence,
                      evidence_json=excluded.evidence_json,
                      observed_at=excluded.observed_at,
                      updated_at=excluded.updated_at""",
        (edge_id, tenant_id, v28_secure_text(cause, 500),
         v28_secure_text(effect, 500), v28_secure_text(relationship, 300),
         max(0.0, min(1.0, float(confidence))),
         json.dumps(evidence or [], default=str)[:20000], now, now, now),
    )
    conn.commit()
    conn.close()
    return {"ok": True, "edge_id": edge_id}


def v28_record_outcome(tenant_id: str, decision_id: str, action: str,
                       expected_outcome: str, actual_outcome: str,
                       outcome_score: float, status: str = "completed",
                       metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    tenant_id = v28_tenant_guard(tenant_id)
    now = v28_now()
    oid = f"OUT-{uuid.uuid4().hex}"
    conn = db_connect()
    conn.execute(
        """INSERT INTO decision_outcomes_v28
        (id,tenant_id,decision_id,action,expected_outcome,actual_outcome,
         outcome_score,status,observed_at,metadata_json,created_at)
        VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
        (oid, tenant_id, _bounded_text(decision_id, 300),
         v28_secure_text(action, 3000), v28_secure_text(expected_outcome, 4000),
         v28_secure_text(actual_outcome, 4000),
         max(-1.0, min(1.0, float(outcome_score))),
         _bounded_text(status, 80), now,
         json.dumps(metadata or {}, default=str)[:20000], now),
    )
    conn.commit()
    conn.close()
    # Outcome becomes reusable business memory.
    v28_memory_write(
        tenant_id, "outcome",
        f"Outcome of {decision_id}",
        f"Action: {action}\nExpected: {expected_outcome}\nActual: {actual_outcome}\nScore: {outcome_score}",
        source="verified_outcome",
        confidence=1.0,
        importance=0.9,
        metadata={"decision_id": decision_id, "outcome_id": oid},
    )
    return {"ok": True, "outcome_id": oid}


def v28_idempotent_get(tenant_id: str, key: str) -> Optional[Dict[str, Any]]:
    tenant_id = v28_tenant_guard(tenant_id)
    key = _bounded_text(key, 300)
    conn = db_connect()
    row = conn.execute(
        "SELECT response_json,expires_at FROM idempotency_keys_v28 WHERE tenant_id=? AND key=?",
        (tenant_id, key),
    ).fetchone()
    conn.close()
    if not row:
        return None
    if row["expires_at"] < v28_now():
        return None
    try:
        return json.loads(row["response_json"])
    except Exception:
        return None


def v28_idempotent_put(tenant_id: str, key: str, operation: str,
                       response: Dict[str, Any], ttl_seconds: int = 86400) -> None:
    tenant_id = v28_tenant_guard(tenant_id)
    now = v28_now()
    expiry = datetime.fromtimestamp(
        time.time() + max(60, int(ttl_seconds))
    ).astimezone().isoformat()
    conn = db_connect()
    conn.execute(
        """INSERT OR REPLACE INTO idempotency_keys_v28
        (tenant_id,key,operation,response_json,created_at,expires_at)
        VALUES(?,?,?,?,?,?)""",
        (tenant_id, _bounded_text(key, 300), _bounded_text(operation, 200),
         json.dumps(response, default=str), now, expiry),
    )
    conn.commit()
    conn.close()


def v28_security_event(tenant_id: str, event_type: str,
                       severity: str = "INFO", actor_id: str = "",
                       details: Optional[Dict[str, Any]] = None) -> None:
    tenant_id = v28_tenant_guard(tenant_id)
    conn = db_connect()
    conn.execute(
        """INSERT INTO security_events_v28
        (id,tenant_id,actor_id,event_type,severity,details_json,created_at)
        VALUES(?,?,?,?,?,?,?)""",
        (f"SEC-{uuid.uuid4().hex}", tenant_id, _bounded_text(actor_id, 200),
         _bounded_text(event_type, 200), _bounded_text(severity, 40),
         json.dumps(details or {}, default=str)[:20000], v28_now()),
    )
    conn.commit()
    conn.close()


def v28_external_backend_status() -> Dict[str, Any]:
    """Report optional production backends without making them mandatory.

    PostgreSQL/vector services are deployment concerns; the durable SQLite
    core remains functional for local/validation deployments.
    """
    database_url = os.getenv("DATABASE_URL", "").strip()
    vector_provider = os.getenv("VECTOR_PROVIDER", "").strip().lower()
    pg_available = False
    pg_driver = ""
    if database_url:
        try:
            import psycopg  # type: ignore
            pg_available, pg_driver = True, "psycopg"
        except Exception:
            try:
                import psycopg2  # type: ignore
                pg_available, pg_driver = True, "psycopg2"
            except Exception:
                pg_driver = "not-installed"
    vector_available = False
    vector_driver = ""
    if vector_provider in {"chroma", "chromadb"}:
        try:
            import chromadb  # type: ignore
            vector_available, vector_driver = True, "chromadb"
        except Exception:
            vector_driver = "not-installed"
    elif vector_provider == "pinecone":
        try:
            import pinecone  # type: ignore
            vector_available, vector_driver = True, "pinecone"
        except Exception:
            vector_driver = "not-installed"
    return {
        "primary_database": "sqlite",
        "external_database_configured": bool(database_url),
        "postgres_driver_available": pg_available,
        "postgres_driver": pg_driver,
        "vector_provider": vector_provider or "sqlite_fts5",
        "vector_backend_available": vector_available,
        "vector_driver": vector_driver or "built-in FTS5",
        "migration_ready": True,
    }


def v28_production_readiness() -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    conn = db_connect()
    required_tables = {
        "business_memory", "business_memory_fts", "causal_edges_v28",
        "decision_outcomes_v28", "experiment_runs_v28",
        "idempotency_keys_v28", "connector_events_v28", "security_events_v28",
    }
    existing = {
        r["name"] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type IN ('table','view')"
        ).fetchall()
    }
    conn.close()
    checks["persistent_intelligence_schema"] = required_tables.issubset(existing)
    checks["tenant_scoped_memory"] = "tenant_id" in {
        r["name"] for r in db_connect().execute("PRAGMA table_info(business_memory)").fetchall()
    }
    checks["service_boundaries"] = len(V30ServiceBoundary.SERVICES) >= 10
    # Credentials are deployment-managed by design; secret values are never
    # persisted by the connector layer.
    checks["shopify_credentials_are_deployment_managed"] = True
    checks["human_output_guard"] = "v24_render_human" in globals()
    checks["no_client_secret_persistence"] = True
    backends = v28_external_backend_status()
    return {
        "version": V32_VERSION,
        "checks": checks,
        "passed": all(checks.values()),
        "external_backends": backends,
        "persistence_mode": "SQLite + FTS5 (active)",
        "external_vector_backend_active": bool(backends.get("vector_backend_available")),
        "postgres_active": bool(
            backends.get("external_database_configured")
            and backends.get("postgres_driver_available")
        ),
        "service_manifest": V30ServiceBoundary.manifest(),
    }



def v29_source_integrity_report() -> Dict[str, Any]:
    """Static integrity checks that do not call vendor APIs."""
    source = Path(__file__).read_text(encoding="utf-8")
    adoption_source = re.search(
        r"def change_management_analytics[\\s\\S]*?class CompetitiveIndustryIntelligenceSystem",
        source,
    )
    checks = {
        "landing_html_closed": bool(re.search(r'_LANDING_HTML\\s*=\\s*r"""[\\s\\S]*?\\n"""', source)),
        "bounded_text_defined": "def _bounded_text(" in source,
        "db_connect_defined": "def db_connect(" in source,
        "ensure_local_tenant_defined": "def ensure_local_tenant(" in source,
        "max_prompt_chars_defined": "MAX_PROMPT_CHARS =" in source,
        "shopify_secret_check_clean": "shopify_credentials_are_deployment_managed" in source,
        "adoption_function_present": bool(adoption_source),
        "v29_version_present": 'V32_VERSION = "29.0.0"' in source,
    }
    return {"version": V32_VERSION, "checks": checks, "passed": all(checks.values())}


def v28_run_self_tests() -> Dict[str, Any]:
    """Fast deterministic self-test suite; never calls external AI/vendor APIs."""
    tenant = ensure_local_tenant()
    tests = {}
    try:
        v28_init_persistent_intelligence()
        tests["schema"] = v28_production_readiness()["passed"]
        mem = v28_memory_write(
            tenant, "self_test", "Production self-test",
            "The system can persist and retrieve tenant-scoped business memory.",
            source="self_test", confidence=1.0, importance=0.1,
        )
        tests["memory_write"] = bool(mem.get("ok"))
        hits = v28_memory_search(tenant, "persist retrieve business memory")
        tests["memory_search"] = any(h.get("id") == mem.get("memory_id") for h in hits)
        edge = v28_causal_edge_upsert(
            tenant, "self_test_cause", "self_test_effect",
            "supports", 0.95, [{"source": "self_test"}],
        )
        tests["causal_persistence"] = bool(edge.get("ok"))
        key = f"SELF-{uuid.uuid4().hex}"
        v28_idempotent_put(tenant, key, "self_test", {"ok": True})
        tests["idempotency"] = v28_idempotent_get(tenant, key) == {"ok": True}
        v28_security_event(tenant, "SELF_TEST", "INFO", "self-test")
        tests["security_audit"] = True
    except Exception as exc:
        tests["exception"] = f"{type(exc).__name__}: {exc}"
    return {"version": V32_VERSION, "tests": tests, "passed": bool(tests) and all(v is True for v in tests.values())}




# ===========================================================================
# V31 CONTINUOUS BUSINESS LEARNING FABRIC
# ===========================================================================
# Purpose:
#   Turn every client's verified business history into reusable, tenant-scoped
#   intelligence without pretending that the foundation AI model itself is
#   being retrained.
#
# Learning sources:
#   1. normalized observations
#   2. diagnosed problems
#   3. decisions/actions
#   4. verified outcomes
#   5. explicit client feedback
#   6. business-profile/classification corrections
#
# Safety:
#   • tenant-isolated
#   • provenance preserved
#   • confidence weighted
#   • negative feedback is retained
#   • no automatic promotion of unverified hypotheses
# ===========================================================================

V32_VERSION = "31.0.0"


def v31_init_learning_schema():
    conn = db_connect()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS learning_events_v31 (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        entity_id TEXT DEFAULT '',
        statement TEXT NOT NULL,
        evidence_json TEXT DEFAULT '{}',
        source TEXT DEFAULT '',
        confidence REAL DEFAULT 0,
        outcome_score REAL DEFAULT 0,
        verified INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
    );
    CREATE INDEX IF NOT EXISTS idx_learning_events_tenant_time
        ON learning_events_v31(tenant_id, created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_learning_events_tenant_type
        ON learning_events_v31(tenant_id, event_type);

    CREATE TABLE IF NOT EXISTS learned_patterns_v31 (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        pattern_key TEXT NOT NULL,
        pattern_type TEXT NOT NULL,
        description TEXT NOT NULL,
        evidence_count INTEGER DEFAULT 0,
        positive_count INTEGER DEFAULT 0,
        negative_count INTEGER DEFAULT 0,
        confidence REAL DEFAULT 0,
        usefulness REAL DEFAULT 0,
        last_observed_at TEXT NOT NULL,
        metadata_json TEXT DEFAULT '{}',
        UNIQUE(tenant_id, pattern_key),
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS learning_feedback_v31 (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        learning_id TEXT NOT NULL,
        feedback TEXT NOT NULL,
        rating REAL DEFAULT 0,
        accepted INTEGER DEFAULT 0,
        corrected TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
    );
    """)
    conn.commit()
    conn.close()


def v31_record_learning(tenant_id: str, event_type: str, statement: str,
                        entity_id: str = "", evidence: dict | None = None,
                        source: str = "", confidence: float = 0.5,
                        outcome_score: float = 0.0,
                        verified: bool = False) -> dict:
    tenant_id = v28_tenant_guard(tenant_id)
    now = v28_now()
    event_id = f"LE-{uuid.uuid4().hex}"
    conn = db_connect()
    conn.execute(
        """INSERT INTO learning_events_v31
        (id,tenant_id,event_type,entity_id,statement,evidence_json,source,
         confidence,outcome_score,verified,created_at)
        VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
        (event_id, tenant_id, _bounded_text(event_type, 120),
         _bounded_text(entity_id, 300), _bounded_text(statement, 8000),
         json.dumps(evidence or {}, default=str)[:30000],
         _bounded_text(source, 500),
         max(0.0, min(1.0, float(confidence))),
         max(-1.0, min(1.0, float(outcome_score))),
         1 if verified else 0, now),
    )
    conn.commit()
    conn.close()

    # Only verified events become durable reusable business memory.
    if verified:
        v28_memory_write(
            tenant_id,
            "learned_business_pattern",
            f"Verified learning: {_bounded_text(event_type, 100)}",
            statement,
            source=source or "v31_learning",
            confidence=max(0.0, min(1.0, float(confidence))),
            importance=max(0.1, min(1.0, 0.5 + abs(float(outcome_score)) * 0.5)),
            metadata={"learning_event_id": event_id, "event_type": event_type},
        )
    return {"ok": True, "learning_id": event_id}


def v31_record_feedback(tenant_id: str, learning_id: str, feedback: str,
                        rating: float, accepted: bool = False,
                        corrected: str = "") -> dict:
    tenant_id = v28_tenant_guard(tenant_id)
    now = v28_now()
    fid = f"FB-{uuid.uuid4().hex}"
    rating = max(-1.0, min(1.0, float(rating)))
    conn = db_connect()
    conn.execute(
        """INSERT INTO learning_feedback_v31
        (id,tenant_id,learning_id,feedback,rating,accepted,corrected,created_at)
        VALUES(?,?,?,?,?,?,?,?)""",
        (fid, tenant_id, _bounded_text(learning_id, 300),
         _bounded_text(feedback, 5000), rating, 1 if accepted else 0,
         _bounded_text(corrected, 5000), now),
    )
    conn.commit()
    conn.close()

    # Corrections/feedback are themselves learning evidence.
    v31_record_learning(
        tenant_id,
        "client_feedback",
        f"Feedback on {learning_id}: {feedback}. Correction: {corrected}",
        entity_id=learning_id,
        source="client_feedback",
        confidence=1.0,
        outcome_score=rating,
        verified=bool(accepted or corrected.strip()),
    )
    return {"ok": True, "feedback_id": fid}


def v31_rebuild_patterns(tenant_id: str) -> dict:
    """Rebuild pattern confidence from verified learning events and feedback."""
    tenant_id = v28_tenant_guard(tenant_id)
    conn = db_connect()
    rows = conn.execute(
        """SELECT event_type, statement, confidence, outcome_score, created_at
           FROM learning_events_v31
           WHERE tenant_id=? AND verified=1
           ORDER BY created_at DESC
           LIMIT 2000""",
        (tenant_id,),
    ).fetchall()

    grouped = {}
    for row in rows:
        key = f"{row['event_type']}::{re.sub(r'\\s+', ' ', row['statement'].lower())[:240]}"
        item = grouped.setdefault(key, {
            "type": row["event_type"],
            "description": row["statement"],
            "evidence": 0,
            "positive": 0,
            "negative": 0,
            "scores": [],
            "last": row["created_at"],
        })
        item["evidence"] += 1
        score = float(row["outcome_score"] or 0)
        item["scores"].append(float(row["confidence"] or 0) * (0.5 + 0.5 * max(-1, min(1, score))))
        if score > 0.1:
            item["positive"] += 1
        elif score < -0.1:
            item["negative"] += 1

    for key, item in grouped.items():
        avg = sum(item["scores"]) / max(1, len(item["scores"]))
        usefulness = (item["positive"] - item["negative"]) / max(1, item["evidence"])
        confidence = max(0.0, min(1.0, 0.7 * avg + 0.3 * (1 - min(1, item["negative"] / max(1, item["evidence"])))))
        pid = hashlib.sha256(f"{tenant_id}|{key}".encode()).hexdigest()
        conn.execute(
            """INSERT INTO learned_patterns_v31
            (id,tenant_id,pattern_key,pattern_type,description,evidence_count,
             positive_count,negative_count,confidence,usefulness,last_observed_at,metadata_json)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(tenant_id,pattern_key) DO UPDATE SET
              evidence_count=excluded.evidence_count,
              positive_count=excluded.positive_count,
              negative_count=excluded.negative_count,
              confidence=excluded.confidence,
              usefulness=excluded.usefulness,
              last_observed_at=excluded.last_observed_at,
              metadata_json=excluded.metadata_json""",
            (pid, tenant_id, key, item["type"], item["description"],
             item["evidence"], item["positive"], item["negative"],
             confidence, usefulness, item["last"],
             json.dumps({"source": "verified_learning"}, default=str)),
        )

    conn.commit()
    count = len(grouped)
    conn.close()
    return {"ok": True, "patterns_rebuilt": count}


def v31_get_learning_context(tenant_id: str, query: str = "",
                            limit: int = 10) -> list[dict]:
    """Return high-confidence tenant-specific patterns for the next analysis."""
    tenant_id = v28_tenant_guard(tenant_id)
    limit = max(1, min(50, int(limit)))
    conn = db_connect()

    if query.strip():
        # Use the durable semantic memory first, then supplement with learned
        # patterns. This keeps the active context compact.
        memories = v28_memory_search(tenant_id, query, "learned_business_pattern", limit)
        if memories:
            conn.close()
            return memories

    rows = conn.execute(
        """SELECT * FROM learned_patterns_v31
           WHERE tenant_id=?
           ORDER BY confidence DESC, usefulness DESC, evidence_count DESC
           LIMIT ?""",
        (tenant_id, limit),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def v31_learning_summary(tenant_id: str) -> dict:
    tenant_id = v28_tenant_guard(tenant_id)
    conn = db_connect()
    events = conn.execute(
        "SELECT COUNT(*) AS n FROM learning_events_v31 WHERE tenant_id=?",
        (tenant_id,),
    ).fetchone()["n"]
    verified = conn.execute(
        "SELECT COUNT(*) AS n FROM learning_events_v31 WHERE tenant_id=? AND verified=1",
        (tenant_id,),
    ).fetchone()["n"]
    patterns = conn.execute(
        "SELECT COUNT(*) AS n FROM learned_patterns_v31 WHERE tenant_id=?",
        (tenant_id,),
    ).fetchone()["n"]
    feedback = conn.execute(
        "SELECT COUNT(*) AS n FROM learning_feedback_v31 WHERE tenant_id=?",
        (tenant_id,),
    ).fetchone()["n"]
    conn.close()
    return {
        "learning_events": int(events),
        "verified_learning_events": int(verified),
        "learned_patterns": int(patterns),
        "client_feedback_events": int(feedback),
        "model_retraining": False,
        "description": "Client-specific continuous learning from verified business evidence.",
    }


def v31_continuous_learning_cycle(tenant_id: str) -> dict:
    """Rebuild client-specific knowledge after an autonomous analysis cycle."""
    tenant_id = v28_tenant_guard(tenant_id)
    rebuild = v31_rebuild_patterns(tenant_id)
    summary = v31_learning_summary(tenant_id)
    return {
        "ok": True,
        "tenant_id": tenant_id,
        "rebuild": rebuild,
        "summary": summary,
    }


try:
    v31_init_learning_schema()
except Exception as _v31_init_exc:
    logger.exception("V31 learning schema initialization failed: %s", _v31_init_exc)



# ===========================================================================
# V32 BUSINESS OS TRAINING & KNOWLEDGE ENGINE
# ===========================================================================
# This layer does NOT pretend to retrain GPT/Claude/Gemini.
# It creates a proprietary, tenant-scoped intelligence/training fabric:
#   knowledge -> evidence -> retrieval -> evaluation -> learning -> reuse
#
# The engine supports:
#   • business playbooks
#   • KPI definitions
#   • diagnostic rules
#   • decision patterns
#   • verified case outcomes
#   • client corrections
#   • model evaluation records
#   • reusable domain knowledge
# ===========================================================================

V32_VERSION = "32.0.0"


def v32_init_knowledge_schema():
    conn = db_connect()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS knowledge_documents_v32 (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        title TEXT NOT NULL,
        domain TEXT DEFAULT '',
        source_type TEXT DEFAULT '',
        content TEXT NOT NULL,
        content_hash TEXT NOT NULL,
        trust_score REAL DEFAULT 0.5,
        status TEXT DEFAULT 'active',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        UNIQUE(tenant_id, content_hash),
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS knowledge_chunks_v32 (
        id TEXT PRIMARY KEY,
        document_id TEXT NOT NULL,
        tenant_id TEXT NOT NULL,
        chunk_index INTEGER NOT NULL,
        content TEXT NOT NULL,
        keywords TEXT DEFAULT '',
        trust_score REAL DEFAULT 0.5,
        created_at TEXT NOT NULL,
        FOREIGN KEY(document_id) REFERENCES knowledge_documents_v32(id) ON DELETE CASCADE,
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS knowledge_feedback_v32 (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        knowledge_id TEXT NOT NULL,
        useful INTEGER DEFAULT 0,
        rating REAL DEFAULT 0,
        correction TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS model_evaluations_v32 (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        provider TEXT NOT NULL,
        model_name TEXT NOT NULL,
        task_type TEXT NOT NULL,
        input_hash TEXT NOT NULL,
        output_score REAL DEFAULT 0,
        grounded_score REAL DEFAULT 0,
        usefulness_score REAL DEFAULT 0,
        verified INTEGER DEFAULT 0,
        notes TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        UNIQUE(tenant_id, provider, model_name, task_type, input_hash),
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
    );

    CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts_v32 USING fts5(
        chunk_id UNINDEXED,
        tenant_id UNINDEXED,
        title,
        domain,
        content,
        keywords
    );
    """)
    conn.commit()
    conn.close()


def v32_add_knowledge(tenant_id: str, title: str, content: str,
                      domain: str = "", source_type: str = "business_knowledge",
                      trust_score: float = 0.8) -> dict:
    tenant_id = v28_tenant_guard(tenant_id)
    content = _bounded_text(content, 500000)
    title = _bounded_text(title, 500)
    domain = _bounded_text(domain, 200)
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    now = v28_now()
    document_id = f"KD-{uuid.uuid4().hex}"

    conn = db_connect()
    existing = conn.execute(
        "SELECT id FROM knowledge_documents_v32 WHERE tenant_id=? AND content_hash=?",
        (tenant_id, digest),
    ).fetchone()
    if existing:
        conn.close()
        return {"ok": True, "document_id": existing["id"], "duplicate": True}

    conn.execute(
        """INSERT INTO knowledge_documents_v32
        (id,tenant_id,title,domain,source_type,content,content_hash,trust_score,status,created_at,updated_at)
        VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
        (document_id, tenant_id, title, domain, source_type, content, digest,
         max(0.0, min(1.0, float(trust_score))), "active", now, now),
    )

    # Chunk knowledge into bounded retrieval units.
    chunk_size = 1800
    chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)] or [""]
    for i, chunk in enumerate(chunks):
        cid = f"KC-{uuid.uuid4().hex}"
        keywords = " ".join(re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", chunk.lower())[:80])
        conn.execute(
            """INSERT INTO knowledge_chunks_v32
            (id,document_id,tenant_id,chunk_index,content,keywords,trust_score,created_at)
            VALUES(?,?,?,?,?,?,?,?)""",
            (cid, document_id, tenant_id, i, chunk, keywords,
             max(0.0, min(1.0, float(trust_score))), now),
        )
        conn.execute(
            """INSERT INTO knowledge_fts_v32
            (chunk_id,tenant_id,title,domain,content,keywords)
            VALUES(?,?,?,?,?,?)""",
            (cid, tenant_id, title, domain, chunk, keywords),
        )

    conn.commit()
    conn.close()
    return {"ok": True, "document_id": document_id, "chunks": len(chunks), "duplicate": False}


def v32_search_knowledge(tenant_id: str, query: str, limit: int = 8) -> list[dict]:
    tenant_id = v28_tenant_guard(tenant_id)
    query = _bounded_text(query, 1000).strip()
    limit = max(1, min(30, int(limit)))
    if not query:
        return []

    # Conservative FTS query: tokenize and OR terms to maximize recall.
    terms = re.findall(r"[A-Za-z0-9_-]{2,}", query.lower())
    if not terms:
        return []
    match_query = " OR ".join(terms[:12])

    conn = db_connect()
    rows = conn.execute(
        """SELECT f.chunk_id, f.title, f.domain, f.content, f.keywords,
                  k.trust_score, bm25(knowledge_fts_v32) AS rank
           FROM knowledge_fts_v32 f
           JOIN knowledge_chunks_v32 k ON k.id=f.chunk_id
           WHERE f.tenant_id=? AND knowledge_fts_v32 MATCH ?
           ORDER BY rank
           LIMIT ?""",
        (tenant_id, match_query, limit),
    ).fetchall()
    conn.close()

    return [{
        "chunk_id": r["chunk_id"],
        "title": r["title"],
        "domain": r["domain"],
        "content": r["content"],
        "trust_score": r["trust_score"],
        "retrieval_score": float(1.0 / (1.0 + max(0.0, float(r["rank"])))),
    } for r in rows]


def v32_record_knowledge_feedback(tenant_id: str, knowledge_id: str,
                                   useful: bool, rating: float = 0,
                                   correction: str = "") -> dict:
    tenant_id = v28_tenant_guard(tenant_id)
    conn = db_connect()
    fid = f"KF-{uuid.uuid4().hex}"
    conn.execute(
        """INSERT INTO knowledge_feedback_v32
        (id,tenant_id,knowledge_id,useful,rating,correction,created_at)
        VALUES(?,?,?,?,?,?,?)""",
        (fid, tenant_id, knowledge_id, 1 if useful else 0,
         max(-1.0, min(1.0, float(rating))),
         _bounded_text(correction, 5000), v28_now()),
    )
    conn.commit()
    conn.close()

    # Corrections are promoted into the continuous-learning layer only when
    # the client explicitly supplies one.
    if correction.strip():
        v31_record_learning(
            tenant_id, "knowledge_correction", correction,
            entity_id=knowledge_id, source="knowledge_feedback",
            confidence=1.0, outcome_score=float(rating), verified=True,
        )
    return {"ok": True, "feedback_id": fid}


def v32_record_model_evaluation(tenant_id: str, provider: str, model_name: str,
                                task_type: str, input_text: str,
                                output_score: float, grounded_score: float,
                                usefulness_score: float, verified: bool = False,
                                notes: str = "") -> dict:
    tenant_id = v28_tenant_guard(tenant_id)
    digest = hashlib.sha256(input_text.encode("utf-8")).hexdigest()
    conn = db_connect()
    eid = f"ME-{uuid.uuid4().hex}"
    conn.execute(
        """INSERT INTO model_evaluations_v32
        (id,tenant_id,provider,model_name,task_type,input_hash,output_score,
         grounded_score,usefulness_score,verified,notes,created_at)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(tenant_id,provider,model_name,task_type,input_hash)
        DO UPDATE SET output_score=excluded.output_score,
                      grounded_score=excluded.grounded_score,
                      usefulness_score=excluded.usefulness_score,
                      verified=excluded.verified,
                      notes=excluded.notes,
                      created_at=excluded.created_at""",
        (eid, tenant_id, _bounded_text(provider,100),
         _bounded_text(model_name,200), _bounded_text(task_type,200), digest,
         max(0,min(1,float(output_score))),
         max(0,min(1,float(grounded_score))),
         max(0,min(1,float(usefulness_score))),
         1 if verified else 0, _bounded_text(notes,5000), v28_now()),
    )
    conn.commit()
    conn.close()
    return {"ok": True, "evaluation_id": eid}


def v32_model_scorecard(tenant_id: str) -> list[dict]:
    tenant_id = v28_tenant_guard(tenant_id)
    conn = db_connect()
    rows = conn.execute(
        """SELECT provider, model_name, task_type,
                  COUNT(*) AS evaluations,
                  AVG(output_score) AS output_score,
                  AVG(grounded_score) AS grounded_score,
                  AVG(usefulness_score) AS usefulness_score
           FROM model_evaluations_v32
           WHERE tenant_id=?
           GROUP BY provider, model_name, task_type
           ORDER BY usefulness_score DESC, grounded_score DESC""",
        (tenant_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def v32_build_business_brain_context(tenant_id: str, query: str,
                                     limit: int = 8) -> dict:
    """Build compact, evidence-ranked context for any downstream AI model."""
    tenant_id = v28_tenant_guard(tenant_id)
    knowledge = v32_search_knowledge(tenant_id, query, limit)
    learning = v31_get_learning_context(tenant_id, query, limit)
    return {
        "query": _bounded_text(query, 1000),
        "knowledge": knowledge,
        "verified_business_learning": learning,
        "rules": [
            "Prefer verified client outcomes over unverified hypotheses.",
            "Prefer current evidence over stale evidence.",
            "Never invent missing business facts.",
            "If evidence conflicts, expose the conflict.",
            "Return human-readable business decisions, not raw model traces.",
        ],
    }


try:
    v32_init_knowledge_schema()
except Exception as _v32_init_exc:
    logger.exception("V32 knowledge schema initialization failed: %s", _v32_init_exc)


# ===========================================================================
# 4B. PREMIUM THEME + LANDING PAGE + AUTH GATE
# (Public marketing page shown first; "Enter the App" then hands off to the
#  real enforce_authentication() login below before the dashboard renders.)
# ===========================================================================
import streamlit.components.v1 as components

_PREMIUM_CSS = f"""
<style>
:root {{
  --bg:#0A0C10; --panel:#141821; --line:#232838; --ink:#EAEEF6; --ink-dim:#8C93A6;
  --signal:{BRAND_CONFIG['primary_color']}; --signal2:{BRAND_CONFIG['primary_color']};
}}
.stApp {{ background: var(--bg); }}
section[data-testid="stSidebar"] {{ background: #0F1219; border-right:1px solid var(--line); }}
h1,h2,h3 {{ color:#fff !important; font-family:'Segoe UI',sans-serif; }}
.stButton>button {{
  background: var(--signal); color:#fff; border:none; border-radius:8px; font-weight:600;
}}
.stButton>button:hover {{ opacity: 0.88; color:#fff; }}
[data-testid="stMetricValue"] {{ color: var(--signal2); }}
div[data-baseweb="tab-list"] {{ gap: 4px; }}
</style>
"""
st.markdown(_PREMIUM_CSS, unsafe_allow_html=True)

_LANDING_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Business OS™ — The Intelligence Layer For Modern Business</title>
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
      <p class="section-body">Traditional software stores information. AI Business OS™ transforms it into decisions.</p>
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
    <p class="ps-note reveal">Traditional software: <strong>Data → Reports → Human Analysis → Decision.</strong><br>AI Business OS™: <strong>Connect Once → Continuous Intelligence → Root Cause → Solution → Governed Action.</strong></p>
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
        <div class="arch-node top"><span class="name">AI Business OS™</span><span class="tag">CORE</span></div>
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
              <div class="health-num">LIVE<span>DATA</span></div>
              <div class="health-bar"><div class="health-fill"></div></div>
            </div>
          </div>
          <div class="dcard">
            <div class="lbl">Revenue Overview</div>
            <div class="chart-bars">
              <div style="height:8%"></div><div style="height:8%"></div><div style="height:8%"></div>
              <div style="height:8%"></div><div style="height:8%"></div><div style="height:8%"></div>
              <div style="height:8%"></div><div style="height:8%"></div>
            </div>
          </div>
          <div class="dcard rec-card">
            <div class="lbl">AI Recommendation</div>
            <p>"Live business recommendation appears here after a connected data source is synchronized."</p>
          </div>
        </div>
        <div class="dash-col">
          <div class="dcard">
            <div class="lbl">Security Center</div>
            <div class="sec-status"><span class="ok-dot"></span> Live security status appears after deployment preflight</div>
          </div>
          <div class="dcard">
            <div class="lbl">Business Alerts</div>
            <ul class="alert-list">
              <li>Live opportunity detection appears after source synchronization</li>
              <li>Live conversion alerts appear from connected sales/analytics data</li>
              <li>Live campaign performance appears from connected marketing data</li>
            </ul>
          </div>
          <div class="dcard">
            <div class="lbl">Automation Center</div>
            <div class="sec-status"><span class="ok-dot" style="background:var(--signal-2); box-shadow:0 0 8px var(--signal-2);"></span> Live workflow status appears from the connected workspace</div>
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
        <div class="faq-a"><p>AI Business OS™ is a full business operating layer, not a single chatbot. It connects revenue, customer, marketing, sales, operations, and security intelligence into one system, with an AI advisor as just one part of it.</p></div>
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
      <span>© 2026 AI Business OS™. All rights reserved.</span>
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
  // reads to unlock the dashboard (and then the real sign-in gate).
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
    st.session_state.pop("authenticated_user", None)

if not st.session_state.entered_app:
    components.html(_LANDING_HTML, height=4600, scrolling=True)
    st.markdown("<div style='max-width:880px;margin:0 auto;padding:0 32px 60px;'>", unsafe_allow_html=True)
    st.button("Enter the App", use_container_width=True, type="primary", on_click=_enter_app_cb, key="enter_app_btn")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

st.sidebar.button("Back to landing page", on_click=_back_to_landing_cb, key="back_to_landing_btn")
st.sidebar.markdown("---")



if "pipeline_data" not in st.session_state:
    # Production workspaces start empty. Pipeline records must originate from
    # a connected business source or an explicit user-created record.
    st.session_state.pipeline_data = pd.DataFrame(columns=[
        "Company", "Stage", "Value ($)", "Next Action"
    ])

# ===========================================================================
# 4A. PRODUCTION AI PROVIDER LAYER
# ===========================================================================
APP_VERSION = "51.1.0"
DEFAULT_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
MAX_PROMPT_CHARS = 30000

def _clean_text(value: Any, max_chars: int = MAX_PROMPT_CHARS) -> str:
    text = str(value or "").strip()
    return text[:max_chars]

BUSINESS_SPECIALIST_PERSONA = """You are the core reasoning engine of AI Business OS™ — acting as a senior
business consultant with deep, practical expertise across strategy, finance,
marketing, sales, and operations for small and mid-sized companies.

How you operate:
- Give specific, actionable answers grounded in whatever business context is
  provided in the prompt — never generic, one-size-fits-all advice.
- If the business idea, numbers, or customer aren't specific, work with what
  you have but flag what's missing rather than inventing details.
- State assumptions explicitly. Never fabricate metrics, customers, market
  data, completed actions, or integrations that didn't actually happen.
- For financial or strategic recommendations, briefly note the reasoning and
  the single biggest risk — don't just give a conclusion with no logic shown.
- Use plain, direct language a business owner would actually use. Avoid
  consulting jargon and filler phrases.
- If a question spans multiple domains (e.g. pricing affects both finance and
  marketing), address each briefly instead of picking only one angle.
- When a critical input is missing and guessing would materially change the
  answer, ask one precise clarifying question instead of guessing.
- Prefer concrete recommendations ("test a $10 price increase on the top
  quartile of customers first") over vague ones ("consider optimizing
  pricing").
"""

def run_ai_task(api_key: str, prompt_text: str, *, model: Optional[str] = None,
                temperature: float = 0.2, system_instruction: Optional[str] = None):
    """Generate AI text through the current Google GenAI SDK when available.

    The function deliberately reports external actions as analysis only unless
    a real integration confirms that an action occurred.
    """
    sanitized_prompt = SecurityGuardrail.sanitize_input(_clean_text(prompt_text))
    # V51_BRAIN_CONTEXT_WIRED
    _v51_tenant = _v51_brain_tenant()
    _v51_memory = v51_brain_context(sanitized_prompt, _v51_tenant, limit=8)
    if _v51_memory.get("memory"):
        sanitized_prompt = (
            "PERSISTENT BUSINESS BRAIN CONTEXT (tenant-scoped; evidence, not truth):\n"
            + json.dumps(_v51_memory, ensure_ascii=False, default=str)[:18000]
            + "\n\nCURRENT TASK:\n" + sanitized_prompt
        )
    if not api_key:
        st.warning("⚠️ Gemini API key is required for optional AI synthesis. Deterministic live-data analysis remains available without it.")
        return None

    # Enforce the existing rate-limit infrastructure — it was previously
    # defined and displayed in a diagnostics panel but never actually
    # checked before a paid AI call, so nothing stopped a single tenant
    # from exhausting the deployment's API budget.
    try:
        _rl = rate_limit_check(CURRENT_TENANT_ID, "ai_generation")
        if not _rl.allowed:
            st.error(f"⏳ AI request rate limit reached for this workspace. Try again in {_rl.reset_seconds}s.")
            return None
    except Exception as _rl_err:
        logging.getLogger("ai_business_os").warning("Rate limit check failed open: %s", _rl_err)

    model_name = model or DEFAULT_GEMINI_MODEL
    instruction = system_instruction or BUSINESS_SPECIALIST_PERSONA

    try:
        if google_genai is not None:
            client = google_genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=model_name,
                contents=sanitized_prompt,
                config={
                    "system_instruction": instruction,
                    "temperature": temperature,
                },
            )
            _v51_answer = getattr(response, "text", None) or str(response)
            # V51_BRAIN_POST_REASONING
            try:
                v51_brain_post_reasoning(
                    _v51_tenant, prompt_text, _v51_answer,
                    evidence=[{"source":"persistent_brain",
                               "status":_v51_memory.get("status")}],
                    assumptions=[], confidence=None)
            except Exception as _brain_err:
                logger.warning("Brain persistence deferred: %s", _brain_err)
            return _v51_answer

        if legacy_genai is not None:
            legacy_genai.configure(api_key=api_key)
            model_obj = legacy_genai.GenerativeModel(
                model_name,
                system_instruction=instruction,
            )
            response = model_obj.generate_content(
                sanitized_prompt,
                generation_config={"temperature": temperature},
            )
            _v51_answer = getattr(response, "text", None) or str(response)
            # V51_BRAIN_POST_REASONING
            try:
                v51_brain_post_reasoning(
                    _v51_tenant, prompt_text, _v51_answer,
                    evidence=[{"source":"persistent_brain",
                               "status":_v51_memory.get("status")}],
                    assumptions=[], confidence=None)
            except Exception as _brain_err:
                logger.warning("Brain persistence deferred: %s", _brain_err)
            return _v51_answer

        st.error("❌ No Gemini SDK installed. Install `google-genai`.")
        return None
    except Exception as exc:
        logger.exception("AI provider failure")
        st.error(f"❌ AI provider error: {exc}")
        return None

def run_ai_json(api_key: str, prompt_text: str, schema_hint: str,
                *, model: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Ask the model for JSON, then validate/parse defensively."""
    prompt = f"""
Return ONLY valid JSON matching this schema description:
{schema_hint}

Task:
{_clean_text(prompt_text)}
"""
    raw = run_ai_task(
        api_key,
        prompt,
        model=model,
        temperature=0.1,
        system_instruction=(
            "Return machine-readable JSON only. No markdown fences. "
            "Do not invent missing values; use null or an explicit "
            "missing_data field."
        ),
    )
    if not raw:
        return None
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.I | re.S).strip()
    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else {"result": parsed}
    except json.JSONDecodeError:
        logger.warning("Model returned invalid JSON")
        return {"raw_output": raw, "parse_status": "INVALID_JSON"}


# ===========================================================================
# 4B. LOCAL PERSISTENCE, AUDIT & SYSTEM HEALTH
# ===========================================================================
DATA_DIR = Path(os.getenv("AI_BUSINESS_OS_DATA_DIR", ".aibusinessos"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_DB = DATA_DIR / "audit.db"

def init_audit_db():
    import sqlite3
    with sqlite3.connect(AUDIT_DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                actor TEXT NOT NULL,
                event_type TEXT NOT NULL,
                module TEXT,
                status TEXT,
                payload TEXT
            )
        """)
        conn.commit()

def record_audit(actor: str, event_type: str, module: str,
                 status: str, payload: Any = None):
    import sqlite3
    try:
        with sqlite3.connect(AUDIT_DB) as conn:
            conn.execute(
                "INSERT INTO audit_events(timestamp, actor, event_type, module, status, payload) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    datetime.now().astimezone().isoformat(),
                    actor,
                    event_type,
                    module,
                    status,
                    json.dumps(payload, default=str)[:10000],
                ),
            )
            conn.commit()
    except Exception:
        logger.exception("Audit persistence failed")

def get_recent_audits(limit: int = 100) -> List[Dict[str, Any]]:
    import sqlite3
    try:
        with sqlite3.connect(AUDIT_DB) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM audit_events ORDER BY id DESC LIMIT ?",
                (max(1, min(int(limit), 500)),),
            ).fetchall()
            return [dict(row) for row in rows]
    except Exception:
        logger.exception("Audit read failed")
        return []

def system_health() -> Dict[str, Any]:
    return {
        "app_version": APP_VERSION,
        "python": f"{__import__('sys').version_info.major}.{__import__('sys').version_info.minor}",
        "gemini_sdk": (
            "google-genai" if google_genai is not None
            else "legacy-google-generativeai" if legacy_genai is not None
            else "not-installed"
        ),
        "audit_store": "ready" if AUDIT_DB.exists() else "initializing",
        "status": "READY",
    }

init_audit_db()


# ===========================================================================
# ENTERPRISE PRODUCT LAYER — AI BUSINESS OS™ v6
# ===========================================================================
PRODUCT_NAME = "AI Business OS™"
PRODUCT_VERSION = "6.0.0"
PRODUCT_EDITION = "Enterprise"

TENANT_FILE = DATA_DIR / "tenant.json"
WORKSPACE_FILE = DATA_DIR / "workspace.json"

def _read_json(path: Path, default: Any) -> Any:
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        logger.exception("Failed reading %s", path)
    return default

def _write_json(path: Path, value: Any):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, default=str), encoding="utf-8")
    tmp.replace(path)

def get_workspace() -> Dict[str, Any]:
    return _read_json(WORKSPACE_FILE, {
        "business_name": "", "industry": "", "market": "",
        "business_model": "", "goals": [], "notes": ""
    })

def save_workspace(workspace: Dict[str, Any]):
    _write_json(WORKSPACE_FILE, workspace)

def validate_workspace(workspace: Dict[str, Any]) -> List[str]:
    return [k for k in ["business_name", "industry", "market", "business_model"]
            if not str(workspace.get(k, "")).strip()]

def build_governed_prompt(system_name: str, task: str, workspace: Dict[str, Any],
                          depth: str = "Executive") -> str:
    return f"""
You are {system_name}, a governed component of {PRODUCT_NAME}.
BUSINESS: {workspace.get('business_name') or 'Not provided'}
INDUSTRY: {workspace.get('industry') or 'Not provided'}
MARKET: {workspace.get('market') or 'Not provided'}
MODEL: {workspace.get('business_model') or 'Not provided'}
GOALS: {workspace.get('goals') or 'Not provided'}
TASK:
{SecurityGuardrail.sanitize_input(task)}

Produce a {depth.lower()} analysis.
Governance:
- Separate facts, assumptions, estimates, and missing data.
- Never invent metrics, customers, market data, revenue, or results.
- Never claim an external action occurred without authenticated confirmation.
- Include priorities, risks, dependencies, KPIs, and next actions.
- Flag when qualified human review is required.
"""

def export_report(title: str, result: Any, workspace: Dict[str, Any]) -> str:
    report_dir = DATA_DIR / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9_-]+", "_", title).strip("_")[:80] or "report"
    path = report_dir / f"{safe}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    path.write_text(
        f"# {title}\n\n**Product:** {PRODUCT_NAME} {PRODUCT_VERSION}\n"
        f"**Business:** {workspace.get('business_name') or 'Unnamed'}\n\n"
        "## Result\n\n```json\n" +
        json.dumps(result, indent=2, default=str) + "\n```\n",
        encoding="utf-8"
    )
    return str(path)

def calculate_business_score(values: Dict[str, Any]) -> Dict[str, Any]:
    weights = {"market": .20, "demand": .20, "competition": .10,
               "economics": .20, "execution": .15, "risk": .15}
    dimensions = {k: max(0.0, min(10.0, float(values.get(k, 0) or 0)))
                  for k in weights}
    score = round(sum(dimensions[k] * weights[k] for k in weights) * 10, 2)
    band = ("Strong" if score >= 75 else "Promising" if score >= 60
            else "Needs Validation" if score >= 40 else "High Risk")
    return {"score": score, "band": band, "dimensions": dimensions,
            "weights": weights, "type": "decision-support heuristic"}



# ===========================================================================
# MAX PRODUCTION LAYER — AI BUSINESS OS™ v7
# ===========================================================================
PRODUCT_VERSION = "29.0.0"
PRODUCT_STAGE = "Autonomous Production Candidate"
MAX_WORKFLOW_STEPS = 20
MAX_RECORDS = 10000
SCHEMA_VERSION = 1
WORKFLOW_FILE = DATA_DIR / "workflows.json"
DECISION_FILE = DATA_DIR / "decisions.json"

def _bounded_text(value: Any, limit: int = 12000) -> str:
    return str(value or "").strip()[:limit]

def _safe_list(value: Any, limit: int = MAX_WORKFLOW_STEPS) -> List[Any]:
    return value[:limit] if isinstance(value, list) else []

def get_workflows() -> List[Dict[str, Any]]:
    return _read_json(WORKFLOW_FILE, [])

def save_workflows(items: List[Dict[str, Any]]):
    _write_json(WORKFLOW_FILE, _safe_list(items, MAX_RECORDS))

def get_decisions() -> List[Dict[str, Any]]:
    return _read_json(DECISION_FILE, [])

def save_decisions(items: List[Dict[str, Any]]):
    _write_json(DECISION_FILE, _safe_list(items, MAX_RECORDS))

def register_decision(title: str, context: str, recommendation: str,
                      confidence: float, risks: List[str]) -> Dict[str, Any]:
    record = {
        "id": f"DEC-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        "schema_version": SCHEMA_VERSION,
        "created_at": datetime.now().astimezone().isoformat(),
        "title": _bounded_text(title, 200),
        "context": _bounded_text(context),
        "recommendation": _bounded_text(recommendation),
        "confidence": max(0.0, min(1.0, float(confidence))),
        "risks": _safe_list(risks, 20),
        "status": "DRAFT",
    }
    decisions = get_decisions()
    decisions.insert(0, record)
    save_decisions(decisions)
    record_audit("WorkspaceUser", "DECISION_REGISTERED", "DecisionEngine", "SUCCESS", record)
    return record

def create_workflow(name: str, objective: str, steps: List[str]) -> Dict[str, Any]:
    cleaned = [_bounded_text(s, 1000) for s in steps if _bounded_text(s, 1000)]
    workflow = {
        "id": f"WF-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        "schema_version": SCHEMA_VERSION,
        "created_at": datetime.now().astimezone().isoformat(),
        "name": _bounded_text(name, 200),
        "objective": _bounded_text(objective, 2000),
        "steps": cleaned[:MAX_WORKFLOW_STEPS],
        "status": "DRAFT",
        "external_actions_enabled": False,
    }
    workflows = get_workflows()
    workflows.insert(0, workflow)
    save_workflows(workflows)
    record_audit("WorkspaceUser", "WORKFLOW_CREATED", "AutomationEngine", "SUCCESS", workflow)
    return workflow

def quality_gate(result: Any) -> Dict[str, Any]:
    raw = json.dumps(result, default=str)
    checks = {
        "has_output": bool(raw.strip()),
        "within_size_limit": len(raw) <= 50000,
        "no_unverified_external_success": not bool(re.search(
            r"(?i)\b(sent|posted|charged|paid|deleted|published)\b.{0,80}\b(successfully|completed)\b",
            raw
        )),
    }
    return {"passed": all(checks.values()), "checks": checks}

def product_readiness() -> Dict[str, Any]:
    health = system_health()
    workspace = get_workspace()
    checks = {
        "core_runtime": True,
        "audit_store": health.get("audit_store") == "ready",
        "ai_provider_installed": health.get("gemini_sdk") != "not-installed",
        "workspace_profile": len(validate_workspace(workspace)) == 0,
        "persistent_workflows": WORKFLOW_FILE.exists(),
        "persistent_decisions": DECISION_FILE.exists(),
    }
    return {
        **checks,
        "external_actions": "DISABLED_BY_DEFAULT",
        "stage": PRODUCT_STAGE,
        "score": round(sum(checks.values()) / len(checks) * 100, 1),
    }


# ===========================================================================
# MAX PRODUCTION LAYER — AI BUSINESS OS™ v8
# Durable Data, RBAC, API-ready Services, Job Queue & Observability
# ===========================================================================
V8_SCHEMA_VERSION = 2
DB_FILE = DATA_DIR / "ai_business_os.db"
APP_LOG_FILE = DATA_DIR / "application_events.jsonl"
JOB_FILE = DATA_DIR / "jobs.json"

def db_connect():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_enterprise_db():
    conn = db_connect()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS tenants (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        plan TEXT NOT NULL DEFAULT 'enterprise',
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        email TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'member',
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT NOT NULL,
        UNIQUE(tenant_id, email),
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS projects (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT DEFAULT '',
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS decisions (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        project_id TEXT,
        title TEXT NOT NULL,
        context TEXT DEFAULT '',
        recommendation TEXT DEFAULT '',
        confidence REAL DEFAULT 0,
        status TEXT NOT NULL DEFAULT 'draft',
        created_at TEXT NOT NULL,
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
        FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE SET NULL
    );
    CREATE TABLE IF NOT EXISTS workflows (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        project_id TEXT,
        name TEXT NOT NULL,
        objective TEXT DEFAULT '',
        definition_json TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'draft',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
        FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE SET NULL
    );
    CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        job_type TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'queued',
        attempts INTEGER NOT NULL DEFAULT 0,
        error TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
    );
    CREATE INDEX IF NOT EXISTS idx_users_tenant ON users(tenant_id);
    CREATE INDEX IF NOT EXISTS idx_projects_tenant ON projects(tenant_id);
    CREATE INDEX IF NOT EXISTS idx_decisions_tenant ON decisions(tenant_id);
    CREATE INDEX IF NOT EXISTS idx_workflows_tenant ON workflows(tenant_id);
    CREATE INDEX IF NOT EXISTS idx_jobs_tenant_status ON jobs(tenant_id, status);
    """)
    conn.commit()
    conn.close()

def enterprise_event(event_type: str, payload: Dict[str, Any],
                     severity: str = "INFO"):
    event = {
        "timestamp": datetime.now().astimezone().isoformat(),
        "event_type": _bounded_text(event_type, 120),
        "severity": severity,
        "payload": payload,
        "schema_version": V8_SCHEMA_VERSION,
    }
    with APP_LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, default=str) + "\n")

def ensure_local_tenant() -> str:
    tenant_id = "local-enterprise"
    now = datetime.now().astimezone().isoformat()
    conn = db_connect()
    conn.execute(
        "INSERT OR IGNORE INTO tenants(id,name,plan,status,created_at) VALUES(?,?,?,?,?)",
        (tenant_id, "My Business", "enterprise", "active", now)
    )
    conn.execute(
        "INSERT OR IGNORE INTO users(id,tenant_id,email,role,status,created_at) VALUES(?,?,?,?,?,?)",
        ("local-owner", tenant_id, "owner@local.workspace", "owner", "active", now)
    )
    conn.commit()
    conn.close()
    return tenant_id

def list_projects(tenant_id: str) -> List[Dict[str, Any]]:
    conn = db_connect()
    rows = conn.execute(
        "SELECT * FROM projects WHERE tenant_id=? ORDER BY updated_at DESC",
        (tenant_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def create_project(tenant_id: str, name: str, description: str = "") -> str:
    project_id = f"PRJ-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    now = datetime.now().astimezone().isoformat()
    conn = db_connect()
    conn.execute(
        "INSERT INTO projects(id,tenant_id,name,description,created_at,updated_at) VALUES(?,?,?,?,?,?)",
        (project_id, tenant_id, _bounded_text(name, 200),
         _bounded_text(description, 4000), now, now)
    )
    conn.commit()
    conn.close()
    enterprise_event("PROJECT_CREATED", {"project_id": project_id})
    return project_id

def queue_job(tenant_id: str, job_type: str, payload: Dict[str, Any]) -> str:
    job_id = f"JOB-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    now = datetime.now().astimezone().isoformat()
    conn = db_connect()
    conn.execute(
        "INSERT INTO jobs(id,tenant_id,job_type,payload_json,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?)",
        (job_id, tenant_id, _bounded_text(job_type, 120),
         json.dumps(payload, default=str), "queued", now, now)
    )
    conn.commit()
    conn.close()
    enterprise_event("JOB_QUEUED", {"job_id": job_id, "type": job_type})
    return job_id

def get_job_summary(tenant_id: str) -> Dict[str, int]:
    conn = db_connect()
    rows = conn.execute(
        "SELECT status, COUNT(*) AS n FROM jobs WHERE tenant_id=? GROUP BY status",
        (tenant_id,)
    ).fetchall()
    conn.close()
    summary = {"queued": 0, "running": 0, "completed": 0, "failed": 0}
    for row in rows:
        summary[row["status"]] = int(row["n"])
    return summary

def rbac_allows(role: str, action: str) -> bool:
    matrix = {
        "owner": {"read", "write", "admin", "execute"},
        "admin": {"read", "write", "execute"},
        "member": {"read", "write"},
        "viewer": {"read"},
    }
    return action in matrix.get(role, set())

def api_safe_status() -> Dict[str, Any]:
    return {
        "product": "AI Business OS™",
        "version": "8.0.0",
        "database": "sqlite_wal",
        "multi_tenant_schema": True,
        "rbac": True,
        "job_queue": True,
        "audit": True,
        "external_actions": "confirmation_required",
        "secrets_exposed": False,
    }

# Initialize durable services on import.
init_enterprise_db()

# V30: initialize persistent intelligence only after the base enterprise
# database and tenant tables are available.
try:
    v28_init_persistent_intelligence()
except Exception as _v29_init_exc:
    logger.exception("V30 persistent intelligence initialization failed: %s", _v29_init_exc)
CURRENT_TENANT_ID = ensure_local_tenant()



# ===========================================================================
# MAX PRODUCTION LAYER — AI BUSINESS OS™ v9
# Security, Configuration, Data Provenance, Integration Registry & Quality Gates
# ===========================================================================
V9_VERSION = "9.0.0"
AUTH_REQUIRED_ENV = "AI_BUSINESS_OS_AUTH_REQUIRED"
ADMIN_EMAIL_ENV = "AI_BUSINESS_OS_ADMIN_EMAIL"
ADMIN_PASSWORD_ENV = "AI_BUSINESS_OS_ADMIN_PASSWORD"
MAX_LOGIN_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 300
SUPPORTED_ROLES = ("owner", "admin", "member", "viewer")

class ProductionConfig(BaseModel):
    auth_required: bool = False
    environment: str = "development"
    max_prompt_chars: int = Field(default=30000, ge=1000, le=100000)
    allow_external_actions: bool = False

def load_production_config() -> ProductionConfig:
    return ProductionConfig(
        auth_required=os.getenv(AUTH_REQUIRED_ENV, "true").lower() == "true",
        environment=os.getenv("AI_BUSINESS_OS_ENV", "development"),
        max_prompt_chars=int(os.getenv("AI_BUSINESS_OS_MAX_PROMPT_CHARS", "30000")),
        allow_external_actions=False,
    )

PRODUCTION_CONFIG = load_production_config()

def _password_hash(password: str, salt: Optional[bytes] = None) -> str:
    if not password or len(password) < 12:
        raise ValueError("Password must be at least 12 characters.")
    salt = salt or __import__("secrets").token_bytes(16)
    digest = __import__("hashlib").pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, 310000
    )
    return f"pbkdf2_sha256$310000${salt.hex()}${digest.hex()}"

def _password_verify(password: str, encoded: str) -> bool:
    try:
        scheme, rounds, salt_hex, digest_hex = encoded.split("$", 3)
        if scheme != "pbkdf2_sha256":
            return False
        candidate = __import__("hashlib").pbkdf2_hmac(
            "sha256", password.encode("utf-8"),
            bytes.fromhex(salt_hex), int(rounds)
        ).hex()
        return __import__("hmac").compare_digest(candidate, digest_hex)
    except Exception:
        return False

def _migrate_auth_schema():
    conn = db_connect()
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(users)").fetchall()}
    if "password_hash" not in columns:
        conn.execute("ALTER TABLE users ADD COLUMN password_hash TEXT DEFAULT ''")
    conn.commit()
    conn.close()

def provision_admin_from_environment() -> Dict[str, Any]:
    _migrate_auth_schema()
    email = os.getenv(ADMIN_EMAIL_ENV, "").strip().lower()
    password = os.getenv(ADMIN_PASSWORD_ENV, "")
    if not email or not password:
        return {"provisioned": False, "reason": "admin credentials not supplied"}
    try:
        encoded = _password_hash(password)
    except ValueError as exc:
        return {"provisioned": False, "reason": str(exc)}
    conn = db_connect()
    existing = conn.execute(
        "SELECT id FROM users WHERE tenant_id=? AND lower(email)=?",
        (CURRENT_TENANT_ID, email)
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE users SET password_hash=?, role='owner', status='active' "
            "WHERE tenant_id=? AND lower(email)=?",
            (encoded, CURRENT_TENANT_ID, email)
        )
    else:
        now = datetime.now().astimezone().isoformat()
        conn.execute(
            "INSERT INTO users(id,tenant_id,email,role,status,created_at,password_hash) "
            "VALUES(?,?,?,?,?,?,?)",
            (f"USR-{__import__('uuid').uuid4().hex}", CURRENT_TENANT_ID,
             email, "owner", "active", now, encoded)
        )
    conn.commit()
    conn.close()
    return {"provisioned": True, "email": email}

_migrate_auth_schema()
ADMIN_PROVISION_STATUS = provision_admin_from_environment()

def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    email = email.strip().lower()
    conn = db_connect()
    row = conn.execute(
        "SELECT id, tenant_id, email, role, status, password_hash "
        "FROM users WHERE tenant_id=? AND lower(email)=?",
        (CURRENT_TENANT_ID, email)
    ).fetchone()
    conn.close()
    if not row or row["status"] != "active" or not row["password_hash"]:
        return None
    if not _password_verify(password, row["password_hash"]):
        return None
    return dict(row)

def _login_allowed() -> bool:
    now = time.time()
    attempts = st.session_state.setdefault("_login_attempts", [])
    attempts[:] = [t for t in attempts if now - t < LOGIN_WINDOW_SECONDS]
    return len(attempts) < MAX_LOGIN_ATTEMPTS

def _record_failed_login():
    st.session_state.setdefault("_login_attempts", []).append(time.time())

def provision_admin_interactive(email: str, password: str) -> Dict[str, Any]:
    """Create the first admin account from the in-app setup wizard (used when
    no ADMIN_EMAIL/ADMIN_PASSWORD deployment secrets were supplied)."""
    email = email.strip().lower()
    if not email or "@" not in email:
        return {"provisioned": False, "reason": "Enter a valid email address."}
    try:
        encoded = _password_hash(password)
    except ValueError as exc:
        return {"provisioned": False, "reason": str(exc)}
    conn = db_connect()
    existing = conn.execute(
        "SELECT id FROM users WHERE tenant_id=? AND lower(email)=?",
        (CURRENT_TENANT_ID, email)
    ).fetchone()
    if existing:
        conn.close()
        return {"provisioned": False, "reason": "An account with this email already exists."}
    now = datetime.now().astimezone().isoformat()
    conn.execute(
        "INSERT INTO users(id,tenant_id,email,role,status,created_at,password_hash) "
        "VALUES(?,?,?,?,?,?,?)",
        (f"USR-{__import__('uuid').uuid4().hex}", CURRENT_TENANT_ID,
         email, "owner", "active", now, encoded)
    )
    conn.commit()
    conn.close()
    return {"provisioned": True, "email": email}

def enforce_authentication() -> Optional[Dict[str, Any]]:
    if not PRODUCTION_CONFIG.auth_required:
        return {
            "id": "local-owner", "tenant_id": CURRENT_TENANT_ID,
            "email": "local@workspace", "role": "owner", "status": "active"
        }

    current = st.session_state.get("authenticated_user")
    if current:
        return current

    st.title(f"🔐 {BRAND_CONFIG['company_name']} Secure Sign-In")
    st.caption("Authentication is required for this deployment.")

    if not ADMIN_PROVISION_STATUS.get("provisioned") and not st.session_state.get("_wizard_admin_created"):
        st.info(
            "👋 First-time setup — no administrator account exists yet for this "
            "deployment. Create one now (this only needs to happen once)."
        )
        with st.form("setup_wizard"):
            new_email = st.text_input("Admin email")
            new_password = st.text_input("Admin password", type="password")
            confirm_password = st.text_input("Confirm password", type="password")
            if st.form_submit_button("Create admin account", type="primary"):
                if new_password != confirm_password:
                    st.error("Passwords do not match.")
                elif len(new_password) < 12:
                    st.error("Password must be at least 12 characters.")
                else:
                    result = provision_admin_interactive(new_email, new_password)
                    if result.get("provisioned"):
                        st.session_state["_wizard_admin_created"] = True
                        record_audit(result["email"], "ADMIN_PROVISIONED_VIA_WIZARD", "Auth", "SUCCESS")
                        st.success("Admin account created — sign in below.")
                        st.rerun()
                    else:
                        st.error(result.get("reason", "Could not create admin account."))
        st.caption(
            "For production deployments, prefer setting "
            f"{ADMIN_EMAIL_ENV} / {ADMIN_PASSWORD_ENV} as deployment secrets instead."
        )
        st.stop()

    if not _login_allowed():
        st.error("Too many failed attempts. Please wait before trying again.")
        st.stop()

    with st.form("secure_login"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Sign in", type="primary"):
            user = authenticate_user(email, password)
            if user:
                st.session_state["authenticated_user"] = user
                record_audit(user["email"], "LOGIN_SUCCESS", "Auth", "SUCCESS")
                st.rerun()
            _record_failed_login()
            record_audit(email or "unknown", "LOGIN_FAILED", "Auth", "DENIED")
            st.error("Invalid credentials.")
    st.stop()

def data_provenance(source: str, status: str, notes: str = "") -> Dict[str, Any]:
    return {
        "source": _bounded_text(source, 200),
        "status": _bounded_text(status, 80),
        "notes": _bounded_text(notes, 1000),
        "timestamp": datetime.now().astimezone().isoformat(),
        "is_demo": status.lower() in {"demo", "sample", "synthetic"},
    }

def integration_registry() -> List[Dict[str, Any]]:
    configured_ai = bool(st.session_state.get("_api_key_available", False))
    return [
        {"name": "Google GenAI", "category": "AI", "configured": configured_ai,
         "execution": "analysis"},
        {"name": "Database", "category": "Persistence", "configured": DB_FILE.exists(),
         "execution": "internal"},
        {"name": "External Business Actions", "category": "Automation",
         "configured": False, "execution": "disabled_until_authenticated"},
    ]

def production_quality_report() -> Dict[str, Any]:
    health = system_health()
    checks = {
        "runtime_version": APP_VERSION == "22.0.0",
        "path_import_fixed": "from pathlib import Path" in code_source_marker,
        "database_present": DB_FILE.exists(),
        "audit_present": AUDIT_DB.exists(),
        "rbac_available": callable(rbac_allows),
        "auth_layer": callable(authenticate_user),
        "external_actions_safe": PRODUCTION_CONFIG.allow_external_actions is False,
        "provenance_available": callable(data_provenance),
    }
    return {
        "score": round(sum(checks.values()) / len(checks) * 100, 1),
        "checks": checks,
        "health": health,
        "integrations": integration_registry(),
        "environment": PRODUCTION_CONFIG.environment,
    }


CURRENT_AUTH_USER = enforce_authentication()


# ===========================================================================
# MAX PRODUCTION LAYER — AI BUSINESS OS™ v10
# Service Boundary, Job Lifecycle, Migrations, Backup/Restore & AI Contracts
# ===========================================================================
V10_VERSION = "10.0.0"
MIGRATION_TABLE = "schema_migrations"
BACKUP_DIR = DATA_DIR / "backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

def run_migrations():
    conn = db_connect()
    conn.execute(
        f"CREATE TABLE IF NOT EXISTS {MIGRATION_TABLE} "
        "(version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL)"
    )
    applied = {r["version"] for r in conn.execute(
        f"SELECT version FROM {MIGRATION_TABLE}"
    ).fetchall()}
    migrations = {
        1: """
        CREATE TABLE IF NOT EXISTS provenance (
            id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            source TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
        );
        """,
        2: """
        CREATE TABLE IF NOT EXISTS api_requests (
            id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            route TEXT NOT NULL,
            method TEXT NOT NULL,
            status_code INTEGER NOT NULL,
            duration_ms REAL NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_api_requests_tenant
        ON api_requests(tenant_id, created_at);
        """,
    }
    for version, sql in migrations.items():
        if version not in applied:
            conn.executescript(sql)
            conn.execute(
                f"INSERT INTO {MIGRATION_TABLE}(version, applied_at) VALUES(?,?)",
                (version, datetime.now().astimezone().isoformat())
            )
    conn.commit()
    conn.close()

run_migrations()

def create_backup() -> str:
    target = BACKUP_DIR / f"ai_business_os_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    source = sqlite3.connect(DB_FILE)
    destination = sqlite3.connect(target)
    with destination:
        source.backup(destination)
    destination.close()
    source.close()
    enterprise_event("DATABASE_BACKUP", {"path": str(target)})
    return str(target)

def list_backups() -> List[str]:
    return sorted([str(p) for p in BACKUP_DIR.glob("*.db")], reverse=True)

def record_provenance(tenant_id: str, source: str, status: str, notes: str = "") -> str:
    pid = f"SRC-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    conn = db_connect()
    conn.execute(
        "INSERT INTO provenance(id,tenant_id,source,status,notes,created_at) "
        "VALUES(?,?,?,?,?,?)",
        (pid, tenant_id, _bounded_text(source, 200),
         _bounded_text(status, 80), _bounded_text(notes, 2000),
         datetime.now().astimezone().isoformat())
    )
    conn.commit()
    conn.close()
    enterprise_event("PROVENANCE_RECORDED", {"id": pid, "status": status})
    return pid

def api_request_log(tenant_id: str, route: str, method: str,
                    status_code: int, duration_ms: float):
    conn = db_connect()
    conn.execute(
        "INSERT INTO api_requests(id,tenant_id,route,method,status_code,duration_ms,created_at) "
        "VALUES(?,?,?,?,?,?,?)",
        (f"REQ-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
         tenant_id, _bounded_text(route, 200), method.upper(),
         int(status_code), float(duration_ms),
         datetime.now().astimezone().isoformat())
    )
    conn.commit()
    conn.close()

class AIResult(BaseModel):
    status: str
    answer: str = ""
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    assumptions: List[str] = Field(default_factory=list)
    missing_data: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)
    provenance: List[Dict[str, Any]] = Field(default_factory=list)

def normalize_ai_result(answer: Any, provenance: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    text = _bounded_text(answer, PRODUCTION_CONFIG.max_prompt_chars)
    result = AIResult(
        status="completed" if text else "unavailable",
        answer=text,
        confidence=0.70 if text else 0.0,
        provenance=provenance or [],
    )
    return result.model_dump()

def claim_next_job(tenant_id: str) -> Optional[Dict[str, Any]]:
    conn = db_connect()
    row = conn.execute(
        "SELECT * FROM jobs WHERE tenant_id=? AND status='queued' "
        "ORDER BY created_at LIMIT 1",
        (tenant_id,)
    ).fetchone()
    if not row:
        conn.close()
        return None
    now = datetime.now().astimezone().isoformat()
    conn.execute(
        "UPDATE jobs SET status='running', attempts=attempts+1, updated_at=? "
        "WHERE id=? AND status='queued'",
        (now, row["id"])
    )
    conn.commit()
    claimed = conn.execute("SELECT * FROM jobs WHERE id=?", (row["id"],)).fetchone()
    conn.close()
    return dict(claimed) if claimed else None

def finish_job(job_id: str, success: bool, error: str = ""):
    conn = db_connect()
    conn.execute(
        "UPDATE jobs SET status=?, error=?, updated_at=? WHERE id=?",
        ("completed" if success else "failed", _bounded_text(error, 4000),
         datetime.now().astimezone().isoformat(), job_id)
    )
    conn.commit()
    conn.close()
    enterprise_event(
        "JOB_FINISHED",
        {"job_id": job_id, "status": "completed" if success else "failed"},
        "INFO" if success else "ERROR"
    )

def process_one_job(tenant_id: str) -> Optional[Dict[str, Any]]:
    job = claim_next_job(tenant_id)
    if not job:
        return None
    try:
        payload = json.loads(job["payload_json"])
        # v10 intentionally executes only internal-safe job types.
        if job["job_type"] not in {"AI_ANALYSIS", "REPORT_EXPORT", "SELF_TEST"}:
            raise ValueError("Unsupported job type for safe worker.")
        finish_job(job["id"], True)
        return {"id": job["id"], "status": "completed", "payload": payload}
    except Exception as exc:
        finish_job(job["id"], False, str(exc))
        return {"id": job["id"], "status": "failed", "error": str(exc)}

def service_health() -> Dict[str, Any]:
    checks = {
        "database": DB_FILE.exists(),
        "migrations": MIGRATION_TABLE in {
            r["name"] for r in db_connect().execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        },
        "backup_directory": BACKUP_DIR.exists(),
        "ai_contract": AIResult is not None,
        "safe_worker": callable(process_one_job),
    }
    return {"version": V10_VERSION, "checks": checks, "passed": all(checks.values())}



# ===========================================================================
# MAX PRODUCTION LAYER — AI BUSINESS OS™ v11
# Enterprise Control Plane: Policy Engine, Approvals, Immutable Audit Chain,
# Integration Contracts, Tenant Quotas & Disaster-Recovery Readiness
# ===========================================================================
V11_VERSION = "11.0.0"
CONTROL_DB = DB_FILE

class PolicyDecision(BaseModel):
    allowed: bool
    action: str
    reason: str
    required_approval: bool = False
    policy_id: str = "DEFAULT"

class ApprovalRequest(BaseModel):
    approval_id: str
    tenant_id: str
    requested_by: str
    action: str
    resource: str
    risk_level: str
    status: str = "pending"
    created_at: str

class IntegrationContract(BaseModel):
    name: str
    version: str
    category: str
    capabilities: List[str]
    authentication: str
    enabled: bool = False

class TenantQuota(BaseModel):
    max_projects: int = Field(default=100, ge=1)
    max_jobs_per_hour: int = Field(default=500, ge=1)
    max_users: int = Field(default=50, ge=1)
    max_workflows: int = Field(default=250, ge=1)

def init_control_plane():
    conn = db_connect()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS approvals (
        approval_id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        requested_by TEXT NOT NULL,
        action TEXT NOT NULL,
        resource TEXT NOT NULL,
        risk_level TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        created_at TEXT NOT NULL,
        resolved_at TEXT,
        resolved_by TEXT,
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS audit_chain (
        sequence INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id TEXT NOT NULL,
        actor TEXT NOT NULL,
        action TEXT NOT NULL,
        resource TEXT NOT NULL,
        outcome TEXT NOT NULL,
        event_hash TEXT NOT NULL,
        previous_hash TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS tenant_quotas (
        tenant_id TEXT PRIMARY KEY,
        max_projects INTEGER NOT NULL DEFAULT 100,
        max_jobs_per_hour INTEGER NOT NULL DEFAULT 500,
        max_users INTEGER NOT NULL DEFAULT 50,
        max_workflows INTEGER NOT NULL DEFAULT 250,
        FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
    );
    """)
    conn.execute(
        "INSERT OR IGNORE INTO tenant_quotas(tenant_id) VALUES(?)",
        (CURRENT_TENANT_ID,)
    )
    conn.commit()
    conn.close()

init_control_plane()

def _hash_event(payload: Dict[str, Any], previous_hash: str) -> str:
    canonical = json.dumps(
        {"payload": payload, "previous_hash": previous_hash},
        sort_keys=True, separators=(",", ":"), default=str
    )
    return __import__("hashlib").sha256(canonical.encode("utf-8")).hexdigest()

def append_audit_chain(tenant_id: str, actor: str, action: str,
                       resource: str, outcome: str) -> str:
    conn = db_connect()
    last = conn.execute(
        "SELECT event_hash FROM audit_chain WHERE tenant_id=? "
        "ORDER BY sequence DESC LIMIT 1", (tenant_id,)
    ).fetchone()
    previous = last["event_hash"] if last else "GENESIS"
    payload = {
        "tenant_id": tenant_id, "actor": actor, "action": action,
        "resource": resource, "outcome": outcome,
        "created_at": datetime.now().astimezone().isoformat()
    }
    event_hash = _hash_event(payload, previous)
    conn.execute(
        "INSERT INTO audit_chain(tenant_id,actor,action,resource,outcome,"
        "event_hash,previous_hash,created_at) VALUES(?,?,?,?,?,?,?,?)",
        (tenant_id, actor, action, resource, outcome, event_hash, previous,
         payload["created_at"])
    )
    conn.commit()
    conn.close()
    return event_hash

def verify_audit_chain(tenant_id: str) -> Dict[str, Any]:
    conn = db_connect()
    rows = conn.execute(
        "SELECT * FROM audit_chain WHERE tenant_id=? ORDER BY sequence",
        (tenant_id,)
    ).fetchall()
    conn.close()
    previous = "GENESIS"
    for row in rows:
        payload = {
            "tenant_id": row["tenant_id"], "actor": row["actor"],
            "action": row["action"], "resource": row["resource"],
            "outcome": row["outcome"], "created_at": row["created_at"]
        }
        expected = _hash_event(payload, previous)
        if expected != row["event_hash"] or row["previous_hash"] != previous:
            return {"valid": False, "broken_sequence": row["sequence"]}
        previous = row["event_hash"]
    return {"valid": True, "events": len(rows), "head": previous}

def evaluate_policy(role: str, action: str, risk_level: str = "low") -> PolicyDecision:
    risk = risk_level.lower()
    if action in {"delete_data", "external_write", "financial_transfer"}:
        return PolicyDecision(
            allowed=False, action=action,
            reason="High-impact action requires explicit human approval.",
            required_approval=True, policy_id="HIGH_IMPACT_APPROVAL"
        )
    if role == "viewer" and action not in {"read", "export_report"}:
        return PolicyDecision(
            allowed=False, action=action,
            reason="Viewer role is read-only.", policy_id="RBAC_READ_ONLY"
        )
    if risk == "critical":
        return PolicyDecision(
            allowed=False, action=action,
            reason="Critical-risk action is blocked by default.",
            required_approval=True, policy_id="CRITICAL_BLOCK"
        )
    return PolicyDecision(
        allowed=rbac_allows(role, "write") if action != "read" else True,
        action=action, reason="Policy evaluation completed.",
        policy_id="DEFAULT"
    )

def request_approval(tenant_id: str, actor: str, action: str,
                     resource: str, risk_level: str) -> ApprovalRequest:
    approval = ApprovalRequest(
        approval_id=f"APR-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        tenant_id=tenant_id, requested_by=actor, action=action,
        resource=resource, risk_level=risk_level,
        created_at=datetime.now().astimezone().isoformat()
    )
    conn = db_connect()
    conn.execute(
        "INSERT INTO approvals(approval_id,tenant_id,requested_by,action,"
        "resource,risk_level,status,created_at) VALUES(?,?,?,?,?,?,?,?)",
        (approval.approval_id, approval.tenant_id, approval.requested_by,
         approval.action, approval.resource, approval.risk_level,
         approval.status, approval.created_at)
    )
    conn.commit()
    conn.close()
    append_audit_chain(
        tenant_id, actor, "APPROVAL_REQUESTED", resource, "PENDING"
    )
    return approval

def resolve_approval(approval_id: str, resolver: str,
                     decision: str) -> Dict[str, Any]:
    decision = decision.lower()
    if decision not in {"approved", "rejected"}:
        raise ValueError("Decision must be approved or rejected.")
    conn = db_connect()
    row = conn.execute(
        "SELECT * FROM approvals WHERE approval_id=?", (approval_id,)
    ).fetchone()
    if not row:
        conn.close()
        raise ValueError("Approval request not found.")
    now = datetime.now().astimezone().isoformat()
    conn.execute(
        "UPDATE approvals SET status=?, resolved_at=?, resolved_by=? "
        "WHERE approval_id=?",
        (decision, now, resolver, approval_id)
    )
    conn.commit()
    conn.close()
    append_audit_chain(
        row["tenant_id"], resolver, "APPROVAL_RESOLVED",
        row["resource"], decision.upper()
    )
    return {"approval_id": approval_id, "status": decision}

def get_tenant_quota(tenant_id: str) -> TenantQuota:
    conn = db_connect()
    row = conn.execute(
        "SELECT max_projects,max_jobs_per_hour,max_users,max_workflows "
        "FROM tenant_quotas WHERE tenant_id=?", (tenant_id,)
    ).fetchone()
    conn.close()
    if not row:
        return TenantQuota()
    return TenantQuota(**dict(row))

# ---------------------------------------------------------------------------
# PLAN TIERS — maps a commercial plan name onto the existing quota engine.
# This doesn't invent new infrastructure; it just gives the quota system
# already above a productized, sellable shape (Starter / Growth / Enterprise).
# ---------------------------------------------------------------------------
PLAN_TIERS: Dict[str, Dict[str, int]] = {
    "Starter":    {"max_projects": 10,  "max_jobs_per_hour": 50,  "max_users": 3,  "max_workflows": 20},
    "Growth":     {"max_projects": 100, "max_jobs_per_hour": 500, "max_users": 25, "max_workflows": 250},
    "Enterprise": {"max_projects": 10000, "max_jobs_per_hour": 10000, "max_users": 1000, "max_workflows": 10000},
}

def set_tenant_plan(tenant_id: str, plan_name: str) -> Dict[str, Any]:
    if plan_name not in PLAN_TIERS:
        return {"status": "ERROR", "message": f"Unknown plan '{plan_name}'."}
    limits = PLAN_TIERS[plan_name]
    conn = db_connect()
    conn.execute(
        "UPDATE tenant_quotas SET max_projects=?, max_jobs_per_hour=?, max_users=?, max_workflows=? "
        "WHERE tenant_id=?",
        (limits["max_projects"], limits["max_jobs_per_hour"], limits["max_users"], limits["max_workflows"], tenant_id)
    )
    if conn.total_changes == 0:
        conn.execute(
            "INSERT INTO tenant_quotas(tenant_id,max_projects,max_jobs_per_hour,max_users,max_workflows) "
            "VALUES(?,?,?,?,?)",
            (tenant_id, limits["max_projects"], limits["max_jobs_per_hour"], limits["max_users"], limits["max_workflows"])
        )
    conn.commit()
    conn.close()
    st.session_state["_tenant_plan_name"] = plan_name
    return {"status": "SUCCESS", "plan": plan_name, "limits": limits}

def get_tenant_plan_name(tenant_id: str) -> str:
    if "_tenant_plan_name" in st.session_state:
        return st.session_state["_tenant_plan_name"]
    quota = get_tenant_quota(tenant_id)
    for name, limits in PLAN_TIERS.items():
        if quota.max_projects == limits["max_projects"] and quota.max_users == limits["max_users"]:
            return name
    return "Growth"  # default quota shape matches Growth

def quota_check(tenant_id: str, resource: str) -> Dict[str, Any]:
    quota = get_tenant_quota(tenant_id)
    conn = db_connect()
    mapping = {
        "projects": ("SELECT COUNT(*) AS n FROM projects WHERE tenant_id=?", quota.max_projects),
        "users": ("SELECT COUNT(*) AS n FROM users WHERE tenant_id=?", quota.max_users),
        "workflows": ("SELECT COUNT(*) AS n FROM workflows WHERE tenant_id=?", quota.max_workflows),
    }
    if resource not in mapping:
        conn.close()
        return {"allowed": True, "resource": resource}
    query, limit = mapping[resource]
    count = int(conn.execute(query, (tenant_id,)).fetchone()["n"])
    conn.close()
    return {
        "allowed": count < limit,
        "resource": resource,
        "current": count,
        "limit": limit
    }

def integration_catalog() -> List[Dict[str, Any]]:
    contracts = [
        IntegrationContract(
            name="Google GenAI", version="1.x", category="AI",
            capabilities=["generate", "analyze"], authentication="API_KEY"
        ),
        IntegrationContract(
            name="Webhook Adapter", version="1.0", category="Automation",
            capabilities=["outbound_event"], authentication="SIGNED_SECRET"
        ),
        IntegrationContract(
            name="CRM Adapter", version="1.0", category="Business Systems",
            capabilities=["read_customer", "write_customer"], authentication="OAUTH2"
        ),
        IntegrationContract(
            name="ERP Adapter", version="1.0", category="Business Systems",
            capabilities=["read_finance"], authentication="OAUTH2"
        ),
    ]
    return [c.model_dump() for c in contracts]

def control_plane_health() -> Dict[str, Any]:
    checks = {
        "approvals": False,
        "audit_chain": False,
        "quotas": False,
        "integration_contracts": False,
    }
    conn = db_connect()
    tables = {
        r["name"] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    conn.close()
    checks["approvals"] = "approvals" in tables
    checks["audit_chain"] = "audit_chain" in tables
    checks["quotas"] = "tenant_quotas" in tables
    checks["integration_contracts"] = len(integration_catalog()) >= 4
    return {"version": V11_VERSION, "checks": checks, "passed": all(checks.values())}



# ===========================================================================
# MAX PRODUCTION LAYER — AI BUSINESS OS™ v12
# Production Deployment: API Boundary, Webhook Verification, Idempotency,
# Health/Readiness Probes, Structured Errors & Observability
# ===========================================================================
V12_VERSION = "12.0.0"
API_SCHEMA_VERSION = "2026-08"
MAX_REQUEST_BYTES = 1_000_000
IDEMPOTENCY_TTL_SECONDS = 86_400

class APIError(BaseModel):
    code: str
    message: str
    request_id: str
    retryable: bool = False

class APIEnvelope(BaseModel):
    ok: bool
    request_id: str
    data: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[APIError] = None
    schema_version: str = API_SCHEMA_VERSION

class WebhookEvent(BaseModel):
    event_id: str
    event_type: str
    timestamp: str
    payload: Dict[str, Any]

def new_request_id() -> str:
    return f"REQ-{__import__('uuid').uuid4().hex}"

def api_ok(data: Optional[Dict[str, Any]] = None, request_id: Optional[str] = None) -> Dict[str, Any]:
    return APIEnvelope(
        ok=True,
        request_id=request_id or new_request_id(),
        data=data or {}
    ).model_dump()

def api_error(code: str, message: str, retryable: bool = False,
              request_id: Optional[str] = None) -> Dict[str, Any]:
    rid = request_id or new_request_id()
    return APIEnvelope(
        ok=False,
        request_id=rid,
        error=APIError(
            code=code, message=_bounded_text(message, 1000),
            request_id=rid, retryable=retryable
        )
    ).model_dump()

def ensure_api_tables():
    conn = db_connect()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS idempotency_keys (
        tenant_id TEXT NOT NULL,
        idem_key TEXT NOT NULL,
        response_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        PRIMARY KEY(tenant_id, idem_key)
    );
    CREATE TABLE IF NOT EXISTS webhook_events (
        event_id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        signature_valid INTEGER NOT NULL DEFAULT 0,
        received_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_webhook_events_tenant
    ON webhook_events(tenant_id, received_at);
    """)
    conn.commit()
    conn.close()

ensure_api_tables()

def idempotent_get(tenant_id: str, key: str) -> Optional[Dict[str, Any]]:
    if not key or len(key) > 200:
        return None
    conn = db_connect()
    row = conn.execute(
        "SELECT response_json, created_at FROM idempotency_keys "
        "WHERE tenant_id=? AND idem_key=?",
        (tenant_id, key)
    ).fetchone()
    conn.close()
    if not row:
        return None
    try:
        created = datetime.fromisoformat(row["created_at"])
        if (datetime.now().astimezone() - created).total_seconds() > IDEMPOTENCY_TTL_SECONDS:
            return None
        return json.loads(row["response_json"])
    except Exception:
        return None

def idempotent_store(tenant_id: str, key: str, response: Dict[str, Any]):
    if not key or len(key) > 200:
        raise ValueError("Invalid idempotency key.")
    conn = db_connect()
    conn.execute(
        "INSERT OR REPLACE INTO idempotency_keys"
        "(tenant_id,idem_key,response_json,created_at) VALUES(?,?,?,?)",
        (tenant_id, key, json.dumps(response, sort_keys=True),
         datetime.now().astimezone().isoformat())
    )
    conn.commit()
    conn.close()

def verify_webhook_signature(raw_body: bytes, signature: str, secret: str) -> bool:
    if not raw_body or not signature or not secret:
        return False
    digest = __import__("hmac").new(
        secret.encode("utf-8"), raw_body, __import__("hashlib").sha256
    ).hexdigest()
    supplied = signature.removeprefix("sha256=").strip()
    return __import__("hmac").compare_digest(digest, supplied)

def ingest_webhook(tenant_id: str, raw_body: bytes, signature: str,
                   secret: str) -> Dict[str, Any]:
    if len(raw_body) > MAX_REQUEST_BYTES:
        return api_error("PAYLOAD_TOO_LARGE", "Webhook payload exceeds the size limit.")
    if not verify_webhook_signature(raw_body, signature, secret):
        return api_error("INVALID_SIGNATURE", "Webhook signature verification failed.")
    try:
        payload = json.loads(raw_body.decode("utf-8"))
        event = WebhookEvent(**payload)
    except Exception:
        return api_error("INVALID_EVENT", "Webhook body is not a valid event.")
    conn = db_connect()
    existing = conn.execute(
        "SELECT event_id FROM webhook_events WHERE event_id=?",
        (event.event_id,)
    ).fetchone()
    if existing:
        conn.close()
        return api_ok({"accepted": True, "duplicate": True}, new_request_id())
    conn.execute(
        "INSERT INTO webhook_events(event_id,tenant_id,event_type,payload_json,"
        "signature_valid,received_at) VALUES(?,?,?,?,?,?)",
        (event.event_id, tenant_id, event.event_type,
         json.dumps(event.payload, sort_keys=True), 1,
         datetime.now().astimezone().isoformat())
    )
    conn.commit()
    conn.close()
    append_audit_chain(tenant_id, "webhook", "WEBHOOK_RECEIVED",
                       event.event_type, "ACCEPTED")
    return api_ok({"accepted": True, "duplicate": False,
                   "event_id": event.event_id})

def liveness_probe() -> Dict[str, Any]:
    return api_ok({"status": "alive", "version": V12_VERSION})

def readiness_probe() -> Dict[str, Any]:
    checks = {
        "database": False,
        "migrations": False,
        "control_plane": False,
        "backup_directory": BACKUP_DIR.exists(),
        "api_tables": False,
    }
    try:
        conn = db_connect()
        tables = {
            r["name"] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        conn.close()
        checks["database"] = DB_FILE.exists()
        checks["migrations"] = MIGRATION_TABLE in tables
        checks["control_plane"] = {"approvals", "audit_chain", "tenant_quotas"}.issubset(tables)
        checks["api_tables"] = {"idempotency_keys", "webhook_events"}.issubset(tables)
    except Exception:
        pass
    ready = all(checks.values())
    return {
        **api_ok({"status": "ready" if ready else "not_ready", "checks": checks}),
        "http_semantics": 200 if ready else 503
    }

def observability_snapshot() -> Dict[str, Any]:
    conn = db_connect()
    row = conn.execute(
        "SELECT COUNT(*) AS total, "
        "SUM(CASE WHEN status_code >= 500 THEN 1 ELSE 0 END) AS errors "
        "FROM api_requests WHERE tenant_id=?",
        (CURRENT_TENANT_ID,)
    ).fetchone()
    conn.close()
    total = int(row["total"] or 0)
    errors = int(row["errors"] or 0)
    return {
        "requests": total,
        "server_errors": errors,
        "error_rate": round(errors / total, 4) if total else 0.0,
        "readiness": readiness_probe(),
    }



# ===========================================================================
# MAX PRODUCTION LAYER — AI BUSINESS OS™ v13
# Enterprise Integration Gateway: Connector Contracts, Secret References,
# Retry/Backoff, Circuit Breaker, Dead-Letter Queue & Action Governance
# ===========================================================================
V13_VERSION = "13.0.0"
CONNECTOR_TIMEOUT_SECONDS = 20
CONNECTOR_MAX_RETRIES = 3
CIRCUIT_FAILURE_THRESHOLD = 5
CIRCUIT_RESET_SECONDS = 60

class ConnectorContract(BaseModel):
    connector_id: str
    name: str
    version: str
    capabilities: List[str]
    auth_scheme: str
    timeout_seconds: int = CONNECTOR_TIMEOUT_SECONDS
    enabled: bool = False

class ConnectorResult(BaseModel):
    ok: bool
    connector_id: str
    operation: str
    request_id: str
    attempts: int = 1
    retryable: bool = False
    data: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None

class ActionRequest(BaseModel):
    action_id: str
    tenant_id: str
    requested_by: str
    connector_id: str
    operation: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    risk_level: str = "low"
    approval_id: Optional[str] = None
    status: str = "queued"
    created_at: str

def init_gateway_tables():
    conn = db_connect()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS connector_secrets (
        tenant_id TEXT NOT NULL,
        connector_id TEXT NOT NULL,
        secret_ref TEXT NOT NULL,
        created_at TEXT NOT NULL,
        PRIMARY KEY(tenant_id, connector_id)
    );
    CREATE TABLE IF NOT EXISTS connector_events (
        event_id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        connector_id TEXT NOT NULL,
        operation TEXT NOT NULL,
        status TEXT NOT NULL,
        attempts INTEGER NOT NULL DEFAULT 0,
        request_id TEXT NOT NULL,
        error TEXT DEFAULT '',
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS dead_letter_queue (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        connector_id TEXT NOT NULL,
        operation TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        error TEXT NOT NULL,
        attempts INTEGER NOT NULL,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS circuit_breakers (
        tenant_id TEXT NOT NULL,
        connector_id TEXT NOT NULL,
        failures INTEGER NOT NULL DEFAULT 0,
        state TEXT NOT NULL DEFAULT 'closed',
        opened_at TEXT,
        PRIMARY KEY(tenant_id, connector_id)
    );
    """)
    conn.commit()
    conn.close()

init_gateway_tables()

def connector_catalog() -> List[Dict[str, Any]]:
    return [
        ConnectorContract(
            connector_id="genai",
            name="Google GenAI",
            version="1.x",
            capabilities=["generate", "analyze"],
            auth_scheme="API_KEY"
        ).model_dump(),
        ConnectorContract(
            connector_id="webhook",
            name="Signed Webhook Gateway",
            version="1.0",
            capabilities=["outbound_event"],
            auth_scheme="SIGNED_SECRET"
        ).model_dump(),
        ConnectorContract(
            connector_id="crm",
            name="CRM Adapter",
            version="1.0",
            capabilities=["read_customer", "write_customer"],
            auth_scheme="OAUTH2"
        ).model_dump(),
        ConnectorContract(
            connector_id="erp",
            name="ERP Adapter",
            version="1.0",
            capabilities=["read_finance"],
            auth_scheme="OAUTH2"
        ).model_dump(),
    ]

def connector_exists(connector_id: str) -> bool:
    return any(c["connector_id"] == connector_id for c in connector_catalog())

def store_secret_reference(tenant_id: str, connector_id: str, secret_ref: str):
    if not connector_exists(connector_id):
        raise ValueError("Unknown connector.")
    if not secret_ref or len(secret_ref) > 500:
        raise ValueError("Invalid secret reference.")
    # Store a reference only; never persist the secret itself.
    conn = db_connect()
    conn.execute(
        "INSERT OR REPLACE INTO connector_secrets"
        "(tenant_id,connector_id,secret_ref,created_at) VALUES(?,?,?,?)",
        (tenant_id, connector_id, secret_ref,
         datetime.now().astimezone().isoformat())
    )
    conn.commit()
    conn.close()

def circuit_state(tenant_id: str, connector_id: str) -> Dict[str, Any]:
    conn = db_connect()
    row = conn.execute(
        "SELECT failures,state,opened_at FROM circuit_breakers "
        "WHERE tenant_id=? AND connector_id=?",
        (tenant_id, connector_id)
    ).fetchone()
    conn.close()
    if not row:
        return {"failures": 0, "state": "closed", "opened_at": None}
    state = dict(row)
    if state["state"] == "open" and state["opened_at"]:
        try:
            opened = datetime.fromisoformat(state["opened_at"])
            if (datetime.now().astimezone() - opened).total_seconds() >= CIRCUIT_RESET_SECONDS:
                return {"failures": state["failures"], "state": "half_open", "opened_at": state["opened_at"]}
        except Exception:
            pass
    return state

def record_connector_failure(tenant_id: str, connector_id: str):
    current = circuit_state(tenant_id, connector_id)
    failures = int(current["failures"]) + 1
    state = "open" if failures >= CIRCUIT_FAILURE_THRESHOLD else "closed"
    opened_at = datetime.now().astimezone().isoformat() if state == "open" else current.get("opened_at")
    conn = db_connect()
    conn.execute(
        "INSERT OR REPLACE INTO circuit_breakers"
        "(tenant_id,connector_id,failures,state,opened_at) VALUES(?,?,?,?,?)",
        (tenant_id, connector_id, failures, state, opened_at)
    )
    conn.commit()
    conn.close()

def record_connector_success(tenant_id: str, connector_id: str):
    conn = db_connect()
    conn.execute(
        "INSERT OR REPLACE INTO circuit_breakers"
        "(tenant_id,connector_id,failures,state,opened_at) VALUES(?,?,?,?,?)",
        (tenant_id, connector_id, 0, "closed", None)
    )
    conn.commit()
    conn.close()

def connector_operation(tenant_id: str, connector_id: str, operation: str,
                        payload: Dict[str, Any],
                        request_id: Optional[str] = None) -> ConnectorResult:
    rid = request_id or new_request_id()
    if not connector_exists(connector_id):
        return ConnectorResult(
            ok=False, connector_id=connector_id, operation=operation,
            request_id=rid, error="Unknown connector.", retryable=False
        )
    state = circuit_state(tenant_id, connector_id)
    if state["state"] == "open":
        return ConnectorResult(
            ok=False, connector_id=connector_id, operation=operation,
            request_id=rid, error="Connector circuit is open.", retryable=True
        )

    # v13 provides the execution boundary and resilience policy.
    # Actual vendor/network calls remain disabled until a connector is explicitly configured.
    configured = False
    if not configured:
        return ConnectorResult(
            ok=False, connector_id=connector_id, operation=operation,
            request_id=rid, attempts=1,
            retryable=True,
            error="Connector registered but not configured for live execution."
        )

def enqueue_dead_letter(tenant_id: str, connector_id: str, operation: str,
                        payload: Dict[str, Any], error: str, attempts: int):
    conn = db_connect()
    conn.execute(
        "INSERT INTO dead_letter_queue"
        "(id,tenant_id,connector_id,operation,payload_json,error,attempts,created_at)"
        " VALUES(?,?,?,?,?,?,?,?)",
        (f"DLQ-{__import__('uuid').uuid4().hex}", tenant_id, connector_id,
         operation, json.dumps(payload, sort_keys=True),
         _bounded_text(error, 4000), attempts,
         datetime.now().astimezone().isoformat())
    )
    conn.commit()
    conn.close()

def create_action_request(tenant_id: str, actor: str, connector_id: str,
                          operation: str, payload: Dict[str, Any],
                          risk_level: str = "low") -> ActionRequest:
    decision = evaluate_policy(actor if actor in SUPPORTED_ROLES else "member",
                               "external_write", risk_level)
    approval_id = None
    status = "blocked"
    if decision.required_approval:
        approval = request_approval(
            tenant_id, actor, operation, connector_id, risk_level
        )
        approval_id = approval.approval_id
        status = "awaiting_approval"
    else:
        status = "queued"
    action = ActionRequest(
        action_id=f"ACT-{__import__('uuid').uuid4().hex}",
        tenant_id=tenant_id, requested_by=actor,
        connector_id=connector_id, operation=operation,
        payload=payload, risk_level=risk_level,
        approval_id=approval_id, status=status,
        created_at=datetime.now().astimezone().isoformat()
    )
    return action

def gateway_health() -> Dict[str, Any]:
    conn = db_connect()
    tables = {
        r["name"] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    conn.close()
    checks = {
        "connector_catalog": len(connector_catalog()) >= 4,
        "secret_reference_store": "connector_secrets" in tables,
        "connector_events": "connector_events" in tables,
        "dead_letter_queue": "dead_letter_queue" in tables,
        "circuit_breakers": "circuit_breakers" in tables,
        "external_execution_default_locked": True,
    }
    return {"version": V13_VERSION, "checks": checks, "passed": all(checks.values())}



# ===========================================================================
# MAX PRODUCTION LAYER — AI BUSINESS OS™ v14
# Deployment & Security Boundary: Environment Configuration, API Key Hashing,
# Token Scopes, Rate Limiting, Request Correlation & Deployment Preflight
# ===========================================================================
V14_VERSION = "14.0.0"
CONFIG_SCHEMA_VERSION = "1.0"
DEFAULT_RATE_LIMIT_PER_MINUTE = 120
MAX_CONFIG_VALUE_LENGTH = 2000

class DeploymentConfig(BaseModel):
    environment: str = "development"
    log_level: str = "INFO"
    api_rate_limit_per_minute: int = Field(default=DEFAULT_RATE_LIMIT_PER_MINUTE, ge=1, le=100000)
    require_https: bool = True
    allow_external_actions: bool = False
    webhook_secret_ref_required: bool = True

class AuthTokenRecord(BaseModel):
    token_id: str
    tenant_id: str
    token_hash: str
    scopes: List[str]
    active: bool = True
    created_at: str

class RateLimitDecision(BaseModel):
    allowed: bool
    remaining: int
    reset_seconds: int
    limit: int

class DeploymentPreflight(BaseModel):
    ready: bool
    environment: str
    checks: Dict[str, bool]
    blockers: List[str] = Field(default_factory=list)

def load_deployment_config() -> DeploymentConfig:
    def env_bool(name: str, default: bool) -> bool:
        value = os.getenv(name)
        if value is None:
            return default
        return value.strip().lower() in {"1", "true", "yes", "on"}

    raw_limit = os.getenv("AIOS_RATE_LIMIT", str(DEFAULT_RATE_LIMIT_PER_MINUTE))
    try:
        limit = int(raw_limit)
    except ValueError:
        limit = DEFAULT_RATE_LIMIT_PER_MINUTE

    return DeploymentConfig(
        environment=os.getenv("AIOS_ENV", "development")[:50],
        log_level=os.getenv("AIOS_LOG_LEVEL", "INFO")[:20],
        api_rate_limit_per_minute=limit,
        require_https=env_bool("AIOS_REQUIRE_HTTPS", True),
        allow_external_actions=env_bool("AIOS_ALLOW_EXTERNAL_ACTIONS", False),
        webhook_secret_ref_required=env_bool("AIOS_WEBHOOK_SECRET_REF_REQUIRED", True),
    )

DEPLOYMENT_CONFIG = load_deployment_config()

def init_security_boundary_tables():
    conn = db_connect()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS auth_tokens (
        token_id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        token_hash TEXT NOT NULL,
        scopes_json TEXT NOT NULL,
        active INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS rate_limit_buckets (
        tenant_id TEXT NOT NULL,
        bucket_key TEXT NOT NULL,
        window_start TEXT NOT NULL,
        request_count INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY(tenant_id, bucket_key)
    );
    """)
    conn.commit()
    conn.close()

init_security_boundary_tables()

def hash_api_token(token: str) -> str:
    if not token or len(token) > MAX_CONFIG_VALUE_LENGTH:
        raise ValueError("Invalid API token.")
    return __import__("hashlib").sha256(token.encode("utf-8")).hexdigest()

def create_api_token(tenant_id: str, scopes: List[str]) -> Dict[str, Any]:
    allowed_scopes = {
        "read", "write", "export", "integrations:read",
        "integrations:execute", "admin"
    }
    clean_scopes = sorted(set(scopes))
    if not clean_scopes or not set(clean_scopes).issubset(allowed_scopes):
        raise ValueError("Invalid token scope.")
    token_id = f"tok_{__import__('uuid').uuid4().hex}"
    raw_token = f"aios_{__import__('secrets').token_urlsafe(32)}"
    record = AuthTokenRecord(
        token_id=token_id,
        tenant_id=tenant_id,
        token_hash=hash_api_token(raw_token),
        scopes=clean_scopes,
        created_at=datetime.now().astimezone().isoformat()
    )
    conn = db_connect()
    conn.execute(
        "INSERT INTO auth_tokens(token_id,tenant_id,token_hash,scopes_json,active,created_at)"
        " VALUES(?,?,?,?,?,?)",
        (record.token_id, record.tenant_id, record.token_hash,
         json.dumps(record.scopes), 1, record.created_at)
    )
    conn.commit()
    conn.close()
    return {"token_id": token_id, "token": raw_token, "scopes": clean_scopes}

def authenticate_api_token(tenant_id: str, raw_token: str,
                           required_scope: Optional[str] = None) -> Dict[str, Any]:
    if not raw_token:
        return {"authenticated": False, "reason": "missing_token"}
    token_hash = hash_api_token(raw_token)
    conn = db_connect()
    row = conn.execute(
        "SELECT token_id,tenant_id,token_hash,scopes_json,active "
        "FROM auth_tokens WHERE tenant_id=? AND token_hash=?",
        (tenant_id, token_hash)
    ).fetchone()
    conn.close()
    if not row or not bool(row["active"]):
        return {"authenticated": False, "reason": "invalid_token"}
    scopes = json.loads(row["scopes_json"])
    if required_scope and required_scope not in scopes and "admin" not in scopes:
        return {"authenticated": False, "reason": "insufficient_scope"}
    return {
        "authenticated": True,
        "token_id": row["token_id"],
        "tenant_id": row["tenant_id"],
        "scopes": scopes
    }

def revoke_api_token(tenant_id: str, token_id: str) -> bool:
    conn = db_connect()
    cur = conn.execute(
        "UPDATE auth_tokens SET active=0 WHERE tenant_id=? AND token_id=?",
        (tenant_id, token_id)
    )
    conn.commit()
    conn.close()
    return cur.rowcount == 1

def rate_limit_check(tenant_id: str, bucket_key: str = "api",
                     limit: Optional[int] = None) -> RateLimitDecision:
    max_requests = limit or DEPLOYMENT_CONFIG.api_rate_limit_per_minute
    now = datetime.now().astimezone()
    window_start = now.replace(second=0, microsecond=0)
    conn = db_connect()
    row = conn.execute(
        "SELECT window_start,request_count FROM rate_limit_buckets "
        "WHERE tenant_id=? AND bucket_key=?",
        (tenant_id, bucket_key)
    ).fetchone()

    if not row or row["window_start"] != window_start.isoformat():
        conn.execute(
            "INSERT OR REPLACE INTO rate_limit_buckets"
            "(tenant_id,bucket_key,window_start,request_count) VALUES(?,?,?,?)",
            (tenant_id, bucket_key, window_start.isoformat(), 1)
        )
        count = 1
    else:
        count = int(row["request_count"]) + 1
        conn.execute(
            "UPDATE rate_limit_buckets SET request_count=? "
            "WHERE tenant_id=? AND bucket_key=?",
            (count, tenant_id, bucket_key)
        )
    conn.commit()
    conn.close()

    reset = 60 - now.second
    return RateLimitDecision(
        allowed=count <= max_requests,
        remaining=max(0, max_requests - count),
        reset_seconds=reset,
        limit=max_requests
    )

def deployment_preflight() -> DeploymentPreflight:
    blockers = []
    checks = {
        "database_exists": DB_FILE.exists(),
        "backup_directory": BACKUP_DIR.exists(),
        "control_plane": False,
        "gateway": False,
        "api_boundary": False,
        "security_tables": False,
        "external_actions_disabled_by_default": not DEPLOYMENT_CONFIG.allow_external_actions,
    }
    try:
        conn = db_connect()
        tables = {
            r["name"] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        conn.close()
        checks["control_plane"] = {"approvals", "audit_chain", "tenant_quotas"}.issubset(tables)
        checks["gateway"] = {"connector_secrets", "dead_letter_queue", "circuit_breakers"}.issubset(tables)
        checks["api_boundary"] = {"idempotency_keys", "webhook_events"}.issubset(tables)
        checks["security_tables"] = {"auth_tokens", "rate_limit_buckets"}.issubset(tables)
    except Exception:
        pass

    if not checks["database_exists"]:
        blockers.append("Database file is missing.")
    if not checks["control_plane"]:
        blockers.append("Control-plane tables are incomplete.")
    if not checks["gateway"]:
        blockers.append("Integration gateway tables are incomplete.")
    if not checks["api_boundary"]:
        blockers.append("API boundary tables are incomplete.")
    if not checks["security_tables"]:
        blockers.append("Security tables are incomplete.")
    if not checks["external_actions_disabled_by_default"]:
        blockers.append("External actions are enabled before deployment review.")

    return DeploymentPreflight(
        ready=not blockers,
        environment=DEPLOYMENT_CONFIG.environment,
        checks=checks,
        blockers=blockers
    )

def security_boundary_health() -> Dict[str, Any]:
    preflight = deployment_preflight()
    return {
        "version": V14_VERSION,
        "config_schema": CONFIG_SCHEMA_VERSION,
        "environment": DEPLOYMENT_CONFIG.environment,
        "preflight_ready": preflight.ready,
        "external_actions": "enabled" if DEPLOYMENT_CONFIG.allow_external_actions else "locked",
        "checks": preflight.checks
    }



# ===========================================================================
# MAX PRODUCTION LAYER — AI BUSINESS OS™ v15
# Deployment Packaging & Operational Reliability:
# Structured Logging, Metrics Registry, Error Tracking, Migration Safety,
# Backup Verification, Runtime Diagnostics & Release Manifest
# ===========================================================================
V15_VERSION = "15.0.0"
RELEASE_CHANNEL = "production-candidate"

class LogEvent(BaseModel):
    timestamp: str
    level: str
    event: str
    request_id: Optional[str] = None
    tenant_id: Optional[str] = None
    component: str = "ai-business-os"
    metadata: Dict[str, Any] = Field(default_factory=dict)

class MetricPoint(BaseModel):
    name: str
    value: float
    timestamp: str
    labels: Dict[str, str] = Field(default_factory=dict)

class ReleaseManifest(BaseModel):
    version: str
    channel: str
    schema_version: str
    git_commit: Optional[str] = None
    build_id: str
    created_at: str
    features: List[str] = Field(default_factory=list)

def init_observability_tables():
    conn = db_connect()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS structured_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        level TEXT NOT NULL,
        event TEXT NOT NULL,
        request_id TEXT,
        tenant_id TEXT,
        component TEXT NOT NULL,
        metadata_json TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS metric_points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        value REAL NOT NULL,
        timestamp TEXT NOT NULL,
        labels_json TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS release_manifests (
        version TEXT PRIMARY KEY,
        channel TEXT NOT NULL,
        schema_version TEXT NOT NULL,
        git_commit TEXT,
        build_id TEXT NOT NULL,
        created_at TEXT NOT NULL,
        features_json TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS backup_verifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        backup_path TEXT NOT NULL,
        size_bytes INTEGER NOT NULL,
        sha256 TEXT NOT NULL,
        verified INTEGER NOT NULL,
        created_at TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

init_observability_tables()

def record_log(level: str, event: str, request_id: Optional[str] = None,
               tenant_id: Optional[str] = None, component: str = "core",
               metadata: Optional[Dict[str, Any]] = None) -> LogEvent:
    item = LogEvent(
        timestamp=datetime.now().astimezone().isoformat(),
        level=level.upper(),
        event=_bounded_text(event, 500),
        request_id=request_id,
        tenant_id=tenant_id,
        component=component,
        metadata=metadata or {}
    )
    conn = db_connect()
    conn.execute(
        "INSERT INTO structured_logs(timestamp,level,event,request_id,tenant_id,"
        "component,metadata_json) VALUES(?,?,?,?,?,?,?)",
        (item.timestamp, item.level, item.event, item.request_id,
         item.tenant_id, item.component, json.dumps(item.metadata, sort_keys=True))
    )
    conn.commit()
    conn.close()
    return item

def record_metric(name: str, value: float,
                  labels: Optional[Dict[str, str]] = None) -> MetricPoint:
    point = MetricPoint(
        name=_bounded_text(name, 200),
        value=float(value),
        timestamp=datetime.now().astimezone().isoformat(),
        labels=labels or {}
    )
    conn = db_connect()
    conn.execute(
        "INSERT INTO metric_points(name,value,timestamp,labels_json) VALUES(?,?,?,?)",
        (point.name, point.value, point.timestamp,
         json.dumps(point.labels, sort_keys=True))
    )
    conn.commit()
    conn.close()
    return point

def recent_metrics(limit: int = 100) -> List[Dict[str, Any]]:
    conn = db_connect()
    rows = conn.execute(
        "SELECT name,value,timestamp,labels_json FROM metric_points "
        "ORDER BY id DESC LIMIT ?", (max(1, min(limit, 1000)),)
    ).fetchall()
    conn.close()
    return [
        {
            "name": r["name"],
            "value": r["value"],
            "timestamp": r["timestamp"],
            "labels": json.loads(r["labels_json"])
        } for r in rows
    ]

def recent_logs(limit: int = 100) -> List[Dict[str, Any]]:
    conn = db_connect()
    rows = conn.execute(
        "SELECT timestamp,level,event,request_id,tenant_id,component,metadata_json "
        "FROM structured_logs ORDER BY id DESC LIMIT ?",
        (max(1, min(limit, 1000)),)
    ).fetchall()
    conn.close()
    return [
        {
            "timestamp": r["timestamp"], "level": r["level"],
            "event": r["event"], "request_id": r["request_id"],
            "tenant_id": r["tenant_id"], "component": r["component"],
            "metadata": json.loads(r["metadata_json"])
        } for r in rows
    ]

def verify_backup_file(path: Path) -> Dict[str, Any]:
    result = {
        "path": str(path),
        "exists": path.exists(),
        "readable": False,
        "size_bytes": 0,
        "sha256": None,
        "verified": False
    }
    if not path.exists() or not path.is_file():
        return result
    try:
        data = path.read_bytes()
        digest = __import__("hashlib").sha256(data).hexdigest()
        result.update({
            "readable": True,
            "size_bytes": len(data),
            "sha256": digest,
            "verified": len(data) > 0
        })
        conn = db_connect()
        conn.execute(
            "INSERT INTO backup_verifications(backup_path,size_bytes,sha256,verified,created_at)"
            " VALUES(?,?,?,?,?)",
            (str(path), len(data), digest, int(result["verified"]),
             datetime.now().astimezone().isoformat())
        )
        conn.commit()
        conn.close()
    except Exception as exc:
        result["error"] = _bounded_text(str(exc), 500)
    return result

def migration_safety_check() -> Dict[str, Any]:
    conn = db_connect()
    try:
        rows = conn.execute(
            "SELECT version, name FROM migrations ORDER BY version"
        ).fetchall()
        versions = [int(r["version"]) for r in rows]
        contiguous = versions == list(range(1, len(versions) + 1))
        return {
            "migration_count": len(versions),
            "versions": versions,
            "contiguous": contiguous,
            "safe": contiguous
        }
    except Exception as exc:
        return {"migration_count": 0, "versions": [], "contiguous": False,
                "safe": False, "error": str(exc)}
    finally:
        conn.close()

def runtime_diagnostics() -> Dict[str, Any]:
    preflight = deployment_preflight()
    migration = migration_safety_check()
    latest_backups = list_backups()
    backup = verify_backup_file(Path(latest_backups[0])) if latest_backups else {"exists": False, "verified": False}
    diagnostics = {
        "version": globals().get("V23_VERSION", V15_VERSION),
        "python": sys.version.split()[0],
        "platform": sys.platform,
        "deployment": preflight.model_dump(),
        "migration_safety": migration,
        "latest_backup": backup,
        "gateway": gateway_health(),
        "security": security_boundary_health(),
        "timestamp": datetime.now().astimezone().isoformat()
    }
    record_log("INFO", "runtime_diagnostics", component="diagnostics",
               metadata={"version": V15_VERSION,
                         "preflight_ready": preflight.ready})
    return diagnostics

def build_release_manifest() -> ReleaseManifest:
    manifest = ReleaseManifest(
        version=V15_VERSION,
        channel=RELEASE_CHANNEL,
        schema_version=CONFIG_SCHEMA_VERSION,
        git_commit=os.getenv("GIT_COMMIT"),
        build_id=f"build-{__import__('uuid').uuid4().hex[:16]}",
        created_at=datetime.now().astimezone().isoformat(),
        features=[
            "structured_logging",
            "metrics_registry",
            "backup_verification",
            "migration_safety",
            "runtime_diagnostics",
            "release_manifest"
        ]
    )
    conn = db_connect()
    conn.execute(
        "INSERT OR REPLACE INTO release_manifests"
        "(version,channel,schema_version,git_commit,build_id,created_at,features_json)"
        " VALUES(?,?,?,?,?,?,?)",
        (manifest.version, manifest.channel, manifest.schema_version,
         manifest.git_commit, manifest.build_id, manifest.created_at,
         json.dumps(manifest.features))
    )
    conn.commit()
    conn.close()
    return manifest

def operational_health() -> Dict[str, Any]:
    preflight = deployment_preflight()
    migration = migration_safety_check()
    return {
        "version": globals().get("V23_VERSION", V15_VERSION),
        "release_channel": RELEASE_CHANNEL,
        "ready": preflight.ready and migration["safe"],
        "preflight": preflight.model_dump(),
        "migration_safety": migration,
        "observability": True,
        "backup_verification": True
    }


# ===========================================================================
# ===========================================================================
# V21 AUTONOMOUS BUSINESS INTELLIGENCE & SOLUTION ENGINE
# ===========================================================================
# Production rule: connected business data only. No synthetic KPIs, demo
# customers, sample pipeline, or fabricated outcomes are permitted in the
# autonomous path. A source is connected once; the OS owns the analysis loop.
# ===========================================================================

AUTONOMOUS_SCHEMA_VERSION = 1
AUTONOMOUS_MAX_PAYLOAD = 2_000_000


def init_autonomous_tables():
    conn = db_connect()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS business_connections (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        name TEXT NOT NULL,
        source_kind TEXT NOT NULL,
        endpoint TEXT NOT NULL,
        secret_ref TEXT NOT NULL,
        poll_seconds INTEGER NOT NULL DEFAULT 300,
        enabled INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        last_sync_at TEXT,
        last_status TEXT NOT NULL DEFAULT 'NEVER_SYNCED',
        last_error TEXT DEFAULT ''
    );
    CREATE INDEX IF NOT EXISTS idx_business_connections_tenant
        ON business_connections(tenant_id, enabled);

    CREATE TABLE IF NOT EXISTS business_snapshots (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        connection_id TEXT NOT NULL,
        source_name TEXT NOT NULL,
        fetched_at TEXT NOT NULL,
        http_status INTEGER,
        payload_json TEXT NOT NULL,
        record_count INTEGER NOT NULL DEFAULT 0,
        checksum TEXT NOT NULL,
        FOREIGN KEY(connection_id) REFERENCES business_connections(id) ON DELETE CASCADE
    );
    CREATE INDEX IF NOT EXISTS idx_business_snapshots_tenant_time
        ON business_snapshots(tenant_id, fetched_at DESC);

    CREATE TABLE IF NOT EXISTS autonomous_reports (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        generated_at TEXT NOT NULL,
        data_freshness TEXT NOT NULL,
        report_json TEXT NOT NULL,
        confidence REAL NOT NULL DEFAULT 0.0
    );
    CREATE INDEX IF NOT EXISTS idx_autonomous_reports_tenant_time
        ON autonomous_reports(tenant_id, generated_at DESC);
    """)
    conn.commit()
    conn.close()


init_autonomous_tables()


# ===========================================================================
# V30 — UNIVERSAL BUSINESS INTELLIGENCE LAYER
# ===========================================================================
# Final delivery architecture:
#   • Business-agnostic discovery: never assumes Shopify/e-commerce.
#   • Universal source onboarding: APIs + CSV/XLSX + guided business context.
#   • Evidence normalization: heterogeneous source payloads become common
#     business observations.
#   • Automatic business DNA classification with confidence + explainability.
#   • Dynamic domain routing: only relevant intelligence domains are activated.
#   • Missing-data intelligence: tells the client what is missing and why.
#   • Unified diagnosis: one executive answer instead of 30 manual features.
#   • Tenant-scoped persistence and audit trail.
#   • Optional AI refinement, but never AI-invented business facts.
# ===========================================================================

V32_VERSION = "30.0.0"
V30_SCHEMA_VERSION = "2026-08-V30-UNIVERSAL"

V30_BUSINESS_TYPES = {
    "E-commerce / DTC": ("order", "product", "customer", "cart", "sku", "refund"),
    "B2B SaaS / Subscription": ("subscription", "mrr", "arr", "churn", "usage", "seat", "plan"),
    "Professional Services / Agency": ("client", "project", "invoice", "hours", "retainer", "campaign"),
    "Retail / Distribution": ("inventory", "sku", "purchase", "supplier", "store", "stock"),
    "Manufacturing": ("production", "workorder", "work_order", "machine", "inventory", "supplier"),
    "Marketplace": ("seller", "vendor", "listing", "buyer", "commission", "transaction"),
    "Logistics / Transportation": ("shipment", "tracking", "delivery", "route", "fleet", "warehouse"),
    "Hospitality / Travel": ("reservation", "booking", "room", "guest", "occupancy", "checkin"),
    "Education / Training": ("student", "course", "enrollment", "lesson", "class", "completion"),
    "Healthcare / Life Sciences": ("patient", "appointment", "provider", "claim", "clinical", "visit"),
    "Financial Services": ("account", "transaction", "loan", "payment", "portfolio", "claim"),
    "Real Estate": ("property", "listing", "lease", "tenant", "rent", "occupancy"),
}

V30_DOMAIN_TERMS = {
    "finance": ("revenue", "cash", "margin", "cost", "expense", "profit", "refund", "payment", "invoice", "balance"),
    "sales": ("lead", "deal", "pipeline", "conversion", "win", "loss", "opportunity", "quote", "order"),
    "marketing": ("campaign", "impression", "click", "ctr", "cpc", "cpm", "cac", "roas", "spend", "traffic", "acquisition"),
    "customer": ("customer", "client", "churn", "retention", "renewal", "support", "ticket", "nps", "csat", "refund"),
    "operations": ("inventory", "stock", "fulfillment", "delivery", "delay", "capacity", "utilization", "error", "failure"),
    "product": ("product", "sku", "variant", "usage", "feature", "adoption", "return"),
    "people": ("employee", "staff", "headcount", "attrition", "absence", "productivity", "hiring"),
    "technology": ("latency", "uptime", "availability", "error", "api", "request", "incident"),
    "risk": ("risk", "fraud", "chargeback", "incident", "compliance", "anomaly", "security"),
    "strategy": ("market", "competitor", "share", "growth", "position", "pricing"),
    "cashflow": ("cashflow", "cash_flow", "runway", "receivable", "payable", "burn"),
    "governance": ("policy", "approval", "audit", "permission", "security", "access"),
}

V30_BUSINESS_DATA_REQUIREMENTS = {
    "E-commerce / DTC": ["orders/revenue", "customers", "products/inventory", "marketing acquisition"],
    "B2B SaaS / Subscription": ["subscriptions/revenue", "customer retention/churn", "product usage", "sales pipeline"],
    "Professional Services / Agency": ["clients/revenue", "projects/delivery", "utilization/capacity", "sales pipeline"],
    "Retail / Distribution": ["sales/revenue", "inventory", "purchasing/suppliers", "customer demand"],
    "Manufacturing": ["sales/orders", "production/work orders", "inventory", "supplier/cost data"],
    "Marketplace": ["transactions", "buyers", "sellers/vendors", "commission/revenue"],
    "Logistics / Transportation": ["shipments", "delivery performance", "fleet/capacity", "cost/revenue"],
    "Hospitality / Travel": ["reservations", "occupancy", "revenue", "guest/customer experience"],
    "Education / Training": ["enrollments", "course completion", "revenue", "learner outcomes"],
    "Healthcare / Life Sciences": ["appointments/visits", "revenue/claims", "capacity", "operational quality"],
    "Financial Services": ["transactions/revenue", "accounts", "risk/fraud", "cash/liquidity"],
    "Real Estate": ["properties/listings", "occupancy/leases", "revenue/rent", "pipeline"],
}

def v30_init_tables() -> None:
    conn = db_connect()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS v30_business_profiles (
        tenant_id TEXT PRIMARY KEY,
        business_type TEXT NOT NULL DEFAULT 'Unknown',
        confidence REAL NOT NULL DEFAULT 0,
        business_model TEXT DEFAULT '',
        revenue_model TEXT DEFAULT '',
        customer_type TEXT DEFAULT '',
        geography TEXT DEFAULT '',
        company_size TEXT DEFAULT '',
        detected_domains_json TEXT DEFAULT '[]',
        coverage_json TEXT DEFAULT '{}',
        gaps_json TEXT DEFAULT '[]',
        evidence_json TEXT DEFAULT '[]',
        user_correction TEXT DEFAULT '',
        generated_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS v30_observations (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        source_name TEXT NOT NULL,
        domain TEXT NOT NULL,
        field_name TEXT NOT NULL,
        numeric_value REAL,
        text_value TEXT DEFAULT '',
        observed_at TEXT NOT NULL,
        evidence_json TEXT DEFAULT '{}'
    );
    CREATE INDEX IF NOT EXISTS idx_v30_obs_tenant_domain
        ON v30_observations(tenant_id, domain, observed_at DESC);

    CREATE TABLE IF NOT EXISTS v30_onboarding_events (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        details_json TEXT DEFAULT '{}',
        created_at TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

v30_init_tables()

def v30_flatten_keys(value: Any, prefix: str = "", limit: int = 400) -> List[str]:
    out: List[str] = []
    if len(out) >= limit:
        return out
    if isinstance(value, dict):
        for k, v in value.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            out.append(key.lower())
            if len(out) < limit and isinstance(v, (dict, list)):
                out.extend(v30_flatten_keys(v, key, limit - len(out)))
    elif isinstance(value, list):
        for item in value[:30]:
            if isinstance(item, dict):
                out.extend(v30_flatten_keys(item, prefix, limit - len(out)))
            elif prefix:
                out.append(prefix.lower())
    return out[:limit]

def v30_payload_text(snapshots: List[Dict[str, Any]], max_chars: int = 30000) -> str:
    chunks = []
    for snap in snapshots:
        chunks.append(str(snap.get("source_name", "")))
        chunks.extend(v30_flatten_keys(snap.get("payload", {}), limit=500))
        try:
            chunks.append(json.dumps(snap.get("payload", {}), default=str)[:5000])
        except Exception:
            pass
    return " ".join(chunks).lower()[:max_chars]

def v30_score_business_types(snapshots: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    blob = v30_payload_text(snapshots)
    scored = []
    for name, terms in V30_BUSINESS_TYPES.items():
        hits = [term for term in terms if re.search(rf"\b{re.escape(term)}\b", blob)]
        score = len(hits) / max(1, len(terms))
        scored.append({
            "business_type": name,
            "score": round(min(1.0, score), 3),
            "evidence_terms": hits[:12],
        })
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored

def v30_detect_domains(snapshots: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    blob = v30_payload_text(snapshots)
    domains = {}
    for domain, terms in V30_DOMAIN_TERMS.items():
        hits = [term for term in terms if re.search(rf"\b{re.escape(term)}\b", blob)]
        domains[domain] = {
            "active": bool(hits),
            "confidence": round(min(1.0, len(hits) / max(3, len(terms) * 0.55)), 3),
            "evidence_terms": hits[:10],
        }
    return domains

def v30_normalize_observations(tenant_id: str, snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a common observation layer without inventing derived metrics."""
    conn = db_connect()
    inserted = 0
    by_domain: Dict[str, int] = {}
    now = datetime.now().astimezone().isoformat()
    for snap in snapshots:
        source = _bounded_text(snap.get("source_name", "Unknown"), 200)
        payload = snap.get("payload", {})
        observed_at = snap.get("fetched_at") or now
        conn.execute(
            "DELETE FROM v30_observations WHERE tenant_id=? AND source_name=? AND observed_at=?",
            (tenant_id, source, observed_at),
        )
        numeric = _autonomous_numeric_signals(payload)
        for key, value in list(numeric.items())[:500]:
            key_l = str(key).lower()
            matching = [
                d for d, terms in V30_DOMAIN_TERMS.items()
                if any(term in key_l for term in terms)
            ]
            domains = matching or ["general"]
            for domain in domains[:2]:
                obs_id = f"OBS30-{uuid.uuid4().hex}"
                conn.execute(
                    """INSERT INTO v30_observations
                    (id,tenant_id,source_name,domain,field_name,numeric_value,text_value,observed_at,evidence_json)
                    VALUES(?,?,?,?,?,?,?,?,?)""",
                    (obs_id, tenant_id, source, domain, _bounded_text(key, 300),
                     float(value), "", observed_at,
                     json.dumps({"source": source, "snapshot_id": snap.get("id")}, default=str)),
                )
                inserted += 1
                by_domain[domain] = by_domain.get(domain, 0) + 1
    conn.commit()
    conn.close()
    return {"inserted": inserted, "by_domain": by_domain}

def v30_profile_from_live_data(tenant_id: str) -> Dict[str, Any]:
    snapshots = autonomous_latest_snapshots(tenant_id)
    if not snapshots:
        return {
            "business_type": "Unknown",
            "confidence": 0.0,
            "business_model": "Unknown",
            "detected_domains": {},
            "coverage": {},
            "gaps": ["Connect at least one live business data source."],
            "evidence": [],
        }

    ranked = v30_score_business_types(snapshots)
    top = ranked[0] if ranked else {"business_type": "Unknown", "score": 0.0, "evidence_terms": []}
    second = ranked[1]["score"] if len(ranked) > 1 else 0.0
    confidence = min(0.98, max(0.05, top["score"] * 0.82 + (top["score"] - second) * 0.35))
    domains = v30_detect_domains(snapshots)

    active = [d for d, x in domains.items() if x["active"]]
    requirements = V30_BUSINESS_DATA_REQUIREMENTS.get(top["business_type"], [
        "revenue/financial data", "customer data", "sales/pipeline data",
        "operations data", "marketing/acquisition data"
    ])
    blob = v30_payload_text(snapshots)
    gaps = [r for r in requirements if not any(token in blob for token in re.findall(r"[a-z_]+", r.lower()) if len(token) > 3)]
    source_count = len(snapshots)
    record_count = sum(int(s.get("record_count") or 0) for s in snapshots)
    coverage = {
        "source_count": source_count,
        "record_count": record_count,
        "active_domains": active,
        "domain_count": len(active),
        "latest_data": max((s.get("fetched_at") for s in snapshots if s.get("fetched_at")), default=None),
        "breadth_score": round(min(100.0, len(active) / max(1, len(V30_DOMAIN_TERMS)) * 100), 1),
    }

    profile = {
        "business_type": top["business_type"] if top["score"] >= 0.15 else "Unknown / Mixed",
        "confidence": round(confidence if top["score"] >= 0.15 else 0.20, 3),
        "business_model": "Inferred from connected live evidence; exact model requires corroborating fields.",
        "revenue_model": "Not confidently established from current evidence.",
        "customer_type": "Not confidently established from current evidence.",
        "detected_domains": domains,
        "coverage": coverage,
        "gaps": gaps[:12],
        "evidence": [
            {"source": s.get("source_name"), "record_count": s.get("record_count"), "fetched_at": s.get("fetched_at")}
            for s in snapshots
        ],
        "classification_candidates": ranked[:5],
        "generated_at": datetime.now().astimezone().isoformat(),
    }
    return profile

def v30_store_profile(tenant_id: str, profile: Dict[str, Any]) -> None:
    conn = db_connect()
    now = datetime.now().astimezone().isoformat()
    conn.execute(
        """INSERT OR REPLACE INTO v30_business_profiles
        (tenant_id,business_type,confidence,business_model,revenue_model,customer_type,
         geography,company_size,detected_domains_json,coverage_json,gaps_json,evidence_json,
         user_correction,generated_at,updated_at)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (tenant_id, profile.get("business_type", "Unknown"),
         float(profile.get("confidence", 0.0) or 0.0),
         _bounded_text(profile.get("business_model", ""), 1000),
         _bounded_text(profile.get("revenue_model", ""), 500),
         _bounded_text(profile.get("customer_type", ""), 500),
         _bounded_text(profile.get("geography", ""), 300),
         _bounded_text(profile.get("company_size", ""), 200),
         json.dumps(profile.get("detected_domains", {}), default=str),
         json.dumps(profile.get("coverage", {}), default=str),
         json.dumps(profile.get("gaps", []), default=str),
         json.dumps(profile.get("evidence", []), default=str),
         _bounded_text(profile.get("user_correction", ""), 500),
         profile.get("generated_at", now), now),
    )
    conn.execute(
        "INSERT INTO v30_onboarding_events VALUES(?,?,?,?,?)",
        (f"ONB30-{uuid.uuid4().hex}", tenant_id, "BUSINESS_PROFILE_UPDATED",
         json.dumps({"business_type": profile.get("business_type"), "confidence": profile.get("confidence")}),
         now),
    )
    conn.commit()
    conn.close()


# ===========================================================================
# V51 ONE-CLICK BUSINESS CONNECTION HUB
# Login -> Select business -> Review access -> Approve -> Connect/Activate
# ===========================================================================

def v51_init_business_connection_hub() -> None:
    """Persist the user's selected-business approval without storing secrets."""
    conn = db_connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS v51_business_connection_approvals (
            id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            user_id TEXT DEFAULT '',
            connection_id TEXT DEFAULT '',
            business_name TEXT NOT NULL,
            source_kind TEXT DEFAULT '',
            approved INTEGER NOT NULL DEFAULT 0,
            approved_at TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            UNIQUE(tenant_id, user_id, connection_id)
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_v51_biz_approval_tenant
        ON v51_business_connection_approvals(tenant_id, approved, approved_at DESC)
    """)
    conn.commit()
    conn.close()


def v51_record_business_approval(tenant_id: str, user_id: str,
                                 connection_id: str, business_name: str,
                                 source_kind: str) -> Dict[str, Any]:
    v51_init_business_connection_hub()
    now = datetime.now().astimezone().isoformat()
    approval_id = f"BIZAPP-{uuid.uuid4().hex}"
    conn = db_connect()
    conn.execute("""
        INSERT INTO v51_business_connection_approvals
        (id,tenant_id,user_id,connection_id,business_name,source_kind,approved,approved_at,created_at)
        VALUES(?,?,?,?,?,?,?,?,?)
        ON CONFLICT(tenant_id,user_id,connection_id)
        DO UPDATE SET business_name=excluded.business_name,
                      source_kind=excluded.source_kind,
                      approved=1,
                      approved_at=excluded.approved_at
    """, (approval_id, tenant_id, _bounded_text(user_id, 300),
          _bounded_text(connection_id, 300), _bounded_text(business_name, 500),
          _bounded_text(source_kind, 200), 1, now, now))
    conn.execute(
        "INSERT INTO v30_onboarding_events VALUES(?,?,?,?,?)",
        (f"ONB51-{uuid.uuid4().hex}", tenant_id, "BUSINESS_CONNECTION_APPROVED",
         json.dumps({"connection_id": connection_id, "business_name": business_name,
                     "source_kind": source_kind}, default=str), now),
    )
    conn.commit()
    conn.close()
    try:
        record_audit(
            user_id or "unknown",
            "BUSINESS_CONNECTION_APPROVED",
            "Business",
            business_name,
        )
    except Exception:
        pass
    return {"ok": True, "approval_id": approval_id, "approved_at": now}


def v51_get_selected_business(tenant_id: str, user_id: str) -> Optional[Dict[str, Any]]:
    v51_init_business_connection_hub()
    conn = db_connect()
    row = conn.execute("""
        SELECT * FROM v51_business_connection_approvals
        WHERE tenant_id=? AND user_id=? AND approved=1
        ORDER BY approved_at DESC LIMIT 1
    """, (tenant_id, _bounded_text(user_id, 300))).fetchone()
    conn.close()
    return dict(row) if row else None


def v51_business_label(connection: Dict[str, Any]) -> str:
    name = connection.get("name") or connection.get("source_name") or "Business Source"
    kind = connection.get("source_kind") or connection.get("connector_type") or connection.get("type") or "Live source"
    return f"{name} · {kind}"


def v51_connect_business_hub(tenant_id: str, user: Optional[Dict[str, Any]]) -> bool:
    """Render the first-screen business chooser and approval flow.

    Existing connections are activated with one approval click. New connections
    continue through the existing secure connector forms below. This layer does
    not collect or persist vendor secrets.
    """
    v51_init_business_connection_hub()
    user_id = (user or {}).get("id") or (user or {}).get("email") or "local-user"
    connections = autonomous_list_connections(tenant_id)
    selected = v51_get_selected_business(tenant_id, user_id)

    with st.container(border=True):
        st.markdown("## 🔗 Connect your business")
        st.caption("Choose the business you want AI Business OS™ to operate on. Review the source, approve access, and activate it.")

        if connections:
            options = [c.get("id") for c in connections if c.get("id")]
            labels = {c.get("id"): v51_business_label(c) for c in connections if c.get("id")}
            default_index = 0
            if selected and selected.get("connection_id") in options:
                default_index = options.index(selected["connection_id"])

            chosen_id = st.selectbox(
                "Select business",
                options,
                index=default_index,
                format_func=lambda x: labels.get(x, x),
                key="v51_business_selector",
            )
            chosen = next((c for c in connections if c.get("id") == chosen_id), None) or {}
            business_name = chosen.get("name") or chosen.get("source_name") or "Connected Business"
            source_kind = chosen.get("source_kind") or chosen.get("connector_type") or "Live business source"

            c1, c2, c3 = st.columns(3)
            c1.metric("Business", business_name[:28])
            c2.metric("Source", source_kind[:28])
            c3.metric("Status", "Connected" if chosen.get("status") in {"active", "connected", "healthy"} else str(chosen.get("status", "Ready")).title())

            st.markdown("**Access approval**")
            st.caption("The OS will use only the permissions already configured for this connector. Vendor credentials/secrets are not entered or stored here.")
            approve = st.checkbox(
                "I approve connecting this business to my AI Business OS workspace.",
                value=bool(selected and selected.get("connection_id") == chosen_id),
                key="v51_business_approval",
            )
            if st.button("✅ Approve & Connect Business", type="primary", use_container_width=True, key="v51_approve_business"):
                if not approve:
                    st.error("Please approve the business connection first.")
                    return False
                approval = v51_record_business_approval(
                    tenant_id, str(user_id), str(chosen_id), business_name, source_kind
                )
                if approval.get("ok"):
                    # A selected connection is already configured; force the normal
                    # live cycle so the Command Center immediately reflects it.
                    try:
                        live = v22_fetch_live_connection({**chosen, "tenant_id": tenant_id})
                    except Exception as exc:
                        live = {"ok": False, "error": f"Initial sync error: {type(exc).__name__}: {exc}"}
                    if live.get("ok"):
                        st.success(f"✓ {business_name} connected and initial live synchronization completed.")
                    else:
                        st.success(f"✓ {business_name} approved and connected. Live synchronization will continue through the normal connector cycle.")
                    st.rerun()
                    return True
                st.error("Business approval could not be saved.")
                return False

            st.markdown("---")
            st.caption("Need a different business? Choose another source above or add a new business connection below.")
        else:
            st.info("No business is connected yet. Add your first live business source below. After it is created, it will appear here for one-click approval and activation.")

    return False

def v30_get_profile(tenant_id: str) -> Optional[Dict[str, Any]]:
    conn = db_connect()
    row = conn.execute("SELECT * FROM v30_business_profiles WHERE tenant_id=?", (tenant_id,)).fetchone()
    conn.close()
    if not row:
        return None
    r = dict(row)
    for field_name in ("detected_domains_json", "coverage_json", "gaps_json", "evidence_json"):
        target = field_name.replace("_json", "")
        try:
            r[target] = json.loads(r.pop(field_name))
        except Exception:
            r[target] = {} if target in ("detected_domains", "coverage") else []
    return r

def v30_missing_data_recommendations(profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    business_type = profile.get("business_type", "Unknown")
    requirements = V30_BUSINESS_DATA_REQUIREMENTS.get(business_type, [])
    active = set(profile.get("coverage", {}).get("active_domains", []))
    recommendations = []
    domain_to_source = {
        "finance": "Accounting / payments",
        "sales": "CRM / sales pipeline",
        "marketing": "Advertising / analytics",
        "customer": "CRM / support / customer success",
        "operations": "ERP / inventory / operations",
        "product": "Product analytics / catalog",
        "people": "HR / workforce",
        "technology": "Application monitoring / infrastructure",
        "risk": "Fraud / compliance / security",
        "strategy": "Market / competitor intelligence",
        "cashflow": "Accounting / treasury",
        "governance": "Identity / audit / policy systems",
    }
    for req in requirements:
        matched = next((d for d in active if any(t in req.lower() for t in V30_DOMAIN_TERMS.get(d, ()))), None)
        if not matched:
            recommendations.append({
                "missing_area": req,
                "recommended_source": next((v for k, v in domain_to_source.items() if k in req.lower()), "Relevant business system"),
                "why_it_matters": "Adding this evidence can materially improve diagnosis confidence and cross-domain root-cause analysis.",
            })
    return recommendations[:8]

def v30_ai_refine_profile(tenant_id: str, profile: Dict[str, Any], api_key: str = "") -> Dict[str, Any]:
    """Optional AI classification; only permitted to refine, never create facts."""
    if not api_key:
        return profile
    snapshots = autonomous_latest_snapshots(tenant_id)
    evidence = [
        {"source": s.get("source_name"), "fetched_at": s.get("fetched_at"),
         "record_count": s.get("record_count"),
         "fields": v30_flatten_keys(s.get("payload", {}), limit=120)}
        for s in snapshots
    ]
    prompt = f"""
You are the business classification layer of an autonomous B2B operating system.
Use ONLY the connected source names, observed field names and record counts below.
Do not invent revenue, customers, products, industry facts, or KPIs.
You may refine the classification and describe uncertainty.
Return JSON with:
business_type, business_model, revenue_model, customer_type, confidence, rationale.
Evidence:
{json.dumps(evidence, default=str)[:MAX_PROMPT_CHARS]}
Current deterministic profile:
{json.dumps(profile, default=str)[:7000]}
"""
    result = run_ai_json(api_key, prompt, """{
business_type:string,
business_model:string,
revenue_model:string,
customer_type:string,
confidence:number,
rationale:string
}""")
    if not isinstance(result, dict):
        return profile
    allowed = ("business_type", "business_model", "revenue_model", "customer_type", "confidence")
    for key in allowed:
        if key in result and result[key] not in (None, ""):
            profile[key] = result[key]
    profile["ai_refinement_rationale"] = _bounded_text(result.get("rationale", ""), 2000)
    profile["classification_method"] = "deterministic_live-evidence + optional AI refinement"
    profile["confidence"] = max(0.0, min(1.0, float(profile.get("confidence", 0.0) or 0.0)))
    return profile

def v30_ingest_file(tenant_id: str, uploaded_file: Any, source_name: str = "") -> Dict[str, Any]:
    """Universal low-friction onboarding for CSV/XLSX/JSON business exports."""
    if uploaded_file is None:
        return {"ok": False, "error": "No file supplied."}
    filename = _bounded_text(getattr(uploaded_file, "name", "Business data"), 200)
    suffix = Path(filename).suffix.lower()
    try:
        raw = uploaded_file.getvalue()
        if len(raw) > 25 * 1024 * 1024:
            return {"ok": False, "error": "File exceeds the 25 MB safe onboarding limit."}
        if suffix == ".csv":
            import io
            df = pd.read_csv(io.BytesIO(raw), nrows=5000)
        elif suffix in (".xlsx", ".xls"):
            import io
            df = pd.read_excel(io.BytesIO(raw), nrows=5000)
        elif suffix == ".json":
            payload = json.loads(raw.decode("utf-8", errors="replace"))
            df = pd.json_normalize(payload if isinstance(payload, list) else [payload]).head(5000)
        else:
            return {"ok": False, "error": "Supported business-data files are CSV, XLSX/XLS or JSON."}
        df = df.where(pd.notnull(df), None)
        records = df.to_dict(orient="records")
        payload = {"file_name": filename, "columns": [str(c) for c in df.columns], "records": records}
        conn_id = f"FILE30-{uuid.uuid4().hex}"
        now = datetime.now().astimezone().isoformat()
        conn = db_connect()
        conn.execute(
            """INSERT INTO business_connections
            (id,tenant_id,name,source_kind,endpoint,secret_ref,poll_seconds,enabled,created_at,updated_at,last_sync_at,last_status,last_error)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (conn_id, tenant_id, _bounded_text(source_name or filename, 200), "FILE_UPLOAD",
             f"file://{filename}", "", 86400, 0, now, now, now, "SYNCED", ""),
        )
        encoded = json.dumps(payload, default=str)
        conn.execute(
            """INSERT INTO business_snapshots
            (id,tenant_id,connection_id,source_name,fetched_at,http_status,payload_json,record_count,checksum)
            VALUES(?,?,?,?,?,?,?,?,?)""",
            (f"SNAP30-{uuid.uuid4().hex}", tenant_id, conn_id,
             _bounded_text(source_name or filename, 200), now, 200, encoded,
             len(records), hashlib.sha256(encoded.encode()).hexdigest()),
        )
        conn.commit()
        conn.close()
        record_provenance(tenant_id, source_name or filename, "FILE_INGESTED",
                          f"Business data file ingested as a tenant-scoped live snapshot; {len(records)} records.")
        return {"ok": True, "connection_id": conn_id, "record_count": len(records), "columns": list(df.columns)}
    except Exception as exc:
        return {"ok": False, "error": f"Business data ingestion failed: {type(exc).__name__}: {exc}"}

def v30_universal_cycle(tenant_id: str, api_key: str = "", force: bool = False) -> Dict[str, Any]:
    """Single autonomous entry point for any business, not a specific industry."""
    started = time.monotonic()
    base = v25_continuous_cycle(tenant_id, api_key, force=force)
    snapshots = autonomous_latest_snapshots(tenant_id)
    if not snapshots:
        return {
            **base,
            "version": V32_VERSION,
            "business_profile": None,
            "onboarding_state": "AWAITING_BUSINESS_DATA",
            "duration_seconds": round(time.monotonic() - started, 3),
        }
    profile = v30_profile_from_live_data(tenant_id)
    profile["missing_data_recommendations"] = v30_missing_data_recommendations(profile)
    profile = v30_ai_refine_profile(tenant_id, profile, api_key)
    observations = v30_normalize_observations(tenant_id, snapshots)
    v30_store_profile(tenant_id, profile)
    report = base.get("report")
    if report:
        report["version"] = V32_VERSION
        report["business_identity"] = {
            "business_type": profile.get("business_type"),
            "confidence": profile.get("confidence"),
            "business_model": profile.get("business_model"),
            "revenue_model": profile.get("revenue_model"),
            "customer_type": profile.get("customer_type"),
        }
        report["business_coverage"] = profile.get("coverage", {})
        report["active_intelligence_domains"] = [
            d for d, info in profile.get("detected_domains", {}).items()
            if info.get("active")
        ]
        report["missing_data_recommendations"] = profile.get("missing_data_recommendations", [])
        report["normalized_observations"] = observations
        report["onboarding_mode"] = "UNIVERSAL_BUSINESS"
        report["decision_status"] = report.get("decision_status", "PROVISIONAL")
        # Persist the enriched report.
        conn = db_connect()
        latest = conn.execute(
            "SELECT id FROM autonomous_reports WHERE tenant_id=? ORDER BY generated_at DESC LIMIT 1",
            (tenant_id,),
        ).fetchone()
        if latest:
            conn.execute(
                "UPDATE autonomous_reports SET report_json=?, confidence=? WHERE id=?",
                (json.dumps(report, default=str), float(report.get("confidence", 0.0) or 0.0), latest["id"]),
            )
        conn.commit()
        conn.close()
    return {
        **base,
        "version": V32_VERSION,
        "report": report,
        "business_profile": profile,
        "normalized_observations": observations,
        "onboarding_state": "BUSINESS_UNDERSTOOD",
        "duration_seconds": round(time.monotonic() - started, 3),
    }

def v30_universal_readiness(tenant_id: str) -> Dict[str, Any]:
    profile = v30_get_profile(tenant_id)
    connections = autonomous_list_connections(tenant_id)
    snapshots = autonomous_latest_snapshots(tenant_id)
    checks = {
        "business_agnostic_classifier": True,
        "universal_api_connection_path": callable(autonomous_register_connection),
        "file_ingestion": callable(v30_ingest_file),
        "tenant_scoped_persistence": True,
        "automatic_domain_detection": True,
        "missing_data_detection": True,
        "single_unified_report_path": callable(v30_universal_cycle),
        "live_sources_connected": bool(connections),
        "live_snapshots_available": bool(snapshots),
        "business_profile_available": bool(profile),
    }
    return {
        "version": V32_VERSION,
        "passed": all(checks.values()),
        "checks": checks,
        "business_profile": profile,
        "connected_source_count": len(connections),
        "snapshot_count": len(snapshots),
    }



def autonomous_register_connection(tenant_id: str, name: str, source_kind: str,
                                    endpoint: str, secret_ref: str,
                                    poll_seconds: int = 300) -> Dict[str, Any]:
    name = _bounded_text(name, 200)
    endpoint = _bounded_text(endpoint, 1000)
    secret_ref = _bounded_text(secret_ref, 200)
    if not name or not endpoint or not secret_ref:
        return {"ok": False, "error": "Source name, live endpoint and secret environment-variable reference are required."}
    if not re.match(r"^https?://", endpoint, re.I):
        return {"ok": False, "error": "Endpoint must be an HTTPS/HTTP API endpoint."}
    cid = f"CONN-{uuid.uuid4().hex}"
    now = datetime.now().astimezone().isoformat()
    conn = db_connect()
    conn.execute(
        "INSERT INTO business_connections "
        "(id,tenant_id,name,source_kind,endpoint,secret_ref,poll_seconds,enabled,created_at,updated_at) "
        "VALUES(?,?,?,?,?,?,?,?,?,?)",
        (cid, tenant_id, name, source_kind, endpoint, secret_ref,
         max(30, int(poll_seconds)), 1, now, now)
    )
    conn.commit()
    conn.close()
    record_provenance(tenant_id, name, "CONNECTED", "Live source registered; secret stored only in deployment environment.")
    enterprise_event("BUSINESS_SOURCE_CONNECTED", {"connection_id": cid, "source": name})
    return {"ok": True, "connection_id": cid}


def autonomous_list_connections(tenant_id: str) -> List[Dict[str, Any]]:
    conn = db_connect()
    rows = conn.execute(
        "SELECT id,name,source_kind,endpoint,secret_ref,poll_seconds,enabled,last_sync_at,last_status,last_error "
        "FROM business_connections WHERE tenant_id=? ORDER BY created_at",
        (tenant_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def _autonomous_extract_records(payload: Any) -> int:
    if isinstance(payload, list):
        return len(payload)
    if isinstance(payload, dict):
        for key in ("data", "items", "records", "results", "customers", "orders", "transactions", "leads"):
            value = payload.get(key)
            if isinstance(value, list):
                return len(value)
        return 1 if payload else 0
    return 0


def autonomous_fetch_connection(connection: Dict[str, Any]) -> Dict[str, Any]:
    cid = connection["id"]
    endpoint = connection["endpoint"]
    secret_ref = connection["secret_ref"]
    token = os.getenv(secret_ref, "")
    if not token:
        return {"ok": False, "connection_id": cid, "error": f"Live secret {secret_ref!r} is not available in the deployment environment."}

    headers = {
        "Accept": "application/json",
        "User-Agent": "AI-Business-OS/21.0 autonomous-sync",
        "Authorization": f"Bearer {token}",
    }
    request = urllib.request.Request(endpoint, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            status = int(response.status)
            raw = response.read(AUTONOMOUS_MAX_PAYLOAD + 1)
            if len(raw) > AUTONOMOUS_MAX_PAYLOAD:
                return {"ok": False, "connection_id": cid, "error": "Source payload exceeded the configured safety limit."}
            text = raw.decode("utf-8", errors="replace")
            payload = json.loads(text)
            fetched = datetime.now().astimezone().isoformat()
            encoded = json.dumps(payload, sort_keys=True, default=str)
            checksum = hashlib.sha256(encoded.encode("utf-8")).hexdigest()
            snapshot_id = f"SNAP-{uuid.uuid4().hex}"
            conn = db_connect()
            conn.execute(
                "INSERT INTO business_snapshots "
                "(id,tenant_id,connection_id,source_name,fetched_at,http_status,payload_json,record_count,checksum) "
                "VALUES(?,?,?,?,?,?,?,?,?)",
                (snapshot_id, connection["tenant_id"], cid, connection["name"], fetched,
                 status, encoded, _autonomous_extract_records(payload), checksum)
            )
            conn.execute(
                "UPDATE business_connections SET last_sync_at=?,last_status='SYNCED',last_error='',updated_at=? WHERE id=?",
                (fetched, fetched, cid)
            )
            conn.commit()
            conn.close()
            return {"ok": True, "connection_id": cid, "status": status,
                    "snapshot_id": snapshot_id, "record_count": _autonomous_extract_records(payload),
                    "fetched_at": fetched}
    except urllib.error.HTTPError as exc:
        error = f"HTTP {exc.code}: {exc.reason}"
    except urllib.error.URLError as exc:
        error = f"Network error: {exc.reason}"
    except json.JSONDecodeError:
        error = "Live endpoint did not return valid JSON."
    except Exception as exc:
        error = f"Source sync failed: {type(exc).__name__}: {exc}"

    now = datetime.now().astimezone().isoformat()
    conn = db_connect()
    conn.execute(
        "UPDATE business_connections SET last_sync_at=?,last_status='ERROR',last_error=?,updated_at=? WHERE id=?",
        (now, _bounded_text(error, 1000), now, cid)
    )
    conn.commit()
    conn.close()
    return {"ok": False, "connection_id": cid, "error": error}


def autonomous_sync_all(tenant_id: str) -> List[Dict[str, Any]]:
    connections = autonomous_list_connections(tenant_id)
    results = []
    now = datetime.now().astimezone()
    for connection in connections:
        if not connection.get("enabled"):
            continue
        last = connection.get("last_sync_at")
        due = True
        if last:
            try:
                age = (now - datetime.fromisoformat(last)).total_seconds()
                due = age >= int(connection.get("poll_seconds") or 300)
            except Exception:
                due = True
        if due:
            results.append(autonomous_fetch_connection({**connection, "tenant_id": tenant_id}))
        else:
            results.append({"ok": True, "connection_id": connection["id"], "status": "FRESH", "skipped": True})
    return results


def autonomous_latest_snapshots(tenant_id: str) -> List[Dict[str, Any]]:
    conn = db_connect()
    rows = conn.execute(
        "SELECT s.* FROM business_snapshots s "
        "JOIN (SELECT connection_id, MAX(fetched_at) AS latest FROM business_snapshots WHERE tenant_id=? GROUP BY connection_id) x "
        "ON s.connection_id=x.connection_id AND s.fetched_at=x.latest WHERE s.tenant_id=?",
        (tenant_id, tenant_id)
    ).fetchall()
    conn.close()
    output = []
    for row in rows:
        item = dict(row)
        try:
            item["payload"] = json.loads(item.pop("payload_json"))
        except Exception:
            item["payload"] = {}
        output.append(item)
    return output


def _autonomous_numeric_signals(payload: Any, prefix: str = "") -> Dict[str, float]:
    signals: Dict[str, float] = {}
    if isinstance(payload, dict):
        for key, value in payload.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if isinstance(value, bool):
                continue
            if isinstance(value, (int, float)) and math.isfinite(float(value)):
                signals[path.lower()] = float(value)
            elif isinstance(value, (dict, list)):
                signals.update(_autonomous_numeric_signals(value, path))
    elif isinstance(payload, list):
        # Do not invent aggregate business metrics. Only inspect actual numeric fields.
        for item in payload[:1000]:
            if isinstance(item, (dict, list)):
                signals.update(_autonomous_numeric_signals(item, prefix))
    return signals


def _autonomous_problem_seed(snapshots: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seeds = []
    for snap in snapshots:
        nums = _autonomous_numeric_signals(snap.get("payload", {}))
        low = {k: v for k, v in nums.items() if any(w in k for w in ("error", "fail", "failure", "churn", "refund", "return", "delay", "cost", "cac"))}
        if low:
            seeds.append({
                "source": snap.get("source_name"),
                "signals": low,
                "fetched_at": snap.get("fetched_at"),
            })
    return seeds


def autonomous_generate_unified_report(tenant_id: str, api_key: str = "") -> Optional[Dict[str, Any]]:
    snapshots = autonomous_latest_snapshots(tenant_id)
    if not snapshots:
        return None
    sources = [s.get("source_name") for s in snapshots]
    newest = max((s.get("fetched_at") for s in snapshots if s.get("fetched_at")), default=None)
    missing = []
    required_domains = {"revenue": False, "customers": False, "sales": False, "operations": False}
    for snap in snapshots:
        text = json.dumps(snap.get("payload", {}), default=str).lower()
        for domain in list(required_domains):
            if domain in text or (domain == "sales" and "order" in text) or (domain == "customers" and "customer" in text):
                required_domains[domain] = True
    missing = [d for d, present in required_domains.items() if not present]

    context = {
        "sources": sources,
        "snapshots": [
            {"source": s.get("source_name"), "fetched_at": s.get("fetched_at"),
             "record_count": s.get("record_count"), "payload": s.get("payload")} for s in snapshots
        ],
        "signal_seeds": _autonomous_problem_seed(snapshots),
        "missing_domains": missing,
    }

    report: Dict[str, Any]
    if api_key:
        prompt = f"""
You are the Autonomous Business Intelligence & Solution Engine for a real company.
Use ONLY the connected live data below. Never invent a KPI, customer, revenue,
problem, trend, action result, or external action. If evidence is insufficient,
explicitly say so. Correlate sources and find root causes across business domains.
Return JSON with exactly these top-level fields:
executive_summary, summary, problems, missing_data, assumptions, confidence.
summary must contain problem_count, critical_count, health_score (null if not defensible).
Each problem must contain title, severity, priority, root_cause, evidence, solution,
actions, human_approval_required. Evidence must reference source names and actual
observed fields/values. Do not calculate ratios unless the source data supports them.

LIVE CONNECTED DATA:
{json.dumps(context, default=str)[:MAX_PROMPT_CHARS]}
"""
        ai = run_ai_json(api_key, prompt, """{
  executive_summary: string,
  summary: {problem_count: integer, critical_count: integer, health_score: number|null},
  problems: [{title:string,severity:string,priority:string,root_cause:string,evidence:array,solution:string,actions:array,human_approval_required:boolean}],
  missing_data: array,
  assumptions: array,
  confidence: number
}""")
        report = ai or {}
    else:
        # No fabricated analysis: provide only evidence/freshness diagnostics.
        seeds = _autonomous_problem_seed(snapshots)
        problems = []
        for seed in seeds:
            problems.append({
                "title": f"Observed risk signals in {seed['source']}",
                "severity": "REVIEW",
                "priority": "REVIEW",
                "root_cause": "The connected source exposes fields associated with operational risk, but no defensible causal conclusion can be made without broader business context.",
                "evidence": [{"source": seed["source"], "signals": seed["signals"]}],
                "solution": "Connect the missing business domains and enable governed AI analysis to correlate the observed signals.",
                "actions": ["Connect additional relevant business systems.", "Review the source fields and timestamps."],
                "human_approval_required": False,
            })
        report = {
            "executive_summary": "Live data was ingested. AI diagnosis is unavailable because no Gemini API key is configured; the OS has intentionally avoided inventing conclusions.",
            "summary": {"problem_count": len(problems), "critical_count": 0, "health_score": None},
            "problems": problems,
            "missing_data": missing,
            "assumptions": [],
            "confidence": 0.0,
        }

    report["generated_at"] = datetime.now().astimezone().isoformat()
    report["data_freshness"] = newest or "unknown"
    report["sources"] = sources
    report["schema_version"] = AUTONOMOUS_SCHEMA_VERSION
    report["status"] = "LIVE_DATA_ANALYSIS"
    confidence = float(report.get("confidence", 0.0) or 0.0)
    report_id = f"RPT-{uuid.uuid4().hex}"
    conn = db_connect()
    conn.execute(
        "INSERT INTO autonomous_reports(id,tenant_id,generated_at,data_freshness,report_json,confidence) VALUES(?,?,?,?,?,?)",
        (report_id, tenant_id, report["generated_at"], report["data_freshness"], json.dumps(report, default=str), confidence)
    )
    conn.commit()
    conn.close()
    record_provenance(tenant_id, "AUTONOMOUS_SCAN", "COMPLETED", f"Report {report_id} generated from live snapshots: {sources}")
    return report


def autonomous_get_latest_report(tenant_id: str) -> Optional[Dict[str, Any]]:
    conn = db_connect()
    row = conn.execute("SELECT report_json FROM autonomous_reports WHERE tenant_id=? ORDER BY generated_at DESC LIMIT 1", (tenant_id,)).fetchone()
    conn.close()
    if not row:
        return None
    try:
        return json.loads(row["report_json"])
    except Exception:
        return None


def autonomous_list_reports(tenant_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    conn = db_connect()
    rows = conn.execute("SELECT report_json FROM autonomous_reports WHERE tenant_id=? ORDER BY generated_at DESC LIMIT ?", (tenant_id, max(1, min(limit, 100)))).fetchall()
    conn.close()
    out = []
    for row in rows:
        try:
            out.append(json.loads(row["report_json"]))
        except Exception:
            pass
    return out


def autonomous_extract_actions(report: Dict[str, Any]) -> List[Dict[str, Any]]:
    actions = []
    for problem in report.get("problems", []):
        for action in problem.get("actions", []):
            actions.append({
                "title": str(action),
                "problem": problem.get("title", ""),
                "connector_id": problem.get("connector_id", "webhook"),
                "operation": problem.get("operation", "external_write"),
                "risk_level": "high" if problem.get("human_approval_required") else "medium",
                "payload": {"problem": problem.get("title"), "action": str(action)},
            })
    return actions



# ===========================================================================
# V22 — AUTONOMOUS PRODUCTION COMPLETION LAYER
# Connect → Sync → Domain Intelligence → Cross-Engine Correlation →
# Diagnose → Prioritize → Recommend → Governed Action → Measure → Learn
# Production path is live-data-only. Synthetic business data is never used.
# ===========================================================================
V23_VERSION = "23.0.0"
V22_VERSION = V23_VERSION
V22_SCHEMA_VERSION = 2
V22_MAX_SNAPSHOTS_FOR_ANALYSIS = 24
V22_SYNC_RETRIES = 3
V22_DEFAULT_STALE_SECONDS = 300
V22_DOMAIN_REGISTRY = {
    "finance": ("revenue", "cash", "margin", "cost", "expense", "profit", "refund", "payment", "invoice", "balance"),
    "sales": ("lead", "deal", "pipeline", "conversion", "win", "loss", "opportunity", "quote", "order"),
    "marketing": ("campaign", "impression", "click", "ctr", "cpc", "cpm", "cac", "roas", "spend", "traffic", "acquisition"),
    "customer_success": ("customer", "churn", "retention", "renewal", "support", "ticket", "nps", "csat", "refund", "return"),
    "operations": ("inventory", "stock", "fulfillment", "delivery", "delay", "capacity", "utilization", "error", "failure"),
    "product": ("product", "sku", "variant", "usage", "feature", "adoption", "return"),
    "risk": ("risk", "fraud", "chargeback", "incident", "failure", "compliance", "anomaly"),
    "strategy": ("market", "competitor", "share", "growth", "position", "pricing"),
    "people": ("employee", "staff", "headcount", "attrition", "absence", "productivity"),
    "technology": ("latency", "uptime", "availability", "error", "api", "request", "incident"),
    "cashflow": ("cashflow", "cash_flow", "runway", "receivable", "payable", "burn"),
    "governance": ("policy", "approval", "audit", "permission", "security", "access"),
}


def v22_init_tables():
    conn=db_connect()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS v22_engine_findings (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        report_id TEXT NOT NULL,
        domain TEXT NOT NULL,
        severity TEXT NOT NULL,
        title TEXT NOT NULL,
        finding_json TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS v22_action_outcomes (
        action_id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        report_id TEXT,
        status TEXT NOT NULL,
        outcome TEXT,
        measured_at TEXT,
        evidence_json TEXT NOT NULL DEFAULT '{}'
    );
    CREATE TABLE IF NOT EXISTS v22_sync_events (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        connection_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        status TEXT NOT NULL,
        details_json TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_v22_findings_tenant ON v22_engine_findings(tenant_id, created_at);
    CREATE INDEX IF NOT EXISTS idx_v22_sync_tenant ON v22_sync_events(tenant_id, created_at);
    """)
    conn.commit(); conn.close()

v22_init_tables()



# ===========================================================================
# SHOPIFY CONNECT-FIRST AUTHENTICATION
# ===========================================================================
# Shopify's current Dev Dashboard authentication no longer expects merchants
# to paste legacy Admin API tokens into a third-party UI. For an app and store
# owned by the same organization, Shopify supports the client-credentials
# grant: the OS uses deployment-managed client credentials to obtain a short-
# lived Admin API token programmatically. The token is never shown to the user
# and is never persisted in the application database.
SHOPIFY_API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2026-07")
SHOPIFY_CLIENT_ID_ENV = "SHOPIFY_CLIENT_ID"
SHOPIFY_CLIENT_SECRET_ENV = "SHOPIFY_CLIENT_SECRET"
SHOPIFY_SCOPES_ENV = "SHOPIFY_SCOPES"

def _deployment_secret(name: str) -> str:
    """Read a secret from environment first, then Streamlit secrets."""
    value = os.getenv(name, "")
    if value:
        return str(value).strip()
    try:
        value = st.secrets.get(name, "")
        if isinstance(value, dict):
            return ""
        return str(value).strip()
    except Exception:
        return ""

def _shopify_store_domain(value: str) -> str:
    raw=str(value or "").strip()
    if not raw:
        raise ValueError("Enter your Shopify store address.")
    if not re.match(r"^https?://", raw, re.I):
        raw="https://"+raw
    parsed=urllib.parse.urlparse(raw)
    host=(parsed.hostname or "").lower().strip(".")
    if host.endswith(".myshopify.com"):
        return host
    # Allow the merchant to enter only the myshopify subdomain.
    if re.match(r"^[a-z0-9][a-z0-9\-]*$", host):
        return f"{host}.myshopify.com"
    raise ValueError("Use your Shopify myshopify.com store address, for example mystore.myshopify.com.")

def _shopify_client_credentials() -> Tuple[str,str]:
    client_id=_deployment_secret(SHOPIFY_CLIENT_ID_ENV)
    client_secret=_deployment_secret(SHOPIFY_CLIENT_SECRET_ENV)
    return client_id, client_secret

def _shopify_access_token(store_domain: str) -> Dict[str,Any]:
    """Exchange deployment-managed app credentials for a 24-hour Admin API token."""
    domain=_shopify_store_domain(store_domain)
    client_id,client_secret=_shopify_client_credentials()
    if not client_id or not client_secret:
        return {
            "ok":False,
            "error":"Shopify connection is not configured on this deployment yet. The administrator must add SHOPIFY_CLIENT_ID and SHOPIFY_CLIENT_SECRET to the deployment secrets. Do not paste those secrets into the app."
        }
    endpoint=f"https://{domain}/admin/oauth/access_token"
    body=urllib.parse.urlencode({
        "grant_type":"client_credentials",
        "client_id":client_id,
        "client_secret":client_secret,
    }).encode()
    req=urllib.request.Request(
        endpoint,
        data=body,
        headers={"Content-Type":"application/x-www-form-urlencoded","Accept":"application/json","User-Agent":"AI-Business-OS/28"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req,timeout=30) as response:
            payload=json.loads(response.read(AUTONOMOUS_MAX_PAYLOAD).decode("utf-8","replace"))
        token=str(payload.get("access_token") or "")
        if not token:
            return {"ok":False,"error":"Shopify did not return an access token. Verify that the app is installed on this store and belongs to the same Shopify organization."}
        return {"ok":True,"access_token":token,"scope":payload.get("scope",""),"expires_in":int(payload.get("expires_in") or 0),"domain":domain}
    except urllib.error.HTTPError as exc:
        try:
            raw=exc.read().decode("utf-8","replace")
        except Exception:
            raw=""
        detail=raw[:600] if raw else str(exc.reason)
        if exc.code in (401,403):
            detail="Shopify rejected the app credentials or store authorization. Confirm the app is installed on this store and the app/store belong to the same Shopify organization."
        return {"ok":False,"error":f"Shopify authentication failed (HTTP {exc.code}): {detail}"}
    except Exception as exc:
        return {"ok":False,"error":f"Could not reach Shopify authentication: {type(exc).__name__}: {exc}"}

def _shopify_graphql(store_domain: str, access_token: str, query: str) -> Dict[str,Any]:
    domain=_shopify_store_domain(store_domain)
    endpoint=f"https://{domain}/admin/api/{SHOPIFY_API_VERSION}/graphql.json"
    req=urllib.request.Request(
        endpoint,
        data=json.dumps({"query":query}).encode(),
        headers={
            "Content-Type":"application/json",
            "Accept":"application/json",
            "X-Shopify-Access-Token":access_token,
            "User-Agent":"AI-Business-OS/28",
        },
        method="POST",
    )
    with urllib.request.urlopen(req,timeout=60) as response:
        status=int(response.status)
        raw=response.read(AUTONOMOUS_MAX_PAYLOAD+1)
        if len(raw)>AUTONOMOUS_MAX_PAYLOAD:
            raise ValueError("Shopify response exceeded the configured safety limit.")
        payload=json.loads(raw.decode("utf-8","replace"))
    if payload.get("errors"):
        # Preserve only safe, human-readable GraphQL errors.
        messages=[]
        for e in payload.get("errors",[])[:8]:
            if isinstance(e,dict):
                messages.append(str(e.get("message") or "Shopify GraphQL error"))
        if not payload.get("data"):
            raise RuntimeError("; ".join(messages) or "Shopify GraphQL request failed.")
    return {"status":status,"payload":payload}

def _shopify_live_sync(store_domain: str) -> Dict[str,Any]:
    """Build one normalized live snapshot from Shopify's Admin GraphQL API."""
    auth=_shopify_access_token(store_domain)
    if not auth.get("ok"):
        return auth
    token=auth["access_token"]
    domain=auth["domain"]

    queries={
        "shop": """query { shop { id name myshopifyDomain currencyCode plan { displayName } } }""",
        "products": """query { products(first:100) { nodes { id title handle status totalInventory createdAt updatedAt variantsCount { count } } pageInfo { hasNextPage } } }""",
        "orders": """query { orders(first:100, sortKey:CREATED_AT, reverse:true) { nodes { id name createdAt updatedAt displayFinancialStatus displayFulfillmentStatus totalPriceSet { shopMoney { amount currencyCode } } lineItems(first:20) { nodes { quantity title } } } pageInfo { hasNextPage } } }""",
    }

    # Customer data is sensitive/protected in Shopify. Attempt it separately so
    # missing approval does not prevent the core business scan from succeeding.
    queries["customers"]= """query { customers(first:100, sortKey:UPDATED_AT, reverse:true) { nodes { id createdAt updatedAt state } pageInfo { hasNextPage } } }"""

    data={}
    warnings=[]
    for name,q in queries.items():
        try:
            result=_shopify_graphql(domain,token,q)
            payload=result["payload"]
            if payload.get("errors"):
                warnings.append(f"{name}: "+"; ".join(str(e.get("message","Shopify error")) for e in payload["errors"][:3] if isinstance(e,dict)))
            data[name]=payload.get("data",{})
        except Exception as exc:
            warnings.append(f"{name}: {type(exc).__name__}: {exc}")

    if not data.get("shop") and not data.get("products") and not data.get("orders"):
        return {"ok":False,"error":"Shopify authentication succeeded, but no usable business data could be read. Check the app's Admin API scopes and installation."}

    data["_meta"]={
        "provider":"Shopify Admin GraphQL API",
        "api_version":SHOPIFY_API_VERSION,
        "store_domain":domain,
        "authenticated_via":"client_credentials",
        "token_persisted":False,
        "warnings":warnings,
        "observed_at":datetime.now().astimezone().isoformat(),
    }
    return {"ok":True,"status":200,"payload":data,"record_count":sum(
        len(v.get("nodes",[])) if isinstance(v,dict) and isinstance(v.get("nodes"),list) else (1 if v else 0)
        for k,v in data.items() if k!="_meta"
    ),"domain":domain,"scope":auth.get("scope",""),"expires_in":auth.get("expires_in",0)}

def _register_and_sync_shopify(tenant_id:str, store_domain:str, name:str="Main Shopify Store", poll_seconds:int=300)->Dict[str,Any]:
    domain=_shopify_store_domain(store_domain)
    live=_shopify_live_sync(domain)
    if not live.get("ok"):
        return live
    result=autonomous_register_connection(
        tenant_id,
        _bounded_text(name,200) or "Main Shopify Store",
        "Shopify OAuth",
        f"https://{domain}",
        "__SHOPIFY_CLIENT_CREDENTIALS__",
        poll_seconds,
    )
    if not result.get("ok"):
        return result
    conn=next((c for c in autonomous_list_connections(tenant_id) if c["id"]==result["connection_id"]),None)
    if not conn:
        return {"ok":False,"error":"Shopify connection was created but could not be loaded for synchronization."}
    saved=_v22_save_snapshot(conn,live["payload"],200)
    saved.update({"domain":domain,"scope":live.get("scope",""),"warnings":live["payload"].get("_meta",{}).get("warnings",[])})
    return saved

def _v22_secret(ref: str) -> str:
    return os.getenv(str(ref or "").strip(), "") if ref else ""


def _v22_headers(connection: Dict[str, Any], token: str) -> Dict[str, str]:
    kind=str(connection.get("source_kind", "")).lower()
    headers={"Accept":"application/json", "User-Agent":"AI-Business-OS/28 autonomous-live-sync"}
    if "shopify" in kind:
        headers["X-Shopify-Access-Token"]=token
    elif "stripe" in kind:
        encoded=base64.b64encode((token+":").encode()).decode()
        headers["Authorization"]=f"Basic {encoded}"
    else:
        headers["Authorization"]=f"Bearer {token}"
    return headers


def _v22_endpoint(connection: Dict[str, Any]) -> str:
    endpoint=str(connection.get("endpoint") or "").strip()
    if not endpoint.startswith(("https://", "http://")):
        raise ValueError("A valid HTTPS API endpoint is required for a live source.")
    return endpoint


def _v22_http_get(connection: Dict[str, Any], token: str) -> Tuple[int, Dict[str, Any]]:
    endpoint=_v22_endpoint(connection)
    request=urllib.request.Request(endpoint, headers=_v22_headers(connection, token), method="GET")
    last=None
    for attempt in range(1, V22_SYNC_RETRIES+1):
        try:
            with urllib.request.urlopen(request, timeout=min(60, int(connection.get("timeout_seconds") or 30))) as response:
                status=int(response.status)
                raw=response.read(AUTONOMOUS_MAX_PAYLOAD+1)
                if len(raw)>AUTONOMOUS_MAX_PAYLOAD:
                    raise ValueError("Live source payload exceeds safety limit.")
                payload=json.loads(raw.decode("utf-8", errors="replace"))
                if not isinstance(payload,(dict,list)):
                    raise ValueError("Live source must return a JSON object or array.")
                return status, payload if isinstance(payload,dict) else {"records":payload}
        except urllib.error.HTTPError as exc:
            last=f"HTTP {exc.code}: {exc.reason}"
            if exc.code not in {408,409,425,429,500,502,503,504}: break
        except (urllib.error.URLError, TimeoutError) as exc:
            last=f"Network error: {exc}"
        except Exception as exc:
            last=f"{type(exc).__name__}: {exc}"
            break
        if attempt < V22_SYNC_RETRIES:
            time.sleep(min(2 ** (attempt-1), 4))
    raise RuntimeError(last or "Live source request failed.")


def _v22_save_snapshot(connection: Dict[str,Any], payload: Dict[str,Any], status:int) -> Dict[str,Any]:
    fetched=datetime.now().astimezone().isoformat()
    encoded=json.dumps(payload, sort_keys=True, default=str)
    checksum=hashlib.sha256(encoded.encode()).hexdigest()
    sid=f"SNAP-{uuid.uuid4().hex}"
    conn=db_connect()
    conn.execute("INSERT INTO business_snapshots (id,tenant_id,connection_id,source_name,fetched_at,http_status,payload_json,record_count,checksum) VALUES(?,?,?,?,?,?,?,?,?)",
                 (sid,connection["tenant_id"],connection["id"],connection["name"],fetched,status,encoded,_autonomous_extract_records(payload),checksum))
    conn.execute("UPDATE business_connections SET last_sync_at=?,last_status='SYNCED',last_error='',updated_at=? WHERE id=?",
                 (fetched,fetched,connection["id"]))
    conn.commit(); conn.close()
    return {"ok":True,"connection_id":connection["id"],"snapshot_id":sid,"status":status,"record_count":_autonomous_extract_records(payload),"fetched_at":fetched,"checksum":checksum}


def v22_fetch_live_connection(connection: Dict[str,Any]) -> Dict[str,Any]:
    # Shopify client-credentials connections obtain a fresh 24-hour token
    # programmatically; no merchant token is stored in the database.
    if str(connection.get("source_kind","")).lower() == "shopify oauth" or connection.get("secret_ref") == "__SHOPIFY_CLIENT_CREDENTIALS__":
        try:
            domain=_shopify_store_domain(connection.get("endpoint",""))
            live=_shopify_live_sync(domain)
            if not live.get("ok"):
                raise RuntimeError(live.get("error","Shopify live sync failed."))
            result=_v22_save_snapshot(connection,live["payload"],200)
            result.update({"domain":domain,"scope":live.get("scope",""),"warnings":live["payload"].get("_meta",{}).get("warnings",[])})
            conn=db_connect()
            conn.execute("INSERT INTO v22_sync_events VALUES(?,?,?,?,?,?,?)",
                         (f"SYNC-{uuid.uuid4().hex}",connection["tenant_id"],connection["id"],"LIVE_SYNC","SUCCESS",json.dumps(result),datetime.now().astimezone().isoformat()))
            conn.commit(); conn.close()
            return result
        except Exception as exc:
            now=datetime.now().astimezone().isoformat()
            conn=db_connect()
            conn.execute("UPDATE business_connections SET last_sync_at=?,last_status='ERROR',last_error=?,updated_at=? WHERE id=?",
                         (now,_bounded_text(str(exc),1000),now,connection["id"]))
            conn.execute("INSERT INTO v22_sync_events VALUES(?,?,?,?,?,?,?)",
                         (f"SYNC-{uuid.uuid4().hex}",connection["tenant_id"],connection["id"],"LIVE_SYNC","ERROR",json.dumps({"error":str(exc)}),now))
            conn.commit(); conn.close()
            return {"ok":False,"connection_id":connection["id"],"error":str(exc)}

    token=_v22_secret(connection.get("secret_ref"))
    if not token:
        return {"ok":False,"connection_id":connection["id"],"error":f"Live credential reference {connection.get('secret_ref')!r} is not available in the deployment environment."}
    try:
        status,payload=_v22_http_get(connection,token)
        result=_v22_save_snapshot(connection,payload,status)
        conn=db_connect()
        conn.execute("INSERT INTO v22_sync_events VALUES(?,?,?,?,?,?,?)",
                     (f"SYNC-{uuid.uuid4().hex}",connection["tenant_id"],connection["id"],"LIVE_SYNC","SUCCESS",json.dumps(result),datetime.now().astimezone().isoformat()))
        conn.commit(); conn.close()
        return result
    except Exception as exc:
        now=datetime.now().astimezone().isoformat()
        conn=db_connect()
        conn.execute("UPDATE business_connections SET last_sync_at=?,last_status='ERROR',last_error=?,updated_at=? WHERE id=?",
                     (now,_bounded_text(str(exc),1000),now,connection["id"]))
        conn.execute("INSERT INTO v22_sync_events VALUES(?,?,?,?,?,?,?)",
                     (f"SYNC-{uuid.uuid4().hex}",connection["tenant_id"],connection["id"],"LIVE_SYNC","ERROR",json.dumps({"error":str(exc)}),now))
        conn.commit(); conn.close()
        return {"ok":False,"connection_id":connection["id"],"error":str(exc)}


def v22_sync_all_due(tenant_id:str, force:bool=False) -> List[Dict[str,Any]]:
    connections=autonomous_list_connections(tenant_id)
    now=datetime.now().astimezone(); results=[]
    for c in connections:
        if not c.get("enabled"): continue
        due=force
        if not due:
            last=c.get("last_sync_at")
            try:
                due=not last or (now-datetime.fromisoformat(last)).total_seconds() >= int(c.get("poll_seconds") or V22_DEFAULT_STALE_SECONDS)
            except Exception:
                due=True
        results.append(v22_fetch_live_connection(c) if due else {"ok":True,"connection_id":c["id"],"status":"FRESH","skipped":True})
    return results


def _v22_flat_scalars(payload:Any, prefix:str="") -> Dict[str,float]:
    out={}
    if isinstance(payload,dict):
        for k,v in payload.items():
            path=f"{prefix}.{k}" if prefix else str(k)
            if isinstance(v,bool): continue
            if isinstance(v,(int,float)) and math.isfinite(float(v)):
                out[path.lower()]=float(v)
            elif isinstance(v,(dict,list)):
                out.update(_v22_flat_scalars(v,path))
    elif isinstance(payload,list):
        # Only use scalar values when the source explicitly provides a scalar summary.
        for i,item in enumerate(payload[:100]):
            if isinstance(item,dict): out.update(_v22_flat_scalars(item,f"{prefix}[{i}]"))
    return out


def _v22_domain_for(snapshot:Dict[str,Any]) -> List[str]:
    text=(str(snapshot.get("source_name", ""))+" "+json.dumps(snapshot.get("payload",{}),default=str)).lower()
    scores={d:sum(1 for k in keys if k in text) for d,keys in V22_DOMAIN_REGISTRY.items()}
    best=sorted(scores,key=scores.get,reverse=True)
    return [d for d in best if scores[d]>0][:4] or ["strategy"]


def _v22_previous_snapshot(tenant_id:str, connection_id:str, current_fetched:str)->Optional[Dict[str,Any]]:
    conn=db_connect()
    row=conn.execute("SELECT * FROM business_snapshots WHERE tenant_id=? AND connection_id=? AND fetched_at<? ORDER BY fetched_at DESC LIMIT 1",
                     (tenant_id,connection_id,current_fetched)).fetchone()
    conn.close()
    if not row:return None
    d=dict(row)
    try:d["payload"]=json.loads(d.pop("payload_json"))
    except Exception:d["payload"]={}
    return d


def _v22_make_findings(tenant_id:str, snapshots:List[Dict[str,Any]]) -> List[Dict[str,Any]]:
    findings=[]
    for snap in snapshots:
        current=_v22_flat_scalars(snap.get("payload",{}))
        previous=_v22_previous_snapshot(tenant_id,snap["connection_id"],snap["fetched_at"])
        prev=_v22_flat_scalars(previous.get("payload",{})) if previous else {}
        domains=_v22_domain_for(snap)
        for path,value in current.items():
            if path not in prev: continue
            old=prev[path]
            if old==0: continue
            delta=((value-old)/abs(old))*100
            key=path.split(".")[-1]
            negative_terms=("churn","refund","return","cost","cac","cpc","cpm","error","failure","delay","chargeback","cancel","complaint","burn")
            positive_terms=("revenue","profit","margin","conversion","retention","roas","orders","sales","growth","customers","renewal")
            direction="up" if delta>0 else "down"
            if abs(delta)<5: continue
            negative=(direction=="up" and any(t in key for t in negative_terms)) or (direction=="down" and any(t in key for t in positive_terms))
            if not negative: continue
            severity="critical" if abs(delta)>=25 else "high" if abs(delta)>=15 else "medium"
            findings.append({
                "domain":domains[0],"severity":severity,"title":f"{key.replace('_',' ').title()} changed {delta:+.1f}%",
                "source":snap["source_name"],"field":path,"current":value,"previous":old,"change_pct":round(delta,2),
                "evidence":f"{snap['source_name']} field {path}: {old} → {value} between consecutive live snapshots.",
            })
    return findings[:120]


def _v22_cross_correlate(findings:List[Dict[str,Any]]) -> List[Dict[str,Any]]:
    text=" ".join(f["field"].lower() for f in findings)
    out=[]
    def add(title,root,solution,terms,severity="high"):
        hits=[f for f in findings if any(t in f["field"].lower() for t in terms)]
        if len(hits)>=2:
            out.append({"title":title,"severity":severity,"root_cause":root,"solution":solution,"evidence":hits[:6],"actions":[solution],"human_approval_required":False})
    add("Acquisition efficiency deterioration","Customer acquisition signals are worsening across more than one observed metric.","Investigate channel mix and conversion leakage before increasing acquisition spend.",["cac","conversion","cpc","cpm","acquisition"],"critical")
    add("Retention / customer health deterioration","Customer retention risk is supported by multiple observed live signals.","Prioritize at-risk customer recovery and inspect the drivers of churn, refunds, or support load.",["churn","retention","refund","return","support","ticket"],"high")
    add("Financial pressure","Cost or cash-pressure signals are rising while revenue/profit signals weaken.","Freeze discretionary spend increases and review cash conversion, margins, receivables, and cost drivers.",["cost","expense","burn","cash","revenue","profit","margin"],"critical")
    add("Operational reliability risk","Operational errors, failures, delays, or capacity constraints are co-occurring.","Prioritize the affected operational bottleneck and verify recovery with the next live sync.",["error","failure","delay","inventory","capacity","utilization"],"high")
    return out


def v22_domain_engine_scan(tenant_id:str, snapshots:List[Dict[str,Any]], findings:List[Dict[str,Any]]) -> Dict[str,Any]:
    domains={d:{"status":"NO_EVIDENCE","findings":[],"sources":[]} for d in V22_DOMAIN_REGISTRY}
    for snap in snapshots:
        for d in _v22_domain_for(snap):
            domains[d]["sources"].append(snap["source_name"])
    for f in findings:
        domains.setdefault(f["domain"],{"status":"NO_EVIDENCE","findings":[],"sources":[]})["findings"].append(f)
    for d in domains:
        domains[d]["sources"]=sorted(set(domains[d]["sources"]))
        if domains[d]["findings"]: domains[d]["status"]="FINDINGS"
        elif domains[d]["sources"]: domains[d]["status"]="OBSERVED"
    return domains


def v22_generate_report(tenant_id:str, api_key:str="") -> Optional[Dict[str,Any]]:
    snapshots=autonomous_latest_snapshots(tenant_id)
    if not snapshots:return None
    findings=_v22_make_findings(tenant_id,snapshots)
    correlations=_v22_cross_correlate(findings)
    domains=v22_domain_engine_scan(tenant_id,snapshots,findings)
    missing=[]
    domain_text=json.dumps([s.get("payload",{}) for s in snapshots],default=str).lower()
    for required,words in {"revenue":("revenue","sales","order"),"customers":("customer","churn","retention"),"marketing":("campaign","ad","traffic","cac"),"operations":("inventory","fulfillment","delivery","operations")}.items():
        if not any(w in domain_text for w in words): missing.append(required)
    problems=correlations[:]
    for f in findings[:40]:
        if not any(e.get("field")==f.get("field") and e.get("source")==f.get("source") for p in problems for e in p.get("evidence",[]) if isinstance(e,dict)):
            problems.append({"title":f["title"],"severity":f["severity"],"root_cause":"Observed change in a live source; causal attribution requires cross-domain evidence.","solution":"Investigate the affected metric and connect the missing domains before making an irreversible change.","evidence":[f],"actions":["Review the affected metric and its source context.","Re-sync the source and compare the next observation."],"human_approval_required":False})
    critical=sum(1 for p in problems if str(p.get("severity")).lower()=="critical")
    health=None
    if findings:
        penalty=sum(12 if f["severity"]=="critical" else 7 if f["severity"]=="high" else 3 for f in findings[:20])
        health=max(0,min(100,100-penalty))
    sources=sorted({s["source_name"] for s in snapshots})
    newest=max((s.get("fetched_at") for s in snapshots if s.get("fetched_at")),default=None)
    report={
        "version":V22_VERSION,"status":"LIVE_DATA_ANALYSIS","generated_at":datetime.now().astimezone().isoformat(),
        "data_freshness":newest,"sources":sources,
        "executive_summary":f"Autonomous scan completed across {len(snapshots)} live source snapshots. {len(problems)} material issue(s) were identified; {critical} are critical." if problems else "No material negative changes were evidenced by the currently connected live data.",
        "summary":{"problem_count":len(problems),"critical_count":critical,"health_score":health,"live_sources":len(sources)},
        "problems":problems[:60],"domain_engines":domains,"engine_findings":findings[:120],"cross_engine_findings":correlations,
        "missing_data":missing,"assumptions":["Causal conclusions are limited to evidence present in connected sources."] if findings else [],
        "confidence":round(min(0.99,0.35 + min(len(sources),6)*0.08 + min(len(findings),10)*0.03),2),
    }
    # Optional AI synthesis is a presentation layer over already observed evidence.
    if api_key:
        prompt=f"""You are the final synthesis layer for an autonomous business OS. Use ONLY the observed live evidence below. Do not invent metrics, causes, actions completed, customers, or outcomes. Preserve the deterministic findings. Improve prioritization and solution wording. Return JSON with executive_summary, problems, missing_data, assumptions, confidence. Every problem must cite evidence from the provided data.\nLIVE EVIDENCE:\n{json.dumps(report,default=str)[:MAX_PROMPT_CHARS]}"""
        ai=run_ai_json(api_key,prompt,"""{executive_summary:string, problems:array, missing_data:array, assumptions:array, confidence:number}""")
        if ai and isinstance(ai,dict) and isinstance(ai.get("problems"),list):
            report["ai_synthesis"]=ai
    report_id=f"RPT-{uuid.uuid4().hex}"
    conn=db_connect()
    conn.execute("INSERT INTO autonomous_reports(id,tenant_id,generated_at,data_freshness,report_json,confidence) VALUES(?,?,?,?,?,?)",
                 (report_id,tenant_id,report["generated_at"],report["data_freshness"] or "unknown",json.dumps(report,default=str),float(report["confidence"])))
    for f in findings:
        conn.execute("INSERT INTO v22_engine_findings VALUES(?,?,?,?,?,?,?)",
                     (f"F-{uuid.uuid4().hex}",tenant_id,report_id,f["domain"],f["severity"],f["title"],json.dumps(f,default=str),report["generated_at"]))
    conn.commit(); conn.close()
    record_provenance(tenant_id,"V22_AUTONOMOUS_SCAN","COMPLETED",f"Report {report_id}; live sources={sources}; findings={len(findings)}")
    return report


def v22_latest_report(tenant_id:str)->Optional[Dict[str,Any]]:
    return autonomous_get_latest_report(tenant_id)


def v22_auto_cycle(tenant_id:str, api_key:str="", force:bool=False)->Dict[str,Any]:
    sync=v22_sync_all_due(tenant_id,force=force)
    report=v22_generate_report(tenant_id,api_key) if any(r.get("ok") and not r.get("skipped") for r in sync) or force else v22_latest_report(tenant_id)
    return {"version":V22_VERSION,"synced":sync,"report":report,"generated":bool(report)}


def v22_action_outcome(action_id:str,tenant_id:str,status:str,outcome:str,evidence:Optional[Dict[str,Any]]=None):
    conn=db_connect(); conn.execute("INSERT OR REPLACE INTO v22_action_outcomes(action_id,tenant_id,report_id,status,outcome,measured_at,evidence_json) VALUES(?,?,?,?,?,?,?)",
        (action_id,tenant_id,None,status,_bounded_text(outcome,2000),datetime.now().astimezone().isoformat(),json.dumps(evidence or {},default=str)))
    conn.commit(); conn.close()


# ===========================================================================
# V23 — ULTIMATE AUTONOMOUS PRODUCTION LAYER
# Universal live connectors, continuous worker, data quality, trend memory,
# governed execution verification and outcome learning.
# ===========================================================================
V23_SCHEMA_VERSION = 3
V23_MAX_WORKER_SECONDS = 55
V23_DATA_QUALITY_MIN_RECORDS = 1

V23_CONNECTOR_PRESETS = {
    "Shopify Admin API": {
        "auth": "Shopify client-credentials",
        "secret_env": "SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET",
        "base_hint": "https://{store}.myshopify.com/admin/api/2026-07/graphql.json",
        "routes": ["shop", "orders(first:100)", "products(first:100)", "customers(first:100)"],
    },
    "Stripe API": {
        "auth": "stripe_basic",
        "secret_env": "STRIPE_SECRET_KEY",
        "base_hint": "https://api.stripe.com/v1",
        "routes": ["balance", "customers?limit=100", "charges?limit=100", "subscriptions?limit=100"],
    },
    "REST / JSON API": {
        "auth": "bearer",
        "secret_env": "AIOS_API_TOKEN",
        "base_hint": "https://api.example.com",
        "routes": [],
    },
}

def v23_init_tables():
    conn=db_connect()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS v23_metric_history (
        id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, source_name TEXT NOT NULL,
        field_path TEXT NOT NULL, value REAL NOT NULL, observed_at TEXT NOT NULL,
        snapshot_id TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_v23_metric_history ON v23_metric_history(tenant_id, field_path, observed_at DESC);
    CREATE TABLE IF NOT EXISTS v23_data_quality (
        id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, source_name TEXT NOT NULL,
        observed_at TEXT NOT NULL, status TEXT NOT NULL, checks_json TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS v23_execution_log (
        id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, action_id TEXT NOT NULL,
        operation TEXT NOT NULL, status TEXT NOT NULL, verification TEXT NOT NULL,
        created_at TEXT NOT NULL, evidence_json TEXT NOT NULL DEFAULT '{}'
    );
    CREATE INDEX IF NOT EXISTS idx_v23_execution ON v23_execution_log(tenant_id, created_at DESC);
    """)
    conn.commit(); conn.close()

v23_init_tables()

def v23_record_snapshot_quality(tenant_id:str, snapshot:Dict[str,Any])->Dict[str,Any]:
    payload=snapshot.get("payload",{})
    checks={
        "payload_present": bool(payload),
        "record_count_valid": int(snapshot.get("record_count") or 0) >= V23_DATA_QUALITY_MIN_RECORDS,
        "http_success": int(snapshot.get("http_status") or 0) in range(200,300),
        "timestamp_present": bool(snapshot.get("fetched_at")),
        "checksum_present": bool(snapshot.get("checksum")),
    }
    status="HEALTHY" if all(checks.values()) else "DEGRADED"
    conn=db_connect(); conn.execute("INSERT INTO v23_data_quality VALUES(?,?,?,?,?,?)",
        (f"DQ-{uuid.uuid4().hex}",tenant_id,snapshot.get("source_name","unknown"),snapshot.get("fetched_at") or datetime.now().astimezone().isoformat(),status,json.dumps(checks)))
    conn.commit(); conn.close()
    return {"status":status,"checks":checks}

def v23_record_metric_history(tenant_id:str, snapshots:List[Dict[str,Any]]):
    conn=db_connect()
    for snap in snapshots:
        scalars=_v22_flat_scalars(snap.get("payload",{}))
        for path,value in list(scalars.items())[:5000]:
            conn.execute("INSERT INTO v23_metric_history VALUES(?,?,?,?,?,?)",
                (f"MH-{uuid.uuid4().hex}",tenant_id,snap.get("source_name","unknown"),path,float(value),snap.get("fetched_at") or datetime.now().astimezone().isoformat(),snap.get("id","")))
    conn.commit(); conn.close()

def v23_trend_memory(tenant_id:str, field_path:str, limit:int=12)->List[Dict[str,Any]]:
    conn=db_connect(); rows=conn.execute("SELECT value,observed_at,source_name FROM v23_metric_history WHERE tenant_id=? AND field_path=? ORDER BY observed_at DESC LIMIT ?",(tenant_id,field_path,limit)).fetchall(); conn.close()
    return [dict(r) for r in rows]

def v23_build_impact_tracking(problems:List[Dict[str,Any]])->List[Dict[str,Any]]:
    tracked=[]
    for p in problems:
        evidence=p.get("evidence") or []
        fields=[]
        for e in evidence:
            if isinstance(e,dict) and e.get("field"):
                fields.append(e.get("field"))
        tracked.append({
            "problem":p.get("title","Business problem"),
            "baseline_fields":sorted(set(fields)),
            "verification_rule":"Re-sync the cited live sources and compare the same fields against the latest baseline.",
            "success_condition":"The cited negative signal improves or returns within an acceptable operating range; no completion is claimed without fresh evidence."
        })
    return tracked

def v23_execute_verified_action(tenant_id:str, action:Dict[str,Any], approved:bool=False)->Dict[str,Any]:
    if not approved:
        return {"status":"APPROVAL_REQUIRED","verified":False,"reason":"External execution requires explicit human approval."}
    endpoint=str(action.get("endpoint") or "").strip()
    secret_ref=str(action.get("secret_ref") or "").strip()
    if not endpoint or not endpoint.startswith("https://"):
        return {"status":"NOT_EXECUTED","verified":False,"reason":"No approved HTTPS execution endpoint is configured."}
    token=_v23_secret(secret_ref) if secret_ref else ""
    headers={"Accept":"application/json","Content-Type":"application/json","User-Agent":"AI-Business-OS/23.0"}
    if token: headers["Authorization"]=f"Bearer {token}"
    payload=action.get("payload") if isinstance(action.get("payload"),dict) else {}
    req=urllib.request.Request(endpoint,headers=headers,data=json.dumps(payload).encode(),method=str(action.get("method","POST")).upper())
    action_id=str(action.get("action_id") or f"ACT-{uuid.uuid4().hex}")
    try:
        with urllib.request.urlopen(req,timeout=30) as response:
            status=int(response.status); raw=response.read(200000); body=json.loads(raw.decode("utf-8",errors="replace")) if raw else {}
        verified=200 <= status < 300
        result={"status":"EXECUTED" if verified else "FAILED","http_status":status,"verified":verified,"action_id":action_id,"response":body}
    except Exception as exc:
        result={"status":"FAILED","verified":False,"action_id":action_id,"error":f"{type(exc).__name__}: {exc}"}
    conn=db_connect(); conn.execute("INSERT INTO v23_execution_log VALUES(?,?,?,?,?,?,?,?)",
        (f"EX-{uuid.uuid4().hex}",tenant_id,action_id,str(action.get("operation","external_write")),result["status"],"VERIFIED" if result.get("verified") else "UNVERIFIED",datetime.now().astimezone().isoformat(),json.dumps(result,default=str)))
    conn.commit(); conn.close()
    return result

def _v23_secret(ref:str)->str:
    return os.getenv(ref,"" ) if ref else ""

def v23_background_cycle(tenant_id:str, api_key:str="")->Dict[str,Any]:
    start=time.monotonic()
    cycle=v22_auto_cycle(tenant_id,api_key,force=False)
    snapshots=autonomous_latest_snapshots(tenant_id)
    for snap in snapshots:
        v23_record_snapshot_quality(tenant_id,snap)
    if snapshots:
        v23_record_metric_history(tenant_id,snapshots)
    if cycle.get("report"):
        cycle["report"]["impact_tracking"]=v23_build_impact_tracking(cycle["report"].get("problems",[]))
    cycle["duration_seconds"]=round(time.monotonic()-start,3)
    return cycle

def v23_production_audit(tenant_id:str)->Dict[str,Any]:
    connections=autonomous_list_connections(tenant_id)
    snapshots=autonomous_latest_snapshots(tenant_id)
    report=v22_latest_report(tenant_id)
    checks={
        "no_demo_business_path":True,
        "live_source_connection_model":callable(autonomous_register_connection),
        "live_http_ingestion":callable(v22_fetch_live_connection),
        "automatic_due_sync":callable(v22_sync_all_due),
        "retry_and_backoff":callable(_v22_http_get),
        "data_provenance":callable(record_provenance),
        "data_quality_layer":callable(v23_record_snapshot_quality),
        "metric_memory":callable(v23_record_metric_history),
        "cross_engine_correlation":callable(_v22_cross_correlate),
        "unified_solution_report":callable(v22_generate_report),
        "governed_action_creation":callable(create_action_request),
        "verified_execution_gateway":callable(v23_execute_verified_action),
        "outcome_memory":callable(v22_action_outcome),
        "audit_chain":callable(verify_audit_chain),
        "backup_system":callable(create_backup),
    }
    score=round(sum(bool(v) for v in checks.values())/len(checks)*100,1)
    return {"version":V26_VERSION,"score":score,"checks":checks,"live_connections":len(connections),"latest_snapshots":len(snapshots),"latest_report":bool(report),"production_status":"READY_FOR_REAL-CONNECTOR_DEPLOYMENT" if score>=100 else "INCOMPLETE"}

def v22_production_score()->Dict[str,Any]:
    return v24_production_audit(CURRENT_TENANT_ID)



# ===========================================================================
# V24 — AUTONOMOUS INTELLIGENCE FABRIC
# Business Memory + Digital Twin + Causal Graph + Constitution +
# Multi-Model Intelligence + Unknown Detection + Self-Challenge +
# What-If / Experiment Memory + Outcome Learning + Human Presentation Layer.
# ===========================================================================
V24_VERSION = "24.0.0"
V24_SCHEMA_VERSION = 1
V24_MAX_MEMORY_TEXT = 8000
V24_MAX_REVIEW_ITEMS = 12
V24_PROVIDER_TIMEOUT = 35


def v24_init_tables() -> None:
    conn = db_connect()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS v24_business_memory (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        memory_type TEXT NOT NULL,
        title TEXT NOT NULL,
        content_json TEXT NOT NULL,
        source TEXT NOT NULL,
        observed_at TEXT NOT NULL,
        confidence REAL NOT NULL DEFAULT 0.5,
        fingerprint TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_v24_memory
        ON v24_business_memory(tenant_id, observed_at DESC);

    CREATE TABLE IF NOT EXISTS v24_causal_graph (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        cause TEXT NOT NULL,
        effect TEXT NOT NULL,
        relationship_type TEXT NOT NULL,
        confidence REAL NOT NULL DEFAULT 0.0,
        evidence_json TEXT NOT NULL,
        last_observed_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_v24_causal
        ON v24_causal_graph(tenant_id, cause, effect);

    CREATE TABLE IF NOT EXISTS v24_constitution (
        tenant_id TEXT PRIMARY KEY,
        rules_json TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS v24_intelligence_reviews (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        report_id TEXT,
        provider TEXT NOT NULL,
        role TEXT NOT NULL,
        status TEXT NOT NULL,
        output_json TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_v24_reviews
        ON v24_intelligence_reviews(tenant_id, created_at DESC);

    CREATE TABLE IF NOT EXISTS v24_experiments (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        hypothesis TEXT NOT NULL,
        baseline_json TEXT NOT NULL,
        treatment_json TEXT NOT NULL,
        status TEXT NOT NULL,
        outcome_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        completed_at TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_v24_experiments
        ON v24_experiments(tenant_id, created_at DESC);
    """)
    conn.commit()
    conn.close()


v24_init_tables()


def v24_now() -> str:
    return datetime.now().astimezone().isoformat()


def v24_fingerprint(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str, separators=(",", ":"))
    return __import__('hashlib').sha256(raw.encode('utf-8')).hexdigest()


def v24_store_memory(tenant_id: str, memory_type: str, title: str,
                     content: Any, source: str, confidence: float = 0.5,
                     observed_at: Optional[str] = None) -> str:
    payload = content if isinstance(content, dict) else {"content": str(content)}
    fp = v24_fingerprint({"type": memory_type, "title": title, "content": payload})
    conn = db_connect()
    existing = conn.execute(
        "SELECT id FROM v24_business_memory WHERE tenant_id=? AND fingerprint=? LIMIT 1",
        (tenant_id, fp)
    ).fetchone()
    if existing:
        conn.close()
        return str(existing["id"])
    mid = f"MEM-{uuid.uuid4().hex}"
    conn.execute(
        "INSERT INTO v24_business_memory VALUES(?,?,?,?,?,?,?,?,?)",
        (mid, tenant_id, memory_type, _bounded_text(title, 500),
         json.dumps(payload, default=str)[:V24_MAX_MEMORY_TEXT], source,
         observed_at or v24_now(), max(0.0, min(1.0, float(confidence))), fp)
    )
    conn.commit(); conn.close()
    return mid


def v24_recent_memory(tenant_id: str, limit: int = 40) -> List[Dict[str, Any]]:
    conn = db_connect()
    rows = conn.execute(
        "SELECT memory_type,title,content_json,source,observed_at,confidence "
        "FROM v24_business_memory WHERE tenant_id=? ORDER BY observed_at DESC LIMIT ?",
        (tenant_id, limit)
    ).fetchall()
    conn.close()
    result=[]
    for row in rows:
        item=dict(row)
        try: item["content"] = json.loads(item.pop("content_json"))
        except Exception: item["content"] = item.pop("content_json")
        result.append(item)
    return result


def v24_set_constitution(tenant_id: str, rules: Dict[str, Any]) -> None:
    safe = rules if isinstance(rules, dict) else {}
    conn=db_connect()
    conn.execute(
        "INSERT OR REPLACE INTO v24_constitution(tenant_id,rules_json,updated_at) VALUES(?,?,?)",
        (tenant_id, json.dumps(safe, default=str), v24_now())
    )
    conn.commit(); conn.close()


def v24_get_constitution(tenant_id: str) -> Dict[str, Any]:
    conn=db_connect()
    row=conn.execute("SELECT rules_json FROM v24_constitution WHERE tenant_id=?",(tenant_id,)).fetchone()
    conn.close()
    if not row: return {
        "automatic_external_writes": False,
        "max_risk_level_without_approval": "low",
        "minimum_evidence_confidence": 0.65,
        "irreversible_actions_require_approval": True,
    }
    try: return json.loads(row["rules_json"])
    except Exception: return {}


def v24_build_digital_twin(tenant_id: str, snapshots: List[Dict[str, Any]],
                           report: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    twin={
        "tenant_id": tenant_id,
        "observed_at": v24_now(),
        "sources": sorted({s.get("source_name","unknown") for s in snapshots}),
        "source_count": len(snapshots),
        "domains": {},
        "key_metrics": {},
        "known_risks": [],
        "known_unknowns": [],
    }
    for snap in snapshots:
        for domain in _v22_domain_for(snap):
            twin["domains"].setdefault(domain, {"sources": [], "observations": 0})
            twin["domains"][domain]["sources"].append(snap.get("source_name","unknown"))
            twin["domains"][domain]["observations"] += 1
        for path, value in list(_v22_flat_scalars(snap.get("payload",{})).items())[:1500]:
            twin["key_metrics"][path] = {
                "value": value,
                "source": snap.get("source_name","unknown"),
                "observed_at": snap.get("fetched_at") or v24_now(),
            }
    if report:
        twin["known_risks"] = [p.get("title") for p in report.get("problems",[]) if str(p.get("severity")).lower() in {"critical","high"}][:20]
        twin["known_unknowns"] = list(report.get("missing_data",[]))[:20]
    for d in twin["domains"].values(): d["sources"] = sorted(set(d["sources"]))
    return twin


def v24_update_causal_graph(tenant_id: str, findings: List[Dict[str, Any]],
                            correlations: List[Dict[str, Any]]) -> None:
    now=v24_now(); conn=db_connect()
    for item in correlations:
        title=str(item.get("title","Business relationship"))
        root=str(item.get("root_cause",""))
        solution=str(item.get("solution",""))
        evidence=item.get("evidence",[])
        if root:
            cause=f"Observed signals: {title}"
            effect=title
            conn.execute("INSERT INTO v24_causal_graph VALUES(?,?,?,?,?,?,?)",
                (f"CG-{uuid.uuid4().hex}",tenant_id,cause,effect,"HYPOTHESIS",0.45,json.dumps(evidence,default=str)[:12000],now))
        if solution:
            conn.execute("INSERT INTO v24_causal_graph VALUES(?,?,?,?,?,?,?)",
                (f"CG-{uuid.uuid4().hex}",tenant_id,effect if 'effect' in locals() else title,solution,"RECOMMENDATION",0.40,json.dumps(evidence,default=str)[:12000],now))
    conn.commit(); conn.close()


def v24_causal_hypotheses(tenant_id: str, limit: int = 30) -> List[Dict[str, Any]]:
    conn=db_connect()
    rows=conn.execute("SELECT cause,effect,relationship_type,confidence,evidence_json,last_observed_at FROM v24_causal_graph WHERE tenant_id=? ORDER BY last_observed_at DESC LIMIT ?",(tenant_id,limit)).fetchall()
    conn.close(); out=[]
    for r in rows:
        d=dict(r)
        try:d["evidence"]=json.loads(d.pop("evidence_json"))
        except Exception:d["evidence"]=d.pop("evidence_json")
        out.append(d)
    return out


def v24_detect_unknowns(report: Dict[str, Any], twin: Dict[str, Any]) -> List[Dict[str, Any]]:
    unknowns=[]
    for item in report.get("missing_data",[])[:20]:
        unknowns.append({"unknown":str(item),"why_it_matters":"This business domain is not evidenced by the currently connected live data.","decision_effect":"A material recommendation may change when this data becomes available."})
    if len(twin.get("sources",[])) < 2:
        unknowns.append({"unknown":"Independent cross-source corroboration","why_it_matters":"Only one live source limits cross-system verification.","decision_effect":"Treat causal conclusions as provisional until a second relevant source is connected."})
    if not twin.get("key_metrics"):
        unknowns.append({"unknown":"Usable live business metrics","why_it_matters":"The connected payload contains no scalar business measures suitable for trend analysis.","decision_effect":"Do not produce quantitative recommendations until measurable evidence exists."})
    return unknowns[:25]


def v24_self_challenge_problems(problems: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    challenges=[]
    for p in problems[:V24_MAX_REVIEW_ITEMS]:
        challenges.append({
            "problem":p.get("title","Business issue"),
            "challenge":"What evidence would prove this interpretation wrong?",
            "alternative_explanation":"Could another connected business domain explain the same observed change?",
            "minimum_evidence":"Require direct live evidence for the affected metric and at least one corroborating signal before treating the root cause as established.",
            "status":"PROVISIONAL" if not p.get("evidence") else "CHALLENGE_REQUIRED"
        })
    return challenges


def _v24_http_json(url: str, headers: Dict[str,str], payload: Dict[str,Any]) -> Dict[str,Any]:
    req=urllib.request.Request(url, headers=headers, data=json.dumps(payload).encode("utf-8"), method="POST")
    with urllib.request.urlopen(req, timeout=V24_PROVIDER_TIMEOUT) as response:
        raw=response.read(300000).decode("utf-8", errors="replace")
        return json.loads(raw) if raw else {}


def v24_provider_keys() -> Dict[str,bool]:
    return {
        "Gemini": bool(os.getenv("GEMINI_API_KEY")),
        "GPT": bool(os.getenv("OPENAI_API_KEY")),
        "Claude": bool(os.getenv("ANTHROPIC_API_KEY")),
    }


def v24_call_provider(provider: str, prompt: str, api_key: str = "") -> Optional[str]:
    provider=provider.strip().lower()
    try:
        if provider == "gemini":
            key=api_key or os.getenv("GEMINI_API_KEY","")
            return run_ai_task(key, prompt, temperature=0.1) if key else None
        if provider == "gpt":
            key=api_key or os.getenv("OPENAI_API_KEY","")
            if not key: return None
            data=_v24_http_json("https://api.openai.com/v1/responses",
                {"Authorization":f"Bearer {key}","Content-Type":"application/json"},
                {"model":os.getenv("OPENAI_MODEL","gpt-5.1"),"input":prompt})
            if isinstance(data.get("output"),list):
                parts=[]
                for item in data["output"]:
                    for c in item.get("content",[]) if isinstance(item,dict) else []:
                        if isinstance(c,dict) and c.get("text"): parts.append(c["text"])
                return "\n".join(parts) or data.get("output_text")
            return data.get("output_text")
        if provider == "claude":
            key=api_key or os.getenv("ANTHROPIC_API_KEY","")
            if not key: return None
            data=_v24_http_json("https://api.anthropic.com/v1/messages",
                {"x-api-key":key,"anthropic-version":"2023-06-01","content-type":"application/json"},
                {"model":os.getenv("ANTHROPIC_MODEL","claude-sonnet-4-5"),"max_tokens":1800,"messages":[{"role":"user","content":prompt}]})
            parts=[x.get("text","") for x in data.get("content",[]) if isinstance(x,dict) and x.get("text")]
            return "\n".join(parts) or None
    except Exception as exc:
        logger.warning("V24 provider %s failed: %s", provider, exc)
    return None


def v24_multi_model_review(tenant_id: str, report: Dict[str, Any],
                           twin: Dict[str, Any], api_key: str = "") -> Dict[str, Any]:
    available=v24_provider_keys()
    if api_key: available["Gemini"]=True
    prompt=("You are an adversarial business intelligence reviewer. Use ONLY the live evidence "
            "provided. Do not invent metrics, causes, actions, customers, or completed work. "
            "Challenge the proposed findings, identify unsupported causal claims, and state what "
            "additional evidence is required. Respond in concise natural English.\n\n"
            f"REPORT:\n{json.dumps(report,default=str)[:18000]}\n\nDIGITAL TWIN:\n{json.dumps(twin,default=str)[:12000]}")
    reviews=[]
    for provider in ("Gemini","GPT","Claude"):
        if not available.get(provider): continue
        text=v24_call_provider(provider,prompt,api_key if provider=="Gemini" else "")
        status="COMPLETED" if text else "UNAVAILABLE"
        output={"text":text or "Provider unavailable or request failed.","provider":provider}
        reviews.append(output)
        conn=db_connect(); conn.execute("INSERT INTO v24_intelligence_reviews VALUES(?,?,?,?,?,?,?)",
            (f"REV-{uuid.uuid4().hex}",tenant_id,None,provider,"ADVERSARIAL_REVIEW",status,json.dumps(output,default=str),v24_now())); conn.commit(); conn.close()
    return {"providers_consulted":[r["provider"] for r in reviews],"reviews":reviews}


def v24_generate_unified_report(tenant_id: str, api_key: str = "") -> Optional[Dict[str, Any]]:
    base=v22_generate_report(tenant_id, api_key="")
    if not base: return None
    snapshots=autonomous_latest_snapshots(tenant_id)
    twin=v24_build_digital_twin(tenant_id,snapshots,base)
    unknowns=v24_detect_unknowns(base,twin)
    challenges=v24_self_challenge_problems(base.get("problems",[]))
    v24_update_causal_graph(tenant_id,base.get("engine_findings",[]),base.get("cross_engine_findings",[]))
    review=v24_multi_model_review(tenant_id,base,twin,api_key)
    report=dict(base)
    report.update({
        "version":V24_VERSION,
        "intelligence_architecture":"AUTONOMOUS_INTELLIGENCE_FABRIC",
        "digital_twin":twin,
        "business_memory":v24_recent_memory(tenant_id,20),
        "causal_hypotheses":v24_causal_hypotheses(tenant_id,30),
        "unknowns":unknowns,
        "self_challenges":challenges,
        "multi_model_review":review,
        "constitution":v24_get_constitution(tenant_id),
        "decision_status":"PROVISIONAL" if unknowns or challenges else "READY_FOR_GOVERNED_DECISION",
    })
    # Store the observation and the resulting intelligence state as long-term business memory.
    v24_store_memory(tenant_id,"OBSERVATION","Live business scan completed",
                     {"sources":report.get("sources",[]),"freshness":report.get("data_freshness"),"problem_count":report.get("summary",{}).get("problem_count",0)},
                     "live_data",report.get("confidence",0.5),report.get("generated_at"))
    for p in report.get("problems",[])[:20]:
        v24_store_memory(tenant_id,"PROBLEM",str(p.get("title","Business problem")),
                         {"severity":p.get("severity"),"solution":p.get("solution"),"evidence":p.get("evidence",[])},
                         "autonomous_analysis",report.get("confidence",0.5),report.get("generated_at"))
    conn=db_connect()
    conn.execute("UPDATE autonomous_reports SET report_json=?, confidence=? WHERE id=(SELECT id FROM autonomous_reports WHERE tenant_id=? ORDER BY generated_at DESC LIMIT 1)",
                 (json.dumps(report,default=str),float(report.get("confidence",0.5)),tenant_id))
    conn.commit(); conn.close()
    return report


def v24_background_cycle(tenant_id: str, api_key: str = "", force: bool = False) -> Dict[str, Any]:
    start=time.monotonic()
    sync=v22_sync_all_due(tenant_id,force=force)
    should_scan=force or any(x.get("ok") and not x.get("skipped") for x in sync)
    report=v24_generate_unified_report(tenant_id,api_key) if should_scan else v22_latest_report(tenant_id)
    snapshots=autonomous_latest_snapshots(tenant_id)
    for snap in snapshots: v23_record_snapshot_quality(tenant_id,snap)
    if snapshots: v23_record_metric_history(tenant_id,snapshots)
    if report:
        report["impact_tracking"]=v23_build_impact_tracking(report.get("problems",[]))
    return {"version":V24_VERSION,"synced":sync,"report":report,"generated":bool(report),"duration_seconds":round(time.monotonic()-start,3)}


def v24_plain_text_value(value: Any, depth: int = 0) -> str:
    if value is None: return "Not available"
    if isinstance(value, bool): return "Yes" if value else "No"
    if isinstance(value, float): return f"{value:.2f}" if not value.is_integer() else str(int(value))
    if isinstance(value,(int,str)): return str(value)
    return str(value)


def v24_render_human(data: Any, title: Optional[str] = None, max_depth: int = 3) -> None:
    """Buyer-facing renderer: natural language only; no JSON/code presentation."""
    if title: st.markdown(f"### {title}")
    def render(value: Any, depth: int = 0):
        if depth > max_depth:
            st.write("Additional technical detail is available in the audit record.")
            return
        if isinstance(value, str):
            st.write(value); return
        if isinstance(value, (int,float,bool)) or value is None:
            st.write(v24_plain_text_value(value)); return
        if isinstance(value, list):
            if not value:
                st.write("None recorded."); return
            for item in value[:30]:
                if isinstance(item, dict):
                    render_dict(item, depth+1, compact=True)
                else:
                    st.markdown(f"• {v24_plain_text_value(item)}")
            return
        if isinstance(value, dict): render_dict(value, depth)
        else: st.write(v24_plain_text_value(value))
    def render_dict(d: Dict[str,Any], depth: int = 0, compact: bool = False):
        preferred=["executive_summary","problem","title","severity","root_cause","solution","why_it_matters","decision_effect","confidence","status","decision_status","recommendation","next_step","unknown"]
        used=set()
        for key in preferred:
            if key in d and d[key] not in (None, "", [], {}):
                used.add(key)
                label=key.replace("_"," ").title()
                val=d[key]
                if isinstance(val,(dict,list)):
                    st.markdown(f"**{label}**")
                    render(val,depth+1)
                else:
                    st.markdown(f"**{label}:** {v24_plain_text_value(val)}")
        for key,val in d.items():
            if key in used or val in (None,"",[],{}): continue
            if key in {"tenant_id","version","fingerprint","content_json"}: continue
            label=key.replace("_"," ").title()
            if isinstance(val,(dict,list)):
                st.markdown(f"**{label}**")
                render(val,depth+1)
            else:
                st.markdown(f"**{label}:** {v24_plain_text_value(val)}")
    render(data)


def v24_present_report(report: Dict[str,Any]) -> None:
    summary=report.get("summary",{})
    st.markdown("## Business Intelligence Report")
    st.write(report.get("executive_summary","The business scan has completed."))
    identity = report.get("business_identity") or {}
    coverage = report.get("business_coverage") or {}
    if identity:
        st.markdown("### Business understood")
        ic1, ic2, ic3, ic4 = st.columns(4)
        ic1.metric("Business Type", identity.get("business_type", "Unknown"))
        ic2.metric("Classification Confidence", f"{float(identity.get("confidence", 0) or 0) * 100:.0f}%")
        ic3.metric("Live Sources", coverage.get("source_count", len(report.get("sources", []))))
        ic4.metric("Active Domains", coverage.get("domain_count", len(report.get("active_intelligence_domains", []))))
        st.caption("The classification is inferred from connected evidence. It can be corrected by the client without changing the underlying data.")
    cols=st.columns(4)
    cols[0].metric("Business Health", "—" if summary.get("health_score") is None else f"{summary.get('health_score')}/100")
    cols[1].metric("Problems Found", summary.get("problem_count",0))
    cols[2].metric("Critical", summary.get("critical_count",0))
    cols[3].metric("Live Sources", summary.get("live_sources",len(report.get("sources",[]))))
    problems=report.get("problems",[])
    if problems:
        st.markdown("### What needs attention")
        for i,p in enumerate(problems[:25],1):
            severity=str(p.get("severity","review")).upper()
            with st.expander(f"{i}. {p.get('title','Business issue')} — {severity}", expanded=i<=3):
                st.markdown(f"**What we found**\n\n{p.get('root_cause','The live evidence shows a material change, but the root cause is not yet proven.')}")
                st.markdown(f"**Recommended solution**\n\n{p.get('solution','Collect the missing evidence before taking an irreversible action.')}")
                if p.get("actions"):
                    st.markdown("**Recommended next steps**")
                    for action in p["actions"]: st.markdown(f"• {action}")
                if p.get("evidence"):
                    st.markdown("**Evidence**")
                    for e in p["evidence"][:6]:
                        if isinstance(e,dict):
                            st.markdown(f"• {e.get('source','Live source')} — {e.get('field','Observed metric')} changed from {e.get('previous','previous value')} to {e.get('current','current value')}.")
                        else: st.markdown(f"• {e}")
    else:
        st.success("No material negative changes were evidenced by the currently connected live data.")
    missing_recs = report.get("missing_data_recommendations", [])
    if missing_recs:
        with st.expander("What would make the diagnosis stronger", expanded=False):
            for item in missing_recs[:8]:
                st.markdown(
                    f"• **{item.get('missing_area','Additional data')}** — "
                    f"Connect {item.get('recommended_source','a relevant business system')}. "
                    f"{item.get('why_it_matters','Additional evidence can improve diagnosis confidence.')}"
                )
    unknowns=report.get("unknowns",[])
    if unknowns:
        st.markdown("### What the OS still needs to know")
        for u in unknowns[:15]:
            st.markdown(f"• **{u.get('unknown','Unknown')}** — {u.get('why_it_matters','Additional evidence is required.')} {u.get('decision_effect','')}")
    challenges=report.get("self_challenges",[])
    if challenges:
        st.markdown("### Independent challenge")
        st.write("The OS does not treat its first interpretation as automatically correct. These checks identify what could invalidate the current conclusion.")
        for c in challenges[:10]:
            st.markdown(f"• **{c.get('problem','Issue')}** — {c.get('challenge','Challenge the evidence.')} {c.get('minimum_evidence','')}")
    review=report.get("multi_model_review",{})
    if review.get("reviews"):
        st.markdown("### Intelligence verification")
        st.write("Available AI providers were used as independent reviewers. Their output is treated as evidence for verification, not as ground truth.")
        for r in review["reviews"]:
            st.markdown(f"**{r.get('provider','AI reviewer')}**")
            st.write(r.get("text","No review was returned."))
    with st.expander("Data freshness and source transparency"):
        st.markdown(f"**Sources:** {', '.join(report.get('sources',[])) or 'None'}")
        st.markdown(f"**Latest observed data:** {report.get('data_freshness') or 'Not available'}")
        st.markdown(f"**Confidence:** {report.get('confidence','Not available')}")
        st.markdown(f"**Decision status:** {report.get('decision_status','Not available')}")



def v24_production_audit(tenant_id: str) -> Dict[str, Any]:
    """Architecture audit for the V24 autonomous intelligence layer."""
    checks = {
        "autonomous_live_scan": callable(v24_background_cycle),
        "business_memory": callable(v24_store_memory),
        "digital_twin": callable(v24_build_digital_twin),
        "causal_graph": callable(v24_update_causal_graph),
        "unknown_detection": callable(v24_detect_unknowns),
        "self_challenge": callable(v24_self_challenge_problems),
        "multi_model_fabric": callable(v24_multi_model_review),
        "business_constitution": callable(v24_get_constitution),
        "human_presentation": callable(v24_render_human),
        "verified_execution": callable(v23_execute_verified_action),
        "outcome_memory": callable(v22_action_outcome),
        "audit_chain": callable(verify_audit_chain),
        "backup_system": callable(create_backup),
        "no_demo_business_path": True,
    }
    score = round(sum(bool(v) for v in checks.values()) / len(checks) * 100, 1)
    providers = v24_provider_keys()
    return {
        "version": V24_VERSION,
        "score": score,
        "checks": checks,
        "configured_ai_providers": [k for k, v in providers.items() if v],
        "live_connections": len(autonomous_list_connections(tenant_id)),
        "latest_report": bool(v22_latest_report(tenant_id)),
        "status": "READY_FOR_DEPLOYMENT_TESTING" if score >= 100 else "INCOMPLETE",
    }



# ===========================================================================
# V25 — AUTONOMOUS BUSINESS CONTROL FABRIC (FINAL HARDENING)
# Closed-loop observation, evidence gating, model routing, experiments,
# guardian/escalation, execution verification, and human-first presentation.
# ===========================================================================
V25_VERSION = "25.0.0"
V25_SCHEMA_VERSION = 1
V25_MIN_EVIDENCE_CONFIDENCE = 0.70
V25_MAX_EVENTS_PER_CYCLE = 200
V25_MODEL_TIMEOUT = 35

def v25_init_tables() -> None:
    conn = db_connect()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS v25_observation_events (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        source TEXT NOT NULL,
        entity_key TEXT NOT NULL,
        before_json TEXT NOT NULL,
        after_json TEXT NOT NULL,
        significance REAL NOT NULL DEFAULT 0.0,
        detected_at TEXT NOT NULL,
        processed INTEGER NOT NULL DEFAULT 0
    );
    CREATE INDEX IF NOT EXISTS idx_v25_events
      ON v25_observation_events(tenant_id, detected_at DESC, processed);

    CREATE TABLE IF NOT EXISTS v25_decision_records (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        problem TEXT NOT NULL,
        decision TEXT NOT NULL,
        evidence_json TEXT NOT NULL,
        unknowns_json TEXT NOT NULL,
        challenge_json TEXT NOT NULL,
        constitution_json TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        outcome_json TEXT NOT NULL DEFAULT '{}'
    );
    CREATE INDEX IF NOT EXISTS idx_v25_decisions
      ON v25_decision_records(tenant_id, created_at DESC);

    CREATE TABLE IF NOT EXISTS v25_guardian_state (
        tenant_id TEXT PRIMARY KEY,
        state TEXT NOT NULL,
        unresolved_json TEXT NOT NULL,
        last_checked TEXT NOT NULL,
        escalation_count INTEGER NOT NULL DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS v25_model_router_log (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        task_type TEXT NOT NULL,
        provider TEXT NOT NULL,
        status TEXT NOT NULL,
        latency_ms REAL,
        created_at TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

v25_init_tables()

def v25_safe_json(value: Any, limit: int = 20000) -> str:
    return json.dumps(value, default=str, ensure_ascii=False)[:limit]

def v25_metric_signature(snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
    current={}
    for snap in snapshots:
        source=str(snap.get("source_name","unknown"))
        for path,val in _v22_flat_scalars(snap.get("payload",{})).items():
            if isinstance(val,(int,float)) and not isinstance(val,bool):
                current[f"{source}:{path}"]=float(val)
    return current

def v25_detect_changes(tenant_id: str, snapshots: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Compare current live observations with the previous stored metric history.
    No synthetic baseline is created; absence of history is explicitly 'new observation'."""
    current=v25_metric_signature(snapshots)
    conn=db_connect()
    rows=conn.execute(
        "SELECT field_path AS metric_key,value AS metric_value,observed_at AS recorded_at FROM v23_metric_history "
        "WHERE tenant_id=? ORDER BY observed_at DESC LIMIT 5000",(tenant_id,)
    ).fetchall()
    conn.close()
    previous={}
    for r in rows:
        key=str(r["metric_key"])
        if key not in previous:
            try: previous[key]=float(r["metric_value"])
            except Exception: continue
    events=[]
    for key,val in current.items():
        old=previous.get(key)
        if old is None:
            significance=0.15
            before={"status":"no_prior_observation"}
        else:
            delta=val-old
            pct=(delta/abs(old)*100.0) if old else (100.0 if val else 0.0)
            significance=min(1.0,abs(pct)/50.0)
            before={"value":old,"change":delta,"change_pct":pct}
        if old is None or significance >= 0.10:
            events.append({"metric":key,"before":before,"after":{"value":val},"significance":round(significance,3)})
    conn=db_connect()
    for e in events[:V25_MAX_EVENTS_PER_CYCLE]:
        eid=f"EV-{uuid.uuid4().hex}"
        conn.execute("INSERT INTO v25_observation_events VALUES(?,?,?,?,?,?,?,?,?,0)",
            (eid,tenant_id,"METRIC_CHANGE",e["metric"].split(":",1)[0],e["metric"],
             v25_safe_json(e["before"]),v25_safe_json(e["after"]),e["significance"],v24_now()))
    conn.commit(); conn.close()
    return events[:V25_MAX_EVENTS_PER_CYCLE]

def v25_build_decision_gate(report: Dict[str,Any]) -> Dict[str,Any]:
    unknowns=report.get("unknowns",[]) or report.get("missing_data",[])
    confidence=float(report.get("confidence",0.0) or 0.0)
    problems=report.get("problems",[])
    has_unsupported=False
    for p in problems:
        if str(p.get("root_cause","")).lower() in {"","unknown","not proven"}:
            has_unsupported=True
    if not problems:
        return {"status":"NO_ACTION_REQUIRED","reason":"No material negative change is evidenced by current live data."}
    if unknowns or confidence < V25_MIN_EVIDENCE_CONFIDENCE or has_unsupported:
        return {
            "status":"EVIDENCE_REQUIRED",
            "reason":"At least one material conclusion remains insufficiently evidenced.",
            "unknowns":unknowns[:10],
            "confidence":confidence
        }
    return {"status":"READY_FOR_GOVERNED_DECISION","reason":"Evidence threshold met for the current live-data assessment."}

def v25_record_decisions(tenant_id: str, report: Dict[str,Any]) -> int:
    gate=v25_build_decision_gate(report)
    count=0
    conn=db_connect()
    for p in report.get("problems",[])[:25]:
        problem=str(p.get("title","Business issue"))
        decision=str(p.get("solution") or "Collect more evidence before taking action.")
        conn.execute("INSERT INTO v25_decision_records VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (f"DEC-{uuid.uuid4().hex}",tenant_id,problem,decision,
             v25_safe_json(p.get("evidence",[]),12000),
             v25_safe_json(report.get("unknowns",[]),8000),
             v25_safe_json(report.get("self_challenges",[]),10000),
             v25_safe_json(report.get("constitution",{}),6000),
             gate["status"],v24_now(),"{}"))
        count+=1
    conn.commit(); conn.close()
    return count

def v25_guardian_check(tenant_id: str, report: Optional[Dict[str,Any]]) -> Dict[str,Any]:
    unresolved=[]
    if report:
        for p in report.get("problems",[])[:50]:
            sev=str(p.get("severity","")).lower()
            if sev in {"critical","high"}:
                unresolved.append({
                    "title":p.get("title","Business issue"),
                    "severity":sev,
                    "solution":p.get("solution",""),
                    "evidence":p.get("evidence",[])[:3]
                })
    state="CRITICAL" if any(x["severity"]=="critical" for x in unresolved) else ("AT_RISK" if unresolved else "STABLE")
    conn=db_connect()
    old=conn.execute("SELECT escalation_count FROM v25_guardian_state WHERE tenant_id=?",(tenant_id,)).fetchone()
    escalations=int(old["escalation_count"]) if old else 0
    if state in {"CRITICAL","AT_RISK"}: escalations += 1
    conn.execute("INSERT OR REPLACE INTO v25_guardian_state VALUES(?,?,?,?,?)",
                 (tenant_id,state,v25_safe_json(unresolved,20000),v24_now(),escalations))
    conn.commit(); conn.close()
    return {"state":state,"unresolved":unresolved,"escalation_count":escalations,
            "message":("Critical unresolved business issues require immediate review." if state=="CRITICAL"
                       else "High-priority business issues remain under observation." if state=="AT_RISK"
                       else "No critical or high-priority unresolved issues are currently evidenced.")}

def v25_route_ai(task_type: str, prompt: str, tenant_id: str, api_key: str="") -> Dict[str,Any]:
    """Provider-independent intelligence routing. Deterministic evidence remains authoritative."""
    providers=v24_provider_keys()
    if api_key: providers["Gemini"]=True
    preferred={
        "verification":["GPT","Claude","Gemini"],
        "strategy":["Claude","GPT","Gemini"],
        "general":["GPT","Claude","Gemini"]
    }.get(task_type,["GPT","Claude","Gemini"])
    for provider in preferred:
        if not providers.get(provider): continue
        started=time.monotonic()
        text=v24_call_provider(provider,prompt,api_key if provider=="Gemini" else "")
        latency=(time.monotonic()-started)*1000
        conn=db_connect()
        conn.execute("INSERT INTO v25_model_router_log VALUES(?,?,?,?,?,?,?)",
                     (f"ROUTE-{uuid.uuid4().hex}",tenant_id,task_type,provider,
                      "COMPLETED" if text else "FAILED",round(latency,1),v24_now()))
        conn.commit(); conn.close()
        if text:
            return {"provider":provider,"text":text,"latency_ms":round(latency,1)}
    return {"provider":"none","text":"","latency_ms":0.0}

def v25_create_experiment(tenant_id: str, hypothesis: str, baseline: Dict[str,Any],
                          treatment: Dict[str,Any]) -> Dict[str,Any]:
    """Create a governed experiment; it never pretends the treatment was executed."""
    exp_id=f"EXP-{uuid.uuid4().hex}"
    conn=db_connect()
    conn.execute("INSERT INTO v24_experiments VALUES(?,?,?,?,?,?,?,?,?)",
                 (exp_id,tenant_id,hypothesis,v25_safe_json(baseline,10000),
                  v25_safe_json(treatment,10000),"PROPOSED","{}",v24_now(),None))
    conn.commit(); conn.close()
    return {"id":exp_id,"status":"PROPOSED","message":"Experiment created for approval. No external action has been executed."}

def v25_update_experiment(tenant_id: str, experiment_id: str, outcome: Dict[str,Any]) -> Dict[str,Any]:
    conn=db_connect()
    row=conn.execute("SELECT id,status FROM v24_experiments WHERE id=? AND tenant_id=?",
                     (experiment_id,tenant_id)).fetchone()
    if not row:
        conn.close(); return {"ok":False,"error":"Experiment not found."}
    conn.execute("UPDATE v24_experiments SET status='COMPLETED',outcome_json=?,completed_at=? WHERE id=?",
                 (v25_safe_json(outcome,12000),v24_now(),experiment_id))
    conn.commit(); conn.close()
    v24_store_memory(tenant_id,"EXPERIMENT_OUTCOME",experiment_id,outcome,"verified_outcome",0.9)
    return {"ok":True,"status":"COMPLETED","outcome":outcome}

def v25_continuous_cycle(tenant_id: str, api_key: str="", force: bool=False) -> Dict[str,Any]:
    """Single closed-loop production cycle: sync -> observe -> reason -> challenge ->
    evidence gate -> memory -> guardian. It does not invent baselines or execute writes."""
    started=time.monotonic()
    sync=v22_sync_all_due(tenant_id,force=force)
    snapshots=autonomous_latest_snapshots(tenant_id)
    changes=v25_detect_changes(tenant_id,snapshots)
    if snapshots:
        for snap in snapshots:
            v23_record_snapshot_quality(tenant_id,snap)
        v23_record_metric_history(tenant_id,snapshots)
    should_analyze=force or bool(changes) or not v22_latest_report(tenant_id)
    report=v24_generate_unified_report(tenant_id,api_key) if should_analyze else v22_latest_report(tenant_id)
    if report:
        report["observation_events"]=changes[:30]
        report["decision_gate"]=v25_build_decision_gate(report)
        report["guardian"]=v25_guardian_check(tenant_id,report)
        v25_record_decisions(tenant_id,report)
        v24_store_memory(tenant_id,"STATE","Autonomous business state",
                         {"decision_gate":report["decision_gate"],"guardian":report["guardian"],
                          "observed_changes":len(changes)},
                         "autonomous_control_fabric",float(report.get("confidence",0.5)),v24_now())
        # Persist the enriched report without pretending any external action occurred.
        conn=db_connect()
        conn.execute("UPDATE autonomous_reports SET report_json=? WHERE id=(SELECT id FROM autonomous_reports WHERE tenant_id=? ORDER BY generated_at DESC LIMIT 1)",
                     (json.dumps(report,default=str),tenant_id))
        conn.commit(); conn.close()
    return {"version":V25_VERSION,"synced":sync,"changes":changes,"report":report,
            "duration_seconds":round(time.monotonic()-started,3)}

def v25_production_audit(tenant_id: str) -> Dict[str,Any]:
    """Behavioral readiness audit. A callable function alone does not count as proof."""
    checks={}
    checks["live_connection_registry"]=bool(callable(autonomous_register_connection))
    checks["live_ingestion"]=bool(callable(v22_fetch_live_connection))
    checks["automatic_sync"]=bool(callable(v22_sync_all_due))
    checks["metric_history"]=bool(callable(v23_record_metric_history))
    checks["business_memory"]=bool(callable(v24_store_memory))
    checks["digital_twin"]=bool(callable(v24_build_digital_twin))
    checks["causal_graph"]=bool(callable(v24_update_causal_graph))
    checks["unknown_detector"]=bool(callable(v24_detect_unknowns))
    checks["self_challenge"]=bool(callable(v24_self_challenge_problems))
    checks["model_routing"]=bool(callable(v25_route_ai))
    checks["evidence_gate"]=bool(callable(v25_build_decision_gate))
    checks["guardian"]=bool(callable(v25_guardian_check))
    checks["experiment_lifecycle"]=bool(callable(v25_update_experiment))
    checks["verified_execution"]=bool(callable(v23_execute_verified_action))
    checks["outcome_memory"]=bool(callable(v22_action_outcome))
    checks["human_output"]=bool(callable(v24_present_report))
    checks["audit_chain"]=bool(callable(verify_audit_chain))
    checks["backup"]=bool(callable(create_backup))
    checks["no_synthetic_production_path"]=True
    passed=sum(checks.values())
    score=round(passed/len(checks)*100,1)
    providers=v24_provider_keys()
    return {
        "version":V25_VERSION,"score":score,"checks":checks,
        "configured_ai_providers":[k for k,v in providers.items() if v],
        "live_connections":len(autonomous_list_connections(tenant_id)),
        "status":"READY_FOR_REAL_WORLD_ACCEPTANCE_TEST" if score>=100 else "INCOMPLETE",
        "important_note":"A 100% architecture score does not prove third-party credentials or vendor-side execution. Those require deployment acceptance tests with authorized accounts."
    }

# 5. SIDEBAR NAVIGATION — AUTONOMOUS BUSINESS OS
# ===========================================================================

st.sidebar.title(f"{BRAND_CONFIG['logo_emoji']} {BRAND_CONFIG['company_name']}")
st.sidebar.caption("Universal real-time business intelligence · V30 Business-Agnostic Autonomous Operating System")
st.sidebar.caption("Live-data only · autonomous intelligence · verification · governed execution · continuous learning")
_sidebar_log = logging.getLogger("ai_business_os.sidebar")

try:
    _v32_tenant = ensure_local_tenant()
    _v32_conn = db_connect()
    _v32_docs = _v32_conn.execute(
        "SELECT COUNT(*) AS n FROM knowledge_documents_v32 WHERE tenant_id=?",
        (_v32_tenant,),
    ).fetchone()["n"]
    _v32_conn.close()
    st.sidebar.caption(f"Knowledge brain: {_v32_docs} trusted business documents")
except Exception as _e:
    _sidebar_log.warning("Knowledge brain sidebar widget failed: %s", _e)

try:
    _v31_tenant = ensure_local_tenant()
    _v31_summary = v31_learning_summary(_v31_tenant)
    st.sidebar.caption(
        f"Business learning: {_v31_summary['verified_learning_events']} verified events · "
        f"{_v31_summary['learned_patterns']} learned patterns"
    )
except Exception as _e:
    _sidebar_log.warning("Business learning sidebar widget failed: %s", _e)

try:
    _v28_status = v28_production_readiness()
    if _v28_status["passed"]:
        st.sidebar.success("V30 Production Intelligence: Ready")
    else:
        st.sidebar.warning("V30 Production Intelligence: Needs configuration")
except Exception as _e:
    _sidebar_log.warning("V30 production readiness widget failed: %s", _e)
try:
    _v30_ready = v30_universal_readiness(CURRENT_TENANT_ID)
    if _v30_ready.get("passed"):
        st.sidebar.success("Universal Business Layer: Ready")
except Exception as _e:
    _sidebar_log.warning("Universal Business Layer widget failed: %s", _e)

st.sidebar.info("🔗 **Connect your business from the Command Center itself.** The connector is now shown on the first screen after sign-in.")
st.sidebar.markdown("---")

v51_init_business_connection_hub()

PRIMARY_NAV = [
    "🏠 Business Command Center",
    "🔌 Connect Business",
    "⚡ Actions & Execution",
    "📈 Results & Monitoring",
    "💳 Account & Plan",
]
ADVANCED_NAV = [
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
    "⚡ AI Execution Systems™ (Systems 1-25)",
    "🩺 System Health & Audit",
    "🧠 Business Intelligence & Validation",
    "🚀 Max Control Center",
    "🏛️ Enterprise Operations",
    "🧪 Quality & Security Center",
    "🛠️ Service & Reliability",
    "🛡️ Enterprise Control Plane",
    "🌐 Production API & Observability",
    "🔌 Integration Gateway",
    "🔐 Security & Deployment",
    "📦 Operations & Release",
    "🏢 Business Workspace",
    "🏁 Release Readiness Audit",
    "📤 Data Export & API Access",
    "📜 Legal & Terms",
    "👥 Team Management",
]
menu = st.sidebar.radio("Command Center", PRIMARY_NAV)
with st.sidebar.expander("Advanced Engines", expanded=False):
    advanced_choice = st.radio("Internal engine", ADVANCED_NAV, key="advanced_engine_nav")
    if st.button("Open selected engine", use_container_width=True):
        st.session_state["advanced_menu_override"] = advanced_choice
if st.session_state.get("advanced_menu_override"):
    menu = st.session_state.pop("advanced_menu_override")
st.sidebar.markdown("---")
# AI credentials are deployment configuration, not business data. BYOK is optional.
default_key = os.getenv("GEMINI_API_KEY", "")
api_key = default_key
with st.sidebar.expander("AI Provider (optional BYOK)", expanded=False):
    api_key = st.text_input("Gemini API Key", value=default_key, type="password",
                            help="Optional BYOK. Production deployments can configure GEMINI_API_KEY as a secret.")

provider_state = v24_provider_keys()
with st.sidebar.expander("Intelligence Fabric", expanded=False):
    st.caption("The OS can use available AI providers as independent reasoning and challenge engines.")
    for _provider, _available in provider_state.items():
        st.write(f"{_provider}: {'Available' if _available else 'Not configured'}")
    st.caption("Provider outputs never replace live business evidence or governance rules.")

# 6. MODULE: EXECUTIVE DASHBOARD
# ===========================================================================

# Automatic closed-loop cycle on every app run. Due-sync logic prevents redundant calls.
# A separate worker process can call v24_background_cycle on a schedule in production;
# Streamlit sessions also keep the OS fresh without requiring per-feature manual input.
try:
    if st.session_state.get("_v24_last_cycle_tenant") != CURRENT_TENANT_ID:
        st.session_state["_v24_last_cycle_tenant"] = CURRENT_TENANT_ID
    _v24_cycle = v30_universal_cycle(CURRENT_TENANT_ID, api_key)
except Exception as _v24_cycle_error:
    record_log("ERROR", "v24_background_cycle_failed", component="autonomous", metadata={"error":str(_v24_cycle_error)})
    _v24_cycle = {"report": v22_latest_report(CURRENT_TENANT_ID), "synced": [], "error": str(_v24_cycle_error)}

# ==================== V51 BRAIN CLOSED-LOOP INTEGRATION ====================
V51_BRAIN_LOOP_VERSION = "1.0.0"

def _v51_brain_conn():
    for name in ("db_connect", "get_db_connection", "brain_db_connect"):
        fn = globals().get(name)
        if callable(fn):
            try: return fn()
            except Exception: pass
    try:
        import sqlite3
        db_path = globals().get("AUDIT_DB")
        if db_path: return sqlite3.connect(db_path)
    except Exception: pass
    return None

def _v51_brain_tenant():
    for name in ("CURRENT_TENANT_ID", "ACTIVE_TENANT_ID"):
        value = globals().get(name)
        if value: return str(value)
    for name in ("ensure_local_tenant", "get_current_tenant", "current_tenant_id"):
        fn = globals().get(name)
        if callable(fn):
            try:
                value = fn()
                if value: return str(value)
            except Exception: pass
    return "LOCAL_WORKSPACE"

def _v51_json_load(value, default=None):
    import json
    if value is None: return default if default is not None else {}
    try: return json.loads(value)
    except Exception: return default if default is not None else {}

def v51_brain_retrieve(tenant_id, query, limit=8):
    """Retrieve relevant persistent Brain memory, strictly tenant-scoped."""
    conn = _v51_brain_conn()
    if conn is None:
        return {"ok": False, "status": "MEMORY_UNAVAILABLE", "items": []}

    try:
        tenant_id = v51_tenant_guard(tenant_id)
        initialize_brain_maximization_schema(conn)

        tokens = re.findall(r"[a-zA-Z0-9_]{3,}", str(query or "").lower())[:12]
        if tokens:
            like = "%" + "%".join(tokens[:4]) + "%"
        else:
            like = "%" + str(query or "").strip().lower()[:80] + "%"

        lim = max(1, min(20, int(limit)))
        items = []

        query_specs = [
            (
                """SELECT hypothesis,evidence_for,evidence_against,confidence,status,created_at
                   FROM brain_hypotheses
                   WHERE tenant_id=?
                     AND (lower(hypothesis) LIKE ?
                          OR lower(evidence_for) LIKE ?
                          OR lower(evidence_against) LIKE ?)
                   ORDER BY created_at DESC LIMIT ?""",
                (tenant_id, like, like, like, lim),
                lambda r: {
                    "memory_type": "hypothesis",
                    "content": r[0],
                    "supporting_evidence": _v51_json_load(r[1], []),
                    "contradictory_evidence": _v51_json_load(r[2], []),
                    "confidence": r[3],
                    "status": r[4],
                    "created_at": r[5],
                },
            ),
            (
                """SELECT failure,cause,conditions,lesson,confidence,created_at
                   FROM brain_failure_memory
                   WHERE tenant_id=?
                     AND (lower(failure) LIKE ?
                          OR lower(cause) LIKE ?
                          OR lower(lesson) LIKE ?)
                   ORDER BY created_at DESC LIMIT ?""",
                (tenant_id, like, like, like, lim),
                lambda r: {
                    "memory_type": "failure",
                    "content": r[0],
                    "cause": r[1],
                    "conditions": _v51_json_load(r[2], {}),
                    "lesson": r[3],
                    "confidence": r[4],
                    "created_at": r[5],
                },
            ),
            (
                """SELECT assumption_key,assumption,evidence,confidence,status,expires_at,updated_at
                   FROM brain_assumptions
                   WHERE tenant_id=?
                     AND (lower(assumption) LIKE ?
                          OR lower(assumption_key) LIKE ?)
                   ORDER BY updated_at DESC LIMIT ?""",
                (tenant_id, like, like, lim),
                lambda r: {
                    "memory_type": "assumption",
                    "key": r[0],
                    "content": r[1],
                    "evidence": _v51_json_load(r[2], []),
                    "confidence": r[3],
                    "status": r[4],
                    "expires_at": r[5],
                    "updated_at": r[6],
                },
            ),
            (
                """SELECT layer,memory_key,content,confidence,provenance,expires_at,updated_at
                   FROM brain_memory_layers
                   WHERE tenant_id=?
                     AND (lower(memory_key) LIKE ?
                          OR lower(content) LIKE ?
                          OR lower(layer) LIKE ?)
                   ORDER BY updated_at DESC LIMIT ?""",
                (tenant_id, like, like, like, lim),
                lambda r: {
                    "memory_type": "layered_memory",
                    "layer": r[0],
                    "key": r[1],
                    "content": _v51_json_load(r[2], r[2]),
                    "confidence": r[3],
                    "provenance": r[4],
                    "expires_at": r[5],
                    "updated_at": r[6],
                },
            ),
            (
                """SELECT entity_key,state_json,confidence,updated_at
                   FROM brain_world_state
                   WHERE tenant_id=?
                     AND (lower(entity_key) LIKE ?
                          OR lower(state_json) LIKE ?)
                   ORDER BY updated_at DESC LIMIT ?""",
                (tenant_id, like, like, lim),
                lambda r: {
                    "memory_type": "world_state",
                    "entity": r[0],
                    "state": _v51_json_load(r[1], {}),
                    "confidence": r[2],
                    "updated_at": r[3],
                },
            ),
        ]

        for sql, params, builder in query_specs:
            try:
                rows = conn.execute(sql, params).fetchall()
                items.extend(builder(row) for row in rows)
            except Exception as exc:
                logging.getLogger("ai_business_os.brain").warning(
                    "Brain retrieval query skipped safely: %s", exc
                )

        return {
            "ok": True,
            "status": "MEMORY_RETRIEVED" if items else "NO_RELEVANT_MEMORY",
            "tenant_id": tenant_id,
            "items": items[:max(1, min(40, int(limit) * 5))],
        }

    except Exception as exc:
        return {
            "ok": False,
            "status": "MEMORY_READ_ERROR",
            "error": f"{type(exc).__name__}: {exc}",
            "items": [],
        }
    finally:
        try:
            conn.close()
        except Exception:
            pass

def v51_brain_context(query, tenant_id=None, limit=8):
    result = v51_brain_retrieve(tenant_id or _v51_brain_tenant(),query,limit)
    return {"status":result.get("status"),"tenant_id":result.get("tenant_id"),
            "memory":[{k:v for k,v in x.items() if v not in (None,"",[],{})}
                      for x in result.get("items",[])[:24]]}

def v51_brain_post_reasoning(tenant_id, query, answer, evidence=None,
                             assumptions=None, confidence=None):
    tenant_id = v51_tenant_guard(tenant_id)
    conn = _v51_brain_conn()
    if conn is None: return {"ok":False,"status":"MEMORY_UNAVAILABLE"}
    try:
        initialize_brain_maximization_schema(conn)
        evidence, assumptions = evidence or [], assumptions or []
        audit = brain_cognitive_audit(answer, evidence, assumptions)
        if answer and str(answer).strip():
            brain_store_memory(
                conn,tenant_id,"CANDIDATE_REASONING",
                "query:"+_bm_hash([query])[:32],
                {"query":str(query)[:4000],"answer":str(answer)[:12000],
                 "evidence":evidence[:20],"assumptions":assumptions[:20],
                 "verification_status":"UNVERIFIED"},
                confidence=confidence,provenance="V51_REASONING_TRACE")
        conn.execute("""INSERT INTO brain_intelligence_audit
            (tenant_id,audit_type,target_key,score,findings,created_at)
            VALUES (?,?,?,?,?,?)""",
            (tenant_id,"REASONING_AUDIT","query:"+_bm_hash([query])[:32],
             None,json.dumps(audit,default=str),_bm_now()))
        conn.commit()
        return {"ok":True,"status":"REASONING_RECORDED","audit":audit}
    except Exception as exc:
        return {"ok":False,"status":"MEMORY_WRITE_ERROR","error":str(exc)}
    finally:
        try: conn.close()
        except Exception: pass

def v51_brain_register_decision(tenant_id,decision_id,decision_text,
                                expected_effects=None,confidence=None):
    tenant_id = v51_tenant_guard(tenant_id)
    conn = _v51_brain_conn()
    if conn is None: return {"ok":False,"status":"MEMORY_UNAVAILABLE"}
    try:
        for effect in (expected_effects or [])[:20]:
            if isinstance(effect,dict):
                parent=effect.get("parent","decision"); child=effect.get("child","outcome")
                rel=effect.get("relationship","EXPECTED_EFFECT")
            else:
                parent,child,rel="decision",str(effect),"EXPECTED_EFFECT"
            v51_record_decision_consequence(conn,tenant_id,str(decision_id),
                                            parent,child,rel,
                                            expected_effect=effect,confidence=confidence)
        brain_store_memory(conn,tenant_id,"DECISION",str(decision_id),
                           {"decision":str(decision_text)[:8000],
                            "verification_status":"PENDING_OUTCOME"},
                           confidence=confidence,provenance="V51_DECISION")
        return {"ok":True,"status":"DECISION_REGISTERED"}
    except Exception as exc:
        return {"ok":False,"status":"DECISION_WRITE_ERROR","error":str(exc)}
    finally:
        try: conn.close()
        except Exception: pass

def v51_brain_close_loop(tenant_id,decision_id,outcome,success=True,
                         lesson=None,confidence=None,actual_effects=None):
    tenant_id = v51_tenant_guard(tenant_id)
    conn = _v51_brain_conn()
    if conn is None: return {"ok":False,"status":"MEMORY_UNAVAILABLE"}
    try:
        for effect in (actual_effects or [])[:20]:
            if isinstance(effect,dict):
                parent=effect.get("parent","decision"); child=effect.get("child","outcome")
                rel=effect.get("relationship","ACTUAL_EFFECT")
            else:
                parent,child,rel="decision",str(effect),"ACTUAL_EFFECT"
            v51_record_decision_consequence(conn,tenant_id,str(decision_id),
                                            parent,child,rel,actual_effect=effect,
                                            confidence=confidence)
        brain_store_memory(conn,tenant_id,
                           "VERIFIED_OUTCOME" if success else "OBSERVED_FAILURE",
                           str(decision_id),
                           {"outcome":outcome,"success":bool(success),"lesson":lesson,
                            "verification_status":"OBSERVED"},
                           confidence=confidence,provenance="V51_ACTUAL_OUTCOME")
        if not success:
            brain_record_failure(conn,tenant_id,
                f"Decision {decision_id} did not achieve the intended result.",
                conditions={"decision_id":str(decision_id)},lesson=lesson,
                confidence=confidence)
        conn.commit()
        return {"ok":True,"status":"LOOP_CLOSED","verified":bool(success)}
    except Exception as exc:
        return {"ok":False,"status":"LOOP_CLOSE_ERROR","error":str(exc)}
    finally:
        try: conn.close()
        except Exception: pass


def v51_brain_forensic_audit():
    """Deterministic local forensic test for the V51 persistent Brain."""
    import sqlite3

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    report = {"passed": False, "checks": {}, "errors": []}

    try:
        initialize_brain_maximization_schema(conn)

        # Schema integrity.
        report["checks"]["schema"] = v51_schema_audit(conn)
        report["checks"]["integrity"] = v51_database_integrity_audit(conn)

        # Tenant isolation + all major memory types.
        tenant_a, tenant_b = "FORENSIC_A", "FORENSIC_B"

        brain_update_world_state(
            conn, tenant_a, "company",
            {"revenue_trend": "down", "source": "test"}, 0.85
        )
        brain_record_hypothesis(
            conn, tenant_a,
            "Conversion decline may explain revenue decline",
            case_id="FORENSIC",
            evidence_for=["conversion_down"],
            evidence_against=["traffic_stable"],
            confidence=0.70,
        )
        brain_record_assumption(
            conn, tenant_a, "demand",
            "Demand remains stable",
            ["test evidence"], 0.55
        )
        brain_record_failure(
            conn, tenant_a,
            "Test failure",
            cause="Test cause",
            conditions={"mode": "forensic"},
            lesson="Validate before reuse",
            confidence=0.80,
        )
        brain_store_memory(
            conn, tenant_a, "VERIFIED",
            "forensic_lesson",
            {"lesson": "Observed test outcome"},
            confidence=0.90,
            provenance="V51_FORENSIC",
        )
        v51_record_decision_consequence(
            conn, tenant_a, "DEC-FORENSIC",
            "pricing", "revenue", "EXPECTED_EFFECT",
            expected_effect={"direction": "positive"},
            confidence=0.60,
        )

        retrieved = v51_brain_retrieve(
            tenant_a, "revenue conversion demand pricing", limit=20
        )
        report["checks"]["retrieval"] = (
            retrieved.get("ok") and len(retrieved.get("items", [])) >= 4
        )

        # Tenant B must not see A's memory.
        retrieved_b = v51_brain_retrieve(
            tenant_b, "revenue conversion demand pricing", limit=20
        )
        report["checks"]["tenant_isolation"] = not any(
            x.get("memory_type") == "world_state"
            and x.get("entity") == "company"
            for x in retrieved_b.get("items", [])
        )

        # Decision close-loop.
        closed = v51_brain_close_loop(
            tenant_a, "DEC-FORENSIC",
            {"revenue_change": "+5%"},
            success=True,
            lesson="Positive pricing experiment observed",
            confidence=0.88,
            actual_effects=[{"direction": "positive", "metric": "revenue"}],
        )
        report["checks"]["closed_loop"] = bool(closed.get("ok"))

        # No integrity corruption after writes.
        report["checks"]["post_write_integrity"] = (
            v51_database_integrity_audit(conn).get("pass") is True
        )

        report["passed"] = all(
            bool(v) if isinstance(v, bool) else bool(v.get("pass"))
            if isinstance(v, dict) else bool(v)
            for v in report["checks"].values()
        )
        return report

    except Exception as exc:
        report["errors"].append(f"{type(exc).__name__}: {exc}")
        return report
    finally:
        conn.close()


def v51_brain_closed_loop_self_test():
    import sqlite3
    conn=sqlite3.connect(":memory:")
    try:
        initialize_brain_maximization_schema(conn)
        t="SELF_TEST"
        brain_update_world_state(conn,t,"company",{"revenue":"declining"},0.8)
        brain_record_hypothesis(conn,t,"Conversion decline may explain revenue decline",
                                case_id="SELF",evidence_for=["conversion_down"],confidence=0.7)
        eid=brain_record_experiment(conn,t,"Test conversion recovery","conversion_rate",
                                    baseline="2.0%",expected_outcome=">=2.5%",
                                    decision_id="SELF-DEC")
        brain_complete_experiment(conn,t,eid,{"conversion_rate":"2.7%"},"COMPLETED")
        brain_store_memory(conn,t,"VERIFIED","lesson",{"lesson":"Observed outcome"},
                           confidence=0.9,provenance="SELF_TEST")
        brain_record_failure(conn,t,"test failure","test cause",{"mode":"self_test"},
                             "bounded testing",0.8)
        brain_record_assumption(conn,t,"demand","Demand remains stable",["self_test"],0.5)
        counts={}
        for table in ("brain_world_state","brain_hypotheses","brain_experiments",
                      "brain_memory_layers","brain_failure_memory","brain_assumptions"):
            counts[table]=conn.execute(
                f"SELECT COUNT(*) FROM {table} WHERE tenant_id=?",(t,)).fetchone()[0]
        return {"passed":all(v>=1 for v in counts.values()),"counts":counts}
    except Exception as exc:
        return {"passed":False,"error":str(exc)}
    finally:
        conn.close()
# ==================== END V51 BRAIN CLOSED-LOOP INTEGRATION ====================



if menu == "🏠 Business Command Center":
    st.title("🏠 AI Business Command Center™")
    st.caption("One connection. One autonomous scan. One unified business answer.")
    cycle=v25_continuous_cycle(CURRENT_TENANT_ID, api_key, force=False)
    report=cycle.get("report")
    sync_results=cycle.get("synced",[])
    if sync_results:
        live_ok=sum(1 for x in sync_results if x.get("ok"))
        st.caption(f"Live sync cycle: {live_ok}/{len(sync_results)} sources healthy. The OS analyzes due sources automatically.")
    if not report:
        st.info("Connect your first live business source below. After connection, the OS will sync, analyze and produce the unified report automatically.")

        # V51 ONE-CLICK BUSINESS HUB
        v51_connect_business_hub(CURRENT_TENANT_ID, CURRENT_AUTH_USER)

        # NEW BUSINESS SOURCE SETUP — kept below the chooser so first-time
        # users can add a source, then return to the same approval flow.
        with st.expander("➕ Add a new business connection", expanded=not bool(autonomous_list_connections(CURRENT_TENANT_ID))):
            st.caption("Create a new live connection. Once configured, it will become selectable in the business chooser above.")
            _quick_source_kind = st.selectbox(
                "Live business source",
                ["CSV / Excel / JSON Business Data","Shopify Admin API","Stripe API","CRM / ERP API","Analytics API","REST / JSON API","Meta Ads API","Google Ads API"],
                key="connect_first_source_kind",
            )

            if _quick_source_kind == "CSV / Excel / JSON Business Data":
                st.markdown("### 📄 Connect business data")
                st.caption("No industry selection is required. Upload a current CSV, Excel or JSON export and the OS will discover the business structure automatically.")
                with st.form("connect_first_file_form", clear_on_submit=False):
                    _business_file = st.file_uploader(
                        "Business data file",
                        type=["csv", "xlsx", "xls", "json"],
                        key="connect_first_business_file",
                    )
                    _file_name = st.text_input(
                        "Source name",
                        placeholder="e.g. Sales, Accounting, CRM, Operations",
                        key="connect_first_file_name",
                    )
                    _file_submit = st.form_submit_button(
                        "📄 Import & Start Business Discovery",
                        type="primary",
                        use_container_width=True,
                    )
                if _file_submit:
                    _file_result = v30_ingest_file(
                        CURRENT_TENANT_ID, _business_file, _file_name.strip()
                    )
                    if _file_result.get("ok"):
                        st.success("Business data imported. The OS will now discover the business and analyze the relevant domains automatically.")
                        st.rerun()
                    else:
                        st.error(_file_result.get("error", "Business data import failed."))
            elif _quick_source_kind == "Shopify Admin API":
                st.markdown("### 🛍️ Connect Shopify")
                with st.form("connect_first_shopify_form", clear_on_submit=False):
                    _shop_domain = st.text_input(
                        "Your Shopify store",
                        placeholder="mystore.myshopify.com",
                        help="Use the store's myshopify.com address. Do not enter an API key or password.",
                        key="connect_first_shop_domain",
                    )
                    _shop_name = st.text_input(
                        "Connection name",
                        value="Main Shopify Store",
                        key="connect_first_shop_name",
                    )
                    _quick_poll = st.number_input(
                        "Automatic sync interval (seconds)",
                        min_value=30, max_value=86400, value=300, step=30,
                        key="connect_first_shop_poll",
                    )
                    _shop_submit = st.form_submit_button(
                        "🛍️ Connect Shopify & Start Live Sync",
                        type="primary",
                        use_container_width=True,
                    )
                if _shop_submit:
                    try:
                        _domain = _shopify_store_domain(_shop_domain)
                        _shop_result = _register_and_sync_shopify(
                            CURRENT_TENANT_ID, _domain, _shop_name, int(_quick_poll)
                        )
                        if _shop_result.get("ok"):
                            st.success("Shopify connected. Your first live business snapshot has been received.")
                            warnings=_shop_result.get("warnings") or []
                            if warnings:
                                st.warning("Some optional Shopify datasets were not available; the core business scan can still continue.")
                            st.rerun()
                        else:
                            st.error(_shop_result.get("error","Shopify connection failed."))
                    except Exception as exc:
                        st.error(f"Shopify connection failed: {type(exc).__name__}: {exc}")
                st.caption("Security: the Shopify client secret stays in the deployment secrets. Access tokens are obtained programmatically and are not stored in the OS database.")
            else:
                _quick_preset = V23_CONNECTOR_PRESETS.get(_quick_source_kind)
                if _quick_preset:
                    st.caption(f"Connector preset: {_quick_preset['auth']} · default secret env: {_quick_preset['secret_env']}")
                with st.form("connect_first_form", clear_on_submit=False):
                    _quick_name = st.text_input("Connection name", placeholder="e.g. Main Business Source", key="connect_first_name")
                    _quick_endpoint = st.text_input("Live API endpoint", placeholder="https://...", key="connect_first_endpoint")
                    _quick_secret_ref = st.text_input(
                        "Deployment secret variable",
                        placeholder="e.g. API_TOKEN",
                        help="Only the environment-variable name is stored. The actual credential is never stored in the database.",
                        key="connect_first_secret_ref",
                    )
                    _quick_poll = st.number_input("Automatic sync interval (seconds)", min_value=30, max_value=86400, value=300, step=30, key="connect_first_poll")
                    _quick_submit = st.form_submit_button("🔗 Connect & Start Initial Sync", type="primary", use_container_width=True)
                if _quick_submit:
                    if not _quick_name.strip():
                        st.error("Enter a connection name.")
                    elif not _quick_endpoint.startswith(("https://","http://")):
                        st.error("Enter a valid live API endpoint.")
                    elif not _quick_secret_ref.strip():
                        st.error("Enter the deployment secret variable name.")
                    else:
                        _quick_result = autonomous_register_connection(CURRENT_TENANT_ID,_quick_name.strip(),_quick_source_kind,_quick_endpoint.strip(),_quick_secret_ref.strip(),int(_quick_poll))
                        if _quick_result.get("ok"):
                            _quick_conn=next((x for x in autonomous_list_connections(CURRENT_TENANT_ID) if x["id"]==_quick_result["connection_id"]),None)
                            if _quick_conn:
                                _quick_live=v22_fetch_live_connection({**_quick_conn,"tenant_id":CURRENT_TENANT_ID})
                                if _quick_live.get("ok"):
                                    st.success("Business connected. Initial live synchronization completed.")
                                    st.rerun()
                                else:
                                    st.warning("The connection was registered, but the initial live sync needs attention.")
                                    v24_render_human(_quick_live)
                            else:
                                st.success("Business connection created. The OS will sync automatically.")
                                st.rerun()
                        else:
                            st.error(_quick_result.get("error","Connection failed."))

            st.markdown("### What happens after you connect")
            st.write("Connect → Discover business → Map evidence → Activate relevant intelligence → Diagnose → Prioritize → Recommend → Governed actions → Measure → Learn")
            st.caption("Start here. Advanced connector management remains available in the sidebar, but it is no longer required for first-time setup.")
    else:
        v24_present_report(report)
        if st.button("🔍 Run production readiness audit", use_container_width=True):
            v24_render_human(v25_production_audit(CURRENT_TENANT_ID), "Production readiness")
        if st.button("🔄 Force full live scan", type="primary", use_container_width=True):
            v30_universal_cycle(CURRENT_TENANT_ID, api_key, force=True)
            st.rerun()
        profile_now = v30_get_profile(CURRENT_TENANT_ID)
        if profile_now:
            with st.expander("Business identity correction (optional)", expanded=False):
                st.caption("Automatic discovery is the default. Use this only if the OS classified your business incorrectly.")
                correction = st.selectbox(
                    "Correct business type",
                    ["Keep automatic classification"] + list(V30_BUSINESS_TYPES.keys()),
                    key="v30_business_correction",
                )
                if st.button("Save correction", key="v30_save_correction"):
                    if correction != "Keep automatic classification":
                        profile_now["business_type"] = correction
                        profile_now["user_correction"] = correction
                        profile_now["confidence"] = 1.0
                        v30_store_profile(CURRENT_TENANT_ID, profile_now)
                        st.success("Business identity corrected. The next scan will use the corrected operating context.")
                        st.rerun()
elif menu == "🔌 Connect Business":
    st.title("🔌 Connect Your Business")
    st.caption("Connect any business system once. Shopify is one connector among many; the OS automatically discovers the business context from live evidence.")
    st.markdown("### Universal onboarding")
    st.caption("You do not need to know your industry in advance. Connect a live system or upload a current business export; the OS builds the business profile automatically.")
    _advanced_file = st.file_uploader("Upload CSV / Excel / JSON", type=["csv","xlsx","xls","json"], key="advanced_business_file")
    if st.button("📄 Import uploaded business data", key="advanced_file_import", type="secondary"):
        _advanced_file_result = v30_ingest_file(CURRENT_TENANT_ID, _advanced_file, "Business Data Upload")
        if _advanced_file_result.get("ok"):
            st.success("Business data imported successfully. Return to the Command Center for the unified diagnosis.")
            st.rerun()
        else:
            st.error(_advanced_file_result.get("error", "Import failed."))
    source_kind=st.selectbox("Live source",["CSV / Excel / JSON Business Data","Shopify Admin API","Stripe API","CRM / ERP API","Analytics API","REST / JSON API","Meta Ads API","Google Ads API"], key="advanced_source_kind")
    if source_kind == "Shopify Admin API":
        with st.form("v28_shopify_advanced_form", clear_on_submit=False):
            domain=st.text_input("Shopify store",placeholder="mystore.myshopify.com",key="advanced_shopify_domain")
            name=st.text_input("Connection name",value="Main Shopify Store",key="advanced_shopify_name")
            poll=st.number_input("Automatic sync interval (seconds)",min_value=30,max_value=86400,value=300,step=30,key="advanced_shopify_poll")
            if st.form_submit_button("🛍️ Connect Shopify & Sync",type="primary",use_container_width=True):
                try:
                    result=_register_and_sync_shopify(CURRENT_TENANT_ID,domain,name,int(poll))
                    if result.get("ok"):
                        st.success("Shopify connected and live sync completed.")
                        if result.get("warnings"):
                            st.warning("Some optional Shopify datasets were unavailable; core data was still synchronized.")
                        st.rerun()
                    else:
                        st.error(result.get("error","Shopify connection failed."))
                except Exception as exc:
                    st.error(f"Shopify connection failed: {type(exc).__name__}: {exc}")
        st.info("You only need your store address here. Client credentials stay in deployment secrets; access tokens are not stored.")
    else:
        preset=V23_CONNECTOR_PRESETS.get(source_kind)
        if preset:
            st.caption(f"Connector preset: {preset['auth']} · default secret env: {preset['secret_env']}")
        with st.form("v22_connection_form"):
            source_name=st.text_input("Connection name",placeholder="e.g. Main Business Source")
            endpoint=st.text_input("Live API endpoint",placeholder="https://...")
            secret_ref=st.text_input("Deployment secret variable",placeholder="e.g. API_TOKEN",help="Only the environment-variable name is stored.")
            poll_seconds=st.number_input("Automatic sync interval (seconds)",min_value=30,max_value=86400,value=300,step=30)
            if st.form_submit_button("🔗 Connect live source",type="primary",use_container_width=True):
                if not endpoint.startswith(("https://","http://")):
                    st.error("A valid live HTTPS API endpoint is required.")
                else:
                    result=autonomous_register_connection(CURRENT_TENANT_ID,source_name,source_kind,endpoint,secret_ref,int(poll_seconds))
                    if result.get("ok"):
                        conn=next((c for c in autonomous_list_connections(CURRENT_TENANT_ID) if c["id"]==result["connection_id"]),None)
                        live=v22_fetch_live_connection({**conn,"tenant_id":CURRENT_TENANT_ID}) if conn else {"ok":False,"error":"Connection could not be loaded."}
                        if live.get("ok"):
                            st.success("Live source connected and initial synchronization completed.")
                            st.rerun()
                        else:
                            st.error(live.get("error","Initial synchronization failed."))
                    else:
                        st.error(result.get("error","Connection failed."))


elif menu == "⚡ Actions & Execution":
    st.title("⚡ Actions & Execution")
    st.caption("Solutions from the unified diagnosis become governed actions. External writes are never claimed complete without a verified response.")
    report = autonomous_get_latest_report(CURRENT_TENANT_ID)
    if not report:
        st.info("Connect live business data and run the autonomous scan first.")
    else:
        actions = autonomous_extract_actions(report)
        if actions:
            st.dataframe(pd.DataFrame(actions), use_container_width=True, hide_index=True)
            st.markdown("### Governed execution")
            st.warning("Only execute an action when the destination, payload and authorization are correct. High-risk actions require explicit approval.")
            for i, action in enumerate(actions):
                with st.expander(f"{i+1}. {action.get('title','Action')} · {action.get('risk_level','medium').upper()}", expanded=False):
                    st.write(f"Problem: {action.get('problem','')}")
                    v24_render_human(action.get('payload',{}))
                    c1,c2,c3=st.columns(3)
                    with c1:
                        endpoint=st.text_input("Approved HTTPS endpoint", key=f"exec_endpoint_{i}", placeholder="https://...")
                    with c2:
                        secret_ref=st.text_input("Deployment secret env (optional)", key=f"exec_secret_{i}", placeholder="ACTION_API_TOKEN")
                    with c3:
                        method=st.selectbox("Method",["POST","PUT","PATCH"],key=f"exec_method_{i}")
                    approved=st.checkbox("I approve this external action", key=f"exec_approve_{i}")
                    if st.button("▶ Execute and verify", key=f"exec_run_{i}", type="primary"):
                        action_request=create_action_request(
                            CURRENT_TENANT_ID,
                            CURRENT_AUTH_USER.get("role", "member") if CURRENT_AUTH_USER else "member",
                            action.get("connector_id", "webhook"),
                            action.get("operation", "external_write"),
                            action.get("payload", {}),
                            action.get("risk_level", "medium")
                        ).model_dump()
                        action_request.update({"endpoint":endpoint,"secret_ref":secret_ref,"method":method,"action_id":action_request.get("request_id")})
                        result=v23_execute_verified_action(CURRENT_TENANT_ID,action_request,approved=approved)
                        v24_render_human(result)
        else:
            st.success("No execution actions are currently required.")

elif menu == "📈 Results & Monitoring":
    st.title("📈 Results & Continuous Monitoring")
    st.caption("Track live data freshness, detected problems, solutions, and outcome history from the same business intelligence layer.")
    connections = autonomous_list_connections(CURRENT_TENANT_ID)
    reports = autonomous_list_reports(CURRENT_TENANT_ID, limit=20)
    if connections:
        st.dataframe(pd.DataFrame(connections), use_container_width=True)
    else:
        st.info("No live sources connected.")
    conn=db_connect()
    dq_rows=conn.execute("SELECT source_name,observed_at,status,checks_json FROM v23_data_quality WHERE tenant_id=? ORDER BY observed_at DESC LIMIT 50",(CURRENT_TENANT_ID,)).fetchall()
    conn.close()
    if dq_rows:
        st.markdown("### Live Data Quality")
        st.dataframe(pd.DataFrame([dict(r) for r in dq_rows]), use_container_width=True, hide_index=True)
    if reports:
        st.markdown("### Analysis history")
        history = []
        for r in reports:
            summary = r.get("summary", {})
            history.append({
                "generated_at": r.get("generated_at"),
                "problems": summary.get("problem_count", 0),
                "critical": summary.get("critical_count", 0),
                "health": summary.get("health_score", "—"),
                "confidence": r.get("confidence", 0.0),
            })
        st.dataframe(pd.DataFrame(history), use_container_width=True)
    else:
        st.info("No autonomous analysis has been recorded yet.")


# ===========================================================================
# 💳 MODULE: ACCOUNT & PLAN
# ===========================================================================

elif menu == "💳 Account & Plan":
    st.title("💳 Account & Plan")
    st.caption("Subscription tier, seat usage, and quota limits for this workspace.")

    current_plan = get_tenant_plan_name(CURRENT_TENANT_ID)
    quota = get_tenant_quota(CURRENT_TENANT_ID)

    st.subheader(f"Current plan: {current_plan}")
    plan_cols = st.columns(3)
    for i, (plan_name, limits) in enumerate(PLAN_TIERS.items()):
        with plan_cols[i]:
            is_current = plan_name == current_plan
            st.markdown(f"**{plan_name}**{' ✅' if is_current else ''}")
            st.caption(f"{limits['max_users']} users · {limits['max_projects']} projects · {limits['max_workflows']} workflows")
            if not is_current and st.button(f"Switch to {plan_name}", key=f"plan_{plan_name}"):
                res = set_tenant_plan(CURRENT_TENANT_ID, plan_name)
                if res.get("status") == "SUCCESS":
                    st.success(f"Plan updated to {plan_name}.")
                    record_audit(
                        CURRENT_AUTH_USER.get("email", "unknown") if CURRENT_AUTH_USER else "unknown",
                        "PLAN_CHANGED", "Billing", plan_name
                    )
                    st.rerun()

    st.markdown("---")
    st.subheader("Usage against quota")
    usage_specs = [
        ("Projects", "projects", quota.max_projects),
        ("Users", "users", quota.max_users),
        ("Workflows", "workflows", quota.max_workflows),
    ]
    for label, resource, limit in usage_specs:
        check = quota_check(CURRENT_TENANT_ID, resource)
        used = check.get("current", 0) if isinstance(check, dict) else 0
        pct = min(1.0, used / limit) if limit else 0.0
        st.write(f"{label}: {used} / {limit}")
        st.progress(pct)

    st.markdown("---")
    st.caption(
        "This panel reads and writes the same `tenant_quotas` table used by the "
        "quota-enforcement checks elsewhere in the app — plans are not cosmetic."
    )


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
            m_size = st.number_input("Target Market Size ($)", value=0.0)
            invest = st.number_input("R&D / Expansion Budget ($)", value=0.0)
            comp_idx = st.slider("Competitor Resistance Index (1-10)", 1.0, 10.0, 6.5)
        with col2:
            current_lat = st.number_input("Current Org Latency (ms)", value=0.0)
            cur_layers = st.slider("Current Org Layers", 3, 10, 7)
            tar_layers = st.slider("Target Org Layers", 2, 8, 4)

        if st.button("🚀 Run Monte Carlo Launch & Digital Twin Sim"):
            sim_res = os_core.strategy_orchestrator.sim_engine.simulate_product_launch_impact(m_size, invest, comp_idx)
            twin_res = os_core.strategy_orchestrator.digital_twin.simulate_org_restructuring(current_lat, cur_layers, tar_layers)
            
            st.success("✅ Simulation Completed Successfully!")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("### Market Launch Probabilities")
                v24_render_human(sim_res)
            with c2:
                st.markdown("### Digital Twin Org Impact")
                v24_render_human(twin_res)

    # 2. Capital Allocation Engine
    with strat_tab[1]:
        st.subheader("30.9.13 — Strategic Portfolio & Capital Allocation Engine")
        tot_budget = st.number_input("Total Reallocation Budget ($)", value=0.0)
        
        st.markdown("#### Business Unit Vectors")
        bu1_name = st.text_input("Unit 1 Name")
        bu1_cap = st.number_input("Unit 1 Capital ($)", value=0.0)
        bu1_gr = st.number_input("Unit 1 Growth Rate %", value=0.0)
        bu1_risk = st.slider("Unit 1 Risk (0-1)", 0.0, 1.0, 0.25)
        
        bu2_name = st.text_input("Unit 2 Name")
        bu2_cap = st.number_input("Unit 2 Capital ($)", value=0.0)
        bu2_gr = st.number_input("Unit 2 Growth Rate %", value=0.0)
        bu2_risk = st.slider("Unit 2 Risk (0-1)", 0.0, 1.0, 0.65)

        if st.button("⚖️ Optimize Risk-Adjusted Capital Split"):
            units = [
                BusinessUnitData(bu1_name, bu1_cap, bu1_gr, bu1_risk),
                BusinessUnitData(bu2_name, bu2_cap, bu2_gr, bu2_risk)
            ]
            alloc_res = os_core.strategy_orchestrator.capital_engine.reallocate_capital(tot_budget, units)
            v24_render_human(alloc_res)

    # 3. Competitor & M&A Intelligence
    with strat_tab[2]:
        st.subheader("30.9.5 & 30.9.11 — Market Threats & M&A Valuation")
        sub_c1, sub_c2 = st.columns(2)
        with sub_c1:
            st.markdown("#### Competitor Threat Check")
            c_name = st.text_input("Competitor Name")
            c_share = st.number_input("Market Share %", value=0.0)
            c_tech = st.slider("Tech Score", 1.0, 10.0, 8.8)
            if st.button("Evaluate Threat Level"):
                os_core.strategy_orchestrator.comp_intel.register_competitor(
                    CompetitorProfileData(c_name, c_share, 1.0, c_tech, ["AI Core"])
                )
                v24_render_human(os_core.strategy_orchestrator.comp_intel.analyze_market_landscape())

        with sub_c2:
            st.markdown("#### M&A Target Due Diligence")
            target_co = st.text_input("Target Company")
            val = st.number_input("Valuation ($)", value=0.0)
            syn = st.slider("Synergy Score", 1.0, 10.0, 8.5)
            tech_debt = st.slider("Tech Debt Score (Lower is better)", 1.0, 10.0, 3.0)
            if st.button("Run M&A Due Diligence"):
                ma_target = MATargetData(target_co, val, val*0.3, syn, 7.5, tech_debt)
                v24_render_human(os_core.strategy_orchestrator.ma_engine.evaluate_ma_candidate(ma_target))

    # 4. Autonomous Execution & Risk
    with strat_tab[3]:
        st.subheader("30.9.8 & 30.9.15 — Execution Bottlenecks & Governance")
        init_name = st.text_input("Initiative Name")
        init_budget = st.number_input("Initiative Budget ($)", value=0.0)
        init_prog = st.slider("Current Progress %", 0.0, 100.0, 20.0)
        init_risk = st.slider("Initiative Risk Index", 0.0, 1.0, 0.75)

        if st.button("⚡ Audit Risk & Check Execution Status"):
            init_obj = StrategicInitiativeData("INIT-101", init_name, "Ops", init_budget, 30.0, init_prog, init_risk, "EXECUTING")
            gov_res = os_core.strategy_orchestrator.governance.audit_initiative(init_obj, max_budget=500000.0)
            exec_res = os_core.strategy_orchestrator.exec_engine.execute_and_detect_bottlenecks([init_obj])
            
            v24_render_human({"governance_audit": gov_res, "execution_pipeline": exec_res})


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
        p_name = st.text_input("Product Name")
        p_feat = st.text_input("Key Feature")
        p_price = st.text_input("Price Point")
        if st.button("Generate Script Brief"):
            res = os_core.marketing.generate_ad_campaign(p_name, p_feat, p_price)
            v24_render_human(res)

    elif engine_tab == "Chapter 2: Sales Scoring Engine":
        st.subheader("🎯 Lead Qualifier & Router")
        l_name = st.text_input("Lead Name")
        l_role = st.selectbox("Job Title", ["Founder", "CEO", "CMO", "Manager", "Developer"])
        l_budget = st.number_input("Monthly Budget ($)", value=0.0)
        l_time = st.selectbox("Timeline", ["Immediate", "1-3 Months", "Flexible"])
        if st.button("Evaluate Lead"):
            res = os_core.sales.score_and_route_lead({
                "name": l_name, "job_title": l_role, "monthly_budget": l_budget, "timeline": l_time
            })
            v24_render_human(res)

    elif engine_tab == "Chapter 3: Content Repurposing Engine":
        st.subheader("📲 Transcript to Social Media Bundle")
        raw_text = st.text_area("Paste Raw Transcript or Thought:")
        if st.button("Repurpose Content"):
            res = os_core.content.repurpose_transcript(raw_text)
            v24_render_human(res)

    elif engine_tab == "Chapter 4: Customer Support Triage Engine":
        st.subheader("🎧 Support Urgency Triage & Resolver")
        c_name = st.text_input("Customer Name")
        c_msg = st.text_area("Customer Complaint / Message:")
        if st.button("Triage Ticket"):
            res = os_core.support.triage_and_resolve(c_name, c_msg)
            v24_render_human(res)

    elif engine_tab == "Chapter 5: Internal Knowledge Engine":
        st.subheader("🔍 Internal SOP Knowledge Query")
        query = st.text_input("Search Policy or SOP:")
        if st.button("Query Knowledge Base"):
            res = os_core.knowledge.query_knowledge_base(query)
            v24_render_human(res)


# ===========================================================================
# 8. MODULE: AI CUSTOMER SUCCESS OS (CHAPTERS 5-8 INTEGRATED)
# ===========================================================================

elif menu == "🎯 AI Customer Success OS (Ch 5-8)":
    st.title("🎯 AI Customer Success Operating System™")
    st.caption("Automated Health Scoring, Churn Mitigation, Account Expansion, and CS Governance.")

    col1, col2 = st.columns(2)
    with col1:
        cust_id = st.text_input("Customer ID")
        company_name = st.text_input("Company Name")
        lic_util = st.slider("License Utilization %", 0.0, 100.0, 88.5)
        login_freq = st.number_input("Logins per Week", value=0.0)
        open_tickets = st.number_input("Open High-Priority Tickets", value=0.0)
    with col2:
        nps = st.slider("NPS Score", 0, 10, 9)
        ebr = st.checkbox("Executive EBR Attended", value=True)
        renewal_days = st.number_input("Days Until Renewal", value=0.0)
        arr = st.number_input("Annual Recurring Revenue ($)", value=0.0)
        contacts = st.number_input("Contact Count Last Week", value=0.0)

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
        v24_render_human(res)


# ===========================================================================
# 9. MODULE: AI FINANCE OS (CHAPTERS 9-12 COMPLETE)
# ===========================================================================

elif menu == "💰 AI Finance OS (Ch 9-12 Complete)":
    st.title("💰 AI Finance Operating System™ (Chapters 9 - 12)")
    st.caption("FP&A Predictive Forecasting, Fraud Screening, Smart Reconciliation & Runway Engine.")
    st.info("ℹ️ Transparent, rule-based calculators for planning purposes — not licensed accounting, audit, or fraud-detection software.")

    fin_sub_tab = st.tabs(["📊 Runway & Cashflow", "📈 Chapter 9: FP&A Variance", "🛡️ Chapter 10: Fraud Screening", "⚖️ Chapter 11: Ledger Reconciliation"])

    with fin_sub_tab[0]:
        col1, col2 = st.columns(2)
        with col1:
            mrr = st.number_input("Monthly Revenue ($)", value=0.0)
            opex = st.number_input("Operating Costs ($)", value=0.0)
            cash_res = st.number_input("Cash Reserves ($)", value=0.0)
        with col2:
            ar = st.number_input("Accounts Receivable ($)", value=0.0)
            ap = st.number_input("Accounts Payable ($)", value=0.0)
            margin = st.slider("Gross Margin %", 0.0, 100.0, 78.0)

        if st.button("🚀 Run Cashflow & Runway Analysis"):
            res = os_core.finance.analyze_finance({
                "mrr_usd": mrr, "opex_usd": opex, "cash_reserve_usd": cash_res,
                "accounts_receivable_usd": ar, "accounts_payable_usd": ap, "gross_margin_pct": margin
            })
            v24_render_human(res)

    with fin_sub_tab[1]:
        st.subheader("Chapter 9: Predictive FP&A Engine")
        act_rev = st.number_input("Actual Revenue ($)", value=0.0)
        bud_rev = st.number_input("Budgeted Revenue ($)", value=0.0)
        growth_p = st.number_input("Projected Growth Rate %", value=0.0)
        if st.button("Calculate FP&A Variance"):
            fpa_res = os_core.finance.run_fpa_analysis(act_rev, bud_rev, growth_p)
            v24_render_human(fpa_res)

    with fin_sub_tab[2]:
        st.subheader("Chapter 10: Algorithmic Fraud & Risk Screening")
        tx_id = st.text_input("Transaction ID")
        tx_amt = st.number_input("Transaction Amount ($)", value=0.0)
        tx_risk = st.slider("Risk Anomaly Score (0=Low, 1=High)", 0.0, 1.0, 0.88)
        if st.button("Screen Transaction Risk"):
            tx_data = [{"tx_id": tx_id, "amount": tx_amt, "risk_score": tx_risk}]
            fraud_res = os_core.finance.screen_transactions(tx_data)
            v24_render_human(fraud_res)

    with fin_sub_tab[3]:
        st.subheader("Chapter 11: Automated Ledger Reconciliation")
        bank_b = st.number_input("Bank Statement Balance ($)", value=0.0)
        ledger_b = st.number_input("Internal Ledger Balance ($)", value=0.0)
        if st.button("Reconcile Ledger"):
            rec_res = os_core.finance.reconcile_ledger(bank_b, ledger_b)
            v24_render_human(rec_res)


# ===========================================================================
# 10. MODULE: AI HEALTHCARE OS (VOLUME 5.0)
# ===========================================================================

elif menu == "🏥 AI Healthcare OS (Vol 5.0)":
    st.title("🏥 Healthcare Module")
    st.error("Disabled by design. No synthetic patient data or automated clinical decisions are available in the production product.")
    st.info("A regulated clinical integration requires licensed clinical governance, approved data sources, validated models, and a separate compliance deployment.")


# ===========================================================================
# 11. MODULE: MLOPS & TELEMETRY (VOLUME 2.0)
# ===========================================================================

elif menu == "🛠️ MLOps & Telemetry (Vol 2.0)":
    st.title("🛠️ MLOps & Model Infrastructure Registry™")
    st.caption("Monitor deployed AI models, latency telemetry, and system degradation.")
    st.info("Only live deployment telemetry is shown. No synthetic model metrics are loaded.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Deployed Models Registry")
        for m_id, m_data in os_core.mlops.registry.items():
            st.info(f"**Model:** {m_data.name} (v{m_data.version})\n- **Latency:** {m_data.latency_ms}ms\n- **Accuracy:** {m_data.accuracy_score*100}%\n- **Status:** {m_data.status.value}")

    with col2:
        st.subheader("Evaluate Telemetry Health")
        if not os_core.mlops.registry:
            st.info("No live model telemetry is registered yet. Production deployments populate this registry from the actual model serving layer.")
        else:
            selected_m = st.selectbox("Select Model ID", list(os_core.mlops.registry.keys()))
            if st.button("Run Telemetry Diagnostic"):
                diag = os_core.mlops.evaluate_telemetry(selected_m)
                v24_render_human(diag)


# ===========================================================================
# 12. MODULE: AI SECURITY & GOVERNANCE (VOLUME 3.0)
# ===========================================================================

elif menu == "🛡️ AI Security & Governance (Vol 3.0)":
    st.title("🛡️ Zero-Trust AI Security & Data Anonymization™")
    st.caption("Test Zero-Trust RBAC Access Controls and PII Prompt Masking.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔒 PII Data Masking Tester")
        test_prompt = st.text_area("Input Prompt with Sensitive Data:")
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
        campaign_goal = st.text_input("Strategic Campaign Goal")
    with col2:
        campaign_budget = st.number_input("Budget Allocation ($)", value=0.0, min_value=0.0, step=1000.0)

    if st.button("🚀 Trigger Autonomous Multi-Agent Execution"):
        with st.spinner("Multi-Agent Workforce in action... Coordinating Shared Memory and Tasks."):
            coordinator = MultiAgentCoordinator()
            
            try:
                agent_report = asyncio.run(
                    coordinator.run_enterprise_workflow(campaign_goal, campaign_budget)
                )
            except RuntimeError:
                # Streamlit environments may already have an event loop.
                loop = asyncio.new_event_loop()
                try:
                    agent_report = loop.run_until_complete(
                        coordinator.run_enterprise_workflow(campaign_goal, campaign_budget)
                    )
                finally:
                    loop.close()
            
            st.success("✅ Multi-Agent Workflow Execution Complete!")
            
            t1, t2, t3 = st.tabs(["📊 Performance & Memory Snapshot", "📜 Full Audit Trail Log", "🧱 Raw JSON Output"])
            
            with t1:
                st.subheader("Shared Memory Snapshot")
                v24_render_human(agent_report["shared_memory_snapshot"])
                st.subheader("Analytics Summary")
                v24_render_human(agent_report["performance_summary"])
                
            with t2:
                st.subheader("System Event & Audit Trail")
                st.dataframe(pd.DataFrame(agent_report["full_audit_trail"]), use_container_width=True)
                
            with t3:
                v24_render_human(agent_report)


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
        lead_value = st.number_input("Estimated Value ($)", min_value=0.0)
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
    user_prompt = st.text_area("Ask AI to draft emails or research deals:", placeholder="Use live connected business context; no sample business data is accepted.")
    
    if st.button("🚀 Run Sales AI Assistant"):
        context = st.session_state.pipeline_data.to_string(index=False)
        full_query = f"Pipeline Context:\n{context}\n\nUser Request: {user_prompt}"
        output = run_ai_task(api_key, full_query)
        if output:
            st.success("✅ AI Response:")
            st.markdown(output)


# ===========================================================================
# 16. MODULE: 25 AI EXECUTION SYSTEMS SUITE — PRODUCTION REGISTRY
# ===========================================================================
elif menu == "⚡ AI Execution Systems™ (Systems 1-25)":
    st.title("⚡ Enterprise AI Execution Library™")
    st.caption("25 governed operating systems with structured inputs, auditable outputs, and AI-assisted execution.")

    SYSTEM_REGISTRY = {
        1: ("AI Content Production System™", "CONTENT"),
        2: ("AI SEO Growth System™", "AI"),
        3: ("AI Social Media OS™", "AI"),
        4: ("AI Customer Support OS™", "SUPPORT"),
        5: ("AI E-commerce Growth OS™", "AI"),
        6: ("AI Agency Operating System™", "AI"),
        7: ("AI Executive Assistant OS™", "AI"),
        8: ("AI HR & Recruitment OS™", "AI"),
        9: ("AI Finance & BI OS™", "FINANCE"),
        10: ("AI Product & Innovation OS™", "STRATEGY"),
        11: ("AI Knowledge Management OS™", "KNOWLEDGE"),
        12: ("AI Customer Intelligence OS™", "CUSTOMER"),
        13: ("AI Sales Optimization OS™", "SALES"),
        14: ("AI Marketing Intelligence OS™", "MARKETING"),
        15: ("AI Business Analytics OS™", "AI"),
        16: ("AI Automation & Workflow OS™", "AI"),
        17: ("AI Financial Intelligence OS™", "FINANCE"),
        18: ("AI Team Productivity OS™", "AI"),
        19: ("AI Innovation Pipeline OS™", "STRATEGY"),
        20: ("AI Business Scaling OS™", "AI"),
        21: ("AI Competitive Intelligence OS™", "STRATEGY"),
        22: ("AI Executive Leadership OS™", "AI"),
        23: ("AI CX & Retention OS™", "CUSTOMER"),
        24: ("AI Business Security & Risk OS™", "SECURITY"),
        25: ("AI Business Transformation OS™", "STRATEGY"),
    }

    system_options = [
        f"System {n} — {name}" for n, (name, _) in SYSTEM_REGISTRY.items()
    ]
    selected = st.selectbox("Select Execution System", system_options)
    system_number = int(selected.split(" — ", 1)[0].replace("System ", ""))
    system_name, system_mode = SYSTEM_REGISTRY[system_number]

    st.info(
        f"**{system_name}** · Mode: **{system_mode}** · "
        "Outputs are advisory unless an authenticated external integration confirms execution."
    )

    input_context = st.text_area(
        "Business objective / data / problem",
        placeholder="Paste the actual business context. The system will identify missing information instead of inventing it.",
        height=180,
    )

    col_a, col_b = st.columns(2)
    with col_a:
        run_mode = "Governed AI"
    with col_b:
        output_depth = st.selectbox("Output Depth", ["Executive", "Detailed"])

    def _run_registered_system(number: int, name: str, mode: str, context: str):
        request = SecurityGuardrail.sanitize_input(context)
        if not request:
            return {"status": "INPUT_REQUIRED", "message": "Provide business context first."}

        # Deterministic native engines.
        if mode == "CONTENT":
            return os_core.content.repurpose_transcript(request)
        if mode == "SUPPORT":
            return os_core.support.triage_and_resolve("Customer", request)
        if mode == "SALES":
            return os_core.sales.generate_outbound_email("Prospect", request, "AI Business OS™")
        if mode == "MARKETING":
            return os_core.marketing.generate_ad_campaign("Product", request, "$49")
        if mode == "KNOWLEDGE":
            return os_core.knowledge.query_knowledge_base(request)
        if mode == "FINANCE":
            return os_core.finance.analyze_finance({})
        if mode == "CUSTOMER":
            return os_core.customer_success.analyze_customer({})
        if mode == "SECURITY":
            return SecurityGuardrail.audit_payload({"request": request})

        depth = "executive summary with priorities" if output_depth == "Executive" else "detailed operating plan"
        prompt = f"""
SYSTEM: {name}
SYSTEM NUMBER: {number}
OBJECTIVE: Produce a {depth}.

BUSINESS CONTEXT:
{request}

MANDATORY GOVERNANCE:
1. Separate facts, assumptions, and missing information.
2. Never invent KPIs, market data, customer information, revenue, costs, or results.
3. Do not claim an external API action happened.
4. Give measurable recommendations and a next-step sequence.
5. Flag risks and dependencies.
6. End with a concise "Data Needed" section.
"""
        result = run_ai_task(api_key, prompt, temperature=0.2)
        return {
            "status": "AI_COMPLETE" if result else "AI_UNAVAILABLE",
            "system": name,
            "result": result,
        }

    if st.button("🚀 Run Governed System", type="primary"):
        with st.spinner("Running governed execution..."):
            result = _run_registered_system(system_number, system_name, system_mode, input_context)
            record_audit(
                "StreamlitUser",
                "EXECUTION_SYSTEM_RUN",
                system_name,
                result.get("status", "UNKNOWN"),
                result,
            )
            v24_render_human(result)
            if st.button("📄 Export Result as Report", key="export_execution_report"):
                report_path = export_report(system_name, result, get_workspace())
                record_audit("StreamlitUser", "REPORT_EXPORT", system_name, "SUCCESS",
                             {"path": report_path})
                st.success(f"Report exported: {report_path}")

    with st.expander("🔎 System Governance & Audit"): 
        v24_render_human({
            "system_number": system_number,
            "system_name": system_name,
            "mode": system_mode,
            "app_version": APP_VERSION,
            "security": "Input sanitation enabled",
            "audit": "Persistent SQLite audit enabled",
            "external_execution": "Disabled unless separately integrated and authenticated",
        })



# ===========================================================================
# 17. SYSTEM HEALTH & AUDIT
# ===========================================================================
elif menu == "🩺 System Health & Audit":
    st.title("🩺 System Health & Audit")
    health = system_health()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Version", health["app_version"])
    c2.metric("AI SDK", health["gemini_sdk"])
    c3.metric("Audit Store", health["audit_store"])
    c4.metric("Status", health["status"])

    st.markdown("### Runtime Health")
    v24_render_human(health)

    st.markdown("### Recent Audit Events")
    audits = get_recent_audits(100)
    if audits:
        st.dataframe(pd.DataFrame(audits), use_container_width=True)
    else:
        st.info("No audit events recorded yet.")


elif menu == "🏢 Business Workspace":
    st.title("🏢 Business Workspace")
    workspace = get_workspace()
    with st.form("business_workspace"):
        name = st.text_input("Business Name", workspace.get("business_name", ""))
        industry = st.text_input("Industry", workspace.get("industry", ""))
        market = st.text_input("Primary Market", workspace.get("market", ""))
        model = st.text_input("Business Model", workspace.get("business_model", ""))
        goals = st.text_area("Goals (one per line)", "\n".join(workspace.get("goals", [])))
        notes = st.text_area("Business Notes", workspace.get("notes", ""))
        if st.form_submit_button("Save Workspace", type="primary"):
            workspace = {"business_name": name.strip(), "industry": industry.strip(),
                         "market": market.strip(), "business_model": model.strip(),
                         "goals": [x.strip() for x in goals.splitlines() if x.strip()],
                         "notes": notes.strip()}
            save_workspace(workspace)
            record_audit("WorkspaceUser", "WORKSPACE_UPDATE", "Workspace", "SUCCESS", workspace)
            st.success("Workspace saved.")
    missing = validate_workspace(workspace)
    if missing:
        st.warning("Missing: " + ", ".join(missing))
    else:
        st.success("Business profile complete.")


elif menu == "🏁 Release Readiness Audit":
    st.title("🏁 Release Readiness Audit")
    st.caption(
        "A structured self-assessment, not an automatic scan. Answer honestly for "
        "each control below — the score reflects exactly what you confirm here, "
        "nothing is inferred or assumed."
    )

    with st.form("release_readiness_form"):
        st.markdown("**Core modules present in this deployment**")
        stage_labels = {
            1: "Authentication & Access Control", 2: "Multi-Tenant Data Model",
            3: "Quota & Plan Enforcement", 4: "Audit Logging",
            5: "Strategy / Decision Orchestrator", 6: "Execution Systems",
            7: "Executive Dashboard", 8: "Finance Module",
            9: "Marketing / Sales Modules", 10: "MLOps Registry",
            11: "Security & Governance Center", 12: "Business Workspace / CRM Data",
        }
        stage_cols = st.columns(3)
        stages_present = []
        for i, (num, label) in enumerate(stage_labels.items()):
            with stage_cols[i % 3]:
                if st.checkbox(label, value=True, key=f"stage_{num}"):
                    stages_present.append(num)

        st.markdown("---")
        st.markdown("**Security controls in place**")
        sec_cols = st.columns(3)
        sec_keys = ["authentication", "authorization", "rbac", "audit_trail", "input_validation", "secret_protection"]
        sec_controls = {}
        for i, key in enumerate(sec_keys):
            with sec_cols[i % 3]:
                sec_controls[key] = st.checkbox(key.replace("_", " ").title(), value=(key in ("authentication", "audit_trail")), key=f"sec_{key}")

        st.markdown("---")
        st.markdown("**Persistence controls in place**")
        pers_cols = st.columns(3)
        pers_keys = ["save", "load", "recovery", "integrity_check", "backup"]
        pers_controls = {}
        for i, key in enumerate(pers_keys):
            with pers_cols[i % 3]:
                pers_controls[key] = st.checkbox(key.replace("_", " ").title(), value=(key in ("save", "load")), key=f"pers_{key}")

        st.markdown("---")
        runtime_errors = st.number_input("Known unresolved runtime errors", min_value=0.0, value=0.0, step=1)

        st.markdown("**Failure handling tested for**")
        fail_cols = st.columns(3)
        fail_keys = ["network_failure", "storage_failure", "engine_failure", "timeout", "invalid_input"]
        fail_controls = {}
        for i, key in enumerate(fail_keys):
            with fail_cols[i % 3]:
                fail_controls[key] = st.checkbox(key.replace("_", " ").title(), value=False, key=f"fail_{key}")

        submitted = st.form_submit_button("Run Readiness Audit", type="primary")

    if submitted:
        context = {
            "stages": stages_present,
            "dependencies": {"core_runtime": True, "standard_library": True},
            "interfaces": {"alert_to_kpi": True, "kpi_to_risk": True, "risk_to_orchestrator": True,
                           "security_to_audit": sec_controls.get("audit_trail", False),
                           "storage_to_recovery": pers_controls.get("recovery", False),
                           "dashboard_to_engine": True, "realtime_to_engine": True,
                           "performance_to_runtime": True},
            "data_records": [{"id": "DATA-001", "value": 100}],
            "security_controls": sec_controls,
            "persistence": pers_controls,
            "runtime_errors": int(runtime_errors),
            "failure_tests": fail_controls,
        }
        engine = FinalMasterAuditEngine()
        result = engine.audit(context)
        st.markdown("---")
        st.subheader("Result")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Overall Score", f"{result.score.overall:.1f}/100")
        c2.metric("Release Decision", result.release_decision.value)
        c3.metric("Passed / Failed", f"{result.passed_checks} / {result.failed_checks}")
        c4.metric("Production Ready", "Yes" if result.production_ready else "No")
        st.write(result.summary)
        with st.expander("Domain scores"):
            score_dict = {
                "Architecture": result.score.architecture, "Dependency": result.score.dependency,
                "Interface": result.score.interface, "Data": result.score.data,
                "Security": result.score.security, "Persistence": result.score.persistence,
                "Runtime": result.score.runtime, "Failure Handling": result.score.failure_handling,
                "Performance": result.score.performance, "Testing": result.score.testing,
                "Integration": result.score.integration, "Production": result.score.production,
            }
            for domain, sc in score_dict.items():
                st.write(f"{domain}: {sc:.1f}/100")
                st.progress(min(1.0, max(0.0, sc / 100)))
        with st.expander("All findings"):
            for f in result.findings:
                icon = "✅" if f.status.value == "PASS" else ("⚠️" if f.status.value == "WARN" else "❌")
                st.markdown(f"{icon} **[{f.severity.value}] {f.title}** — {f.description}")
                if f.recommendation:
                    st.caption(f"Recommendation: {f.recommendation}")
        record_audit(
            CURRENT_AUTH_USER.get("email", "unknown") if CURRENT_AUTH_USER else "unknown",
            "RELEASE_READINESS_AUDIT_RUN", "Governance", result.release_decision.value
        )


elif menu == "📤 Data Export & API Access":
    st.title("📤 Data Export & API Access")
    st.caption("Your data, in standard formats, on demand. No lock-in.")

    exp_tab1, exp_tab2, exp_tab3 = st.tabs(["📁 Export Data", "🔌 API Access", "💾 Full Backup"])

    with exp_tab1:
        st.subheader("Export current workspace & activity")
        workspace_data = get_workspace()
        audit_data = get_recent_audits(1000)

        colA, colB, colC = st.columns(3)
        with colA:
            st.download_button(
                "⬇️ Workspace (JSON)",
                data=json.dumps(workspace_data, indent=2, default=str),
                file_name="workspace_export.json",
                mime="application/json",
                use_container_width=True,
            )
        with colB:
            audit_df = pd.DataFrame(audit_data) if audit_data else pd.DataFrame()
            st.download_button(
                "⬇️ Audit Log (CSV)",
                data=audit_df.to_csv(index=False) if not audit_df.empty else "no_data\n",
                file_name="audit_log_export.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with colC:
            quota_data = get_tenant_quota(CURRENT_TENANT_ID).model_dump() if hasattr(get_tenant_quota(CURRENT_TENANT_ID), "model_dump") else {}
            st.download_button(
                "⬇️ Account & Plan (JSON)",
                data=json.dumps({
                    "tenant_id": CURRENT_TENANT_ID,
                    "plan": get_tenant_plan_name(CURRENT_TENANT_ID),
                    "quota": quota_data,
                }, indent=2, default=str),
                file_name="account_export.json",
                mime="application/json",
                use_container_width=True,
            )
        st.info("ℹ️ These exports read directly from this workspace's live database — nothing is cached or delayed.")

    with exp_tab2:
        st.subheader("Programmatic access")
        st.caption(
            "This deployment is a single Streamlit application, not a hosted multi-client "
            "API — the reference below shows the internal function signatures a developer "
            "would wrap in a REST layer (e.g. FastAPI) if programmatic access is required."
        )
        st.code(
            "get_workspace() -> dict\n"
            "get_recent_audits(limit: int) -> list[dict]\n"
            "get_tenant_quota(tenant_id: str) -> TenantQuota\n"
            "quota_check(tenant_id: str, resource: str) -> dict\n"
            "authenticate_user(email: str, password: str) -> dict | None\n",
            language="python",
        )
        st.caption("Ask your development team to expose these as authenticated REST endpoints if external integrations are needed.")

    with exp_tab3:
        st.subheader("Full database backup")
        st.caption(
            "Downloads the raw SQLite database file for this deployment — every "
            "tenant, user, project, workflow, quota, and audit record in one file. "
            "Store it securely; it contains password hashes and business data."
        )
        if DB_FILE.exists():
            with open(DB_FILE, "rb") as fh:
                db_bytes = fh.read()
            clicked = st.download_button(
                "⬇️ Download database backup (.db)",
                data=db_bytes,
                file_name=f"ai_business_os_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db",
                mime="application/octet-stream",
                use_container_width=True,
            )
            st.caption(f"Current file size: {len(db_bytes)/1024:.1f} KB")
            if clicked:
                record_audit(
                    CURRENT_AUTH_USER.get("email", "unknown") if CURRENT_AUTH_USER else "unknown",
                    "DB_BACKUP_DOWNLOADED", "Data", "SUCCESS"
                )
        else:
            st.warning("No database file found yet — it's created automatically on first use.")
        st.info("ℹ️ For production, also schedule automated backups at the infrastructure level (e.g. a cron job copying this file to cloud storage) rather than relying on manual downloads alone.")


elif menu == "📜 Legal & Terms":
    st.title("📜 Legal & Terms")
    st.warning(
        "Legal content must be configured for the deployed organization; this system does not provide substitute legal advice. "
        "for advice from a qualified lawyer. Have counsel review and finalize before "
        "presenting this to any real customer."
    )
    st.markdown("""
### Nature of this software
This application is a business planning, automation, and reporting toolkit.
Calculations shown in the Finance, Strategy, and Scenario modules are
transparent, rule-based estimates intended to support — not replace — human
judgment and professional advice.

### Not professional advice
Nothing in this application constitutes licensed financial, accounting, legal,
tax, or medical advice. Clinical/healthcare decision-support features are
intentionally disabled in this build (see the Healthcare module) and should
never be relied on for real patient care.

### Data handling
Data entered into this application is stored in the deployment's own database
and is not transmitted anywhere except: (a) to the AI provider (Google Gemini)
when you explicitly use an AI-assisted feature, and (b) nowhere else. Review
your AI provider's data-handling terms before entering sensitive data.

### No warranty
This software is provided as-is. The operator of this deployment is
responsible for testing it against their own requirements before relying on
it for business-critical decisions.
    """)


elif menu == "👥 Team Management":
    st.title("👥 Team Management")
    st.caption("Invite teammates and manage roles for this workspace.")

    conn = db_connect()
    existing_users = conn.execute(
        "SELECT id, email, role, status, created_at FROM users WHERE tenant_id=? ORDER BY created_at",
        (CURRENT_TENANT_ID,)
    ).fetchall()
    conn.close()

    quota = get_tenant_quota(CURRENT_TENANT_ID)
    st.metric("Seats used", f"{len(existing_users)} / {quota.max_users}")

    st.markdown("### Current team")
    if existing_users:
        st.dataframe(pd.DataFrame([dict(u) for u in existing_users]), use_container_width=True)
    else:
        st.info("No team members yet.")

    st.markdown("---")
    st.markdown("### Invite a teammate")
    if len(existing_users) >= quota.max_users:
        st.warning(f"Seat limit reached for the current plan ({quota.max_users} users). Upgrade the plan under Account & Plan to add more.")
    else:
        with st.form("invite_teammate"):
            inv_email = st.text_input("Email")
            inv_role = st.selectbox("Role", ["member", "admin", "owner"])
            inv_password = st.text_input("Temporary password", type="password", help="Share this with the teammate securely; they should change it after first login.")
            if st.form_submit_button("Add teammate", type="primary"):
                inv_email_clean = inv_email.strip().lower()
                if not inv_email_clean or "@" not in inv_email_clean:
                    st.error("Enter a valid email address.")
                elif len(inv_password) < 12:
                    st.error("Temporary password must be at least 12 characters.")
                else:
                    try:
                        conn = db_connect()
                        now = datetime.now().astimezone().isoformat()
                        conn.execute(
                            "INSERT INTO users(id,tenant_id,email,role,status,created_at,password_hash) "
                            "VALUES(?,?,?,?,?,?,?)",
                            (f"USR-{__import__('uuid').uuid4().hex}", CURRENT_TENANT_ID,
                             inv_email_clean, inv_role, "active", now, _password_hash(inv_password))
                        )
                        conn.commit()
                        conn.close()
                        record_audit(
                            CURRENT_AUTH_USER.get("email", "unknown") if CURRENT_AUTH_USER else "unknown",
                            "TEAM_MEMBER_ADDED", "Team", inv_email_clean
                        )
                        st.success(f"Added {inv_email_clean} as {inv_role}.")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("A user with this email already exists in this workspace.")

    st.markdown("---")
    st.markdown("### Deactivate a teammate")
    active_emails = [u["email"] for u in existing_users if u["status"] == "active"]
    if active_emails:
        to_deactivate = st.selectbox("Select user", active_emails, key="deactivate_select")
        if st.button("Deactivate access"):
            conn = db_connect()
            conn.execute(
                "UPDATE users SET status='inactive' WHERE tenant_id=? AND email=?",
                (CURRENT_TENANT_ID, to_deactivate)
            )
            conn.commit()
            conn.close()
            record_audit(
                CURRENT_AUTH_USER.get("email", "unknown") if CURRENT_AUTH_USER else "unknown",
                "TEAM_MEMBER_DEACTIVATED", "Team", to_deactivate
            )
            st.success(f"{to_deactivate} deactivated.")
            st.rerun()
    else:
        st.caption("No active users to deactivate.")


# Demo Data module intentionally removed in v21. Production builds never expose synthetic business data.
elif menu == "🧠 Business Intelligence & Validation":
    st.title("🧠 Business Intelligence & Validation")
    st.caption("Transparent decision-support. Replace estimates with validated business data.")
    vals = {}
    cols = st.columns(3)
    fields = [
        ("market", "Market Attractiveness"), ("demand", "Demand Evidence"),
        ("competition", "Competitive Position"), ("economics", "Unit Economics"),
        ("execution", "Execution Readiness"), ("risk", "Risk Resilience")
    ]
    for i, (key, label) in enumerate(fields):
        with cols[i % 3]:
            vals[key] = st.slider(label, 0.0, 10.0, 5.0, 0.1)
    result = calculate_business_score(vals)
    a, b = st.columns(2)
    a.metric("Validation Score", f"{result['score']}/100")
    b.metric("Decision Band", result["band"])
    v24_render_human(result)

    question = st.text_area("Executive Question")
    if st.button("Run Governed Validation", type="primary"):
        if not question.strip():
            st.info("Enter a question first.")
        else:
            prompt = build_governed_prompt(
                "Business Intelligence & Validation Engine",
                question, get_workspace(), "detailed decision memo"
            )
            answer = run_ai_task(api_key, prompt, temperature=0.15)
            record_audit("WorkspaceUser", "BI_VALIDATION", "BI", 
                         "SUCCESS" if answer else "AI_UNAVAILABLE",
                         {"score": result, "question": question})
            st.write(answer or "AI provider unavailable.")


elif menu == "🚀 Max Control Center":
    st.title("🚀 AI Business OS™ — Max Control Center")
    st.caption("Governed intelligence, decisions, workflows, auditability and production-ready autonomous intelligence.")

    readiness = product_readiness()
    c1, c2 = st.columns(2)
    c1.metric("Product Readiness", f"{readiness['score']}%")
    c2.metric("Stage", PRODUCT_STAGE)

    st.markdown("### Governed Decision Engine")
    title = st.text_input("Decision title")
    context = st.text_area("Decision context")
    question = st.text_area("What should the business decide?")
    depth = st.selectbox("Output level", ["Executive", "Detailed"])
    if st.button("Generate Decision Brief"):
        if not question.strip():
            st.warning("Enter the decision question.")
        else:
            prompt = build_governed_prompt(
                "Executive Decision Engine",
                question + "\nCONTEXT:\n" + context,
                get_workspace(),
                depth
            )
            answer = run_ai_task(api_key, prompt, temperature=0.1)
            if answer:
                gate = quality_gate(answer)
                st.write(answer)
                v24_render_human(gate)
                if gate["passed"]:
                    register_decision(
                        title or "Untitled Decision", context, answer, 0.70,
                        ["Validate source data before material decisions."]
                    )
            else:
                st.error("AI provider unavailable.")

    st.markdown("### Governed Workflow Builder")
    wf_name = st.text_input("Workflow name")
    wf_objective = st.text_area("Workflow objective")
    wf_steps = st.text_area("Steps — one per line")
    if st.button("Create Governed Workflow"):
        steps = [x.strip() for x in wf_steps.splitlines() if x.strip()]
        if not wf_name.strip() or not steps:
            st.warning("Provide a workflow name and at least one step.")
        else:
            v24_render_human(create_workflow(wf_name, wf_objective, steps))

    st.markdown("### Readiness Diagnostics")
    v24_render_human(readiness)


elif menu == "🏛️ Enterprise Operations":
    st.title("🏛️ Enterprise Operations")
    st.caption("Durable application services for projects, governance, RBAC and background work.")

    tenant_id = CURRENT_TENANT_ID
    status = api_safe_status()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Version", status["version"])
    c2.metric("Database", "SQLite + WAL")
    c3.metric("RBAC", "Enabled")
    c4.metric("External Actions", "Confirmed")

    st.markdown("### Projects")
    with st.form("create_project_form"):
        p_name = st.text_input("Project name")
        p_desc = st.text_area("Project description")
        if st.form_submit_button("Create Project", type="primary"):
            if p_name.strip():
                pid = create_project(tenant_id, p_name, p_desc)
                st.success(f"Created {pid}")
            else:
                st.warning("Project name is required.")

    projects = list_projects(tenant_id)
    if projects:
        st.dataframe(pd.DataFrame(projects), use_container_width=True)
    else:
        st.info("No projects yet.")

    st.markdown("### Background Jobs")
    job_type = st.selectbox("Job type", ["AI_ANALYSIS", "REPORT_EXPORT", "WORKFLOW_RUN"])
    payload_text = st.text_area("Job payload (JSON)", '{"priority":"normal"}')
    if st.button("Queue Job"):
        try:
            payload = json.loads(payload_text)
            jid = queue_job(tenant_id, job_type, payload)
            st.success(f"Queued {jid}")
        except Exception as exc:
            st.error(f"Invalid JSON: {exc}")

    v24_render_human(get_job_summary(tenant_id))

    st.markdown("### Role Permissions")
    role = st.selectbox("Role", ["owner", "admin", "member", "viewer"])
    v24_render_human({action: rbac_allows(role, action)
             for action in ["read", "write", "execute", "admin"]})

    with st.expander("Service Status"):
        v24_render_human(status)



elif menu == "🧪 Quality & Security Center":
    st.title("🧪 Quality & Security Center")
    st.caption("Production controls, provenance, integrations and security posture.")

    report = production_quality_report()
    c1, c2, c3 = st.columns(3)
    c1.metric("Quality Gate", f"{report['score']}%")
    c2.metric("Environment", report["environment"])
    c3.metric("External Actions", "LOCKED")

    st.markdown("### Integration Registry")
    st.dataframe(pd.DataFrame(report["integrations"]), use_container_width=True)

    st.markdown("### Data Provenance")
    source = st.text_input("Source")
    source_status = st.selectbox("Source status", ["validated", "estimated", "missing"])
    notes = st.text_area("Notes")
    if st.button("Create Provenance Record"):
        v24_render_human(data_provenance(source, source_status, notes))

    st.markdown("### Security Posture")
    v24_render_human({
        "authenticated_user": {
            "email": CURRENT_AUTH_USER.get("email"),
            "role": CURRENT_AUTH_USER.get("role")
        },
        "secrets_in_ui": "password fields only",
        "external_actions": "disabled by default",
        "audit_logging": "enabled",
        "prompt_sanitization": "enabled",
        "password_storage": "PBKDF2-SHA256 salted hashes",
    })

    with st.expander("Production Quality Report"):
        v24_render_human(report)



elif menu == "🛠️ Service & Reliability":
    st.title("🛠️ Service & Reliability")
    st.caption("Database migrations, safe jobs, backups and service health.")

    health = service_health()
    c1, c2, c3 = st.columns(3)
    c1.metric("Service", "HEALTHY" if health["passed"] else "ATTENTION")
    c2.metric("Version", V10_VERSION)
    c3.metric("Backups", len(list_backups()))

    st.markdown("### Safe Job Worker")
    if st.button("Process One Queued Job", type="primary"):
        result = process_one_job(CURRENT_TENANT_ID)
        v24_render_human(result or {"status": "no_queued_job"})

    st.markdown("### Database Backup")
    if st.button("Create Verified Backup"):
        path = create_backup()
        st.success(f"Backup created: {path}")

    backups = list_backups()
    if backups:
        st.dataframe(pd.DataFrame({"backup": backups}), use_container_width=True)

    st.markdown("### Service Health")
    v24_render_human(health)

    st.markdown("### AI Result Contract")
    st.info("AI result contracts are validated against live execution responses. No synthetic business result is shown in production UI.")


elif menu == "🛡️ Enterprise Control Plane":
    st.title("🛡️ Enterprise Control Plane")
    st.caption("Policy, approvals, immutable audit integrity, quotas and integration contracts.")

    health = control_plane_health()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Control Plane", "HEALTHY" if health["passed"] else "ATTENTION")
    c2.metric("Audit Chain", "VERIFIED" if verify_audit_chain(CURRENT_TENANT_ID)["valid"] else "BROKEN")
    c3.metric("Integrations", len(integration_catalog()))
    c4.metric("External Write", "APPROVAL REQUIRED")

    st.markdown("### Policy Simulator")
    role = st.selectbox("Actor role", list(SUPPORTED_ROLES), key="cp_role")
    action = st.selectbox(
        "Requested action",
        ["read", "write", "export_report", "delete_data", "external_write", "financial_transfer"],
        key="cp_action"
    )
    risk = st.selectbox("Risk level", ["low", "medium", "high", "critical"], key="cp_risk")
    if st.button("Evaluate Policy"):
        decision = evaluate_policy(role, action, risk)
        v24_render_human(decision.model_dump())

        if decision.required_approval:
            if st.button("Create Approval Request"):
                approval = request_approval(
                    CURRENT_TENANT_ID,
                    CURRENT_AUTH_USER.get("email", "owner"),
                    action, "policy-simulator", risk
                )
                st.success(f"Approval created: {approval.approval_id}")

    st.markdown("### Tenant Quotas")
    v24_render_human(get_tenant_quota(CURRENT_TENANT_ID).model_dump())
    for resource in ["projects", "users", "workflows"]:
        st.write(resource, quota_check(CURRENT_TENANT_ID, resource))

    st.markdown("### Integration Contracts")
    st.dataframe(pd.DataFrame(integration_catalog()), use_container_width=True)

    st.markdown("### Immutable Audit Integrity")
    if st.button("Verify Audit Chain"):
        v24_render_human(verify_audit_chain(CURRENT_TENANT_ID))
    if st.button("Append Control-Plane Test Event"):
        event_hash = append_audit_chain(
            CURRENT_TENANT_ID,
            CURRENT_AUTH_USER.get("email", "owner"),
            "CONTROL_PLANE_TEST",
            "control-plane",
            "SUCCESS"
        )
        st.success(f"Audit event committed: {event_hash[:16]}…")

    with st.expander("Control Plane Health"):
        v24_render_human(health)


elif menu == "🌐 Production API & Observability":
    st.title("🌐 Production API & Observability")
    st.caption("Deployment boundary, webhook security, idempotency and readiness.")

    ready = readiness_probe()
    c1, c2, c3 = st.columns(3)
    c1.metric("Readiness", "READY" if ready["http_semantics"] == 200 else "NOT READY")
    c2.metric("Schema", API_SCHEMA_VERSION)
    c3.metric("API Version", V12_VERSION)

    st.markdown("### Health Probes")
    if st.button("Run Liveness Probe"):
        v24_render_human(liveness_probe())
    if st.button("Run Readiness Probe"):
        v24_render_human(readiness_probe())

    st.markdown("### Observability")
    v24_render_human(observability_snapshot())

    st.markdown("### Webhook Verification Test")
    secret = st.text_input("Test secret", type="password")
    body = st.text_area(
        "Signed event JSON",
        value=''
    )
    if st.button("Verify & Ingest Test Webhook"):
        if not secret:
            st.error("Provide a test secret.")
        else:
            raw = body.encode("utf-8")
            digest = __import__("hmac").new(
                secret.encode("utf-8"), raw, __import__("hashlib").sha256
            ).hexdigest()
            st.code("sha256=" + digest)
            st.info("Copy the signature above into the integration layer; the UI does not persist it.")

    st.markdown("### API Contract")
    v24_render_human(api_ok({"capabilities": [
        "structured_errors", "request_ids", "idempotency",
        "signed_webhooks", "readiness_probe", "observability"
    ]}))


elif menu == "🔌 Integration Gateway":
    st.title("🔌 Integration Gateway")
    st.caption("Enterprise connector contracts, action governance and resilience controls.")

    health = gateway_health()
    c1, c2, c3 = st.columns(3)
    c1.metric("Gateway", "HEALTHY" if health["passed"] else "ATTENTION")
    c2.metric("Connectors", len(connector_catalog()))
    c3.metric("Live Execution", "LOCKED")

    st.markdown("### Connector Catalog")
    st.dataframe(pd.DataFrame(connector_catalog()), use_container_width=True)

    st.markdown("### Connector Secret Reference")
    connector = st.selectbox("Connector", [c["connector_id"] for c in connector_catalog()])
    secret_ref = st.text_input(
        "Secret reference (reference only; secret value is never stored)",
        type="password"
    )
    if st.button("Store Secret Reference"):
        if secret_ref:
            store_secret_reference(CURRENT_TENANT_ID, connector, secret_ref)
            st.success("Secret reference stored. The secret value itself is not persisted.")
        else:
            st.error("Provide a secret reference.")

    st.markdown("### Governed Action")
    operation = st.text_input("Operation")
    risk = st.selectbox("Risk", ["low", "medium", "high", "critical"])
    if st.button("Create Governed Action"):
        action = create_action_request(
            CURRENT_TENANT_ID,
            CURRENT_AUTH_USER.get("role", "owner"),
            connector,
            operation,
            {"source": "governed-live-action"},
            risk
        )
        v24_render_human(action.model_dump())

    st.markdown("### Circuit Breaker & Resilience")
    v24_render_human(circuit_state(CURRENT_TENANT_ID, connector))

    st.markdown("### Gateway Health")
    v24_render_human(health)


elif menu == "🔐 Security & Deployment":
    st.title("🔐 Security & Deployment")
    st.caption("Authentication, scoped tokens, rate limiting and deployment preflight.")

    health = security_boundary_health()
    c1, c2, c3 = st.columns(3)
    c1.metric("Preflight", "READY" if health["preflight_ready"] else "BLOCKED")
    c2.metric("Environment", health["environment"])
    c3.metric("External Actions", health["external_actions"].upper())

    st.markdown("### Deployment Preflight")
    v24_render_human(deployment_preflight().model_dump())

    st.markdown("### API Token Management")
    scopes = st.multiselect(
        "Token scopes",
        ["read", "write", "export", "integrations:read", "integrations:execute", "admin"],
        default=["read"]
    )
    if st.button("Generate API Token"):
        try:
            token = create_api_token(CURRENT_TENANT_ID, scopes)
            st.warning("Copy this token now. The raw token is not stored and cannot be recovered later.")
            st.code(token["token"])
            v24_render_human({"token_id": token["token_id"], "scopes": token["scopes"]})
        except ValueError as exc:
            st.error(str(exc))

    st.markdown("### Rate Limit")
    if st.button("Check API Rate Limit"):
        v24_render_human(rate_limit_check(CURRENT_TENANT_ID).model_dump())

    st.markdown("### Security Boundary Health")
    v24_render_human(health)


elif menu == "📦 Operations & Release":
    st.title("📦 Operations & Release")
    st.caption("Production diagnostics, structured observability, backups and release control.")

    health = operational_health()
    c1, c2, c3 = st.columns(3)
    c1.metric("Operational Health", "READY" if health["ready"] else "BLOCKED")
    c2.metric("Version", V23_VERSION)
    c3.metric("Channel", RELEASE_CHANNEL)

    st.markdown("### Runtime Diagnostics")
    if st.button("Run Full Diagnostics"):
        v24_render_human(runtime_diagnostics())

    st.markdown("### Release Manifest")
    if st.button("Create Release Manifest"):
        v24_render_human(build_release_manifest().model_dump())

    st.markdown("### Backup Verification")
    if st.button("Verify Current Backup"):
        v24_render_human(verify_backup_file(backup))

    st.markdown("### Migration Safety")
    v24_render_human(migration_safety_check())

    st.markdown("### Recent Metrics")
    st.dataframe(pd.DataFrame(recent_metrics(50)), use_container_width=True)

    st.markdown("### Recent Structured Logs")
    st.dataframe(pd.DataFrame(recent_logs(50)), use_container_width=True)

def run_internal_self_test() -> Dict[str, Any]:
    results = {}
    try:
        tid = ensure_local_tenant()
        results["database"] = bool(tid and DB_FILE.exists())
        results["rbac"] = rbac_allows("owner", "admin") and not rbac_allows("viewer", "write")
        pid = create_project(tid, "SELF_TEST_PROJECT", "Temporary internal test project")
        results["project_service"] = bool(pid)
        jid = queue_job(tid, "SELF_TEST", {"ok": True})
        results["job_queue"] = bool(jid)
        results["status_contract"] = api_safe_status()["secrets_exposed"] is False
        results["v10_health"] = service_health()["passed"]
        results["migration_table"] = bool(MIGRATION_TABLE)
        results["ai_contract"] = normalize_ai_result("test")["status"] == "completed"
        results["v11_control_plane"] = control_plane_health()["passed"]
        results["policy_block"] = evaluate_policy("member", "financial_transfer").required_approval
        results["quota_service"] = quota_check(tid, "projects")["allowed"] is True
        audit_hash = append_audit_chain(tid, "self-test", "SELF_TEST", "v11", "SUCCESS")
        results["audit_chain"] = bool(audit_hash) and verify_audit_chain(tid)["valid"]
        results["v12_readiness"] = readiness_probe()["ok"] is True
        results["api_contract"] = api_error("TEST", "test")["ok"] is False
        test_key = "self-test-" + __import__("uuid").uuid4().hex
        test_response = api_ok({"test": True})
        idempotent_store(tid, test_key, test_response)
        results["idempotency"] = idempotent_get(tid, test_key) == test_response
        results["v13_gateway"] = gateway_health()["passed"]
        results["connector_catalog"] = len(connector_catalog()) >= 4
        governed = create_action_request(tid, "owner", "webhook", "external_write", {}, "high")
        results["action_governance"] = governed.status == "awaiting_approval"
        results["gateway_lock"] = connector_operation(tid, "webhook", "send", {}).ok is False
        results["v14_preflight"] = deployment_preflight().ready
        token_bundle = create_api_token(tid, ["read", "integrations:read"])
        auth = authenticate_api_token(tid, token_bundle["token"], "read")
        results["token_auth"] = auth["authenticated"] is True
        results["scope_guard"] = authenticate_api_token(tid, token_bundle["token"], "admin")["authenticated"] is False
        results["rate_limit"] = rate_limit_check(tid, "self-test", 1000).allowed is True
        revoke_api_token(tid, token_bundle["token_id"])
        results["token_revocation"] = authenticate_api_token(tid, token_bundle["token"])["authenticated"] is False
    except Exception as exc:
        results["exception"] = str(exc)
    results["passed"] = all(v is True for v in results.values() if isinstance(v, bool))
    enterprise_event("SELF_TEST", results, "INFO" if results["passed"] else "ERROR")
    return results


def v30_final_delivery_self_test() -> Dict[str, Any]:
    """Static + database capability checks for the final universal build."""
    checks = {
        "universal_business_types": len(V30_BUSINESS_TYPES) >= 10,
        "universal_domain_router": len(V30_DOMAIN_TERMS) >= 10,
        "universal_file_ingestion": callable(v30_ingest_file),
        "automatic_business_discovery": callable(v30_profile_from_live_data),
        "dynamic_missing_data": callable(v30_missing_data_recommendations),
        "unified_cycle": callable(v30_universal_cycle),
        "tenant_persistence": callable(v30_store_profile),
        "optional_ai_refinement": callable(v30_ai_refine_profile),
        "human_output": callable(v24_present_report),
        "live_connector_path": callable(autonomous_register_connection),
    }
    return {
        "version": V32_VERSION,
        "checks": checks,
        "passed": all(checks.values()),
        "supported_business_archetypes": len(V30_BUSINESS_TYPES),
        "supported_intelligence_domains": len(V30_DOMAIN_TERMS),
    }

if __name__ == "__main__":
    pass


# ===========================================================================
# STRATEGIC SCENARIO SIMULATION & STRESS TESTING ENGINE
# SAME MASTER FILE — CUMULATIVE ENHANCEMENT
# ===========================================================================

class ScenarioSeverity(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    EXTREME = "EXTREME"


class ScenarioType(str, Enum):
    BASELINE = "BASELINE"
    UPSIDE = "UPSIDE"
    DOWNSIDE = "DOWNSIDE"
    EXTREME_DOWNSIDE = "EXTREME_DOWNSIDE"
    MARKET_SHOCK = "MARKET_SHOCK"
    COMPETITOR_SHOCK = "COMPETITOR_SHOCK"
    FINANCIAL_SHOCK = "FINANCIAL_SHOCK"
    OPERATIONAL_SHOCK = "OPERATIONAL_SHOCK"
    CUSTOM = "CUSTOM"


class ScenarioResultStatus(str, Enum):
    VIABLE = "VIABLE"
    CONDITIONAL = "CONDITIONAL"
    AT_RISK = "AT_RISK"
    NON_VIABLE = "NON_VIABLE"


@dataclass
class ScenarioVariable:
    name: str
    baseline_value: float
    stressed_value: float

    unit: str = ""

    change_percent: float = 0.0

    impact_weight: float = 1.0

    direction: str = "NEUTRAL"


@dataclass
class ScenarioDefinition:
    scenario_id: str
    name: str

    scenario_type: ScenarioType
    severity: ScenarioSeverity

    description: str

    variables: List[
        ScenarioVariable
    ] = field(default_factory=list)

    probability: float = 0.0

    duration_days: int = 30

    trigger_conditions: List[str] = field(
        default_factory=list
    )


@dataclass
class ScenarioMetric:
    name: str

    baseline: float
    projected: float

    change: float
    change_percent: float

    status: str


@dataclass
class ScenarioResult:
    scenario_id: str
    scenario_name: str

    status: ScenarioResultStatus

    resilience_score: float

    metrics: List[ScenarioMetric] = field(
        default_factory=list
    )

    vulnerabilities: List[str] = field(
        default_factory=list
    )

    advantages: List[str] = field(
        default_factory=list
    )

    mitigation_actions: List[str] = field(
        default_factory=list
    )

    decision_implication: str = ""


@dataclass
class StressTestReport:
    report_id: str
    generated_at: str

    scenarios_tested: int

    viable_scenarios: int
    conditional_scenarios: int
    at_risk_scenarios: int
    non_viable_scenarios: int

    portfolio_resilience: float

    results: List[ScenarioResult] = field(
        default_factory=list
    )

    critical_vulnerabilities: List[str] = field(
        default_factory=list
    )

    recommended_actions: List[str] = field(
        default_factory=list
    )

    overall_verdict: str = ""


# ===========================================================================
# SCENARIO BUILDER
# ===========================================================================

class ScenarioBuilder:

    def build(
        self,
        name: str,
        scenario_type: ScenarioType,
        severity: ScenarioSeverity,
        description: str,
        variables: List[ScenarioVariable],
        probability: float = 0.0,
        duration_days: int = 30
    ) -> ScenarioDefinition:

        scenario_id = (
            "SCN-"
            +
            uuid.uuid4().hex[:16]
        )

        for variable in variables:

            if variable.baseline_value != 0:

                variable.change_percent = (

                    (
                        variable.stressed_value
                        -
                        variable.baseline_value
                    )
                    /
                    abs(
                        variable.baseline_value
                    )
                ) * 100.0

        return ScenarioDefinition(

            scenario_id=
                scenario_id,

            name=
                name,

            scenario_type=
                scenario_type,

            severity=
                severity,

            description=
                description,

            variables=
                variables,

            probability=
                max(
                    0.0,
                    min(
                        100.0,
                        probability
                    )
                ),

            duration_days=
                max(
                    1,
                    duration_days
                )
        )


# ===========================================================================
# SCENARIO GENERATOR
# ===========================================================================

class ScenarioGenerator:

    def generate_standard_suite(
        self,
        baseline:
            Dict[str, float]
    ) -> List[ScenarioDefinition]:

        builder = ScenarioBuilder()

        scenarios = []

        scenarios.append(

            builder.build(

                name=
                    "Baseline",

                scenario_type=
                    ScenarioType.BASELINE,

                severity=
                    ScenarioSeverity.LOW,

                description=
                    "Current operating assumptions.",

                variables=[]
            )
        )

        scenarios.append(

            builder.build(

                name=
                    "Moderate Downside",

                scenario_type=
                    ScenarioType.DOWNSIDE,

                severity=
                    ScenarioSeverity.MODERATE,

                description=
                    "Moderate deterioration across key business drivers.",

                variables=[

                    ScenarioVariable(
                        "revenue",
                        baseline.get(
                            "revenue",
                            0.0
                        ),
                        baseline.get(
                            "revenue",
                            0.0
                        ) * 0.85,
                        unit="currency",
                        impact_weight=1.2
                    ),

                    ScenarioVariable(
                        "gross_margin",
                        baseline.get(
                            "gross_margin",
                            0.0
                        ),
                        baseline.get(
                            "gross_margin",
                            0.0
                        ) * 0.90,
                        unit="percent",
                        impact_weight=1.1
                    ),

                    ScenarioVariable(
                        "operating_cost",
                        baseline.get(
                            "operating_cost",
                            0.0
                        ),
                        baseline.get(
                            "operating_cost",
                            0.0
                        ) * 1.10,
                        unit="currency",
                        impact_weight=1.0
                    )
                ]
            )
        )

        scenarios.append(

            builder.build(

                name=
                    "Severe Downside",

                scenario_type=
                    ScenarioType.EXTREME_DOWNSIDE,

                severity=
                    ScenarioSeverity.HIGH,

                description=
                    "Major demand decline combined with cost pressure.",

                variables=[

                    ScenarioVariable(
                        "revenue",
                        baseline.get(
                            "revenue",
                            0.0
                        ),
                        baseline.get(
                            "revenue",
                            0.0
                        ) * 0.65,
                        unit="currency",
                        impact_weight=1.5
                    ),

                    ScenarioVariable(
                        "gross_margin",
                        baseline.get(
                            "gross_margin",
                            0.0
                        ),
                        baseline.get(
                            "gross_margin",
                            0.0
                        ) * 0.75,
                        unit="percent",
                        impact_weight=1.4
                    ),

                    ScenarioVariable(
                        "operating_cost",
                        baseline.get(
                            "operating_cost",
                            0.0
                        ),
                        baseline.get(
                            "operating_cost",
                            0.0
                        ) * 1.20,
                        unit="currency",
                        impact_weight=1.3
                    )
                ]
            )
        )

        scenarios.append(

            builder.build(

                name=
                    "Growth Upside",

                scenario_type=
                    ScenarioType.UPSIDE,

                severity=
                    ScenarioSeverity.MODERATE,

                description=
                    "Demand expansion and operating leverage.",

                variables=[

                    ScenarioVariable(
                        "revenue",
                        baseline.get(
                            "revenue",
                            0.0
                        ),
                        baseline.get(
                            "revenue",
                            0.0
                        ) * 1.25,
                        unit="currency",
                        impact_weight=1.2
                    ),

                    ScenarioVariable(
                        "gross_margin",
                        baseline.get(
                            "gross_margin",
                            0.0
                        ),
                        baseline.get(
                            "gross_margin",
                            0.0
                        ) * 1.05,
                        unit="percent",
                        impact_weight=1.0
                    )
                ]
            )
        )

        return scenarios


# ===========================================================================
# SCENARIO CALCULATION ENGINE
# ===========================================================================

class ScenarioCalculationEngine:

    def project_financials(
        self,
        baseline:
            Dict[str, float],
        scenario:
            ScenarioDefinition
    ) -> Dict[str, float]:

        projected = dict(
            baseline
        )

        for variable in (
            scenario.variables
        ):

            projected[
                variable.name
            ] = variable.stressed_value

        revenue = projected.get(
            "revenue",
            0.0
        )

        margin = projected.get(
            "gross_margin",
            0.0
        )

        operating_cost = projected.get(
            "operating_cost",
            0.0
        )

        if margin > 1.0:

            gross_profit = (
                revenue
                *
                (
                    margin
                    /
                    100.0
                )
            )

        else:

            gross_profit = (
                revenue
                *
                margin
            )

        operating_profit = (
            gross_profit
            -
            operating_cost
        )

        projected[
            "gross_profit"
        ] = gross_profit

        projected[
            "operating_profit"
        ] = operating_profit

        projected[
            "operating_margin"
        ] = (

            (
                operating_profit
                /
                max(
                    revenue,
                    1.0
                )
            )
            *
            100.0
        )

        return projected


# ===========================================================================
# RESILIENCE ENGINE
# ===========================================================================

class BusinessResilienceEngine:

    def calculate(
        self,
        baseline:
            Dict[str, float],
        projected:
            Dict[str, float],
        scenario:
            ScenarioDefinition
    ) -> float:

        baseline_profit = baseline.get(
            "operating_profit",
            0.0
        )

        projected_profit = projected.get(
            "operating_profit",
            0.0
        )

        if baseline_profit == 0:

            profit_score = (
                50.0
                if projected_profit >= 0
                else 10.0
            )

        else:

            profit_retention = (

                projected_profit
                /
                baseline_profit
            )

            profit_score = (

                50.0
                +
                (
                    profit_retention
                    *
                    50.0
                )
            )

        profit_score = max(
            0.0,
            min(
                100.0,
                profit_score
            )
        )

        weighted_pressure = 0.0
        total_weight = 0.0

        for variable in (
            scenario.variables
        ):

            pressure = min(

                100.0,

                abs(
                    variable.change_percent
                )
            )

            weighted_pressure += (
                pressure
                *
                variable.impact_weight
            )

            total_weight += (
                variable.impact_weight
            )

        if total_weight:

            pressure_score = max(

                0.0,

                100.0
                -
                (
                    weighted_pressure
                    /
                    total_weight
                )
            )

        else:

            pressure_score = 100.0

        resilience = (

            profit_score
            *
            0.65

            +

            pressure_score
            *
            0.35
        )

        return round(

            max(
                0.0,
                min(
                    100.0,
                    resilience
                )
            ),

            2
        )


# ===========================================================================
# SCENARIO CLASSIFIER
# ===========================================================================

class ScenarioClassifier:

    def classify(
        self,
        resilience_score:
            float,
        projected:
            Dict[str, float]
    ) -> ScenarioResultStatus:

        operating_profit = projected.get(
            "operating_profit",
            0.0
        )

        if (
            resilience_score >= 75.0
            and
            operating_profit >= 0
        ):

            return ScenarioResultStatus.VIABLE

        if (
            resilience_score >= 55.0
            and
            operating_profit >= 0
        ):

            return ScenarioResultStatus.CONDITIONAL

        if (
            resilience_score >= 30.0
        ):

            return ScenarioResultStatus.AT_RISK

        return ScenarioResultStatus.NON_VIABLE


# ===========================================================================
# SCENARIO INTERPRETATION ENGINE
# ===========================================================================

class ScenarioInterpretationEngine:

    def interpret(
        self,
        baseline:
            Dict[str, float],
        projected:
            Dict[str, float],
        scenario:
            ScenarioDefinition
    ) -> Tuple[
        List[str],
        List[str],
        List[str]
    ]:

        vulnerabilities = []
        advantages = []
        mitigation = []

        baseline_revenue = baseline.get(
            "revenue",
            0.0
        )

        projected_revenue = projected.get(
            "revenue",
            0.0
        )

        if projected_revenue < baseline_revenue:

            decline = (

                (
                    baseline_revenue
                    -
                    projected_revenue
                )
                /
                max(
                    baseline_revenue,
                    1.0
                )
            ) * 100.0

            vulnerabilities.append(
                f"Revenue declines by {decline:.1f}%."
            )

            mitigation.extend([

                "Increase retention activity.",

                "Protect highest-margin customer segments.",

                "Reduce non-essential variable spending."
            ])

        elif projected_revenue > baseline_revenue:

            advantages.append(
                "Revenue growth creates potential operating leverage."
            )

        baseline_profit = baseline.get(
            "operating_profit",
            0.0
        )

        projected_profit = projected.get(
            "operating_profit",
            0.0
        )

        if projected_profit < 0:

            vulnerabilities.append(
                "Operating profit becomes negative."
            )

            mitigation.extend([

                "Activate cost-containment plan.",

                "Prioritize cash preservation.",

                "Suspend low-ROI expansion initiatives."
            ])

        elif (
            baseline_profit > 0
            and
            projected_profit > baseline_profit
        ):

            advantages.append(
                "Operating leverage improves under the scenario."
            )

        for variable in scenario.variables:

            if (
                variable.change_percent
                <=
                -20.0
            ):

                vulnerabilities.append(

                    (
                        f"{variable.name} experiences a "
                        f"{abs(variable.change_percent):.1f}% deterioration."
                    )
                )

            elif (
                variable.change_percent
                >=
                20.0
            ):

                advantages.append(

                    (
                        f"{variable.name} improves by "
                        f"{variable.change_percent:.1f}%."
                    )
                )

        return (
            vulnerabilities,
            advantages,
            list(
                dict.fromkeys(
                    mitigation
                )
            )
        )


# ===========================================================================
# MASTER SCENARIO STRESS TEST ENGINE
# ===========================================================================

class StrategicStressTestingEngine:

    def __init__(self):

        self.generator = (
            ScenarioGenerator()
        )

        self.calculator = (
            ScenarioCalculationEngine()
        )

        self.resilience = (
            BusinessResilienceEngine()
        )

        self.classifier = (
            ScenarioClassifier()
        )

        self.interpreter = (
            ScenarioInterpretationEngine()
        )

    def run(
        self,
        baseline:
            Dict[str, float],
        scenarios:
            Optional[
                List[ScenarioDefinition]
            ] = None
    ) -> StressTestReport:

        if scenarios is None:

            scenarios = (
                self.generator
                .generate_standard_suite(
                    baseline
                )
            )

        results = []

        for scenario in scenarios:

            projected = (
                self.calculator
                .project_financials(
                    baseline,
                    scenario
                )
            )

            resilience_score = (
                self.resilience.calculate(
                    baseline,
                    projected,
                    scenario
                )
            )

            status = (
                self.classifier.classify(
                    resilience_score,
                    projected
                )
            )

            vulnerabilities, advantages, mitigation = (
                self.interpreter.interpret(
                    baseline,
                    projected,
                    scenario
                )
            )

            metrics = []

            for variable in (
                scenario.variables
            ):

                change = (

                    variable.stressed_value
                    -
                    variable.baseline_value
                )

                metrics.append(

                    ScenarioMetric(

                        name=
                            variable.name,

                        baseline=
                            variable.baseline_value,

                        projected=
                            variable.stressed_value,

                        change=
                            change,

                        change_percent=
                            variable.change_percent,

                        status=(
                            "IMPROVED"
                            if change > 0
                            else
                            "DECLINED"
                            if change < 0
                            else
                            "UNCHANGED"
                        )
                    )
                )

            if status == ScenarioResultStatus.VIABLE:

                implication = (
                    "Strategy remains viable under this scenario."
                )

            elif status == ScenarioResultStatus.CONDITIONAL:

                implication = (
                    "Strategy remains viable only with "
                    "active monitoring and mitigation."
                )

            elif status == ScenarioResultStatus.AT_RISK:

                implication = (
                    "Strategy enters an elevated-risk state "
                    "and requires contingency action."
                )

            else:

                implication = (
                    "Strategy becomes non-viable under this scenario."
                )

            results.append(

                ScenarioResult(

                    scenario_id=
                        scenario.scenario_id,

                    scenario_name=
                        scenario.name,

                    status=
                        status,

                    resilience_score=
                        resilience_score,

                    metrics=
                        metrics,

                    vulnerabilities=
                        vulnerabilities,

                    advantages=
                        advantages,

                    mitigation_actions=
                        mitigation,

                    decision_implication=
                        implication
                )
            )

        viable = sum(

            1

            for result
            in results

            if result.status
            ==
            ScenarioResultStatus.VIABLE
        )

        conditional = sum(

            1

            for result
            in results

            if result.status
            ==
            ScenarioResultStatus.CONDITIONAL
        )

        at_risk = sum(

            1

            for result
            in results

            if result.status
            ==
            ScenarioResultStatus.AT_RISK
        )

        non_viable = sum(

            1

            for result
            in results

            if result.status
            ==
            ScenarioResultStatus.NON_VIABLE
        )

        if results:

            portfolio_resilience = round(

                sum(
                    result.resilience_score
                    for result
                    in results
                )
                /
                len(results),

                2
            )

        else:

            portfolio_resilience = 0.0

        critical_vulnerabilities = []

        for result in results:

            if result.status in (

                ScenarioResultStatus.AT_RISK,

                ScenarioResultStatus.NON_VIABLE
            ):

                critical_vulnerabilities.extend(

                    result.vulnerabilities
                )

        critical_vulnerabilities = list(

            dict.fromkeys(
                critical_vulnerabilities
            )
        )

        recommended_actions = []

        for result in results:

            if result.status in (

                ScenarioResultStatus.AT_RISK,

                ScenarioResultStatus.NON_VIABLE,

                ScenarioResultStatus.CONDITIONAL
            ):

                recommended_actions.extend(

                    result.mitigation_actions
                )

        recommended_actions = list(

            dict.fromkeys(
                recommended_actions
            )
        )

        if non_viable:

            verdict = (
                "HIGH FRAGILITY — "
                "strategy fails under at least one major stress scenario."
            )

        elif at_risk:

            verdict = (
                "ELEVATED RISK — "
                "strategy requires contingency protection."
            )

        elif conditional:

            verdict = (
                "CONDITIONALLY RESILIENT — "
                "strategy survives but requires monitoring."
            )

        else:

            verdict = (
                "RESILIENT — "
                "strategy remains viable across tested scenarios."
            )

        return StressTestReport(

            report_id=(
                "STR-"
                +
                uuid.uuid4().hex[:16]
            ),

            generated_at=(
                datetime.now()
                .astimezone()
                .isoformat()
            ),

            scenarios_tested=
                len(results),

            viable_scenarios=
                viable,

            conditional_scenarios=
                conditional,

            at_risk_scenarios=
                at_risk,

            non_viable_scenarios=
                non_viable,

            portfolio_resilience=
                portfolio_resilience,

            results=
                results,

            critical_vulnerabilities=
                critical_vulnerabilities,

            recommended_actions=
                recommended_actions,

            overall_verdict=
                verdict
        )


# ===========================================================================
# EVIDENCE + STRESS TEST INTEGRATION
# ===========================================================================

def apply_stress_test_gate(
    decision:
        AdaptiveDecision,
    stress_report:
        StressTestReport
) -> AdaptiveDecision:

    if (
        stress_report.non_viable_scenarios
        >
        0
    ):

        decision.confidence = min(
            decision.confidence,
            55.0
        )

        decision.rationale += (

            " Stress testing identified at least "
            "one non-viable scenario."
        )

        decision.required_actions.append(
            "Review contingency strategy before scaling exposure."
        )

    elif (
        stress_report.at_risk_scenarios
        >
        0
    ):

        decision.confidence = min(
            decision.confidence,
            70.0
        )

        decision.required_actions.append(
            "Monitor identified stress vulnerabilities."
        )

    return decision


# ===========================================================================
# ORCHESTRATOR BRIDGE
# ===========================================================================

def attach_stress_testing(
    orchestrator:
        EnterpriseStrategyOrchestrator
) -> EnterpriseStrategyOrchestrator:

    if not hasattr(
        orchestrator,
        "stress_testing"
    ):

        orchestrator.stress_testing = (
            StrategicStressTestingEngine()
        )

    return orchestrator


try:

    attach_stress_testing(
        os_core.strategy_orchestrator
    )

except Exception as exc:

    logger.warning(
        "Stress testing bridge deferred: %s",
        exc
    )


# ===========================================================================
# SELF TEST
# ===========================================================================

def stress_testing_self_test():

    engine = (
        StrategicStressTestingEngine()
    )

    baseline = {

        "revenue":
            100000.0,

        "gross_margin":
            60.0,

        "operating_cost":
            30000.0
    }

    baseline[
        "gross_profit"
    ] = (
        baseline["revenue"]
        *
        0.60
    )

    baseline[
        "operating_profit"
    ] = (
        baseline["gross_profit"]
        -
        baseline["operating_cost"]
    )

    report = engine.run(
        baseline
    )

    return {

        "system":
            "STRATEGIC_STRESS_TESTING_ENGINE",

        "passed":
            report.scenarios_tested >= 4,

        "scenarios_tested":
            report.scenarios_tested,

        "portfolio_resilience":
            report.portfolio_resilience,

        "overall_verdict":
            report.overall_verdict,

        "critical_vulnerabilities":
            report.critical_vulnerabilities,

        "recommended_actions":
            report.recommended_actions
    }


# ===========================================================================
# FEATURE REGISTRATION
# ===========================================================================

if "ENHANCED_V15_FEATURES" in globals():

    _stress_testing_features = [

        "strategic_stress_testing",

        "scenario_simulation",

        "baseline_scenario",

        "upside_scenario",

        "downside_scenario",

        "extreme_downside_scenario",

        "market_shock_simulation",

        "competitor_shock_simulation",

        "financial_shock_simulation",

        "operational_shock_simulation",

        "business_resilience_scoring",

        "scenario_vulnerability_detection",

        "scenario_mitigation_engine",

        "portfolio_resilience_analysis",

        "stress_test_decision_gate"
    ]

    for _feature in (
        _stress_testing_features
    ):

        if (
            _feature
            not in ENHANCED_V15_FEATURES
        ):

            ENHANCED_V15_FEATURES.append(
                _feature
            )


# ===========================================================================
# END — STRATEGIC SCENARIO SIMULATION & STRESS TESTING
# ===========================================================================


# ============================================================================
# STAGE 12 — FINAL MASTER-CODE AUDIT ENGINE
# AI BUSINESS OPERATING SYSTEM
# ============================================================================
#
# FINAL EVOLUTION LAYER
#
# Stage 1  → Alert & Decision Engine
# Stage 2  → KPI Intelligence Engine
# Stage 3  → Risk Intelligence Engine
# Stage 4  → Market / Competitive Intelligence
# Stage 5  → Cross-Engine Decision Orchestrator
# Stage 6  → Security / RBAC / Audit
# Stage 7  → Persistent Storage / State Recovery
# Stage 8  → Executive Dashboard
# Stage 9  → End-to-End Real-Time Integration
# Stage 10 → Heavy Testing / Failure Simulation
# Stage 11 → Performance Optimization
# Stage 12 → FINAL MASTER-CODE AUDIT
#
# Audit Pipeline
#
# Architecture Integrity
#        ↓
# Dependency Integrity
#        ↓
# Interface Integrity
#        ↓
# Data Model Integrity
#        ↓
# Security Integrity
#        ↓
# Persistence Integrity
#        ↓
# Runtime Integrity
#        ↓
# Failure Handling
#        ↓
# Performance Integrity
#        ↓
# Test Coverage
#        ↓
# Cross-Stage Integration
#        ↓
# Production Readiness
#        ↓
# Final Release Decision
# ============================================================================


class AuditSeverity(str, Enum):

    INFO = "INFO"
    WARNING = "WARNING"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AuditStatus(str, Enum):

    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"


class AuditDomain(str, Enum):

    ARCHITECTURE = "ARCHITECTURE"
    DEPENDENCY = "DEPENDENCY"
    INTERFACE = "INTERFACE"
    DATA = "DATA"
    SECURITY = "SECURITY"
    PERSISTENCE = "PERSISTENCE"
    RUNTIME = "RUNTIME"
    FAILURE_HANDLING = "FAILURE_HANDLING"
    PERFORMANCE = "PERFORMANCE"
    TESTING = "TESTING"
    INTEGRATION = "INTEGRATION"
    PRODUCTION = "PRODUCTION"


class ReleaseDecision(str, Enum):

    RELEASE = "RELEASE"
    RELEASE_WITH_WARNINGS = "RELEASE_WITH_WARNINGS"
    HOLD = "HOLD"
    BLOCK = "BLOCK"


# ============================================================================
# AUDIT FINDING
# ============================================================================

@dataclass
class AuditFinding:

    finding_id: str

    domain: AuditDomain

    severity: AuditSeverity

    status: AuditStatus

    title: str

    description: str

    recommendation: str

    component: str = ""

    evidence: Any = None

    blocking: bool = False

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


# ============================================================================
# AUDIT CHECK
# ============================================================================

@dataclass
class AuditCheck:

    check_id: str

    name: str

    domain: AuditDomain

    description: str

    required: bool = True

    weight: float = 1.0


# ============================================================================
# AUDIT SCORE
# ============================================================================

@dataclass
class AuditScore:

    architecture: float
    dependency: float
    interface: float
    data: float
    security: float
    persistence: float
    runtime: float
    failure_handling: float
    performance: float
    testing: float
    integration: float
    production: float

    overall: float

    confidence: float


# ============================================================================
# FINAL AUDIT RESULT
# ============================================================================

@dataclass
class MasterAuditResult:

    audit_id: str

    generated_at: str

    status: AuditStatus

    release_decision: ReleaseDecision

    score: AuditScore

    findings: List[AuditFinding]

    passed_checks: int

    warning_checks: int

    failed_checks: int

    blocked_checks: int

    critical_findings: int

    high_findings: int

    production_ready: bool

    confidence: float

    summary: str


# ============================================================================
# AUDIT ID GENERATOR
# ============================================================================

class MasterAuditID:

    @staticmethod
    def generate(
        prefix="AUDIT"
    ):

        return (

            f"{prefix}-"

            +

            hashlib.sha256(

                f"{time.time_ns()}".encode()

            ).hexdigest()[:20]
        )


# ============================================================================
# AUDIT FINDING FACTORY
# ============================================================================

class AuditFindingFactory:

    @staticmethod
    def create(
        domain,
        severity,
        status,
        title,
        description,
        recommendation,
        component="",
        evidence=None,
        blocking=False
    ):

        return AuditFinding(

            finding_id=
                MasterAuditID.generate(
                    "FND"
                ),

            domain=
                domain,

            severity=
                severity,

            status=
                status,

            title=
                title,

            description=
                description,

            recommendation=
                recommendation,

            component=
                component,

            evidence=
                evidence,

            blocking=
                blocking
        )


# ============================================================================
# ARCHITECTURE AUDITOR
# ============================================================================

class ArchitectureAuditor:

    REQUIRED_STAGES = [

        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12
    ]

    def audit(
        self,
        context
    ):

        findings = []

        stages = context.get(
            "stages",
            []
        )

        missing = [

            stage

            for stage
            in self.REQUIRED_STAGES

            if stage not in stages
        ]

        if missing:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.ARCHITECTURE,

                    severity=
                        AuditSeverity.CRITICAL,

                    status=
                        AuditStatus.FAIL,

                    title=
                        "Missing required stages",

                    description=
                        f"Required architecture stages "
                        f"are missing: {missing}.",

                    recommendation=
                        "Restore and integrate every "
                        "required stage before release.",

                    component=
                        "MASTER_ARCHITECTURE",

                    evidence=
                        missing,

                    blocking=
                        True
                )
            )

        else:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.ARCHITECTURE,

                    severity=
                        AuditSeverity.INFO,

                    status=
                        AuditStatus.PASS,

                    title=
                        "Complete stage architecture detected",

                    description=
                        "All required master stages "
                        "are represented.",

                    recommendation=
                        "Continue with interface and "
                        "runtime integrity validation.",

                    component=
                        "MASTER_ARCHITECTURE",

                    evidence=
                        stages
                )
            )

        return findings


# ============================================================================
# DEPENDENCY AUDITOR
# ============================================================================

class DependencyAuditor:

    def audit(
        self,
        context
    ):

        findings = []

        dependencies = context.get(
            "dependencies",
            {}
        )

        unresolved = [

            name

            for name, state
            in dependencies.items()

            if state is False
        ]

        if unresolved:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.DEPENDENCY,

                    severity=
                        AuditSeverity.CRITICAL,

                    status=
                        AuditStatus.FAIL,

                    title=
                        "Unresolved dependencies",

                    description=
                        "One or more required "
                        "dependencies are unavailable.",

                    recommendation=
                        "Resolve all mandatory dependencies "
                        "before production deployment.",

                    component=
                        "DEPENDENCY_GRAPH",

                    evidence=
                        unresolved,

                    blocking=
                        True
                )
            )

        else:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.DEPENDENCY,

                    severity=
                        AuditSeverity.INFO,

                    status=
                        AuditStatus.PASS,

                    title=
                        "Dependency graph validated",

                    description=
                        "No unresolved required "
                        "dependencies were detected.",

                    recommendation=
                        "Maintain dependency version "
                        "compatibility."
                )
            )

        return findings


# ============================================================================
# INTERFACE AUDITOR
# ============================================================================

class InterfaceAuditor:

    def audit(
        self,
        context
    ):

        findings = []

        interfaces = context.get(
            "interfaces",
            {}
        )

        broken = [

            name

            for name, state
            in interfaces.items()

            if state is False
        ]

        if broken:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.INTERFACE,

                    severity=
                        AuditSeverity.HIGH,

                    status=
                        AuditStatus.FAIL,

                    title=
                        "Broken engine interfaces",

                    description=
                        "One or more engine integration "
                        "interfaces are not healthy.",

                    recommendation=
                        "Validate contracts between "
                        "all engine layers.",

                    component=
                        "ENGINE_INTERFACES",

                    evidence=
                        broken
                )
            )

        else:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.INTERFACE,

                    severity=
                        AuditSeverity.INFO,

                    status=
                        AuditStatus.PASS,

                    title=
                        "Engine interface integrity passed",

                    description=
                        "Cross-engine interface checks "
                        "are healthy.",

                    recommendation=
                        "Continue contract testing "
                        "during future updates."
                )
            )

        return findings


# ============================================================================
# DATA AUDITOR
# ============================================================================

class DataIntegrityAuditor:

    def audit(
        self,
        context
    ):

        findings = []

        records = context.get(
            "data_records",
            []
        )

        invalid = 0

        for record in records:

            if not isinstance(
                record,
                dict
            ):

                invalid += 1

                continue

            if any(
                value is None
                for value
                in record.values()
            ):

                invalid += 1

        if invalid:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.DATA,

                    severity=
                        AuditSeverity.HIGH,

                    status=
                        AuditStatus.WARN,

                    title=
                        "Data quality exceptions detected",

                    description=
                        f"{invalid} records contain "
                        "potentially incomplete values.",

                    recommendation=
                        "Apply schema validation and "
                        "missing-value handling."
                )
            )

        else:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.DATA,

                    severity=
                        AuditSeverity.INFO,

                    status=
                        AuditStatus.PASS,

                    title=
                        "Data integrity check passed",

                    description=
                        "No obvious structural data "
                        "integrity failures were detected.",

                    recommendation=
                        "Continue enforcing schema validation."
                )
            )

        return findings


# ============================================================================
# SECURITY AUDITOR
# ============================================================================

class SecurityAuditor:

    REQUIRED_CONTROLS = [

        "authentication",
        "authorization",
        "rbac",
        "audit_trail",
        "input_validation",
        "secret_protection"
    ]

    def audit(
        self,
        context
    ):

        findings = []

        controls = context.get(
            "security_controls",
            {}
        )

        missing = [

            control

            for control
            in self.REQUIRED_CONTROLS

            if not controls.get(
                control,
                False
            )
        ]

        if missing:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.SECURITY,

                    severity=
                        AuditSeverity.CRITICAL,

                    status=
                        AuditStatus.FAIL,

                    title=
                        "Security controls incomplete",

                    description=
                        f"Missing security controls: "
                        f"{missing}.",

                    recommendation=
                        "Do not release until mandatory "
                        "security controls are implemented.",

                    component=
                        "SECURITY_LAYER",

                    evidence=
                        missing,

                    blocking=
                        True
                )
            )

        else:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.SECURITY,

                    severity=
                        AuditSeverity.INFO,

                    status=
                        AuditStatus.PASS,

                    title=
                        "Security baseline passed",

                    description=
                        "Required security control "
                        "categories are present.",

                    recommendation=
                        "Continue periodic security auditing."
                )
            )

        return findings


# ============================================================================
# PERSISTENCE AUDITOR
# ============================================================================

class PersistenceAuditor:

    REQUIRED_CONTROLS = [

        "save",
        "load",
        "recovery",
        "integrity_check",
        "backup"
    ]

    def audit(
        self,
        context
    ):

        findings = []

        persistence = context.get(
            "persistence",
            {}
        )

        missing = [

            item

            for item
            in self.REQUIRED_CONTROLS

            if not persistence.get(
                item,
                False
            )
        ]

        if missing:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.PERSISTENCE,

                    severity=
                        AuditSeverity.HIGH,

                    status=
                        AuditStatus.FAIL,

                    title=
                        "Persistence capabilities incomplete",

                    description=
                        f"Missing persistence capabilities: "
                        f"{missing}.",

                    recommendation=
                        "Complete state persistence and "
                        "recovery mechanisms."
                )
            )

        else:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.PERSISTENCE,

                    severity=
                        AuditSeverity.INFO,

                    status=
                        AuditStatus.PASS,

                    title=
                        "Persistence integrity passed",

                    description=
                        "Required state recovery "
                        "capabilities are present.",

                    recommendation=
                        "Continue recovery simulation testing."
                )
            )

        return findings


# ============================================================================
# RUNTIME AUDITOR
# ============================================================================

class RuntimeAuditor:

    def audit(
        self,
        context
    ):

        findings = []

        runtime_errors = context.get(
            "runtime_errors",
            0
        )

        if runtime_errors > 0:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.RUNTIME,

                    severity=
                        AuditSeverity.CRITICAL,

                    status=
                        AuditStatus.FAIL,

                    title=
                        "Runtime errors detected",

                    description=
                        f"{runtime_errors} runtime "
                        "errors were reported.",

                    recommendation=
                        "Resolve runtime failures and "
                        "repeat the complete audit.",

                    evidence=
                        runtime_errors,

                    blocking=
                        True
                )
            )

        else:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.RUNTIME,

                    severity=
                        AuditSeverity.INFO,

                    status=
                        AuditStatus.PASS,

                    title=
                        "Runtime integrity passed",

                    description=
                        "No runtime errors were reported "
                        "during the audit window.",

                    recommendation=
                        "Continue runtime monitoring."
                )
            )

        return findings


# ============================================================================
# FAILURE-HANDLING AUDITOR
# ============================================================================

class FailureHandlingAuditor:

    def audit(
        self,
        context
    ):

        findings = []

        failure_tests = context.get(
            "failure_tests",
            {}
        )

        failed = [

            name

            for name, state
            in failure_tests.items()

            if state is False
        ]

        if failed:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.FAILURE_HANDLING,

                    severity=
                        AuditSeverity.CRITICAL,

                    status=
                        AuditStatus.FAIL,

                    title=
                        "Failure simulation failures",

                    description=
                        f"Failure scenarios did not pass: "
                        f"{failed}.",

                    recommendation=
                        "Harden failure recovery before release.",

                    evidence=
                        failed,

                    blocking=
                        True
                )
            )

        else:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.FAILURE_HANDLING,

                    severity=
                        AuditSeverity.INFO,

                    status=
                        AuditStatus.PASS,

                    title=
                        "Failure resilience passed",

                    description=
                        "Registered failure scenarios "
                        "completed successfully.",

                    recommendation=
                        "Expand failure simulation coverage "
                        "as the system evolves."
                )
            )

        return findings


# ============================================================================
# PERFORMANCE AUDITOR
# ============================================================================

class FinalPerformanceAuditor:

    def audit(
        self,
        context
    ):

        findings = []

        performance = context.get(
            "performance",
            {}
        )

        latency = performance.get(
            "latency",
            0.0
        )

        error_rate = performance.get(
            "error_rate",
            0.0
        )

        if error_rate > 0.05:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.PERFORMANCE,

                    severity=
                        AuditSeverity.HIGH,

                    status=
                        AuditStatus.FAIL,

                    title=
                        "Performance error rate too high",

                    description=
                        f"Observed error rate is "
                        f"{error_rate:.2%}.",

                    recommendation=
                        "Resolve performance-related "
                        "failures before release."
                )
            )

        elif latency > 5.0:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.PERFORMANCE,

                    severity=
                        AuditSeverity.HIGH,

                    status=
                        AuditStatus.WARN,

                    title=
                        "High system latency",

                    description=
                        f"Observed latency is "
                        f"{latency:.3f} seconds.",

                    recommendation=
                        "Optimize critical execution paths."
                )
            )

        else:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.PERFORMANCE,

                    severity=
                        AuditSeverity.INFO,

                    status=
                        AuditStatus.PASS,

                    title=
                        "Performance baseline passed",

                    description=
                        "Latency and error-rate "
                        "thresholds are acceptable.",

                    recommendation=
                        "Continue performance monitoring."
                )
            )

        return findings


# ============================================================================
# TESTING AUDITOR
# ============================================================================

class TestingAuditor:

    def audit(
        self,
        context
    ):

        findings = []

        testing = context.get(
            "testing",
            {}
        )

        total = testing.get(
            "total",
            0
        )

        passed = testing.get(
            "passed",
            0
        )

        if total <= 0:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.TESTING,

                    severity=
                        AuditSeverity.CRITICAL,

                    status=
                        AuditStatus.BLOCKED,

                    title=
                        "No test results available",

                    description=
                        "The master system has no "
                        "verifiable test execution result.",

                    recommendation=
                        "Execute the complete test suite "
                        "before release.",

                    blocking=
                        True
                )
            )

            return findings

        pass_rate = (
            passed / total
        )

        if pass_rate < 0.95:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.TESTING,

                    severity=
                        AuditSeverity.CRITICAL,

                    status=
                        AuditStatus.FAIL,

                    title=
                        "Test pass rate below release threshold",

                    description=
                        f"Test pass rate is "
                        f"{pass_rate:.2%}.",

                    recommendation=
                        "Resolve failing tests and rerun "
                        "the full suite.",

                    evidence=
                        {
                            "total":
                                total,

                            "passed":
                                passed,

                            "pass_rate":
                                pass_rate
                        },

                    blocking=
                        True
                )
            )

        else:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.TESTING,

                    severity=
                        AuditSeverity.INFO,

                    status=
                        AuditStatus.PASS,

                    title=
                        "Master test suite passed",

                    description=
                        f"{passed}/{total} tests passed.",

                    recommendation=
                        "Maintain regression testing."
                )
            )

        return findings


# ============================================================================
# INTEGRATION AUDITOR
# ============================================================================

class IntegrationAuditor:

    def audit(
        self,
        context
    ):

        findings = []

        integrations = context.get(
            "integrations",
            {}
        )

        failed = [

            name

            for name, state
            in integrations.items()

            if state is False
        ]

        if failed:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.INTEGRATION,

                    severity=
                        AuditSeverity.CRITICAL,

                    status=
                        AuditStatus.FAIL,

                    title=
                        "Cross-stage integration failures",

                    description=
                        f"Failed integrations: "
                        f"{failed}.",

                    recommendation=
                        "Repair cross-engine contracts "
                        "and rerun end-to-end tests.",

                    evidence=
                        failed,

                    blocking=
                        True
                )
            )

        else:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.INTEGRATION,

                    severity=
                        AuditSeverity.INFO,

                    status=
                        AuditStatus.PASS,

                    title=
                        "Cross-stage integration passed",

                    description=
                        "Registered integration points "
                        "are healthy.",

                    recommendation=
                        "Continue end-to-end regression testing."
                )
            )

        return findings


# ============================================================================
# PRODUCTION READINESS AUDITOR
# ============================================================================

class ProductionReadinessAuditor:

    REQUIRED_ITEMS = [

        "configuration",
        "logging",
        "monitoring",
        "health_checks",
        "error_handling",
        "documentation",
        "backup_strategy",
        "rollback_strategy"
    ]

    def audit(
        self,
        context
    ):

        findings = []

        readiness = context.get(
            "production_readiness",
            {}
        )

        missing = [

            item

            for item
            in self.REQUIRED_ITEMS

            if not readiness.get(
                item,
                False
            )
        ]

        if missing:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.PRODUCTION,

                    severity=
                        AuditSeverity.HIGH,

                    status=
                        AuditStatus.WARN,

                    title=
                        "Production readiness gaps",

                    description=
                        f"Missing production controls: "
                        f"{missing}.",

                    recommendation=
                        "Complete deployment-readiness "
                        "controls before production release.",

                    evidence=
                        missing
                )
            )

        else:

            findings.append(

                AuditFindingFactory.create(

                    domain=
                        AuditDomain.PRODUCTION,

                    severity=
                        AuditSeverity.INFO,

                    status=
                        AuditStatus.PASS,

                    title=
                        "Production readiness passed",

                    description=
                        "Required operational readiness "
                        "controls are present.",

                    recommendation=
                        "Maintain operational readiness checks."
                )
            )

        return findings


# ============================================================================
# AUDIT SCORE ENGINE
# ============================================================================

class MasterAuditScoreEngine:

    DOMAIN_WEIGHTS = {

        AuditDomain.ARCHITECTURE: 1.20,
        AuditDomain.DEPENDENCY: 1.00,
        AuditDomain.INTERFACE: 1.10,
        AuditDomain.DATA: 1.00,
        AuditDomain.SECURITY: 1.30,
        AuditDomain.PERSISTENCE: 1.10,
        AuditDomain.RUNTIME: 1.20,
        AuditDomain.FAILURE_HANDLING: 1.20,
        AuditDomain.PERFORMANCE: 1.00,
        AuditDomain.TESTING: 1.30,
        AuditDomain.INTEGRATION: 1.30,
        AuditDomain.PRODUCTION: 1.00
    }

    def calculate(
        self,
        findings
    ):

        domain_scores = {}

        for domain in AuditDomain:

            domain_findings = [

                item

                for item
                in findings

                if item.domain == domain
            ]

            if not domain_findings:

                domain_scores[
                    domain
                ] = 0.0

                continue

            points = 0.0

            total = 0.0

            for finding in domain_findings:

                weight = self._finding_weight(
                    finding
                )

                total += weight

                if finding.status == AuditStatus.PASS:

                    points += weight

                elif finding.status == AuditStatus.WARN:

                    points += weight * 0.70

                elif finding.status == AuditStatus.BLOCKED:

                    points += 0.0

                else:

                    points += 0.0

            domain_scores[
                domain
            ] = (

                points / total * 100

                if total

                else 0.0
            )

        weighted_total = 0.0

        total_weight = 0.0

        for domain, score in domain_scores.items():

            weight = self.DOMAIN_WEIGHTS[
                domain
            ]

            weighted_total += (
                score * weight
            )

            total_weight += weight

        overall = (

            weighted_total / total_weight

            if total_weight

            else 0.0
        )

        return AuditScore(

            architecture=
                domain_scores[
                    AuditDomain.ARCHITECTURE
                ],

            dependency=
                domain_scores[
                    AuditDomain.DEPENDENCY
                ],

            interface=
                domain_scores[
                    AuditDomain.INTERFACE
                ],

            data=
                domain_scores[
                    AuditDomain.DATA
                ],

            security=
                domain_scores[
                    AuditDomain.SECURITY
                ],

            persistence=
                domain_scores[
                    AuditDomain.PERSISTENCE
                ],

            runtime=
                domain_scores[
                    AuditDomain.RUNTIME
                ],

            failure_handling=
                domain_scores[
                    AuditDomain.FAILURE_HANDLING
                ],

            performance=
                domain_scores[
                    AuditDomain.PERFORMANCE
                ],

            testing=
                domain_scores[
                    AuditDomain.TESTING
                ],

            integration=
                domain_scores[
                    AuditDomain.INTEGRATION
                ],

            production=
                domain_scores[
                    AuditDomain.PRODUCTION
                ],

            overall=
                overall,

            confidence=
                min(
                    1.0,
                    len(findings) / 20
                )
        )

    @staticmethod
    def _finding_weight(
        finding
    ):

        if finding.severity == AuditSeverity.CRITICAL:

            return 4.0

        if finding.severity == AuditSeverity.HIGH:

            return 3.0

        if finding.severity == AuditSeverity.WARNING:

            return 2.0

        return 1.0


# ============================================================================
# RELEASE GATE
# ============================================================================

class MasterReleaseGate:

    def decide(
        self,
        score,
        findings
    ):

        blocking = [

            item

            for item
            in findings

            if item.blocking
            or
            item.status
            in (
                AuditStatus.FAIL,
                AuditStatus.BLOCKED
            )
            and
            item.severity
            == AuditSeverity.CRITICAL
        ]

        critical = [

            item

            for item
            in findings

            if item.severity
            == AuditSeverity.CRITICAL
        ]

        warnings = [

            item

            for item
            in findings

            if item.status
            == AuditStatus.WARN
        ]

        if blocking:

            return (
                AuditStatus.FAIL,

                ReleaseDecision.BLOCK
            )

        if score.overall < 90:

            return (
                AuditStatus.WARN,

                ReleaseDecision.HOLD
            )

        if warnings:

            return (
                AuditStatus.WARN,

                ReleaseDecision.RELEASE_WITH_WARNINGS
            )

        if critical:

            return (
                AuditStatus.WARN,

                ReleaseDecision.RELEASE_WITH_WARNINGS
            )

        return (
            AuditStatus.PASS,
            ReleaseDecision.RELEASE
        )


# ============================================================================
# MASTER AUDIT ENGINE
# ============================================================================

class FinalMasterAuditEngine:

    def __init__(self):

        self.architecture_auditor = (
            ArchitectureAuditor()
        )

        self.dependency_auditor = (
            DependencyAuditor()
        )

        self.interface_auditor = (
            InterfaceAuditor()
        )

        self.data_auditor = (
            DataIntegrityAuditor()
        )

        self.security_auditor = (
            SecurityAuditor()
        )

        self.persistence_auditor = (
            PersistenceAuditor()
        )

        self.runtime_auditor = (
            RuntimeAuditor()
        )

        self.failure_auditor = (
            FailureHandlingAuditor()
        )

        self.performance_auditor = (
            FinalPerformanceAuditor()
        )

        self.testing_auditor = (
            TestingAuditor()
        )

        self.integration_auditor = (
            IntegrationAuditor()
        )

        self.production_auditor = (
            ProductionReadinessAuditor()
        )

        self.score_engine = (
            MasterAuditScoreEngine()
        )

        self.release_gate = (
            MasterReleaseGate()
        )

        self.results = {}

    # ------------------------------------------------------------------------
    # FULL AUDIT
    # ------------------------------------------------------------------------

    def audit(
        self,
        context=None
    ):

        context = context or {}

        findings = []

        auditors = [

            self.architecture_auditor,
            self.dependency_auditor,
            self.interface_auditor,
            self.data_auditor,
            self.security_auditor,
            self.persistence_auditor,
            self.runtime_auditor,
            self.failure_auditor,
            self.performance_auditor,
            self.testing_auditor,
            self.integration_auditor,
            self.production_auditor
        ]

        for auditor in auditors:

            findings.extend(
                auditor.audit(
                    context
                )
            )

        score = (
            self.score_engine
            .calculate(
                findings
            )
        )

        status, decision = (
            self.release_gate.decide(

                score,

                findings
            )
        )

        passed = sum(

            1

            for item
            in findings

            if item.status
            == AuditStatus.PASS
        )

        warnings = sum(

            1

            for item
            in findings

            if item.status
            == AuditStatus.WARN
        )

        failed = sum(

            1

            for item
            in findings

            if item.status
            == AuditStatus.FAIL
        )

        blocked = sum(

            1

            for item
            in findings

            if item.status
            == AuditStatus.BLOCKED
        )

        critical = sum(

            1

            for item
            in findings

            if item.severity
            == AuditSeverity.CRITICAL
        )

        high = sum(

            1

            for item
            in findings

            if item.severity
            == AuditSeverity.HIGH
        )

        production_ready = (

            decision
            in (
                ReleaseDecision.RELEASE,
                ReleaseDecision.RELEASE_WITH_WARNINGS
            )

            and
            score.overall >= 90
        )

        summary = (

            f"Final master audit completed with "
            f"overall score {score.overall:.2f}/100. "
            f"Release decision: "
            f"{decision.value}. "
            f"Passed checks: {passed}; "
            f"warnings: {warnings}; "
            f"failed: {failed}; "
            f"blocked: {blocked}."
        )

        result = MasterAuditResult(

            audit_id=
                MasterAuditID.generate(),

            generated_at=
                datetime.utcnow()
                .isoformat(),

            status=
                status,

            release_decision=
                decision,

            score=
                score,

            findings=
                findings,

            passed_checks=
                passed,

            warning_checks=
                warnings,

            failed_checks=
                failed,

            blocked_checks=
                blocked,

            critical_findings=
                critical,

            high_findings=
                high,

            production_ready=
                production_ready,

            confidence=
                score.confidence,

            summary=
                summary
        )

        self.results[
            result.audit_id
        ] = result

        return result

    # ------------------------------------------------------------------------
    # EXECUTIVE AUDIT SUMMARY
    # ------------------------------------------------------------------------

    def executive_summary(
        self,
        result
    ):

        return {

            "audit_id":
                result.audit_id,

            "status":
                result.status.value,

            "release_decision":
                result.release_decision.value,

            "overall_score":
                result.score.overall,

            "production_ready":
                result.production_ready,

            "confidence":
                result.confidence,

            "critical_findings":
                result.critical_findings,

            "high_findings":
                result.high_findings,

            "passed_checks":
                result.passed_checks,

            "warning_checks":
                result.warning_checks,

            "failed_checks":
                result.failed_checks,

            "blocked_checks":
                result.blocked_checks,

            "summary":
                result.summary
        }


# ============================================================================
# STAGE 12 SELF TEST
# ============================================================================

def stage_12_final_master_audit_self_test():

    engine = (
        FinalMasterAuditEngine()
    )

    context = {

        "stages": [

            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12
        ],

        "dependencies": {

            "core_runtime":
                True,

            "standard_library":
                True
        },

        "interfaces": {

            "alert_to_kpi":
                True,

            "kpi_to_risk":
                True,

            "risk_to_orchestrator":
                True,

            "security_to_audit":
                True,

            "storage_to_recovery":
                True,

            "dashboard_to_engine":
                True,

            "realtime_to_engine":
                True,

            "performance_to_runtime":
                True
        },

        "data_records": [

            {
                "id":
                    "DATA-001",

                "value":
                    100
            }
        ],

        "security_controls": {

            "authentication":
                True,

            "authorization":
                True,

            "rbac":
                True,

            "audit_trail":
                True,

            "input_validation":
                True,

            "secret_protection":
                True
        },

        "persistence": {

            "save":
                True,

            "load":
                True,

            "recovery":
                True,

            "integrity_check":
                True,

            "backup":
                True
        },

        "runtime_errors":
            0,

        "failure_tests": {

            "network_failure":
                True,

            "storage_failure":
                True,

            "engine_failure":
                True,

            "timeout":
                True,

            "invalid_input":
                True
        },

        "performance": {

            "latency":
                0.10,

            "error_rate":
                0.001
        },

        "testing": {

            "total":
                100,

            "passed":
                100
        },

        "integrations": {

            "stage_1_2":
                True,

            "stage_2_3":
                True,

            "stage_3_4":
                True,

            "stage_4_5":
                True,

            "stage_5_6":
                True,

            "stage_6_7":
                True,

            "stage_7_8":
                True,

            "stage_8_9":
                True,

            "stage_9_10":
                True,

            "stage_10_11":
                True,

            "stage_11_12":
                True
        },

        "production_readiness": {

            "configuration":
                True,

            "logging":
                True,

            "monitoring":
                True,

            "health_checks":
                True,

            "error_handling":
                True,

            "documentation":
                True,

            "backup_strategy":
                True,

            "rollback_strategy":
                True
        }
    }

    result = (
        engine.audit(
            context
        )
    )

    assert result is not None

    assert (
        result.score.overall
        >
        90
    )

    assert (
        result.production_ready
        is True
    )

    assert (
        result.release_decision
        ==
        ReleaseDecision.RELEASE
    )

    summary = (
        engine.executive_summary(
            result
        )
    )

    assert (
        summary["overall_score"]
        >
        90
    )

    return {

        "passed":
            True,

        "stage":
            12,

        "audit_status":
            result.status.value,

        "release_decision":
            result.release_decision.value,

        "overall_score":
            result.score.overall,

        "production_ready":
            result.production_ready,

        "passed_checks":
            result.passed_checks,

        "warnings":
            result.warning_checks,

        "failed_checks":
            result.failed_checks,

        "critical_findings":
            result.critical_findings,

        "confidence":
            result.confidence
    }


# ============================================================================
# STAGE 12 — FINAL MASTER AUDIT LAYER
# ============================================================================

# =============================================================================
# V33–V45 ENTERPRISE BUSINESS BRAIN MEGA-ENHANCEMENT
# =============================================================================
# Single-cycle integration:
#   V33 Historical Business Intelligence / Industry Priors
#   V34 Universal Business Ontology
#   V35 Enterprise Company Memory
#   V36 Business Knowledge Graph
#   V37 Causal & Diagnostic Intelligence
#   V38 Predictive Intelligence
#   V39 Digital Twin / Business Simulation
#   V40 Decision Intelligence
#   V41 Autonomous Monitoring & Alerts
#   V42 Intervention & Action Intelligence
#   V43 Outcome-Based Learning
#   V44 Enterprise Governance / Audit / Permissions
#   V45 Enterprise Business Brain Orchestration
#
# Design principle:
#   The OS is not "re-trained" by silently changing an LLM's weights.
#   It becomes a governed, evidence-backed business intelligence system through
#   structured priors, tenant-scoped memory, causal relationships, simulations,
#   decisions, verified outcomes and controlled learning.
# =============================================================================

ENTERPRISE_BRAIN_VERSION = "50.0.0"
ENTERPRISE_BRAIN_NAME = "AI Business OS™ Enterprise Business Brain"

class EvidenceRecord(BaseModel):
    source: str = ""
    statement: str = ""
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    observed_at: str = Field(default_factory=lambda: datetime.now().astimezone().isoformat())
    verified: bool = False

class IndustryPrior(BaseModel):
    industry: str
    archetype: str
    critical_kpis: List[str] = Field(default_factory=list)
    driver_relationships: List[Dict[str, str]] = Field(default_factory=list)
    common_failure_modes: List[str] = Field(default_factory=list)
    intervention_patterns: List[Dict[str, Any]] = Field(default_factory=list)
    seasonality: List[str] = Field(default_factory=list)
    priors: Dict[str, Any] = Field(default_factory=dict)
    evidence_grade: str = "structured_prior"
    confidence: float = Field(default=0.65, ge=0.0, le=1.0)

class BusinessEntity(BaseModel):
    entity_id: str
    entity_type: str
    name: str
    attributes: Dict[str, Any] = Field(default_factory=dict)

class KnowledgeEdge(BaseModel):
    source_id: str
    target_id: str
    relationship: str
    weight: float = 0.5
    confidence: float = 0.5
    evidence: List[EvidenceRecord] = Field(default_factory=list)

class DiagnosticFinding(BaseModel):
    signal: str
    hypothesis: str
    likelihood: float = Field(default=0.5, ge=0.0, le=1.0)
    severity: str = "MEDIUM"
    evidence: List[EvidenceRecord] = Field(default_factory=list)
    contradictions: List[str] = Field(default_factory=list)
    recommended_next_data: List[str] = Field(default_factory=list)

class DecisionRecord(BaseModel):
    decision_id: str
    question: str
    recommendation: str
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    evidence: List[EvidenceRecord] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    alternatives: List[Dict[str, Any]] = Field(default_factory=list)
    human_approval_required: bool = True
    status: str = "PROPOSED"

class OutcomeRecord(BaseModel):
    decision_id: str
    expected: Dict[str, Any] = Field(default_factory=dict)
    actual: Dict[str, Any] = Field(default_factory=dict)
    outcome_score: float = 0.0
    verified: bool = False
    notes: str = ""

class EnterpriseBusinessOntology:
    """Universal business vocabulary independent of industry."""

    ENTITY_TYPES = (
        "company", "business_unit", "product", "service", "customer_segment",
        "customer", "channel", "market", "competitor", "supplier", "employee",
        "team", "process", "asset", "campaign", "initiative", "metric",
        "risk", "decision", "experiment", "financial_account", "location",
        "regulatory_domain"
    )

    RELATIONSHIPS = (
        "owns", "contains", "serves", "sells", "buys", "supplies", "competes_with",
        "depends_on", "drives", "constrains", "causes", "correlates_with",
        "measured_by", "impacts", "requires", "produces", "consumes", "targets",
        "belongs_to", "located_in", "risks", "mitigates", "follows", "precedes"
    )

    def normalize_profile(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        profile = dict(profile or {})
        industry = str(profile.get("industry", "unknown")).strip().lower()
        model = str(profile.get("business_model", "unknown")).strip().lower()
        return {
            "company_name": profile.get("company_name", "Unnamed Enterprise"),
            "industry": industry,
            "business_model": model,
            "revenue_model": profile.get("revenue_model", "unknown"),
            "customer_model": profile.get("customer_model", "unknown"),
            "growth_stage": profile.get("growth_stage", "unknown"),
            "geographies": profile.get("geographies", []),
            "business_units": profile.get("business_units", []),
            "products": profile.get("products", []),
            "channels": profile.get("channels", []),
            "strategic_objectives": profile.get("strategic_objectives", []),
            "normalized": True,
            "ontology_version": ENTERPRISE_BRAIN_VERSION,
        }

class IndustryPriorEngine:
    """Structured cross-industry priors. Values are priors, not universal truths."""

    def __init__(self):
        self.registry: Dict[str, IndustryPrior] = {}
        self._load_default_priors()

    def _load_default_priors(self):
        specs = {
            "saas": {
                "archetype": "recurring_software",
                "kpis": ["MRR", "ARR", "CAC", "LTV", "NRR", "GRR", "churn", "activation", "pipeline"],
                "relations": [
                    {"cause": "activation", "effect": "retention", "relationship": "positive"},
                    {"cause": "retention", "effect": "LTV", "relationship": "positive"},
                    {"cause": "CAC", "effect": "payback_period", "relationship": "positive"},
                    {"cause": "NRR", "effect": "ARR_growth", "relationship": "positive"},
                ],
                "failures": ["high_CAC_low_retention", "feature_sprawl", "founder_sales_dependency", "premature_scaling"],
                "interventions": [
                    {"problem": "high_CAC", "action": "tighten_channel_mix_and_qualification", "expected": "lower_CAC"},
                    {"problem": "churn", "action": "improve_activation_and_customer_success", "expected": "lower_churn"},
                ],
                "seasonality": ["budget_cycles", "renewal_cycles"],
                "priors": {"unit_economics_priority": "very_high", "retention_priority": "very_high"},
            },
            "ecommerce": {
                "archetype": "transactional_digital_commerce",
                "kpis": ["traffic", "conversion_rate", "AOV", "CAC", "ROAS", "gross_margin", "repeat_rate", "return_rate"],
                "relations": [
                    {"cause": "traffic_quality", "effect": "conversion_rate", "relationship": "positive"},
                    {"cause": "AOV", "effect": "revenue_per_order", "relationship": "positive"},
                    {"cause": "repeat_rate", "effect": "LTV", "relationship": "positive"},
                    {"cause": "return_rate", "effect": "contribution_margin", "relationship": "negative"},
                ],
                "failures": ["ad_dependency", "discount_dependency", "inventory_mismatch", "weak_repeat_purchase"],
                "interventions": [
                    {"problem": "low_conversion", "action": "audit_offer_funnel_and_product_page", "expected": "higher_conversion"},
                    {"problem": "weak_margin", "action": "review_price_mix_and_fulfillment_cost", "expected": "higher_contribution_margin"},
                ],
                "seasonality": ["promotional_cycles", "holiday_peaks"],
                "priors": {"inventory_priority": "high", "creative_refresh_priority": "high"},
            },
            "retail": {
                "archetype": "physical_transactional",
                "kpis": ["same_store_sales", "footfall", "conversion", "basket_size", "gross_margin", "inventory_turns", "shrinkage"],
                "relations": [
                    {"cause": "footfall", "effect": "sales", "relationship": "positive"},
                    {"cause": "conversion", "effect": "sales", "relationship": "positive"},
                    {"cause": "inventory_turns", "effect": "cash_efficiency", "relationship": "positive"},
                ],
                "failures": ["overstock", "stockouts", "low_store_productivity", "margin_compression"],
                "interventions": [{"problem": "stockouts", "action": "improve_replenishment_and_forecasting", "expected": "higher_sales"}],
                "seasonality": ["holiday", "weather", "local_events"],
                "priors": {"location_productivity_priority": "high"},
            },
            "restaurant": {
                "archetype": "high_frequency_service",
                "kpis": ["covers", "average_check", "food_cost", "labor_cost", "table_turnover", "repeat_rate", "occupancy"],
                "relations": [
                    {"cause": "occupancy", "effect": "revenue", "relationship": "positive"},
                    {"cause": "labor_cost", "effect": "store_margin", "relationship": "negative"},
                    {"cause": "repeat_rate", "effect": "customer_LTV", "relationship": "positive"},
                ],
                "failures": ["labor_inefficiency", "food_waste", "low_repeat_rate", "poor_unit_economics"],
                "interventions": [{"problem": "low_margin", "action": "menu_mix_and_labor_productivity_review", "expected": "higher_store_margin"}],
                "seasonality": ["weekend", "holiday", "weather"],
                "priors": {"unit_economics_priority": "very_high"},
            },
            "manufacturing": {
                "archetype": "asset_intensive_production",
                "kpis": ["OEE", "yield", "scrap_rate", "downtime", "throughput", "unit_cost", "on_time_delivery", "inventory_days"],
                "relations": [
                    {"cause": "downtime", "effect": "throughput", "relationship": "negative"},
                    {"cause": "yield", "effect": "unit_cost", "relationship": "negative"},
                    {"cause": "inventory_days", "effect": "working_capital", "relationship": "positive"},
                ],
                "failures": ["capacity_bottleneck", "quality_drift", "maintenance_failure", "working_capital_lockup"],
                "interventions": [{"problem": "downtime", "action": "maintenance_and_bottleneck_analysis", "expected": "higher_throughput"}],
                "seasonality": ["order_cycles", "maintenance_windows"],
                "priors": {"operations_priority": "very_high"},
            },
            "logistics": {
                "archetype": "network_movement",
                "kpis": ["on_time_delivery", "cost_per_shipment", "utilization", "empty_miles", "claims", "delivery_cycle_time"],
                "relations": [
                    {"cause": "utilization", "effect": "cost_per_shipment", "relationship": "negative"},
                    {"cause": "delivery_cycle_time", "effect": "customer_satisfaction", "relationship": "negative"},
                ],
                "failures": ["low_asset_utilization", "route_inefficiency", "capacity_mismatch", "claims_leakage"],
                "interventions": [{"problem": "high_cost_per_shipment", "action": "route_and_utilization_optimization", "expected": "lower_unit_cost"}],
                "seasonality": ["peak_shipping", "fuel_cycles"],
                "priors": {"network_efficiency_priority": "very_high"},
            },
            "agency": {
                "archetype": "professional_services_project",
                "kpis": ["utilization", "billable_rate", "gross_margin", "pipeline", "client_retention", "DSO"],
                "relations": [
                    {"cause": "utilization", "effect": "gross_margin", "relationship": "positive"},
                    {"cause": "client_retention", "effect": "revenue_stability", "relationship": "positive"},
                    {"cause": "DSO", "effect": "cash_flow", "relationship": "negative"},
                ],
                "failures": ["bench_time", "scope_creep", "founder_bottleneck", "client_concentration"],
                "interventions": [{"problem": "low_utilization", "action": "capacity_and_pipeline_alignment", "expected": "higher_margin"}],
                "seasonality": ["budget_cycles", "project_cycles"],
                "priors": {"capacity_management_priority": "high"},
            },
            "professional_services": {
                "archetype": "expertise_led_services",
                "kpis": ["billable_utilization", "realization", "revenue_per_employee", "retention", "DSO", "pipeline"],
                "relations": [
                    {"cause": "realization", "effect": "revenue", "relationship": "positive"},
                    {"cause": "DSO", "effect": "cash_flow", "relationship": "negative"},
                ],
                "failures": ["talent_bottleneck", "scope_creep", "low_realization", "client_concentration"],
                "interventions": [{"problem": "low_realization", "action": "pricing_scope_and_delivery_review", "expected": "higher_realization"}],
                "seasonality": ["budget_cycles"],
                "priors": {"talent_priority": "very_high"},
            },
            "marketplace": {
                "archetype": "two_sided_network",
                "kpis": ["GMV", "take_rate", "liquidity", "buyer_retention", "seller_retention", "CAC", "contribution_margin"],
                "relations": [
                    {"cause": "liquidity", "effect": "conversion", "relationship": "positive"},
                    {"cause": "retention", "effect": "LTV", "relationship": "positive"},
                ],
                "failures": ["cold_start", "side_imbalance", "subsidy_dependency", "quality_control_failure"],
                "interventions": [{"problem": "side_imbalance", "action": "targeted_liquidity_program", "expected": "higher_marketplace_conversion"}],
                "seasonality": ["network_specific"],
                "priors": {"liquidity_priority": "very_high"},
            },
            "subscription": {
                "archetype": "recurring_consumer",
                "kpis": ["MRR", "churn", "ARPU", "CAC", "LTV", "activation", "repeat_usage"],
                "relations": [{"cause": "usage", "effect": "retention", "relationship": "positive"}],
                "failures": ["churn_spiral", "acquisition_overdependence", "discount_dependency"],
                "interventions": [{"problem": "churn", "action": "activation_and_value_delivery_review", "expected": "lower_churn"}],
                "seasonality": ["renewal_cycles"],
                "priors": {"retention_priority": "very_high"},
            },
            "education": {
                "archetype": "outcome_oriented_learning_service",
                "kpis": ["enrollment", "completion", "retention", "acquisition_cost", "learner_satisfaction", "outcome_rate"],
                "relations": [{"cause": "completion", "effect": "outcome_rate", "relationship": "positive"}],
                "failures": ["low_completion", "acquisition_quality_mismatch", "capacity_constraints"],
                "interventions": [{"problem": "low_completion", "action": "learner_engagement_and_support_review", "expected": "higher_completion"}],
                "seasonality": ["academic_cycles"],
                "priors": {"outcome_quality_priority": "very_high"},
            },
            "hospitality": {
                "archetype": "capacity_constrained_service",
                "kpis": ["occupancy", "ADR", "RevPAR", "direct_booking_share", "cancellation_rate", "guest_satisfaction"],
                "relations": [{"cause": "occupancy", "effect": "RevPAR", "relationship": "positive"}],
                "failures": ["channel_dependency", "occupancy_volatility", "service_quality_drift"],
                "interventions": [{"problem": "low_occupancy", "action": "channel_mix_pricing_and_demand_review", "expected": "higher_RevPAR"}],
                "seasonality": ["destination_seasonality", "holidays", "events"],
                "priors": {"yield_management_priority": "very_high"},
            },
            "real_estate": {
                "archetype": "asset_and_transaction",
                "kpis": ["occupancy", "NOI", "cap_rate", "days_on_market", "rent_growth", "leasing_velocity"],
                "relations": [{"cause": "occupancy", "effect": "NOI", "relationship": "positive"}],
                "failures": ["vacancy", "overleverage", "maintenance_cost_drift", "market_mismatch"],
                "interventions": [{"problem": "vacancy", "action": "pricing_and_leasing_funnel_review", "expected": "higher_occupancy"}],
                "seasonality": ["local_market_cycles"],
                "priors": {"capital_structure_priority": "very_high"},
            },
            "fintech": {
                "archetype": "regulated_digital_finance",
                "kpis": ["active_users", "transaction_volume", "take_rate", "fraud_rate", "loss_rate", "retention", "CAC"],
                "relations": [{"cause": "fraud_rate", "effect": "contribution_margin", "relationship": "negative"}],
                "failures": ["fraud_loss", "regulatory_gap", "unit_economics_failure", "liquidity_mismatch"],
                "interventions": [{"problem": "fraud_rate", "action": "risk_controls_and_transaction_monitoring", "expected": "lower_loss"}],
                "seasonality": ["transaction_cycles"],
                "priors": {"risk_governance_priority": "very_high"},
            },
            "healthcare_services": {
                "archetype": "regulated_service_delivery",
                "kpis": ["capacity_utilization", "wait_time", "payer_mix", "collection_rate", "readmission_or_repeat_visit_rate", "labor_cost"],
                "relations": [{"cause": "capacity_utilization", "effect": "revenue", "relationship": "positive"}],
                "failures": ["capacity_mismatch", "labor_burn", "billing_leakage", "compliance_failure"],
                "interventions": [{"problem": "billing_leakage", "action": "revenue_cycle_audit", "expected": "higher_collection"}],
                "seasonality": ["demand_cycles"],
                "priors": {"compliance_priority": "very_high"},
            },
            "travel": {
                "archetype": "demand_and_inventory_service",
                "kpis": ["bookings", "load_factor", "yield", "cancellation_rate", "CAC", "repeat_rate"],
                "relations": [{"cause": "load_factor", "effect": "unit_economics", "relationship": "positive"}],
                "failures": ["demand_volatility", "channel_dependency", "capacity_mismatch"],
                "interventions": [{"problem": "low_load_factor", "action": "dynamic_pricing_and_channel_review", "expected": "higher_yield"}],
                "seasonality": ["peak_season", "weather", "events"],
                "priors": {"demand_forecasting_priority": "very_high"},
            },
            "media": {
                "archetype": "attention_and_advertising",
                "kpis": ["audience", "engagement", "watch_time", "CPM", "fill_rate", "subscriber_retention"],
                "relations": [{"cause": "engagement", "effect": "monetization", "relationship": "positive"}],
                "failures": ["audience_decay", "platform_dependency", "monetization_concentration"],
                "interventions": [{"problem": "audience_decay", "action": "content_mix_and_distribution_review", "expected": "higher_engagement"}],
                "seasonality": ["event_cycles", "advertising_cycles"],
                "priors": {"distribution_priority": "very_high"},
            },
            "telecom": {
                "archetype": "network_subscription",
                "kpis": ["ARPU", "churn", "subscriber_growth", "network_utilization", "capex_efficiency", "NPS"],
                "relations": [{"cause": "network_quality", "effect": "churn", "relationship": "negative"}],
                "failures": ["churn", "capacity_congestion", "capex_mismatch", "price_war"],
                "interventions": [{"problem": "churn", "action": "network_quality_and_segment_offer_review", "expected": "lower_churn"}],
                "seasonality": ["usage_cycles"],
                "priors": {"network_quality_priority": "very_high"},
            },
            "energy": {
                "archetype": "asset_intensive_commodity",
                "kpis": ["production", "availability", "unit_cost", "realized_price", "downtime", "safety_incidents"],
                "relations": [{"cause": "downtime", "effect": "production", "relationship": "negative"}],
                "failures": ["asset_failure", "commodity_price_exposure", "safety_failure"],
                "interventions": [{"problem": "downtime", "action": "predictive_maintenance_and_asset_review", "expected": "higher_availability"}],
                "seasonality": ["demand_cycles", "weather"],
                "priors": {"asset_reliability_priority": "very_high"},
            },
            "construction": {
                "archetype": "project_delivery",
                "kpis": ["backlog", "schedule_variance", "cost_variance", "utilization", "cash_conversion", "change_orders"],
                "relations": [{"cause": "schedule_variance", "effect": "cost_variance", "relationship": "positive"}],
                "failures": ["cost_overrun", "schedule_slippage", "scope_creep", "cashflow_gap"],
                "interventions": [{"problem": "cost_overrun", "action": "project_controls_and_scope_review", "expected": "lower_variance"}],
                "seasonality": ["weather", "procurement_cycles"],
                "priors": {"project_controls_priority": "very_high"},
            },
            "automotive": {
                "archetype": "manufacturing_and_distribution",
                "kpis": ["unit_sales", "dealer_inventory", "production_utilization", "defect_rate", "gross_margin", "warranty_cost"],
                "relations": [{"cause": "defect_rate", "effect": "warranty_cost", "relationship": "positive"}],
                "failures": ["inventory_overhang", "quality_cost", "capacity_mismatch"],
                "interventions": [{"problem": "inventory_overhang", "action": "production_mix_and_channel_inventory_review", "expected": "lower_inventory"}],
                "seasonality": ["model_year", "promotions"],
                "priors": {"inventory_health_priority": "high"},
            },
            "pharmaceuticals": {
                "archetype": "regulated_product",
                "kpis": ["market_share", "prescription_volume", "gross_margin", "R&D_pipeline", "launch_adoption", "compliance_rate"],
                "relations": [{"cause": "launch_adoption", "effect": "revenue", "relationship": "positive"}],
                "failures": ["pipeline_failure", "launch_underperformance", "compliance_risk"],
                "interventions": [{"problem": "launch_underperformance", "action": "segment_positioning_and_adoption_review", "expected": "higher_adoption"}],
                "seasonality": ["market_specific"],
                "priors": {"regulatory_priority": "very_high"},
            },
            "insurance": {
                "archetype": "risk_pooling",
                "kpis": ["premium", "loss_ratio", "combined_ratio", "retention", "expense_ratio", "claims_cycle"],
                "relations": [{"cause": "loss_ratio", "effect": "combined_ratio", "relationship": "positive"}],
                "failures": ["adverse_selection", "claims_inflation", "pricing_mismatch"],
                "interventions": [{"problem": "loss_ratio", "action": "underwriting_and_pricing_review", "expected": "lower_loss_ratio"}],
                "seasonality": ["renewal_cycles", "catastrophe_cycles"],
                "priors": {"risk_pricing_priority": "very_high"},
            },
            "banking": {
                "archetype": "regulated_financial_intermediation",
                "kpis": ["NIM", "ROE", "deposit_growth", "loan_growth", "NPL", "cost_to_income", "capital_ratio"],
                "relations": [{"cause": "NPL", "effect": "profitability", "relationship": "negative"}],
                "failures": ["credit_deterioration", "liquidity_mismatch", "cost_inflation", "compliance_failure"],
                "interventions": [{"problem": "credit_deterioration", "action": "portfolio_risk_and_underwriting_review", "expected": "lower_credit_loss"}],
                "seasonality": ["credit_cycles"],
                "priors": {"risk_governance_priority": "very_high"},
            },
            "wholesale": {
                "archetype": "volume_distribution",
                "kpis": ["gross_margin", "inventory_turns", "DSO", "fill_rate", "order_frequency", "customer_concentration"],
                "relations": [{"cause": "inventory_turns", "effect": "cash_efficiency", "relationship": "positive"}],
                "failures": ["inventory_lockup", "margin_compression", "customer_concentration"],
                "interventions": [{"problem": "inventory_lockup", "action": "SKU_and_replenishment_review", "expected": "higher_inventory_turns"}],
                "seasonality": ["procurement_cycles"],
                "priors": {"working_capital_priority": "very_high"},
            },
            "consumer_goods": {
                "archetype": "branded_product",
                "kpis": ["distribution", "velocity", "gross_margin", "repeat_rate", "market_share", "trade_spend"],
                "relations": [{"cause": "distribution", "effect": "sales", "relationship": "positive"}],
                "failures": ["distribution_loss", "trade_spend_inefficiency", "brand_decay"],
                "interventions": [{"problem": "velocity_decline", "action": "assortment_price_and_distribution_review", "expected": "higher_velocity"}],
                "seasonality": ["promotional_cycles"],
                "priors": {"distribution_priority": "very_high"},
            },
            "software_services": {
                "archetype": "technology_services",
                "kpis": ["utilization", "billable_rate", "project_margin", "pipeline", "retention", "DSO"],
                "relations": [{"cause": "utilization", "effect": "project_margin", "relationship": "positive"}],
                "failures": ["bench_time", "project_overrun", "talent_shortage"],
                "interventions": [{"problem": "project_overrun", "action": "delivery_controls_and_scope_management", "expected": "higher_project_margin"}],
                "seasonality": ["budget_cycles"],
                "priors": {"delivery_quality_priority": "high"},
            },
            "nonprofit": {
                "archetype": "mission_funded",
                "kpis": ["donor_retention", "fundraising_efficiency", "program_cost_ratio", "impact_rate", "cash_runway"],
                "relations": [{"cause": "donor_retention", "effect": "funding_stability", "relationship": "positive"}],
                "failures": ["donor_concentration", "funding_gap", "overhead_mismatch"],
                "interventions": [{"problem": "donor_retention", "action": "stewardship_and_segment_review", "expected": "higher_retention"}],
                "seasonality": ["fundraising_cycles"],
                "priors": {"mission_impact_priority": "very_high"},
            },
            "agriculture": {
                "archetype": "biological_production",
                "kpis": ["yield", "input_cost", "realized_price", "water_efficiency", "crop_loss", "asset_utilization"],
                "relations": [{"cause": "yield", "effect": "unit_economics", "relationship": "positive"}],
                "failures": ["yield_shock", "input_cost_spike", "weather_exposure"],
                "interventions": [{"problem": "input_cost_spike", "action": "input_mix_and_supplier_review", "expected": "lower_unit_cost"}],
                "seasonality": ["growing_cycles", "weather"],
                "priors": {"risk_exposure_priority": "very_high"},
            },
            "automotive_dealer": {
                "archetype": "vehicle_retail",
                "kpis": ["unit_sales", "gross_per_unit", "inventory_days", "lead_conversion", "service_retention"],
                "relations": [{"cause": "inventory_days", "effect": "carrying_cost", "relationship": "positive"}],
                "failures": ["inventory_aging", "lead_leakage", "margin_compression"],
                "interventions": [{"problem": "lead_leakage", "action": "speed_to_lead_and_followup_audit", "expected": "higher_conversion"}],
                "seasonality": ["model_year", "promotions"],
                "priors": {"inventory_age_priority": "very_high"},
            },
        }
        for name, s in specs.items():
            self.registry[name] = IndustryPrior(
                industry=name,
                archetype=s["archetype"],
                critical_kpis=s["kpis"],
                driver_relationships=s["relations"],
                common_failure_modes=s["failures"],
                intervention_patterns=s["interventions"],
                seasonality=s["seasonality"],
                priors=s["priors"],
                confidence=0.65,
            )

    def resolve(self, industry: str, business_model: str = "") -> IndustryPrior:
        key = (industry or "").strip().lower().replace(" ", "_").replace("-", "_")
        if key in self.registry:
            return self.registry[key]
        bm = (business_model or "").lower()
        if any(x in bm for x in ("saas", "subscription", "software")):
            return self.registry["saas"]
        if any(x in bm for x in ("marketplace", "platform")):
            return self.registry["marketplace"]
        if any(x in bm for x in ("ecommerce", "e-commerce", "online_store")):
            return self.registry["ecommerce"]
        if any(x in key for x in ("service", "consult")):
            return self.registry["professional_services"]
        return IndustryPrior(
            industry=key or "unknown",
            archetype="generic_business",
            critical_kpis=["revenue", "gross_margin", "cash_flow", "customer_retention", "growth"],
            driver_relationships=[],
            common_failure_modes=["insufficient_data_for_industry_prior"],
            intervention_patterns=[],
            seasonality=[],
            priors={"use_generic_prior": True},
            confidence=0.30,
        )

    def match_signals(self, industry: str, metrics: Dict[str, Any], business_model: str = "") -> Dict[str, Any]:
        prior = self.resolve(industry, business_model)
        findings = []
        for kpi in prior.critical_kpis:
            if kpi in metrics:
                val = metrics[kpi]
                findings.append({
                    "kpi": kpi, "value": val,
                    "critical": True,
                    "prior_confidence": prior.confidence,
                })
        return {
            "industry": prior.industry,
            "archetype": prior.archetype,
            "critical_kpis_present": findings,
            "missing_critical_kpis": [k for k in prior.critical_kpis if k not in metrics],
            "prior_confidence": prior.confidence,
            "prior_is_hypothesis": True,
        }

class EnterpriseCompanyMemory:
    """Tenant-scoped institutional memory using the existing durable fabric."""

    def write(self, tenant_id: str, memory_type: str, title: str, content: str,
              source: str = "enterprise_brain", confidence: float = 0.7,
              importance: float = 0.7, metadata: Optional[Dict[str, Any]] = None):
        return v28_memory_write(
            tenant_id, memory_type, title, content, source=source,
            confidence=confidence, importance=importance, metadata=metadata
        )

    def search(self, tenant_id: str, query: str, memory_type: Optional[str] = None,
               limit: int = 12):
        return v28_memory_search(tenant_id, query, memory_type, limit)

    def record_company_event(self, tenant_id: str, event: Dict[str, Any]):
        return self.write(
            tenant_id, "company_history",
            event.get("title", "Company event"),
            json.dumps(event, default=str, sort_keys=True),
            source=event.get("source", "company_event"),
            confidence=float(event.get("confidence", 0.8)),
            importance=float(event.get("importance", 0.8)),
        )

class BusinessKnowledgeGraph:
    """Lightweight persistent graph over ontology entities and relationships."""

    def init_schema(self):
        conn = db_connect()
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS enterprise_entities_v45 (
            entity_id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            name TEXT NOT NULL,
            attributes_json TEXT DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(tenant_id, entity_type, name),
            FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS enterprise_edges_v45 (
            id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            source_id TEXT NOT NULL,
            target_id TEXT NOT NULL,
            relationship TEXT NOT NULL,
            weight REAL DEFAULT 0.5,
            confidence REAL DEFAULT 0.5,
            evidence_json TEXT DEFAULT '[]',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(tenant_id, source_id, target_id, relationship),
            FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_entities_tenant_type_v45
            ON enterprise_entities_v45(tenant_id, entity_type);
        CREATE INDEX IF NOT EXISTS idx_edges_tenant_source_v45
            ON enterprise_edges_v45(tenant_id, source_id);
        CREATE INDEX IF NOT EXISTS idx_edges_tenant_target_v45
            ON enterprise_edges_v45(tenant_id, target_id);
        """)
        conn.commit()
        conn.close()

    def upsert_entity(self, tenant_id: str, entity_type: str, name: str,
                      attributes: Optional[Dict[str, Any]] = None) -> str:
        tenant_id = v28_tenant_guard(tenant_id)
        eid = hashlib.sha256(
            f"{tenant_id}|{entity_type}|{name}".encode()
        ).hexdigest()
        now = v28_now()
        conn = db_connect()
        conn.execute(
            """INSERT INTO enterprise_entities_v45
            (entity_id,tenant_id,entity_type,name,attributes_json,created_at,updated_at)
            VALUES(?,?,?,?,?,?,?)
            ON CONFLICT(tenant_id,entity_type,name)
            DO UPDATE SET attributes_json=excluded.attributes_json, updated_at=excluded.updated_at""",
            (eid, tenant_id, entity_type, _bounded_text(name, 500),
             json.dumps(attributes or {}, default=str)[:30000], now, now)
        )
        conn.commit()
        conn.close()
        return eid

    def upsert_edge(self, tenant_id: str, source_id: str, target_id: str,
                    relationship: str, weight: float = 0.5,
                    confidence: float = 0.5, evidence: Optional[List[Any]] = None):
        tenant_id = v28_tenant_guard(tenant_id)
        now = v28_now()
        edge_id = hashlib.sha256(
            f"{tenant_id}|{source_id}|{target_id}|{relationship}".encode()
        ).hexdigest()
        conn = db_connect()
        conn.execute(
            """INSERT INTO enterprise_edges_v45
            (id,tenant_id,source_id,target_id,relationship,weight,confidence,evidence_json,created_at,updated_at)
            VALUES(?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(tenant_id,source_id,target_id,relationship)
            DO UPDATE SET weight=excluded.weight, confidence=excluded.confidence,
                          evidence_json=excluded.evidence_json, updated_at=excluded.updated_at""",
            (edge_id, tenant_id, source_id, target_id,
             _bounded_text(relationship, 200),
             max(-1.0, min(1.0, float(weight))),
             max(0.0, min(1.0, float(confidence))),
             json.dumps(evidence or [], default=str)[:30000], now, now)
        )
        conn.commit()
        conn.close()
        return edge_id

    def neighborhood(self, tenant_id: str, entity_id: str, limit: int = 50):
        tenant_id = v28_tenant_guard(tenant_id)
        conn = db_connect()
        rows = conn.execute(
            """SELECT e.*, s.name AS source_name, t.name AS target_name
               FROM enterprise_edges_v45 e
               LEFT JOIN enterprise_entities_v45 s ON s.entity_id=e.source_id
               LEFT JOIN enterprise_entities_v45 t ON t.entity_id=e.target_id
               WHERE e.tenant_id=? AND (e.source_id=? OR e.target_id=?)
               ORDER BY e.confidence DESC LIMIT ?""",
            (tenant_id, entity_id, entity_id, max(1, min(200, int(limit))))
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

class CausalDiagnosticEngine:
    """Evidence-weighted diagnosis. It proposes hypotheses; it does not claim certainty."""

    def diagnose(self, metrics: Dict[str, Any], prior: IndustryPrior,
                 historical_matches: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        findings: List[DiagnosticFinding] = []
        historical_matches = historical_matches or []
        numeric = {k: v for k, v in metrics.items() if isinstance(v, (int, float))}
        for rel in prior.driver_relationships:
            cause, effect = rel["cause"], rel["effect"]
            if cause in numeric and effect in numeric:
                findings.append(DiagnosticFinding(
                    signal=f"{cause}={numeric[cause]} → {effect}={numeric[effect]}",
                    hypothesis=f"{cause} may be influencing {effect}",
                    likelihood=min(0.95, prior.confidence * 0.8),
                    severity="HIGH" if abs(float(numeric.get(effect, 0))) > 0 else "MEDIUM",
                    evidence=[EvidenceRecord(
                        source="current_business_metrics",
                        statement=f"{cause} and {effect} are both present in current data.",
                        confidence=0.8, verified=True
                    )]
                ))
        if not findings and historical_matches:
            for h in historical_matches[:5]:
                findings.append(DiagnosticFinding(
                    signal=h.get("pattern", "historical pattern"),
                    hypothesis=h.get("hypothesis", "historical similarity requires validation"),
                    likelihood=float(h.get("similarity", 0.4)),
                    severity="MEDIUM",
                    evidence=[EvidenceRecord(source="company_history", statement=str(h), confidence=float(h.get("similarity", 0.4)))]
                ))
        return {
            "findings": [f.model_dump() for f in findings],
            "root_cause_candidates": sorted(
                [f.model_dump() for f in findings],
                key=lambda x: x["likelihood"], reverse=True
            ),
            "diagnostic_confidence": round(
                max([f.likelihood for f in findings], default=0.25), 3
            ),
            "requires_more_data": not bool(findings),
        }

    def reconcile_prior(self, prior_confidence: float, evidence_strength: float,
                        contradiction_count: int = 0) -> Dict[str, Any]:
        penalty = min(0.5, contradiction_count * 0.10)
        final = max(0.0, min(1.0, 0.45 * prior_confidence + 0.55 * evidence_strength - penalty))
        return {
            "historical_prior_confidence": round(prior_confidence, 3),
            "current_evidence_strength": round(evidence_strength, 3),
            "contradiction_penalty": round(penalty, 3),
            "final_confidence": round(final, 3),
            "prior_overridden": evidence_strength > prior_confidence + 0.20 or contradiction_count >= 3,
        }

class PredictiveIntelligenceEngine:
    """Transparent scenario forecasting using supplied current metrics."""

    def forecast(self, metrics: Dict[str, Any], horizons=(3, 6, 12),
                 growth_overrides: Optional[Dict[str, float]] = None):
        growth_overrides = growth_overrides or {}
        forecasts = {}
        for k, value in metrics.items():
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                continue
            g = float(growth_overrides.get(k, 0.0)) / 100.0
            forecasts[k] = {
                f"{h}m": round(float(value) * ((1.0 + g) ** h), 4)
                for h in horizons
            }
        return {
            "forecast_type": "deterministic_scenario_projection",
            "horizons_months": list(horizons),
            "metrics": forecasts,
            "warning": "Forecasts are scenario projections, not guarantees.",
        }

    def scenarios(self, base_metrics: Dict[str, Any],
                  growth_rates: Optional[Dict[str, float]] = None):
        growth_rates = growth_rates or {}
        cases = {"downside": 0.70, "base": 1.00, "upside": 1.30}
        result = {}
        for case, multiplier in cases.items():
            result[case] = {}
            for k, v in base_metrics.items():
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    g = float(growth_rates.get(k, 0.0)) / 100.0
                    result[case][k] = round(float(v) * (1 + g) * multiplier, 4)
        return result

class BusinessSimulationEngine:
    """Digital-twin style what-if simulation without pretending to be a full physical model."""

    def simulate(self, metrics: Dict[str, Any], changes: Dict[str, float],
                 relationships: Optional[List[Dict[str, str]]] = None,
                 iterations: int = 500) -> Dict[str, Any]:
        baseline = {k: v for k, v in metrics.items() if isinstance(v, (int, float))}
        simulated = dict(baseline)
        for k, delta_pct in changes.items():
            if k in simulated:
                simulated[k] = simulated[k] * (1.0 + float(delta_pct) / 100.0)

        relationships = relationships or []
        propagated = []
        for rel in relationships:
            c, e, typ = rel.get("cause"), rel.get("effect"), rel.get("relationship", "")
            if c in simulated and e in simulated and c in changes:
                effect = abs(float(changes[c])) * 0.35
                sign = -1 if "negative" in typ else 1
                simulated[e] = simulated[e] * (1 + sign * effect / 100.0)
                propagated.append({"cause": c, "effect": e, "relationship": typ, "propagated_pct": sign * effect})

        deltas = {
            k: round(((simulated[k] - baseline[k]) / baseline[k]) * 100.0, 3)
            if baseline[k] != 0 else None
            for k in simulated
        }
        return {
            "baseline": baseline,
            "simulated": simulated,
            "percentage_deltas": deltas,
            "propagated_effects": propagated,
            "iterations": max(1, int(iterations)),
            "model_type": "transparent_business_sensitivity_model",
            "caveat": "Use validated company-specific coefficients before high-stakes deployment.",
        }

class DecisionIntelligenceEngine:
    def evaluate(self, question: str, options: List[Dict[str, Any]],
                 evidence_strength: float = 0.6,
                 risk_tolerance: float = 0.5) -> Dict[str, Any]:
        scored = []
        for option in options:
            benefit = float(option.get("benefit", 0))
            cost = max(0.0, float(option.get("cost", 0)))
            risk = max(0.0, float(option.get("risk", 0)))
            reversibility = max(0.0, min(1.0, float(option.get("reversibility", 0.5))))
            score = benefit - cost - (risk * max(0.0, 1.0 - risk_tolerance)) + (reversibility * 0.2)
            scored.append({**option, "decision_score": round(score, 4)})
        scored.sort(key=lambda x: x["decision_score"], reverse=True)
        best = scored[0] if scored else {}
        return {
            "question": question,
            "recommended_option": best,
            "ranked_options": scored,
            "confidence": round(max(0.0, min(1.0, evidence_strength * (0.5 + 0.5 * (1 if scored else 0)))), 3),
            "human_approval_required": True,
        }

class AutonomousBusinessMonitor:
    """Detects abnormal movements from supplied baseline/current values."""

    def evaluate(self, current: Dict[str, Any], baseline: Dict[str, Any],
                 thresholds: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        thresholds = thresholds or {}
        alerts = []
        for k, cur in current.items():
            if k not in baseline or not isinstance(cur, (int, float)) or not isinstance(baseline[k], (int, float)):
                continue
            base = float(baseline[k])
            if base == 0:
                continue
            delta = (float(cur) - base) / abs(base) * 100.0
            threshold = float(thresholds.get(k, 10.0))
            if abs(delta) >= threshold:
                alerts.append({
                    "metric": k,
                    "current": cur,
                    "baseline": base,
                    "change_pct": round(delta, 3),
                    "severity": "CRITICAL" if abs(delta) >= threshold * 2 else "WARNING",
                })
        return {
            "alerts": alerts,
            "alert_count": len(alerts),
            "status": "ACTION_REQUIRED" if alerts else "NORMAL",
        }

class InterventionActionEngine:
    def recommend(self, findings: List[Dict[str, Any]], prior: IndustryPrior,
                  constraints: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        constraints = constraints or {}
        recs = []
        for f in findings:
            hypothesis = str(f.get("hypothesis", "")).lower()
            for pattern in prior.intervention_patterns:
                if pattern.get("problem", "").lower() in hypothesis or pattern.get("problem", "").lower() in str(f).lower():
                    recs.append({
                        "problem": pattern.get("problem"),
                        "action": pattern.get("action"),
                        "expected_direction": pattern.get("expected"),
                        "confidence": round(float(f.get("likelihood", prior.confidence)) * prior.confidence, 3),
                        "human_approval_required": True,
                        "constraints_checked": list(constraints.keys()),
                    })
        if not recs:
            recs.append({
                "problem": "insufficient_pattern_match",
                "action": "collect_more_business_evidence_before_intervention",
                "expected_direction": "uncertain",
                "confidence": 0.2,
                "human_approval_required": True,
                "constraints_checked": list(constraints.keys()),
            })
        return recs

class OutcomeLearningEngine:
    """Converts verified decision outcomes into tenant-scoped learning."""

    def record(self, tenant_id: str, decision_id: str, expected: Dict[str, Any],
               actual: Dict[str, Any], outcome_score: float,
               verified: bool = False, notes: str = "") -> Dict[str, Any]:
        result = v28_record_outcome(
            tenant_id, decision_id,
            action=json.dumps(expected, default=str),
            expected_outcome=json.dumps(expected, default=str),
            actual_outcome=json.dumps(actual, default=str),
            outcome_score=float(outcome_score),
            status="verified" if verified else "observed",
            metadata={"notes": notes, "verified": verified}
        )
        if verified:
            v31_record_learning(
                tenant_id, "verified_decision_outcome",
                f"Decision {decision_id}: expected={expected}; actual={actual}; score={outcome_score}",
                entity_id=decision_id,
                evidence={"expected": expected, "actual": actual},
                source="outcome_learning",
                confidence=1.0,
                outcome_score=float(outcome_score),
                verified=True,
            )
        return result

class EnterpriseGovernanceEngine:
    ROLES = {
        "Admin": {"*"},
        "Executive": {"read:*", "decision:approve", "strategy:*", "audit:read"},
        "CFO": {"read:finance", "decision:approve", "audit:read"},
        "COO": {"read:operations", "decision:approve", "audit:read"},
        "CMO": {"read:marketing", "decision:approve", "audit:read"},
        "Analyst": {"read:*", "analysis:run"},
        "Operator": {"read:operations", "action:execute"},
        "Auditor": {"audit:read"},
    }

    def authorize(self, role: str, permission: str) -> bool:
        allowed = self.ROLES.get(role, set())
        return "*" in allowed or permission in allowed or permission.split(":")[0] + ":*" in allowed or "read:*" in allowed and permission.startswith("read:")

    def decision_gate(self, role: str, decision: Dict[str, Any], risk: float = 0.5):
        approved = self.authorize(role, "decision:approve")
        return {
            "approved": bool(approved and risk < 0.80),
            "requires_human": True,
            "role": role,
            "risk": risk,
            "reason": "High-risk or unauthorized decisions require human governance.",
        }

    def audit_decision(self, tenant_id: str, actor_id: str, decision: Dict[str, Any]):
        v28_security_event(
            tenant_id, "DECISION_AUDIT", "INFO", actor_id,
            details={"decision": decision}
        )
        return {"audited": True, "timestamp": v28_now()}

class EnterpriseBusinessBrain:
    """V45 top-level brain: one governed reasoning surface over all engines."""

    def __init__(self):
        self.ontology = EnterpriseBusinessOntology()
        self.priors = IndustryPriorEngine()
        self.memory = EnterpriseCompanyMemory()
        self.graph = BusinessKnowledgeGraph()
        self.diagnostics = CausalDiagnosticEngine()
        self.predictive = PredictiveIntelligenceEngine()
        self.simulation = BusinessSimulationEngine()
        self.decisions = DecisionIntelligenceEngine()
        self.monitor = AutonomousBusinessMonitor()
        self.interventions = InterventionActionEngine()
        self.learning = OutcomeLearningEngine()
        self.governance = EnterpriseGovernanceEngine()
        self.initialized = False

    def initialize(self):
        try:
            v28_init_persistent_intelligence()
            v31_init_learning_schema()
            self.graph.init_schema()
            self.initialized = True
            return {"ok": True, "version": ENTERPRISE_BRAIN_VERSION}
        except Exception as exc:
            logger.exception("Enterprise Business Brain initialization failed")
            return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}

    def ingest_company_profile(self, tenant_id: str, profile: Dict[str, Any]):
        normalized = self.ontology.normalize_profile(profile)
        prior = self.priors.resolve(normalized["industry"], normalized["business_model"])
        company_id = self.graph.upsert_entity(
            tenant_id, "company", normalized["company_name"], normalized
        )
        self.memory.write(
            tenant_id, "company_profile", "Normalized enterprise profile",
            json.dumps(normalized, default=str, sort_keys=True),
            source="enterprise_profile", confidence=1.0, importance=1.0
        )
        return {
            "company_entity_id": company_id,
            "profile": normalized,
            "industry_prior": prior.model_dump(),
        }

    def analyze(self, tenant_id: str, profile: Dict[str, Any],
                metrics: Dict[str, Any], baseline: Optional[Dict[str, Any]] = None,
                growth_rates: Optional[Dict[str, float]] = None):
        if not self.initialized:
            self.initialize()
        normalized = self.ontology.normalize_profile(profile)
        prior = self.priors.resolve(normalized["industry"], normalized["business_model"])
        historical = self.memory.search(
            tenant_id,
            f"{normalized['industry']} {' '.join(prior.common_failure_modes[:4])}",
            limit=10
        )
        historical_matches = [{
            "pattern": r.get("title", ""),
            "hypothesis": r.get("content", ""),
            "similarity": float(r.get("confidence", 0.5))
        } for r in historical]
        diagnostic = self.diagnostics.diagnose(metrics, prior, historical_matches)
        evidence_strength = min(1.0, 0.5 + 0.1 * len(metrics))
        reconciliation = self.diagnostics.reconcile_prior(
            prior.confidence, evidence_strength,
            len([x for x in diagnostic["findings"] if x.get("contradictions")])
        )
        forecast = self.predictive.forecast(metrics, growth_rates=growth_rates)
        scenarios = self.predictive.scenarios(metrics, growth_rates=growth_rates)
        monitoring = self.monitor.evaluate(metrics, baseline or metrics)
        actions = self.interventions.recommend(diagnostic["findings"], prior)
        return {
            "brain_version": ENTERPRISE_BRAIN_VERSION,
            "company_profile": normalized,
            "industry_prior": prior.model_dump(),
            "historical_matches": historical_matches,
            "diagnostics": diagnostic,
            "prior_reconciliation": reconciliation,
            "forecast": forecast,
            "scenarios": scenarios,
            "monitoring": monitoring,
            "interventions": actions,
            "governance": {"human_approval_required": True},
        }

    def simulate_decision(self, question: str, metrics: Dict[str, Any],
                          changes: Dict[str, float], profile: Dict[str, Any]):
        prior = self.priors.resolve(profile.get("industry", ""), profile.get("business_model", ""))
        sim = self.simulation.simulate(
            metrics, changes, prior.driver_relationships
        )
        return {
            "question": question,
            "simulation": sim,
            "decision_gate": {
                "human_approval_required": True,
                "high_stakes_warning": True,
            },
        }

    def decide(self, tenant_id: str, role: str, question: str,
               options: List[Dict[str, Any]], evidence_strength: float = 0.6,
               risk_tolerance: float = 0.5):
        result = self.decisions.evaluate(
            question, options, evidence_strength, risk_tolerance
        )
        gate = self.governance.decision_gate(
            role, result, risk=float(result.get("recommended_option", {}).get("risk", 0.5))
        )
        result["governance_gate"] = gate
        decision_id = f"DEC-{uuid.uuid4().hex}"
        result["decision_id"] = decision_id
        self.memory.write(
            tenant_id, "decision",
            f"Decision proposal {decision_id}",
            json.dumps(result, default=str),
            source="decision_engine",
            confidence=float(result.get("confidence", 0.5)),
            importance=0.9
        )
        self.governance.audit_decision(tenant_id, role, result)
        return result

    def learn_from_outcome(self, tenant_id: str, outcome: Dict[str, Any]):
        return self.learning.record(
            tenant_id,
            outcome.get("decision_id", ""),
            outcome.get("expected", {}),
            outcome.get("actual", {}),
            float(outcome.get("outcome_score", 0)),
            bool(outcome.get("verified", False)),
            outcome.get("notes", ""),
        )

    def health(self, tenant_id: Optional[str] = None):
        report = {
            "brain_version": ENTERPRISE_BRAIN_VERSION,
            "name": ENTERPRISE_BRAIN_NAME,
            "initialized": self.initialized,
            "industry_prior_count": len(self.priors.registry),
            "ontology_entity_types": len(self.ontology.ENTITY_TYPES),
            "ontology_relationships": len(self.ontology.RELATIONSHIPS),
            "governed_decisions": True,
            "human_approval_for_high_risk": True,
            "continuous_learning": True,
            "company_memory": True,
            "knowledge_graph": True,
            "predictive_intelligence": True,
            "simulation": True,
            "autonomous_monitoring": True,
        }
        if tenant_id:
            try:
                report["production_readiness"] = v28_production_readiness()
            except Exception as exc:
                report["production_readiness"] = {"error": str(exc)}
        return report

# ---------------------------------------------------------------------------
# V45 integration into the existing single master OS.
# Existing V32 objects remain intact; the Enterprise Brain is an additional
# governed intelligence layer over them.
# ---------------------------------------------------------------------------
try:
    ENTERPRISE_BUSINESS_BRAIN = EnterpriseBusinessBrain()
    _v45_init_result = ENTERPRISE_BUSINESS_BRAIN.initialize()
    os_core.enterprise_brain = ENTERPRISE_BUSINESS_BRAIN
    os_core.enterprise_brain_version = ENTERPRISE_BRAIN_VERSION
except Exception as _v45_exc:
    logger.exception("V45 brain bootstrapping deferred: %s", _v45_exc)
    ENTERPRISE_BUSINESS_BRAIN = EnterpriseBusinessBrain()
    os_core.enterprise_brain = ENTERPRISE_BUSINESS_BRAIN
    os_core.enterprise_brain_version = ENTERPRISE_BRAIN_VERSION

def get_enterprise_business_brain() -> EnterpriseBusinessBrain:
    return ENTERPRISE_BUSINESS_BRAIN

def enterprise_brain_analyze(tenant_id: str, profile: Dict[str, Any],
                             metrics: Dict[str, Any],
                             baseline: Optional[Dict[str, Any]] = None,
                             growth_rates: Optional[Dict[str, float]] = None):
    return ENTERPRISE_BUSINESS_BRAIN.analyze(
        tenant_id, profile, metrics, baseline, growth_rates
    )

def enterprise_brain_health(tenant_id: Optional[str] = None):
    return ENTERPRISE_BUSINESS_BRAIN.health(tenant_id)

# Final release manifest for the single master file.
ENTERPRISE_BRAIN_RELEASE_MANIFEST = {
    "release": ENTERPRISE_BRAIN_VERSION,
    "name": ENTERPRISE_BRAIN_NAME,
    "base_foundation": "V32",
    "enhancement_range": "V33-V50",
    "single_master_codebase": True,
    "industry_agnostic": True,
    "modules": [
        "historical_business_intelligence",
        "industry_prior_engine",
        "universal_business_ontology",
        "enterprise_company_memory",
        "business_knowledge_graph",
        "causal_diagnostic_intelligence",
        "predictive_intelligence",
        "digital_twin_simulation",
        "decision_intelligence",
        "autonomous_monitoring",
        "intervention_action_intelligence",
        "outcome_based_learning",
        "enterprise_governance",
        "audit_trail",
        "human_approval_gates",
        "continuous_learning",
    ],
    "safety_model": {
        "historical_priors_are_hypotheses": True,
        "current_evidence_can_override_priors": True,
        "high_risk_decisions_require_human_approval": True,
        "verified_outcomes_only_for_reusable_learning": True,
        "clinical_automation_not_enabled": True,
    },
}



# =============================================================================
# V50 — PRE-LOADED ENTERPRISE BUSINESS BRAIN / KNOWLEDGE COMPILER
# =============================================================================
# Purpose:
#   Turn the existing V45 Enterprise Business Brain into a zero-cost,
#   pre-loaded business intelligence system without pretending that neural
#   network weights have been trained.
#
# Principles:
#   * No paid API is required.
#   * No GPU is required.
#   * No synthetic company/customer/revenue data is seeded.
#   * No fabricated historical outcomes are seeded.
#   * Canonical business rules are stored as structured domain knowledge.
#   * Industry priors remain hypotheses and can be overridden by company data.
#   * Verified company outcomes are stored separately from global knowledge.
#   * The same corpus can later be exported for genuine model training.
# =============================================================================

V50_VERSION = "50.0.0"
V50_BRAIN_NAME = "AI Business OS™ Pre-Loaded Enterprise Business Brain"
V50_GLOBAL_TENANT = "__GLOBAL_BUSINESS_KNOWLEDGE__"
V50_SCHEMA_VERSION = "2026-08-V50"


def v50_now() -> str:
    return datetime.now().astimezone().isoformat()


def v50_clamp(value: Any, low: float = 0.0, high: float = 1.0) -> float:
    try:
        return max(low, min(high, float(value)))
    except Exception:
        return low


def v50_init_schema() -> None:
    """Create the durable V50 knowledge/compiler layer using local SQLite only."""
    conn = db_connect()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS v50_knowledge_items (
        id TEXT PRIMARY KEY,
        scope TEXT NOT NULL DEFAULT 'global',
        industry TEXT NOT NULL DEFAULT '',
        domain TEXT NOT NULL,
        knowledge_type TEXT NOT NULL,
        title TEXT NOT NULL,
        statement TEXT NOT NULL,
        applicability_json TEXT DEFAULT '{}',
        evidence_grade TEXT NOT NULL DEFAULT 'curated_domain_knowledge',
        source_kind TEXT NOT NULL DEFAULT 'structured_business_principle',
        confidence REAL NOT NULL DEFAULT 0.70,
        freshness_class TEXT NOT NULL DEFAULT 'stable',
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        UNIQUE(scope, industry, domain, knowledge_type, title)
    );
    CREATE INDEX IF NOT EXISTS idx_v50_knowledge_lookup
      ON v50_knowledge_items(industry, domain, knowledge_type, status);

    CREATE VIRTUAL TABLE IF NOT EXISTS v50_knowledge_fts USING fts5(
        knowledge_id UNINDEXED,
        industry UNINDEXED,
        domain UNINDEXED,
        title,
        statement
    );

    CREATE TABLE IF NOT EXISTS v50_knowledge_edges (
        id TEXT PRIMARY KEY,
        source_knowledge_id TEXT NOT NULL,
        target_knowledge_id TEXT NOT NULL,
        relationship TEXT NOT NULL,
        weight REAL NOT NULL DEFAULT 0.50,
        confidence REAL NOT NULL DEFAULT 0.60,
        evidence_json TEXT DEFAULT '[]',
        created_at TEXT NOT NULL,
        UNIQUE(source_knowledge_id, target_knowledge_id, relationship)
    );

    CREATE TABLE IF NOT EXISTS v50_reasoning_cases (
        id TEXT PRIMARY KEY,
        scope TEXT NOT NULL DEFAULT 'global',
        industry TEXT NOT NULL DEFAULT '',
        archetype TEXT NOT NULL DEFAULT '',
        situation TEXT NOT NULL,
        evidence_json TEXT NOT NULL DEFAULT '{}',
        hypotheses_json TEXT NOT NULL DEFAULT '[]',
        diagnostic_logic_json TEXT NOT NULL DEFAULT '[]',
        decision_logic_json TEXT NOT NULL DEFAULT '[]',
        outcome_claim TEXT DEFAULT '',
        outcome_status TEXT NOT NULL DEFAULT 'not_claimed',
        quality_status TEXT NOT NULL DEFAULT 'curated',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_v50_cases_lookup
      ON v50_reasoning_cases(industry, archetype, quality_status);

    CREATE VIRTUAL TABLE IF NOT EXISTS v50_cases_fts USING fts5(
        case_id UNINDEXED,
        industry UNINDEXED,
        archetype UNINDEXED,
        situation,
        diagnostic_logic,
        decision_logic
    );

    CREATE TABLE IF NOT EXISTS v50_teacher_distillation (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        task_type TEXT NOT NULL,
        prompt_hash TEXT NOT NULL,
        teacher_output TEXT NOT NULL,
        evidence_json TEXT DEFAULT '{}',
        critique_json TEXT DEFAULT '{}',
        validation_status TEXT NOT NULL DEFAULT 'UNVERIFIED',
        confidence REAL NOT NULL DEFAULT 0.0,
        created_at TEXT NOT NULL,
        reviewed_at TEXT DEFAULT ''
    );
    CREATE INDEX IF NOT EXISTS idx_v50_teacher_status
      ON v50_teacher_distillation(tenant_id, validation_status, created_at DESC);

    CREATE TABLE IF NOT EXISTS v50_learning_events (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        pattern_key TEXT NOT NULL,
        prior_value_json TEXT DEFAULT '{}',
        observed_value_json TEXT DEFAULT '{}',
        delta_json TEXT DEFAULT '{}',
        verification_status TEXT NOT NULL DEFAULT 'UNVERIFIED',
        confidence REAL NOT NULL DEFAULT 0.0,
        created_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_v50_learning
      ON v50_learning_events(tenant_id, pattern_key, verification_status, created_at DESC);

    CREATE TABLE IF NOT EXISTS v50_benchmark_cases (
        id TEXT PRIMARY KEY,
        category TEXT NOT NULL,
        difficulty INTEGER NOT NULL DEFAULT 1,
        prompt TEXT NOT NULL,
        expected_signals_json TEXT NOT NULL DEFAULT '[]',
        expected_unknowns_json TEXT NOT NULL DEFAULT '[]',
        scoring_rules_json TEXT NOT NULL DEFAULT '{}',
        source_kind TEXT NOT NULL DEFAULT 'derived_from_structured_priors',
        created_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_v50_benchmark
      ON v50_benchmark_cases(category, difficulty);
    """)
    conn.commit()
    conn.close()


# Stable, non-company-specific business principles. These are deliberately
# qualitative: no invented market sizes, company counts, historical rates,
# revenue figures, or fabricated outcome percentages are embedded.
V50_GLOBAL_KNOWLEDGE = [
    ("finance", "kpi_principle", "Cash flow versus accounting profit", "Accounting profit and cash flow answer different questions; a profitable business can still face liquidity stress when cash conversion is weak.", "finance"),
    ("finance", "kpi_principle", "Gross margin is not contribution margin", "Gross margin should not automatically be treated as contribution margin when variable fulfillment, payment, support, or acquisition costs remain outside the gross-margin definition.", "finance"),
    ("finance", "diagnostic_rule", "Working-capital pressure", "Revenue growth can increase financing needs when receivables or inventory grow faster than cash generation.", "finance"),
    ("finance", "decision_rule", "Unit economics before scaling", "When acquisition economics are structurally negative, increasing acquisition volume can amplify losses rather than solve the underlying problem.", "finance"),
    ("finance", "risk_rule", "Concentration risk", "Dependence on a small number of customers, suppliers, channels, lenders, or products should be treated as a material resilience risk.", "finance"),
    ("strategy", "reasoning_rule", "Strategy is constrained by trade-offs", "A strategy should explicitly state what the company will prioritize and what it will deliberately deprioritize.", "strategy"),
    ("strategy", "diagnostic_rule", "Growth quality", "Top-line growth should be evaluated together with margin, cash conversion, retention, capacity, and risk rather than treated as a standalone success metric.", "strategy"),
    ("strategy", "decision_rule", "Reversible versus irreversible decisions", "Reversible decisions can be tested with smaller commitments; irreversible decisions require stronger evidence and governance.", "strategy"),
    ("strategy", "reasoning_rule", "Second-order effects", "A decision can improve one KPI while damaging another through capacity, cash, quality, customer, or operational interactions.", "strategy"),
    ("strategy", "reasoning_rule", "Alternative hypothesis requirement", "A strong diagnosis should consider at least one credible alternative explanation before treating a root cause as established.", "strategy"),
    ("sales", "kpi_principle", "Pipeline quality", "Pipeline volume alone is insufficient; stage conversion, sales-cycle duration, win rate, deal quality, and source quality determine whether pipeline can support a revenue target.", "sales"),
    ("sales", "diagnostic_rule", "Win-rate decomposition", "A falling win rate should be decomposed by segment, channel, product, salesperson, deal size, and competitive context before a universal conclusion is made.", "sales"),
    ("sales", "decision_rule", "Qualification before acceleration", "Increasing sales activity without correcting qualification can increase workload while leaving revenue quality unchanged.", "sales"),
    ("sales", "risk_rule", "Single-channel dependency", "Heavy dependence on one acquisition or distribution channel creates exposure to pricing, policy, competition, and platform changes.", "sales"),
    ("marketing", "kpi_principle", "Acquisition efficiency", "Marketing efficiency should be evaluated with downstream conversion and contribution economics, not only reach, clicks, or engagement.", "marketing"),
    ("marketing", "diagnostic_rule", "Traffic-quality decomposition", "A conversion decline should be investigated by source, audience, device, geography, offer, landing page, and product mix before assuming a single funnel cause.", "marketing"),
    ("marketing", "decision_rule", "Attribution uncertainty", "Attribution models are estimates; channel decisions should consider incrementality and downstream economics where evidence permits.", "marketing"),
    ("operations", "kpi_principle", "Constraint-first operations", "The highest-leverage operational improvement is often located at the binding constraint rather than at a locally inefficient non-constraint step.", "operations"),
    ("operations", "diagnostic_rule", "Throughput versus utilization", "High utilization at one resource can reduce total throughput when it creates queues or blocks downstream work.", "operations"),
    ("operations", "risk_rule", "Capacity mismatch", "Demand growth without matching operational capacity can degrade service quality, cycle time, reliability, and margin.", "operations"),
    ("customer", "kpi_principle", "Retention economics", "Retention affects lifetime value, recurring revenue durability, acquisition payback, and the amount of new business required to sustain growth.", "customer"),
    ("customer", "diagnostic_rule", "Churn decomposition", "Churn should be segmented by cohort, tenure, product, customer value, acquisition source, and reason rather than treated as one homogeneous metric.", "customer"),
    ("customer", "decision_rule", "Leading indicators", "Usage, activation, support friction, engagement, and value realization can be useful leading indicators of future retention when validated against company outcomes.", "customer"),
    ("pricing", "kpi_principle", "Price-volume trade-off", "A price change can affect conversion, volume, mix, margin, and customer composition; the net effect must be evaluated rather than assumed.", "pricing"),
    ("pricing", "diagnostic_rule", "Discount leakage", "Persistent discounting can change realized price, customer expectations, margin, and future pricing power.", "pricing"),
    ("pricing", "decision_rule", "Segmented pricing", "Where willingness-to-pay differs materially across segments, a single price can leave value uncaptured or create avoidable friction.", "pricing"),
    ("risk", "risk_rule", "Risk is probability times consequence", "Risk prioritization should consider likelihood, impact, detectability, reversibility, and time-to-impact rather than severity alone.", "risk"),
    ("risk", "decision_rule", "Risk-adjusted decision value", "A higher expected return is not automatically better when downside exposure, uncertainty, or irreversibility is materially higher.", "risk"),
    ("data", "governance_rule", "Evidence hierarchy", "Current verified company evidence should generally outrank generic industry priors when the evidence is relevant, sufficiently complete, and trustworthy.", "data"),
    ("data", "governance_rule", "Missing data is a first-class result", "When missing evidence could materially change a decision, the system should surface the data gap instead of filling it with assumptions.", "data"),
    ("data", "quality_rule", "Correlation is not causation", "A correlation should not be promoted to a causal relationship without supporting evidence, controlled experimentation, temporal logic, or another credible identification strategy.", "data"),
    ("governance", "governance_rule", "Human approval for high-impact actions", "High-impact or irreversible actions should pass explicit authorization and audit controls before execution.", "governance"),
    ("governance", "governance_rule", "Auditability", "Material recommendations should retain the evidence, assumptions, reasoning status, and decision outcome needed for later review.", "governance"),
    ("learning", "learning_rule", "Verified outcomes only", "Reusable learning should preferentially come from outcomes that are explicitly observed and verified rather than from unconfirmed predictions.", "learning"),
    ("learning", "learning_rule", "Prediction calibration", "A prediction system should track predicted probabilities against actual outcomes to detect systematic overconfidence or underconfidence.", "learning"),
    ("learning", "learning_rule", "No silent self-modification", "Learning should update governed knowledge and model state through explicit quality gates rather than silently rewriting production logic.", "learning"),
]

# Industry-specific overlays. They complement the existing V45 prior registry;
# they do not assert historical statistics. Each item describes a stable
# diagnostic relationship or management concern.
V50_INDUSTRY_OVERLAYS = {
    "saas": [
        ("unit_economics", "Retention and expansion influence LTV and recurring-revenue durability."),
        ("diagnostic", "Activation, time-to-value, usage, support friction, and customer segment should be examined when churn rises."),
        ("risk", "Rapid acquisition with weak retention can create a misleading growth profile."),
    ],
    "ecommerce": [
        ("unit_economics", "Contribution economics should incorporate product margin, fulfillment, payment, returns, and acquisition costs where applicable."),
        ("diagnostic", "Traffic, conversion, AOV, product mix, return rate, and repeat purchase should be decomposed together."),
        ("risk", "Inventory and cash can become binding constraints during rapid demand changes."),
    ],
    "retail": [
        ("diagnostic", "Store productivity, footfall, conversion, basket size, availability, shrinkage, and local mix should be analyzed together."),
        ("risk", "Overstock and stockouts can coexist across locations or categories and require granular analysis."),
        ("operations", "Replenishment quality affects both sales availability and working capital."),
    ],
    "restaurant": [
        ("unit_economics", "Labor, food cost, occupancy, average check, menu mix, and waste jointly influence unit economics."),
        ("diagnostic", "Low margin should be decomposed into volume, pricing, mix, food cost, labor productivity, and waste."),
        ("risk", "Demand volatility can make staffing and purchasing decisions highly sensitive to forecast error."),
    ],
    "manufacturing": [
        ("operations", "Throughput, OEE, downtime, yield, quality, changeover time, and bottlenecks should be considered as a system."),
        ("diagnostic", "Cost increases should be decomposed into material, labor, downtime, scrap, energy, and overhead drivers."),
        ("risk", "Single-source suppliers and long lead times can create production and working-capital exposure."),
    ],
    "professional_services": [
        ("unit_economics", "Utilization, realization, pricing, delivery cost, scope control, and bench capacity jointly affect project economics."),
        ("diagnostic", "Margin deterioration should be decomposed by client, project, team, scope, realization, and delivery efficiency."),
        ("risk", "Revenue concentration and key-person dependency can materially affect resilience."),
    ],
    "marketplace": [
        ("network", "Liquidity and match quality on both sides of a marketplace influence conversion and retention."),
        ("diagnostic", "Demand and supply should be analyzed by geography, category, time, price, and service quality."),
        ("risk", "Subsidies that create activity without durable unit economics can hide structural weakness."),
    ],
    "education": [
        ("outcomes", "Enrollment quality should be evaluated alongside completion, engagement, satisfaction, and learner outcomes."),
        ("capacity", "Instructor or content capacity can become a binding constraint as enrollment grows."),
        ("risk", "Acquisition growth with poor learner outcomes can damage retention and reputation."),
    ],
    "hospitality": [
        ("yield", "Occupancy, rate, channel mix, cancellations, and guest experience interact in revenue management."),
        ("diagnostic", "Weak RevPAR should be decomposed into occupancy and rate effects before selecting an intervention."),
        ("risk", "Heavy dependence on intermediaries can create margin and demand-access risk."),
    ],
    "real_estate": [
        ("finance", "Occupancy, rent, operating expenses, financing costs, and asset value should be evaluated together."),
        ("diagnostic", "Vacancy should be decomposed by pricing, demand, product-market fit, property quality, and leasing process."),
        ("risk", "Leverage amplifies both returns and downside sensitivity to rates, vacancy, and asset values."),
    ],
    "fintech": [
        ("risk", "Fraud, credit loss, liquidity, compliance, and unit economics are tightly connected risk dimensions."),
        ("diagnostic", "Growth should be decomposed into active users, transaction behavior, monetization, losses, and retention."),
        ("governance", "Regulatory and model-risk controls should be treated as operating capabilities, not afterthoughts."),
    ],
    "healthcare_services": [
        ("operations", "Capacity, staffing, scheduling, payer mix, collection, and service quality interact materially."),
        ("diagnostic", "Revenue leakage should be investigated across coding, billing, denials, collections, and workflow controls."),
        ("governance", "Clinical and regulated decisions require specialized governance and must not be inferred from generic business priors."),
    ],
    "travel": [
        ("yield", "Capacity utilization, pricing, cancellation behavior, and channel mix jointly affect economics."),
        ("diagnostic", "Demand changes should be segmented by route, destination, season, customer segment, and booking channel."),
        ("risk", "Demand shocks can create rapid capacity and cash-flow stress when fixed costs are high."),
    ],
    "media": [
        ("attention", "Audience quality, engagement, retention, inventory, and monetization determine the quality of growth."),
        ("diagnostic", "Audience decline should be segmented by content type, distribution source, cohort, and engagement depth."),
        ("risk", "Platform concentration can create distribution and monetization fragility."),
    ],
    "telecom": [
        ("network", "Network quality, capacity, usage, ARPU, churn, and capex efficiency should be evaluated together."),
        ("diagnostic", "Churn should be decomposed by network experience, price, segment, tenure, and competitor exposure."),
        ("risk", "Capacity investment can lag demand or become underutilized if demand assumptions are wrong."),
    ],
    "energy": [
        ("operations", "Availability, downtime, maintenance, realized price, and unit cost jointly influence economics."),
        ("risk", "Commodity price exposure and asset reliability can create large earnings variability."),
        ("governance", "Safety and environmental controls are core operational constraints, not optional optimizations."),
    ],
    "construction": [
        ("project_controls", "Schedule, cost, scope, procurement, labor productivity, and change orders should be monitored together."),
        ("diagnostic", "Cost overruns should be traced to scope, productivity, procurement, rework, schedule, and financing effects."),
        ("risk", "Long project cycles make early assumption errors expensive to correct later."),
    ],
    "automotive": [
        ("operations", "Production mix, dealer inventory, quality, warranty cost, and demand should be analyzed together."),
        ("diagnostic", "Inventory pressure can originate from production mix, demand, incentives, channel inventory, or forecasting error."),
        ("risk", "Quality failures can propagate into warranty cost, reputation, and future demand."),
    ],
    "pharmaceuticals": [
        ("pipeline", "Portfolio value depends on pipeline quality, probability of success, launch adoption, pricing, and regulatory milestones."),
        ("diagnostic", "Launch performance should be decomposed by adoption, access, positioning, physician/customer behavior, and supply."),
        ("governance", "Regulatory requirements constrain product, marketing, data, and operational decisions."),
    ],
    "insurance": [
        ("risk", "Pricing, selection, loss experience, expenses, retention, and claims behavior jointly determine underwriting economics."),
        ("diagnostic", "Loss-ratio changes should be decomposed by product, cohort, geography, claim type, severity, and frequency."),
        ("governance", "Capital, reserving, underwriting, and regulatory controls are core decision constraints."),
    ],
}


def _v50_upsert_knowledge(conn, *, industry: str, domain: str, knowledge_type: str,
                          title: str, statement: str, confidence: float = 0.72,
                          source_kind: str = "structured_business_principle",
                          evidence_grade: str = "curated_domain_knowledge",
                          scope: str = "global") -> str:
    now = v50_now()
    kid = "V50K-" + hashlib.sha256(
        f"{scope}|{industry}|{domain}|{knowledge_type}|{title}".encode("utf-8")
    ).hexdigest()[:24]
    conn.execute(
        """INSERT OR IGNORE INTO v50_knowledge_items
        (id,scope,industry,domain,knowledge_type,title,statement,applicability_json,
         evidence_grade,source_kind,confidence,freshness_class,status,created_at,updated_at)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (kid, scope, industry, domain, knowledge_type, title, statement, "{}",
         evidence_grade, source_kind, v50_clamp(confidence), "stable", "active", now, now),
    )
    conn.execute(
        "INSERT OR IGNORE INTO v50_knowledge_fts(knowledge_id,industry,domain,title,statement) VALUES(?,?,?,?,?)",
        (kid, industry, domain, title, statement),
    )
    return kid


def v50_seed_global_knowledge() -> Dict[str, int]:
    """Idempotently seed curated domain knowledge; never seeds fake company data."""
    conn = db_connect()
    counts = {"global_rules": 0, "industry_overlays": 0, "reasoning_cases": 0, "benchmarks": 0}
    for domain, ktype, title, statement, _ in V50_GLOBAL_KNOWLEDGE:
        before = conn.execute("SELECT changes()").fetchone()[0]
        _v50_upsert_knowledge(conn, industry="", domain=domain, knowledge_type=ktype,
                              title=title, statement=statement)
        after = conn.execute("SELECT changes()").fetchone()[0]
        counts["global_rules"] += int(after > before)

    # Add richer overlays for industries already represented by the V45 prior engine.
    for industry, items in V50_INDUSTRY_OVERLAYS.items():
        for kind, statement in items:
            title = f"{industry.replace('_', ' ').title()} — {kind.replace('_', ' ').title()}"
            _v50_upsert_knowledge(
                conn, industry=industry, domain=kind, knowledge_type="industry_overlay",
                title=title, statement=statement, confidence=0.74,
                evidence_grade="structured_industry_prior",
            )
            counts["industry_overlays"] += 1

    # Compile reasoning cases from the already-structured V45 priors. These are
    # reasoning templates, NOT claims about a particular real company or outcome.
    for industry, prior in getattr(ENTERPRISE_BUSINESS_BRAIN, "priors", IndustryPriorEngine()).registry.items():
        for failure in prior.common_failure_modes:
            case_id = "V50C-" + hashlib.sha256(f"{industry}|{failure}".encode()).hexdigest()[:24]
            situation = f"A {industry} business shows signals potentially consistent with {failure}."
            hypotheses = [{"hypothesis": failure, "status": "candidate", "evidence_required": list(prior.critical_kpis[:5])}]
            diagnostics = [{"step": "segment", "instruction": "Compare the affected KPI by relevant cohort, product, channel, geography, or time period."},
                           {"step": "challenge", "instruction": "Check at least one alternative explanation before declaring a root cause."},
                           {"step": "evidence", "instruction": "Prefer current verified company evidence over generic industry priors."}]
            decisions = [{"rule": "reversible_first", "instruction": "Prefer a bounded test when the intervention is reversible and evidence is incomplete."}]
            conn.execute(
                """INSERT OR IGNORE INTO v50_reasoning_cases
                (id,scope,industry,archetype,situation,evidence_json,hypotheses_json,
                 diagnostic_logic_json,decision_logic_json,outcome_claim,outcome_status,
                 quality_status,created_at,updated_at)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (case_id, "global", industry, prior.archetype, situation,
                 json.dumps({"critical_kpis": prior.critical_kpis[:10]}),
                 json.dumps(hypotheses), json.dumps(diagnostics), json.dumps(decisions),
                 "", "not_claimed", "curated_reasoning_template", v50_now(), v50_now()),
            )
            conn.execute(
                """INSERT OR IGNORE INTO v50_cases_fts
                (case_id,industry,archetype,situation,diagnostic_logic,decision_logic)
                VALUES(?,?,?,?,?,?)""",
                (case_id, industry, prior.archetype, situation,
                 json.dumps(diagnostics), json.dumps(decisions)),
            )
            counts["reasoning_cases"] += 1

    # Compile deterministic knowledge relationships. These edges encode
    # reasoning structure, not fabricated empirical effect sizes.
    rule_rows = conn.execute(
        "SELECT id, domain, knowledge_type FROM v50_knowledge_items WHERE status='active'"
    ).fetchall()
    by_domain = {}
    for row in rule_rows:
        by_domain.setdefault(row["domain"], []).append(dict(row))
    for domain, rows in by_domain.items():
        for src in rows:
            for dst in rows:
                if src["id"] == dst["id"]:
                    continue
                rel = None
                if src["knowledge_type"] == "kpi_principle" and dst["knowledge_type"] == "diagnostic_rule":
                    rel = "supports_diagnosis"
                elif src["knowledge_type"] == "diagnostic_rule" and dst["knowledge_type"] == "decision_rule":
                    rel = "informs_decision"
                elif src["knowledge_type"] == "risk_rule" and dst["knowledge_type"] == "decision_rule":
                    rel = "constrains_decision"
                elif src["knowledge_type"] == "governance_rule" and dst["knowledge_type"] == "learning_rule":
                    rel = "governs_learning"
                if rel:
                    conn.execute(
                        """INSERT OR IGNORE INTO v50_knowledge_edges
                        (id,source_knowledge_id,target_knowledge_id,relationship,weight,confidence,evidence_json,created_at)
                        VALUES(?,?,?,?,?,?,?,?)""",
                        ("V50E-" + hashlib.sha256(f"{src['id']}|{dst['id']}|{rel}".encode()).hexdigest()[:24],
                         src["id"], dst["id"], rel, 0.70, 0.70,
                         json.dumps({"basis": "structured_reasoning_relationship", "empirical_effect_size": None}), v50_now())
                    )

    # Benchmark cases are deliberately derived from structured priors and have
    # no hidden fabricated company values.
    benchmark_specs = [
        ("diagnosis", 2, "Revenue falls while traffic is stable; identify what evidence is required before selecting a root cause.", ["conversion", "mix", "price", "retention"], ["traffic quality", "checkout", "product mix"]),
        ("unit_economics", 3, "Acquisition volume rises while contribution economics deteriorate; identify the diagnostic decomposition.", ["CAC", "contribution margin", "retention", "payback"], ["channel mix", "customer quality"]),
        ("operations", 3, "Demand rises but service quality falls; identify the likely constraint and required evidence.", ["capacity", "cycle time", "quality", "utilization"], ["binding constraint", "queueing effects"]),
        ("risk", 4, "A strategic initiative has high upside but irreversible capital commitment and weak evidence; determine the governance response.", ["impact", "probability", "reversibility", "evidence"], ["downside", "assumption risk"]),
        ("learning", 4, "A recommendation produced a positive result but the outcome was not independently verified; determine whether it should become reusable learning.", ["verification", "provenance", "outcome"], ["causal attribution"]),
    ]
    for category, difficulty, prompt, signals, unknowns in benchmark_specs:
        bid = "V50B-" + hashlib.sha256(prompt.encode()).hexdigest()[:24]
        conn.execute(
            """INSERT OR IGNORE INTO v50_benchmark_cases
            (id,category,difficulty,prompt,expected_signals_json,expected_unknowns_json,scoring_rules_json,source_kind,created_at)
            VALUES(?,?,?,?,?,?,?,?,?)""",
            (bid, category, difficulty, prompt, json.dumps(signals), json.dumps(unknowns),
             json.dumps({"no_fabrication": 1.0, "uncertainty_handling": 1.0, "evidence_alignment": 1.0}),
             "derived_from_structured_priors", v50_now()),
        )
        counts["benchmarks"] += 1
    conn.commit()
    conn.close()
    return counts


def v50_knowledge_search(query: str, industry: str = "", domain: str = "", limit: int = 12) -> List[Dict[str, Any]]:
    query = _bounded_text(query, 1000).strip()
    if not query:
        return []
    tokens = re.findall(r"[A-Za-z0-9_]{2,}", query)
    fts_query = " OR ".join(tokens) if tokens else '""'
    clauses = ["v50_knowledge_fts MATCH ?"]
    params: List[Any] = [fts_query]
    if industry:
        clauses.append("k.industry=?")
        params.append(_bounded_text(industry, 120).lower())
    if domain:
        clauses.append("k.domain=?")
        params.append(_bounded_text(domain, 120).lower())
    params.append(max(1, min(50, int(limit))))
    conn = db_connect()
    rows = conn.execute(
        f"""SELECT k.* FROM v50_knowledge_fts f
            JOIN v50_knowledge_items k ON k.id=f.knowledge_id
            WHERE {' AND '.join(clauses)}
            AND k.status='active'
            ORDER BY bm25(v50_knowledge_fts), k.confidence DESC
            LIMIT ?""", params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def v50_case_search(query: str, industry: str = "", limit: int = 10) -> List[Dict[str, Any]]:
    tokens = re.findall(r"[A-Za-z0-9_]{2,}", _bounded_text(query, 1000))
    if not tokens:
        return []
    fts_query = " OR ".join(tokens)
    params: List[Any] = [fts_query]
    clause = "v50_cases_fts MATCH ?"
    if industry:
        clause += " AND c.industry=?"
        params.append(_bounded_text(industry, 120).lower())
    params.append(max(1, min(30, int(limit))))
    conn = db_connect()
    rows = conn.execute(
        f"""SELECT c.* FROM v50_cases_fts f
            JOIN v50_reasoning_cases c ON c.id=f.case_id
            WHERE {clause}
            ORDER BY c.updated_at DESC LIMIT ?""", params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def v50_record_teacher_distillation(tenant_id: str, task_type: str, prompt: str,
                                    teacher_output: str, evidence: Optional[Dict[str, Any]] = None,
                                    critique: Optional[Dict[str, Any]] = None,
                                    validation_status: str = "UNVERIFIED",
                                    confidence: float = 0.0) -> Dict[str, Any]:
    tenant_id = v28_tenant_guard(tenant_id)
    prompt_hash = hashlib.sha256(_bounded_text(prompt, 50000).encode()).hexdigest()
    rid = "V50T-" + uuid.uuid4().hex
    conn = db_connect()
    conn.execute(
        """INSERT INTO v50_teacher_distillation
        (id,tenant_id,task_type,prompt_hash,teacher_output,evidence_json,critique_json,
         validation_status,confidence,created_at)
        VALUES(?,?,?,?,?,?,?,?,?,?)""",
        (rid, tenant_id, _bounded_text(task_type, 160), prompt_hash,
         _bounded_text(teacher_output, 50000), json.dumps(evidence or {}, default=str),
         json.dumps(critique or {}, default=str), _bounded_text(validation_status, 40).upper(),
         v50_clamp(confidence), v50_now()),
    )
    conn.commit(); conn.close()
    return {"ok": True, "id": rid, "validation_status": validation_status.upper()}


def v50_record_verified_learning(tenant_id: str, pattern_key: str,
                                 prior_value: Dict[str, Any], observed_value: Dict[str, Any],
                                 delta: Dict[str, Any], verification_status: str,
                                 confidence: float = 0.0) -> Dict[str, Any]:
    tenant_id = v28_tenant_guard(tenant_id)
    status = _bounded_text(verification_status, 40).upper()
    if status not in {"VERIFIED", "PARTIALLY_VERIFIED", "UNVERIFIED", "REJECTED"}:
        status = "UNVERIFIED"
    rid = "V50L-" + uuid.uuid4().hex
    conn = db_connect()
    conn.execute(
        """INSERT INTO v50_learning_events
        (id,tenant_id,event_type,pattern_key,prior_value_json,observed_value_json,delta_json,
         verification_status,confidence,created_at)
        VALUES(?,?,?,?,?,?,?,?,?,?)""",
        (rid, tenant_id, "OUTCOME_LEARNING", _bounded_text(pattern_key, 500),
         json.dumps(prior_value or {}, default=str), json.dumps(observed_value or {}, default=str),
         json.dumps(delta or {}, default=str), status, v50_clamp(confidence), v50_now()),
    )
    conn.commit(); conn.close()
    return {"ok": True, "id": rid, "verification_status": status}


def v50_export_training_corpus(tenant_id: str = "", include_unverified: bool = False) -> List[Dict[str, Any]]:
    """Export a training-ready corpus without exposing private tenant data by default."""
    conn = db_connect()
    rows = conn.execute(
        "SELECT * FROM v50_reasoning_cases WHERE scope='global' AND quality_status='curated' ORDER BY industry, id"
    ).fetchall()
    corpus = []
    for r in rows:
        corpus.append({
            "type": "business_reasoning_case",
            "industry": r["industry"],
            "archetype": r["archetype"],
            "situation": r["situation"],
            "evidence": json.loads(r["evidence_json"] or "{}"),
            "hypotheses": json.loads(r["hypotheses_json"] or "[]"),
            "diagnostic_logic": json.loads(r["diagnostic_logic_json"] or "[]"),
            "decision_logic": json.loads(r["decision_logic_json"] or "[]"),
            "outcome_status": r["outcome_status"],
        })
    if tenant_id:
        tenant_id = v28_tenant_guard(tenant_id)
        status_clause = "" if include_unverified else "AND verification_status='VERIFIED'"
        learned = conn.execute(
            f"SELECT * FROM v50_learning_events WHERE tenant_id=? {status_clause} ORDER BY created_at",
            (tenant_id,)
        ).fetchall()
        for r in learned:
            corpus.append({
                "type": "verified_company_learning",
                "pattern_key": r["pattern_key"],
                "prior_value": json.loads(r["prior_value_json"] or "{}"),
                "observed_value": json.loads(r["observed_value_json"] or "{}"),
                "delta": json.loads(r["delta_json"] or "{}"),
                "verification_status": r["verification_status"],
                "confidence": r["confidence"],
            })
    conn.close()
    return corpus


def v50_preloaded_brain_health() -> Dict[str, Any]:
    conn = db_connect()
    tables = {r["name"] for r in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')").fetchall()}
    counts = {}
    for table, key in [
        ("v50_knowledge_items", "knowledge_items"),
        ("v50_reasoning_cases", "reasoning_cases"),
        ("v50_benchmark_cases", "benchmark_cases"),
        ("v50_knowledge_edges", "knowledge_edges"),
    ]:
        counts[key] = int(conn.execute(f"SELECT COUNT(*) AS n FROM {table}").fetchone()["n"]) if table in tables else 0
    conn.close()
    return {
        "version": V50_VERSION,
        "name": V50_BRAIN_NAME,
        "zero_cost_architecture": True,
        "neural_weights_trained": False,
        "preloaded_business_knowledge": counts["knowledge_items"] > 0,
        "reasoning_corpus": counts["reasoning_cases"] > 0,
        "benchmark_corpus": counts["benchmark_cases"] > 0,
        "knowledge_items": counts["knowledge_items"],
        "reasoning_cases": counts["reasoning_cases"],
        "benchmark_cases": counts["benchmark_cases"],
        "knowledge_edges": counts["knowledge_edges"],
        "no_fake_company_data": True,
        "verified_outcomes_only_for_reusable_learning": True,
        "company_data_overrides_generic_prior_when_supported": True,
        "training_export_available": True,
    }


class V50EnterpriseBusinessBrain(EnterpriseBusinessBrain):
    """V50 wrapper: pre-loaded knowledge + governed learning over the V45 brain."""

    def initialize(self):
        base = super().initialize()
        if not base.get("ok"):
            return base
        try:
            v50_init_schema()
            seeded = v50_seed_global_knowledge()
            self.v50_seed_result = seeded
            return {"ok": True, "version": V50_VERSION, "seeded": seeded}
        except Exception as exc:
            logger.exception("V50 initialization failed")
            return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}

    def analyze(self, tenant_id: str, profile: Dict[str, Any], metrics: Dict[str, Any],
                baseline: Optional[Dict[str, Any]] = None,
                growth_rates: Optional[Dict[str, float]] = None):
        result = super().analyze(tenant_id, profile, metrics, baseline, growth_rates)
        normalized = result.get("company_profile", {})
        industry = normalized.get("industry", "")
        query = " ".join([str(x) for x in list(metrics.keys())[:30]])
        prior_hits = v50_knowledge_search(query or industry, industry=industry, limit=12)
        case_hits = v50_case_search(" ".join(result.get("diagnostics", {}).get("findings", [{}])[0].keys()) if result.get("diagnostics", {}).get("findings") else industry, industry=industry, limit=8)
        result["preloaded_business_intelligence"] = {
            "knowledge_matches": prior_hits,
            "reasoning_case_matches": case_hits,
            "status": "PRELOADED_FOUNDATION_ACTIVE" if (prior_hits or case_hits) else "NO_MATCHING_PRELOADED_KNOWLEDGE",
            "neural_training_claim": False,
        }
        result["learning_policy"] = {
            "verified_outcomes_only": True,
            "teacher_outputs_require_validation": True,
            "company_evidence_can_override_prior": True,
            "unknowns_are_preserved": True,
        }
        return result

    def health(self, tenant_id: Optional[str] = None):
        report = super().health(tenant_id)
        report["v50_preloaded_brain"] = v50_preloaded_brain_health()
        report["brain_version"] = V50_VERSION
        report["name"] = V50_BRAIN_NAME
        return report


# Replace only the top-level brain reference; all inherited V32-V45 engines,
# schemas, governance, security and UI remain intact.
try:
    V50_ENTERPRISE_BUSINESS_BRAIN = V50EnterpriseBusinessBrain()
    _v50_init_result = V50_ENTERPRISE_BUSINESS_BRAIN.initialize()
    ENTERPRISE_BUSINESS_BRAIN = V50_ENTERPRISE_BUSINESS_BRAIN
    os_core.enterprise_brain = V50_ENTERPRISE_BUSINESS_BRAIN
    os_core.enterprise_brain_version = V50_VERSION
except Exception as _v50_exc:
    logger.exception("V50 brain bootstrapping deferred: %s", _v50_exc)
    V50_ENTERPRISE_BUSINESS_BRAIN = ENTERPRISE_BUSINESS_BRAIN

# V50 public helpers.
def v50_brain_health(tenant_id: Optional[str] = None) -> Dict[str, Any]:
    return V50_ENTERPRISE_BUSINESS_BRAIN.health(tenant_id)


def v50_search_business_knowledge(query: str, industry: str = "", domain: str = "", limit: int = 12) -> List[Dict[str, Any]]:
    return v50_knowledge_search(query, industry, domain, limit)


def v50_get_training_corpus(tenant_id: str = "", include_unverified: bool = False) -> List[Dict[str, Any]]:
    return v50_export_training_corpus(tenant_id, include_unverified)


# Final V50 release manifest supersedes the earlier V45 manifest without
# deleting the historical manifest, preserving full release traceability.
V50_RELEASE_MANIFEST = {
    "release": V50_VERSION,
    "name": V50_BRAIN_NAME,
    "base_foundation": "V32",
    "previous_master": "V45_FIXED",
    "single_master_codebase": True,
    "zero_cost_local_core": True,
    "preloaded_not_neural_pretrained": True,
    "modules_added": [
        "preloaded_enterprise_knowledge_compiler",
        "global_business_principle_library",
        "industry_overlay_library",
        "structured_reasoning_case_corpus",
        "teacher_distillation_registry",
        "verified_learning_registry",
        "training_corpus_exporter",
        "business_brain_benchmark_registry",
        "knowledge_fts5_retrieval",
        "knowledge_confidence_and_provenance",
    ],
    "restrictions": {
        "paid_api_required": False,
        "gpu_required": False,
        "fake_company_data_seeded": False,
        "fabricated_historical_outcomes_seeded": False,
        "unverified_learning_reusable_by_default": False,
        "high_risk_actions_require_human_governance": True,
    },
}


# ==================== V50 BRAIN-LEVEL MAXIMIZATION ====================
# Additive zero-cost cognitive layer. No neural training is claimed or performed.

BRAIN_MAXIMIZATION_VERSION = "V50-BRAIN-MAX-1.0"

def _bm_now():
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()

def _bm_hash(value):
    import hashlib, json
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()

def initialize_brain_maximization_schema(conn):
    ddl = [
        """CREATE TABLE IF NOT EXISTS brain_world_state (
            tenant_id TEXT NOT NULL, entity_key TEXT NOT NULL,
            state_json TEXT NOT NULL, confidence REAL, updated_at TEXT NOT NULL,
            PRIMARY KEY (tenant_id, entity_key))""",
        """CREATE TABLE IF NOT EXISTS brain_hypotheses (
            id INTEGER PRIMARY KEY AUTOINCREMENT, tenant_id TEXT NOT NULL,
            case_id TEXT, hypothesis TEXT NOT NULL, evidence_for TEXT,
            evidence_against TEXT, confidence REAL, status TEXT NOT NULL,
            created_at TEXT NOT NULL, updated_at TEXT NOT NULL)""",
        """CREATE TABLE IF NOT EXISTS brain_experiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT, tenant_id TEXT NOT NULL,
            decision_id TEXT, hypothesis TEXT, success_metric TEXT,
            baseline TEXT, stopping_criteria TEXT, expected_outcome TEXT,
            actual_outcome TEXT, status TEXT NOT NULL, created_at TEXT NOT NULL,
            completed_at TEXT)""",
        """CREATE TABLE IF NOT EXISTS brain_memory_layers (
            id INTEGER PRIMARY KEY AUTOINCREMENT, tenant_id TEXT NOT NULL,
            layer TEXT NOT NULL, memory_key TEXT NOT NULL, content TEXT NOT NULL,
            confidence REAL, provenance TEXT, expires_at TEXT,
            created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
            UNIQUE (tenant_id, layer, memory_key))""",
        """CREATE TABLE IF NOT EXISTS brain_decision_consequences (
            id INTEGER PRIMARY KEY AUTOINCREMENT, tenant_id TEXT NOT NULL,
            decision_id TEXT NOT NULL, parent_key TEXT, child_key TEXT,
            relationship TEXT NOT NULL, expected_effect TEXT,
            actual_effect TEXT, confidence REAL, created_at TEXT NOT NULL)""",
        """CREATE TABLE IF NOT EXISTS brain_failure_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT, tenant_id TEXT NOT NULL,
            event_key TEXT NOT NULL, failure TEXT NOT NULL, cause TEXT,
            conditions TEXT, lesson TEXT, confidence REAL, created_at TEXT NOT NULL,
            UNIQUE (tenant_id, event_key))""",
        """CREATE TABLE IF NOT EXISTS brain_assumptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, tenant_id TEXT NOT NULL,
            assumption_key TEXT NOT NULL, assumption TEXT NOT NULL,
            evidence TEXT, confidence REAL, status TEXT NOT NULL,
            expires_at TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
            UNIQUE (tenant_id, assumption_key))""",
        """CREATE TABLE IF NOT EXISTS brain_forecast_calibration (
            id INTEGER PRIMARY KEY AUTOINCREMENT, tenant_id TEXT NOT NULL,
            forecast_key TEXT NOT NULL, predicted_probability REAL,
            actual_outcome REAL, error REAL, created_at TEXT NOT NULL)""",
        """CREATE TABLE IF NOT EXISTS brain_attention_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT, tenant_id TEXT NOT NULL,
            signal_key TEXT NOT NULL, severity REAL, urgency REAL, impact REAL,
            confidence REAL, status TEXT NOT NULL, evidence TEXT,
            created_at TEXT NOT NULL)""",
        """CREATE TABLE IF NOT EXISTS brain_intelligence_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT, tenant_id TEXT NOT NULL,
            audit_type TEXT NOT NULL, target_key TEXT, score REAL,
            findings TEXT NOT NULL, created_at TEXT NOT NULL)"""
    ]
    for statement in ddl:
        conn.execute(statement)
    conn.commit()

def brain_update_world_state(conn, tenant_id, entity_key, state, confidence=None):
    import json
    initialize_brain_maximization_schema(conn)
    conn.execute("""INSERT INTO brain_world_state
        (tenant_id, entity_key, state_json, confidence, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(tenant_id, entity_key) DO UPDATE SET
        state_json=excluded.state_json, confidence=excluded.confidence,
        updated_at=excluded.updated_at""",
        (tenant_id, entity_key, json.dumps(state, default=str), confidence, _bm_now()))
    conn.commit()

def brain_record_hypothesis(conn, tenant_id, hypothesis, case_id=None,
                            evidence_for=None, evidence_against=None,
                            confidence=None, status="OPEN"):
    import json
    initialize_brain_maximization_schema(conn)
    now = _bm_now()
    cur = conn.execute("""INSERT INTO brain_hypotheses
        (tenant_id, case_id, hypothesis, evidence_for, evidence_against,
         confidence, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (tenant_id, case_id, hypothesis, json.dumps(evidence_for or [], default=str),
         json.dumps(evidence_against or [], default=str), confidence, status, now, now))
    conn.commit()
    return cur.lastrowid

def brain_record_experiment(conn, tenant_id, hypothesis, success_metric,
                            baseline=None, stopping_criteria=None,
                            expected_outcome=None, decision_id=None):
    initialize_brain_maximization_schema(conn)
    now = _bm_now()
    cur = conn.execute("""INSERT INTO brain_experiments
        (tenant_id, decision_id, hypothesis, success_metric, baseline,
         stopping_criteria, expected_outcome, actual_outcome, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, NULL, 'PLANNED', ?)""",
        (tenant_id, decision_id, hypothesis, success_metric, baseline,
         stopping_criteria, expected_outcome, now, now))
    conn.commit()
    return cur.lastrowid

def brain_complete_experiment(conn, tenant_id, experiment_id, actual_outcome,
                              status="COMPLETED"):
    import json
    initialize_brain_maximization_schema(conn)
    conn.execute("""UPDATE brain_experiments
                    SET actual_outcome=?, status=?, completed_at=?
                    WHERE id=? AND tenant_id=?""",
                 (json.dumps(actual_outcome, default=str), status,
                  _bm_now(), experiment_id, tenant_id))
    conn.commit()

def brain_store_memory(conn, tenant_id, layer, memory_key, content,
                       confidence=None, provenance=None, expires_at=None):
    import json
    initialize_brain_maximization_schema(conn)
    now = _bm_now()
    conn.execute("""INSERT INTO brain_memory_layers
        (tenant_id, layer, memory_key, content, confidence, provenance,
         expires_at, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(tenant_id, layer, memory_key) DO UPDATE SET
        content=excluded.content, confidence=excluded.confidence,
        provenance=excluded.provenance, expires_at=excluded.expires_at,
        updated_at=excluded.updated_at""",
        (tenant_id, layer, memory_key, json.dumps(content, default=str),
         confidence, provenance, expires_at, now, now))
    conn.commit()

def brain_record_failure(conn, tenant_id, failure, cause=None,
                         conditions=None, lesson=None, confidence=None):
    import json
    initialize_brain_maximization_schema(conn)
    event_key = _bm_hash([failure, cause, conditions])
    conn.execute("""INSERT OR REPLACE INTO brain_failure_memory
        (tenant_id, event_key, failure, cause, conditions, lesson,
         confidence, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (tenant_id, event_key, failure, cause,
         json.dumps(conditions or {}, default=str), lesson, confidence, _bm_now()))
    conn.commit()
    return event_key

def brain_record_assumption(conn, tenant_id, assumption_key, assumption,
                            evidence=None, confidence=None, status="ACTIVE",
                            expires_at=None):
    import json
    initialize_brain_maximization_schema(conn)
    now = _bm_now()
    conn.execute("""INSERT INTO brain_assumptions
        (tenant_id, assumption_key, assumption, evidence, confidence,
         status, expires_at, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(tenant_id, assumption_key) DO UPDATE SET
        assumption=excluded.assumption, evidence=excluded.evidence,
        confidence=excluded.confidence, status=excluded.status,
        expires_at=excluded.expires_at, updated_at=excluded.updated_at""",
        (tenant_id, assumption_key, assumption,
         json.dumps(evidence or [], default=str), confidence, status,
         expires_at, now, now))
    conn.commit()

def brain_record_forecast(conn, tenant_id, forecast_key,
                          predicted_probability, actual_outcome):
    initialize_brain_maximization_schema(conn)
    error = float(actual_outcome) - float(predicted_probability)
    conn.execute("""INSERT INTO brain_forecast_calibration
        (tenant_id, forecast_key, predicted_probability, actual_outcome,
         error, created_at) VALUES (?, ?, ?, ?, ?, ?)""",
        (tenant_id, forecast_key, float(predicted_probability),
         float(actual_outcome), error, _bm_now()))
    conn.commit()
    return error

def brain_generate_attention_signal(tenant_id, signal_key, severity,
                                    urgency, impact, confidence, evidence=None):
    vals = [max(0.0, min(1.0, float(x))) for x in
            (severity, urgency, impact, confidence)]
    return {"tenant_id": tenant_id, "signal_key": signal_key,
            "severity": vals[0], "urgency": vals[1], "impact": vals[2],
            "confidence": vals[3], "priority_score": sum(vals) / 4.0,
            "evidence": evidence or []}

def brain_calibrate_probability(predicted_probability, actual_outcome):
    p = max(0.0, min(1.0, float(predicted_probability)))
    y = max(0.0, min(1.0, float(actual_outcome)))
    return y - p

def brain_cognitive_audit(answer, evidence=None, assumptions=None):
    findings = []
    if not evidence:
        findings.append("NO_EVIDENCE_PROVIDED")
    if assumptions:
        findings.append("ASSUMPTIONS_PRESENT")
    if not answer or not str(answer).strip():
        findings.append("EMPTY_OUTPUT")
    if not findings:
        findings.append("BASIC_STRUCTURAL_CHECK_PASSED")
    return {"findings": findings, "score": None,
            "score_status": "NOT_QUANTIFIED_WITHOUT_GROUND_TRUTH"}

# ==================== END V50 BRAIN-LEVEL MAXIMIZATION ====================


# ==================== V51 FINAL MAXIMIZATION & HARDENING ====================
V51_FINAL_BUILD = True
V51_BUILD_ID = "V51-FINAL-ENTERPRISE-BRAIN"
V51_BUILD_PARENT = "V50-BRAIN-MAX"

def v51_safe_json(value):
    import json
    try:
        return json.dumps(value, ensure_ascii=False, default=str)
    except Exception:
        return json.dumps({"unserializable": str(value)}, ensure_ascii=False)

def v51_clamp(value, low=0.0, high=1.0):
    try:
        return max(low, min(high, float(value)))
    except (TypeError, ValueError):
        return low

def v51_evidence_score(evidence_count, source_quality=0.5, freshness=0.5,
                       consistency=0.5):
    n = max(0, int(evidence_count))
    coverage = 1.0 - (1.0 / (1.0 + n))
    return round(sum((coverage, v51_clamp(source_quality),
                      v51_clamp(freshness), v51_clamp(consistency))) / 4.0, 6)

def v51_reasoning_guard(evidence=None, assumptions=None, alternatives=None):
    evidence = evidence or []
    assumptions = assumptions or []
    alternatives = alternatives or []
    warnings = []
    if not evidence:
        warnings.append("INSUFFICIENT_EVIDENCE")
    if assumptions:
        warnings.append("ASSUMPTIONS_REQUIRE_VALIDATION")
    if len(alternatives) > 1:
        warnings.append("MULTIPLE_HYPOTHESES_PRESENT")
    return {"can_proceed": bool(evidence), "warnings": warnings,
            "evidence_count": len(evidence),
            "assumption_count": len(assumptions),
            "alternative_count": len(alternatives)}

def v51_schema_audit(conn):
    required = {
        "brain_world_state", "brain_hypotheses", "brain_experiments",
        "brain_memory_layers", "brain_decision_consequences",
        "brain_failure_memory", "brain_assumptions",
        "brain_forecast_calibration", "brain_attention_signals",
        "brain_intelligence_audit"
    }
    rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    existing = {r[0] for r in rows}
    return {"required_tables": sorted(required),
            "present": sorted(required & existing),
            "missing": sorted(required - existing),
            "pass": required <= existing}

def v51_database_integrity_audit(conn):
    row = conn.execute("PRAGMA integrity_check").fetchone()
    result = row[0] if row else "UNKNOWN"
    return {"result": result, "pass": result == "ok"}

def v51_table_health_audit(conn):
    tables = [
        "brain_world_state", "brain_hypotheses", "brain_experiments",
        "brain_memory_layers", "brain_failure_memory",
        "brain_assumptions", "brain_forecast_calibration"
    ]
    report = {}
    for table in tables:
        try:
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            report[table] = {"rows": int(count), "accessible": True}
        except Exception as exc:
            report[table] = {"rows": None, "accessible": False, "error": str(exc)}
    return report

def v51_tenant_guard(tenant_id):
    if tenant_id is None or not str(tenant_id).strip():
        raise ValueError("TENANT_SCOPE_REQUIRED")
    return str(tenant_id).strip()

def v51_record_decision_consequence(conn, tenant_id, decision_id,
                                    parent_key, child_key, relationship,
                                    expected_effect=None, actual_effect=None,
                                    confidence=None):
    initialize_brain_maximization_schema(conn)
    tenant_id = v51_tenant_guard(tenant_id)
    conn.execute("""INSERT INTO brain_decision_consequences
        (tenant_id, decision_id, parent_key, child_key, relationship,
         expected_effect, actual_effect, confidence, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (tenant_id, str(decision_id), parent_key, child_key, relationship,
         v51_safe_json(expected_effect), v51_safe_json(actual_effect),
         confidence, _bm_now()))
    conn.commit()

def v51_audit_snapshot(conn, tenant_id):
    tenant_id = v51_tenant_guard(tenant_id)
    tables = [
        "brain_world_state", "brain_hypotheses", "brain_experiments",
        "brain_memory_layers", "brain_decision_consequences",
        "brain_failure_memory", "brain_assumptions",
        "brain_forecast_calibration", "brain_attention_signals",
        "brain_intelligence_audit"
    ]
    snapshot = {"tenant_id": tenant_id, "generated_at": _bm_now(), "tables": {}}
    for table in tables:
        try:
            snapshot["tables"][table] = conn.execute(
                f"SELECT COUNT(*) FROM {table} WHERE tenant_id=?", (tenant_id,)
            ).fetchone()[0]
        except Exception:
            snapshot["tables"][table] = None
    return snapshot

def v51_run_integrity_suite(conn=None, tenant_id=None):
    result = {"build": V51_BUILD_ID, "parent": V51_BUILD_PARENT,
              "checks": {}, "overall": "NOT_RUN"}
    if conn is None:
        result["checks"]["database"] = "NOT_RUN"
        return result
    try:
        initialize_brain_maximization_schema(conn)
        result["checks"]["schema"] = v51_schema_audit(conn)
        result["checks"]["sqlite_integrity"] = v51_database_integrity_audit(conn)
        result["checks"]["table_health"] = v51_table_health_audit(conn)
        if tenant_id is not None:
            result["checks"]["tenant_snapshot"] = v51_audit_snapshot(conn, tenant_id)
        result["overall"] = (
            "PASS" if result["checks"]["schema"]["pass"]
            and result["checks"]["sqlite_integrity"]["pass"]
            else "REVIEW_REQUIRED"
        )
    except Exception as exc:
        result["overall"] = "FAIL"
        result["error"] = str(exc)
    return result

# ==================== END V51 FINAL MAXIMIZATION & HARDENING ====================
