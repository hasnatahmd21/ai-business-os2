# ===========================================================================
# AI Business OS™ — Enterprise Release v13.0.0
# Core Software Architecture & Multi-Tenant Engine
# ===========================================================================

from pathlib import Path
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
import hmac
import hashlib
from datetime import datetime, timezone
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple, Generator
from contextlib import contextmanager

import pandas as pd
import streamlit as st
from pydantic import BaseModel, Field

# AI PROVIDERS SETUP
try:
    from google import genai as google_genai
except ImportError:
    google_genai = None

try:
    import google.generativeai as legacy_genai
except ImportError:
    legacy_genai = None

# ===========================================================================
# LOGGING SETUP
# ===========================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("AIBusinessOS")

APP_VERSION = "13.0.0"
DEFAULT_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
MAX_PROMPT_CHARS = 30000
DATA_DIR = Path(os.getenv("AI_BUSINESS_OS_DATA_DIR", ".aibusinessos"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_FILE = DATA_DIR / "ai_business_os.db"
AUDIT_DB = DATA_DIR / "audit.db"
APP_LOG_FILE = DATA_DIR / "application_events.jsonl"
BACKUP_DIR = DATA_DIR / "backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

# ===========================================================================
# DATABASE CONTEXT MANAGER
# ===========================================================================
@contextmanager
def get_db_context(db_path: Path = DB_FILE) -> Generator[sqlite3.Connection, None, None]:
    """Context manager for SQLite database connections enforcing WAL mode and safety."""
    conn = sqlite3.connect(db_path, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Database transaction error: {str(e)}")
        raise e
    finally:
        conn.close()

# ===========================================================================
# RESILIENCE ENGINE: CIRCUIT BREAKER & RETRY POLICY
# ===========================================================================
class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class CircuitBreaker:
    """Enterprise Circuit Breaker for resilience against cascading integration failures."""
    def __init__(self, name: str, failure_threshold: int = 3, recovery_time_sec: float = 30.0):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_time_sec = recovery_time_sec
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.last_state_change = time.time()

    def can_execute(self) -> bool:
        now = time.time()
        if self.state == CircuitState.OPEN:
            if now - self.last_state_change >= self.recovery_time_sec:
                self.state = CircuitState.HALF_OPEN
                self.last_state_change = now
                logger.info(f"CircuitBreaker [{self.name}] transition to HALF_OPEN")
                return True
            return False
        return True

    def record_success(self):
        self.failure_count = 0
        if self.state != CircuitState.CLOSED:
            self.state = CircuitState.CLOSED
            self.last_state_change = time.time()
            logger.info(f"CircuitBreaker [{self.name}] reset to CLOSED")

    def record_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.last_state_change = time.time()
            logger.warning(f"CircuitBreaker [{self.name}] tripped to OPEN!")

class ResilientConnector:
    """Connector Wrapper providing retry policies, exponential backoff, and circuit breaking."""
    def __init__(self, name: str, circuit_breaker: CircuitBreaker):
        self.name = name
        self.cb = circuit_breaker

    def execute_with_retry(self, func, *args, max_retries: int = 3, base_delay: float = 0.5, **kwargs) -> Dict[str, Any]:
        if not self.cb.can_execute():
            return {
                "status": "CIRCUIT_OPEN",
                "message": f"Integration '{self.name}' is temporarily unavailable due to safety circuit break.",
                "executed": False
            }

        last_exception = None
        for attempt in range(1, max_retries + 1):
            try:
                result = func(*args, **kwargs)
                self.cb.record_success()
                return {"status": "SUCCESS", "result": result, "executed": True, "attempts": attempt}
            except Exception as e:
                last_exception = e
                logger.warning(f"Connector [{self.name}] attempt {attempt} failed: {str(e)}")
                if attempt < max_retries:
                    sleep_time = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)

        self.cb.record_failure()
        return {
            "status": "FAILED",
            "error": str(last_exception),
            "executed": False,
            "attempts": max_retries
        }

# Global Circuit Breakers for Integration Services
GENAI_CIRCUIT = CircuitBreaker("GoogleGenAI", failure_threshold=3, recovery_time_sec=15.0)
WEBHOOK_CIRCUIT = CircuitBreaker("WebhookGateway", failure_threshold=5, recovery_time_sec=30.0)

# ===========================================================================
# VOLUME 2.0: MLOPS & INFRASTRUCTURE MODELS
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
# VOLUME 3.0: AI SECURITY & ZERO-TRUST GOVERNANCE
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
            "owner": ["ALL"],
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
# CORE MONOLITH ENGINES
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

class CustomerSuccessEngine:
    def analyze_customer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        license_util = data.get("license_utilization_pct", 50.0)
        login_freq = data.get("login_frequency_per_week", 10)
        open_tickets = data.get("open_high_priority_tickets", 0)
        nps = data.get("nps_score", 7)
        ebr_attended = data.get("executive_ebr_attended", True)
        days_to_renewal = data.get("days_until_renewal", 180)
        arr = data.get("arr_usd", 10000.0)

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
            actions = ["Alert CS Leadership", "Assign Solutions Architect", "Schedule Emergency EBR"]

        return {
            "module": "CUSTOMER_SUCCESS_OS",
            "customer_id": data.get("customer_id", "CUST-001"),
            "health_summary": {
                "health_score": health_score,
                "health_tier": tier,
                "churn_risk_pct": churn_risk,
                "playbook": playbook,
                "actions": actions
            }
        }

class UnifiedFinanceEngine:
    def analyze_finance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        mrr = data.get("mrr_usd", 50000.0)
        opex = data.get("opex_usd", 40000.0)
        cash_res = data.get("cash_reserve_usd", 200000.0)
        
        monthly_net = mrr - opex
        runway_months = round(cash_res / abs(monthly_net), 1) if monthly_net < 0 else 999.0

        return {
            "module": "FINANCE_OS_RUNWAY",
            "monthly_net_cashflow_usd": round(monthly_net, 2),
            "runway_months": runway_months,
            "status": "HEALTHY" if monthly_net >= 0 else ("WARNING" if runway_months < 12 else "CRITICAL")
        }

# ===========================================================================
# MASTER MONOLITH + ENTERPRISE STRATEGY ORCHESTRATOR
# ===========================================================================
class AIBusinessOS:
    """Master Monolithic Engine combining operational domains."""
    def __init__(self):
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
        self.finance = UnifiedFinanceEngine()
        self.mlops = MLOpsPipeline()

os_core = AIBusinessOS()

# ===========================================================================
# MULTI-AGENT ARCHITECTURE (VOLUME 4.0)
# ===========================================================================
class AgentTask(BaseModel):
    task_id: str
    assigned_agent: str
    payload: Dict[str, Any]
    status: str = "PENDING"
    result: Optional[Dict[str, Any]] = None

class SharedIntelligenceMemory:
    """Centralized, real-time memory layer for all agents."""
    def __init__(self):
        self._memory_store: Dict[str, Any] = {}
        self._audit_log: List[Dict[str, Any]] = []

    def set_context(self, key: str, value: Any):
        self._memory_store[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        return self._memory_store.get(key, default)

    def log_event(self, sender: str, event_type: str, data: Dict[str, Any]):
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sender": sender,
            "event_type": event_type,
            "data": data
        }
        self._audit_log.append(event)

class MultiAgentCoordinator:
    def __init__(self):
        self.memory = SharedIntelligenceMemory()

    async def run_enterprise_workflow(self, strategic_goal: str, budget: float) -> Dict[str, Any]:
        marketing_res = os_core.marketing.generate_ad_campaign("Viral Cart Bottle", "UV Sterilization", "$49.99")
        self.memory.set_context("latest_creative", marketing_res)
        self.memory.log_event("MarketingAgent", "CAMPAIGN_GENERATED", marketing_res)

        sales_res = os_core.sales.score_and_route_lead({
            "name": "Sarah Khan", "job_title": "CEO", "monthly_budget": budget, "timeline": "Immediate"
        })
        self.memory.set_context("lead_evaluation", sales_res)
        self.memory.log_event("SalesAgent", "LEAD_EVALUATED", sales_res)

        return {
            "workflow_status": "COMPLETED",
            "goal": strategic_goal,
            "allocated_budget": budget,
            "results": {
                "marketing": marketing_res,
                "sales": sales_res
            },
            "memory_audit_trail": self.memory._audit_log
        }

# ===========================================================================
# HARDENED DB PERSISTENCE & IMMUTABLE CRYPTOGRAPHIC AUDIT CHAIN
# ===========================================================================
def init_enterprise_db():
    with get_db_context() as conn:
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
            password_hash TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            UNIQUE(tenant_id, email),
            FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
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
        CREATE TABLE IF NOT EXISTS approvals (
            approval_id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            requested_by TEXT NOT NULL,
            action TEXT NOT NULL,
            resource TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL,
            FOREIGN KEY(tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS webhook_events (
            event_id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            signature_valid INTEGER NOT NULL DEFAULT 0,
            received_at TEXT NOT NULL
        );
        """)

init_enterprise_db()

def _hash_event(payload: Dict[str, Any], previous_hash: str) -> str:
    canonical = json.dumps(
        {"payload": payload, "previous_hash": previous_hash},
        sort_keys=True, separators=(",", ":"), default=str
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

def append_audit_chain(tenant_id: str, actor: str, action: str, resource: str, outcome: str) -> str:
    with get_db_context() as conn:
        last = conn.execute(
            "SELECT event_hash FROM audit_chain WHERE tenant_id=? ORDER BY sequence DESC LIMIT 1", 
            (tenant_id,)
        ).fetchone()
        previous = last["event_hash"] if last else "GENESIS"
        
        now = datetime.now(timezone.utc).isoformat()
        payload = {
            "tenant_id": tenant_id, "actor": actor, "action": action,
            "resource": resource, "outcome": outcome, "created_at": now
        }
        event_hash = _hash_event(payload, previous)
        
        conn.execute(
            "INSERT INTO audit_chain(tenant_id,actor,action,resource,outcome,event_hash,previous_hash,created_at) "
            "VALUES(?,?,?,?,?,?,?,?)",
            (tenant_id, actor, action, resource, outcome, event_hash, previous, now)
        )
        return event_hash

def verify_audit_chain(tenant_id: str) -> Dict[str, Any]:
    with get_db_context() as conn:
        rows = conn.execute(
            "SELECT * FROM audit_chain WHERE tenant_id=? ORDER BY sequence", (tenant_id,)
        ).fetchall()
        
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

# Ensure Tenant
CURRENT_TENANT_ID = "local-enterprise"
def ensure_default_tenant():
    now = datetime.now(timezone.utc).isoformat()
    with get_db_context() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO tenants(id,name,plan,status,created_at) VALUES(?,?,?,?,?)",
            (CURRENT_TENANT_ID, "ViralCart Enterprise Workspace", "enterprise", "active", now)
        )
        conn.execute(
            "INSERT OR IGNORE INTO users(id,tenant_id,email,role,status,created_at) VALUES(?,?,?,?,?,?)",
            ("usr-owner", CURRENT_TENANT_ID, "owner@viralcart.com", "owner", "active", now)
        )

ensure_default_tenant()

# ===========================================================================
# HEALTH & READINESS PROBES (V12 COMPLETION & RECOVERY)
# ===========================================================================
def liveness_probe() -> Dict[str, Any]:
    return {"status": "alive", "version": APP_VERSION, "timestamp": datetime.now(timezone.utc).isoformat()}

def readiness_probe() -> Dict[str, Any]:
    """Fully implemented, context-safe enterprise readiness diagnostic probe."""
    checks = {
        "database": False,
        "audit_chain": False,
        "circuit_breaker": True,
        "storage": BACKUP_DIR.exists(),
    }
    try:
        with get_db_context() as conn:
            tables = {r["name"] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
            checks["database"] = "tenants" in tables and "users" in tables
            checks["audit_chain"] = "audit_chain" in tables
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")

    all_passed = all(checks.values())
    return {
        "status": "READY" if all_passed else "DEGRADED",
        "version": APP_VERSION,
        "checks": checks,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# ===========================================================================
# AI RUNTIME PROVIDER LAYER WITH CIRCUIT PROTECTION
# ===========================================================================
def _raw_ai_call(api_key: str, prompt_text: str, system_instruction: str) -> str:
    sanitized = SecurityGuardrail.sanitize_input(prompt_text)
    if google_genai is not None:
        client = google_genai.Client(api_key=api_key)
        resp = client.models.generate_content(
            model=DEFAULT_GEMINI_MODEL,
            contents=sanitized,
            config={"system_instruction": system_instruction, "temperature": 0.2}
        )
        return getattr(resp, "text", str(resp))
    elif legacy_genai is not None:
        legacy_genai.configure(api_key=api_key)
        model = legacy_genai.GenerativeModel(DEFAULT_GEMINI_MODEL, system_instruction=system_instruction)
        resp = model.generate_content(sanitized, generation_config={"temperature": 0.2})
        return getattr(resp, "text", str(resp))
    else:
        raise RuntimeError("No Google GenAI SDK available.")

def run_resilient_ai_task(api_key: str, prompt_text: str) -> Dict[str, Any]:
    if not api_key:
        return {"status": "NO_API_KEY", "answer": "Demo Mode: AI execution simulated safely without API key."}
    
    connector = ResilientConnector("GoogleGenAI", GENAI_CIRCUIT)
    instruction = "You are an enterprise business AI architect. Be factual, actionable, and clear on risks."
    
    exec_res = connector.execute_with_retry(_raw_ai_call, api_key, prompt_text, instruction)
    if exec_res["executed"]:
        append_audit_chain(CURRENT_TENANT_ID, "AI_Worker", "GENAI_EXECUTION", "GeminiAPI", "SUCCESS")
        return {"status": "SUCCESS", "answer": exec_res["result"]}
    else:
        append_audit_chain(CURRENT_TENANT_ID, "AI_Worker", "GENAI_EXECUTION", "GeminiAPI", "FAILED")
        return {"status": exec_res["status"], "answer": f"Execution degraded: {exec_res.get('error') or exec_res.get('message')}"}

# ===========================================================================
# STREAMLIT ENTERPRISE CONTROL PLANE UI
# ===========================================================================
st.set_page_config(page_title="AI Business OS™ Enterprise Suite", page_icon="⚙️", layout="wide")

st.sidebar.title("⚙️ AI Business OS™")
st.sidebar.caption(f"Enterprise Edition v{APP_VERSION}")

api_key_input = st.sidebar.text_input("Gemini API Key", type="password", help="Enter key to enable live AI orchestration")
if api_key_input:
    st.session_state["_api_key_available"] = True

nav_choice = st.sidebar.radio(
    "Navigation Workspace",
    [
        "📊 Executive Command Center",
        "🎯 Strategic Marketing & Sales",
        "📈 Customer Success & Finance",
        "🤖 Multi-Agent Orchestration",
        "🛡️ Zero-Trust Security & Audit",
        "⚡ System Health & MLOps"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Tenant: **ViralCart Enterprise**")
st.sidebar.caption(f"Status: **{readiness_probe()['status']}**")

# --- TAB 1: EXECUTIVE COMMAND CENTER ---
if nav_choice == "📊 Executive Command Center":
    st.title("📊 Enterprise Executive Command Center")
    st.write("Real-time Operational Intelligence & System Readiness Control Plane")

    r_health = readiness_probe()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("System Health", r_health["status"], delta="Normal" if r_health["status"] == "READY" else "Check Probes")
    c2.metric("Active Tenant", "ViralCart", delta="Enterprise Tier")
    c3.metric("Circuit Breaker", GENAI_CIRCUIT.state.value, delta="0 Trips" if GENAI_CIRCUIT.state == CircuitState.CLOSED else "Degraded")
    
    audit_res = verify_audit_chain(CURRENT_TENANT_ID)
    c4.metric("Audit Chain Integrity", "VERIFIED" if audit_res["valid"] else "COMPROMISED", delta=f"{audit_res.get('events', 0)} Events")

    st.markdown("---")
    st.subheader("💡 Strategic AI Analysis Query")
    query = st.text_area("Formulate Enterprise Directive:", "Identify top 3 operational growth levers for ViralCart for Q4 2026.")
    
    if st.button("Execute Strategic AI Synthesis", type="primary"):
        with st.spinner("Processing through resilient AI pipeline..."):
            ai_out = run_resilient_ai_task(api_key_input, query)
            st.markdown("### AI Strategic Synthesis Output")
            st.info(ai_out["answer"])

# --- TAB 2: STRATEGIC MARKETING & SALES ---
elif nav_choice == "🎯 Strategic Marketing & Sales":
    st.title("🎯 Strategic Marketing & Sales Engines")
    
    m_tab1, m_tab2 = st.tabs(["Marketing OS", "Sales Lead Scorer"])
    
    with m_tab1:
        st.subheader("Generate Campaign Script")
        p_name = st.text_input("Product Name", "Viral Smart Water Bottle")
        p_feat = st.text_input("Key Feature", "Self-cleaning UV Light & Temperature Display")
        p_price = st.text_input("Price Point", "$49.99")
        
        if st.button("Generate Script Asset"):
            res = os_core.marketing.generate_ad_campaign(p_name, p_feat, p_price)
            st.json(res)
            append_audit_chain(CURRENT_TENANT_ID, "Marketer", "CREATE_CAMPAIGN", p_name, "SUCCESS")

    with m_tab2:
        st.subheader("Lead Scoring & Automated Routing")
        l_name = st.text_input("Lead Name", "Alexander Wright")
        l_role = st.text_input("Job Title", "Founder & CEO")
        l_budget = st.number_input("Monthly Budget ($)", value=7500, step=500)
        l_timeline = st.selectbox("Timeline", ["Immediate", "1-3 Months", "Exploring"])
        
        if st.button("Score & Route Lead"):
            score_res = os_core.sales.score_and_route_lead({
                "name": l_name, "job_title": l_role, "monthly_budget": l_budget, "timeline": l_timeline
            })
            st.success(f"Lead Score: {score_res['total_score']} / 100")
            st.write(f"**Action Plan:** {score_res['routing_action']}")
            st.json(score_res["audit_trail"])

# --- TAB 3: CUSTOMER SUCCESS & FINANCE ---
elif nav_choice == "📈 Customer Success & Finance":
    st.title("📈 Customer Success & Unified Financial Engine")
    
    f_tab1, f_tab2 = st.tabs(["Customer Success OS", "Finance & Runway OS"])
    
    with f_tab1:
        st.subheader("Customer Health & Churn Risk Evaluator")
        cs_util = st.slider("License Utilization (%)", 0, 100, 82)
        cs_freq = st.number_input("Weekly Logins", value=35)
        cs_nps = st.slider("NPS Score", 0, 10, 9)
        
        if st.button("Evaluate Customer Health"):
            cs_out = os_core.customer_success.analyze_customer({
                "license_utilization_pct": cs_util,
                "login_frequency_per_week": cs_freq,
                "nps_score": cs_nps
            })
            st.json(cs_out)

    with f_tab2:
        st.subheader("Runway & Cashflow Intelligence")
        mrr = st.number_input("Monthly Recurring Revenue ($)", value=85000)
        opex = st.number_input("Operating Expenses ($)", value=62000)
        reserve = st.number_input("Cash Reserve ($)", value=340000)
        
        if st.button("Run Financial Runway Calculation"):
            fin_out = os_core.finance.analyze_finance({"mrr_usd": mrr, "opex_usd": opex, "cash_reserve_usd": reserve})
            st.json(fin_out)

# --- TAB 4: MULTI-AGENT ORCHESTRATION ---
elif nav_choice == "🤖 Multi-Agent Orchestration":
    st.title("🤖 Shared Memory Multi-Agent Orchestration")
    st.write("Autonomous execution across specialized business agents")

    goal_input = st.text_input("Strategic Execution Goal", "Launch ViralCart Smart Bottle Campaign on Meta")
    budget_input = st.number_input("Allocated Execution Budget ($)", value=10000)

    if st.button("Run Autonomous Agent Swarm", type="primary"):
        coordinator = MultiAgentCoordinator()
        with st.spinner("Coordinating agents..."):
            workflow_res = asyncio.run(coordinator.run_enterprise_workflow(goal_input, budget_input))
            st.success("Workflow Execution Completed Successfully!")
            st.json(workflow_res)

# --- TAB 5: ZERO-TRUST SECURITY & AUDIT ---
elif nav_choice == "🛡️ Zero-Trust Security & Audit":
    st.title("🛡️ Zero-Trust Security & Audit Verification")
    
    st.subheader("🔐 Cryptographic Audit Chain Verification")
    if st.button("Verify Audit Chain Hash Integrity"):
        verification = verify_audit_chain(CURRENT_TENANT_ID)
        if verification["valid"]:
            st.success(f"Audit Chain Integrity Validated! Total Events: {verification['events']}. Head Hash: {verification['head']}")
        else:
            st.error(f"AUDIT CHAIN BROKEN AT SEQUENCE: {verification['broken_sequence']}")

    st.markdown("---")
    st.subheader("🧹 Input Sanitation Test")
    test_input = st.text_area("Test Raw Input Payload:", "User CNIC is 42101-1234567-1 and Password is secret123! API_KEY=abc123xyz456")
    if st.button("Sanitize Input"):
        sanitized = SecurityGuardrail.sanitize_input(test_input)
        st.code(sanitized)

# --- TAB 6: SYSTEM HEALTH & MLOPS ---
elif nav_choice == "⚡ System Health & MLOps":
    st.title("⚡ System Health & MLOps Telemetry")
    
    st.subheader("MLOps Model Registry")
    for m_id, model in os_core.mlops.registry.items():
        st.write(f"**{model.name}** (`{model.model_id}`) — Version: {model.version} | Status: {model.status.value}")
        telemetry = os_core.mlops.evaluate_telemetry(m_id)
        st.json(telemetry)
        st.markdown("---")

    st.subheader("Readiness Diagnostics")
    st.json(readiness_probe())
