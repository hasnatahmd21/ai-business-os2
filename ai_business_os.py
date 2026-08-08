#!/usr/bin/env python3
"""
=============================================================================
AI BUSINESS OPERATING SYSTEM™ — MASTER MONOLITH (V1.0.0)
=============================================================================
Unified Architecture containing:
  - Chapter 1: AI Marketing Operating System™
  - Chapter 2: AI Sales Operating System™
  - Chapter 3: AI Content Operating System™
  - Chapter 4: AI Customer Support Operating System™
  - Chapter 5: Knowledge & Operations OS™
=============================================================================
"""

import json
import re
import time
from typing import Dict, List, Any, Optional

# ===========================================================================
# 1. AI MARKETING OPERATING SYSTEM
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
        """Creates a structured 30-second video ad script breakdown."""
        hooks = [
            f"Stop scrolling! If you hate wasting time, you need to see this {product_name}.",
            f"Why is everyone ordering the new {product_name} from {self.brand_name}?",
            f"This simple {product_name} hack will change your daily routine."
        ]
        
        script = {
            "00:00-00:03_Hook": hooks[0],
            "00:03-00:10_Problem": f"Tired of dealing with messy, inefficient tools? Most options break in a week.",
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


# ===========================================================================
# 2. AI SALES OPERATING SYSTEM
# ===========================================================================

class SalesEngine:
    """Scores leads dynamically, routes them, and generates personalized outbound outreach."""
    
    def __init__(self):
        self.high_value_roles = ["CEO", "Founder", "CMO", "Owner", "E-commerce Manager"]

    def score_and_route_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates lead score based on budget, role, and timeline."""
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
        """Drafts short, non-spammy personalized cold outbound email."""
        subject = f"quick question re: {pain_point.lower()}"
        body = (
            f"Hi {lead_name},\n\n"
            f"Noticed a lot of teams struggle with {pain_point}.\n\n"
            f"We built {offer} specifically to eliminate that headache without the friction.\n\n"
            f"Worth a 2-minute look?\n\n"
            f"Best,\nSales Team"
        )
        return {"subject": subject, "body": body}


# ===========================================================================
# 3. AI CONTENT OPERATING SYSTEM
# ===========================================================================

class ContentEngine:
    """Extracts key insights and repurposes content into social threads and video scripts."""

    def repurpose_transcript(self, raw_transcript: str) -> Dict[str, Any]:
        """Extracts key takeaways and builds a multi-platform content bundle."""
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


# ===========================================================================
# 4. AI CUSTOMER SUPPORT OPERATING SYSTEM
# ===========================================================================

class SupportEngine:
    """Triages support tickets by urgency and drafts automated empathetic responses."""

    def __init__(self):
        self.urgent_keywords = ["broken", "refund", "stolen", "scam", "defective", "missing", "cancel"]

    def triage_and_resolve(self, customer_name: str, message: str) -> Dict[str, Any]:
        """Triages urgency and returns an automated resolution response."""
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


# ===========================================================================
# 5. KNOWLEDGE & OPERATIONS OS
# ===========================================================================

class KnowledgeEngine:
    """Simulates internal document retrieval (RAG) and operational QA."""

    def __init__(self):
        self.knowledge_base = {
            "shipping_policy": "Standard delivery takes 2-3 business days. Free shipping applies to orders over $50.",
            "refund_policy": "Full refunds are accepted within 30 days of item delivery in original condition.",
            "fulfillment_sop": "Orders received before 2 PM PKT are processed and dispatched on the same day."
        }

    def query_knowledge_base(self, query: str) -> Dict[str, Any]:
        """Matches internal query against knowledge base keys."""
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
# MASTER ORCHESTRATOR
# ===========================================================================

class AIBusinessOS:
    """Master OS Orchestrator connecting all sub-systems into a single interface."""

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

    def run_full_system_demo(self):
        """Executes an end-to-end simulation across all 5 OS modules."""
        print("\n" + "="*70)
        print("          AI BUSINESS OPERATING SYSTEM™ — FULL PIPELINE DEMO")
        print("="*70 + "\n")

        # 1. Marketing OS Execution
        print(">>> [1/5] RUNNING MARKETING OPERATING SYSTEM...")
        mkt_res = self.marketing.generate_ad_campaign("UltraClean Pro", "Sonic Vibration Tech", "$29.99")
        print(json.dumps(mkt_res, indent=2))
        print("-" * 70)

        # 2. Sales OS Execution
        print(">>> [2/5] RUNNING SALES OPERATING SYSTEM...")
        lead_data = {"name": "Sarah Khan", "job_title": "Founder", "monthly_budget": 5000, "timeline": "Immediate"}
        lead_score = self.sales.score_and_route_lead(lead_data)
        outreach = self.sales.generate_outbound_email("Sarah Khan", "slow delivery times", "ViralCart Express Dispatch")
        print(json.dumps({"lead_evaluation": lead_score, "outreach_draft": outreach}, indent=2))
        print("-" * 70)

        # 3. Content OS Execution
        print(">>> [3/5] RUNNING CONTENT OPERATING SYSTEM...")
        raw_text = "Testing video hooks in the first 3 seconds is critical. Most ad spend is wasted on bad opening frames. Optimize the visual interrupt before increasing budget."
        content_res = self.content.repurpose_transcript(raw_text)
        print(json.dumps(content_res, indent=2))
        print("-" * 70)

        # 4. Support OS Execution
        print(">>> [4/5] RUNNING CUSTOMER SUPPORT OPERATING SYSTEM...")
        support_res = self.support.triage_and_resolve("Ali Raza", "My item arrived broken and I want a full refund immediately!")
        print(json.dumps(support_res, indent=2))
        print("-" * 70)

        # 5. Knowledge OS Execution
        print(">>> [5/5] RUNNING KNOWLEDGE & OPERATIONS OS...")
        kb_res = self.knowledge.query_knowledge_base("What is our refund policy?")
        print(json.dumps(kb_res, indent=2))
        print("="*70)
        print("          SYSTEM EXECUTION COMPLETED SUCCESSFULLY!")
        print("="*70 + "\n")


# ===========================================================================
# EXECUTION ENTRY POINT
# ===========================================================================

if __name__ == "__main__":
    system = AIBusinessOS()
    system.run_full_system_demo()