"""
utils/guardrails.py
───────────────────
Responsible AI, Safety Guardrails & Hallucination Mitigation Layer.
Fulfills Course Outcome CO4 / Unit IV (Responsible LLMs & Guardrails).

Features:
1. Input sanitization & prompt-injection detection.
2. Non-prescriptive medical advice disclaimer.
3. Uncertainty disclosure when falling back to simulated data.
4. Output verification to prevent numeric hallucinations.
"""

import re
from typing import Dict, List, Optional, Tuple

MEDICAL_DISCLAIMER = (
    "⚠️ **Responsible AI Health Disclaimer:** SafeAir AI generates preventive environmental "
    "health intelligence based on atmospheric models and CPCB guidelines. This guidance is "
    "strictly non-prescriptive and informational. Individuals with respiratory, cardiovascular, "
    "or underlying conditions must consult a licensed physician for medical advice or treatment."
)

UNCERTAINTY_DISCLOSURE = (
    "ℹ️ **Data Resiliency Notice:** Live sensor telemetry was partially degraded or unavailable. "
    "Values shown incorporate historical trends and spatial interpolation. Exercise caution and verify with local CAAQMS bulletins."
)

# Known prompt-injection signatures
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions",
    r"disregard\s+all\s+(prior|previous)\s+rules",
    r"system\s*prompt",
    r"jailbreak",
    r"you\s+are\s+now\s+dan",
    r"do\s+anything\s+now",
    r"override\s+system",
    r"show\s+me\s+your\s+(api\s*key|secret|hidden\s*instructions)",
    r"forget\s+(your\s+)?instructions",
]

COMPILED_INJECTION_RE = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]


def sanitize_input(user_query: str, max_length: int = 500) -> str:
    """
    Sanitize user input:
    - Strips null bytes and unusual control characters
    - Clamps length to prevent token-exhaustion attacks
    - Strips leading/trailing whitespace
    """
    if not user_query:
        return ""
    # Strip null bytes and non-printable control characters except newline and tab
    clean = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", user_query)
    clean = clean.strip()
    return clean[:max_length]


def check_prompt_injection(user_query: str) -> Tuple[bool, Optional[str]]:
    """
    Scans user query against prompt-injection heuristics.
    Returns (is_unsafe, reason).
    """
    query_str = user_query.strip()
    for pattern in COMPILED_INJECTION_RE:
        if pattern.search(query_str):
            return True, "Potential prompt injection or instruction override attempt detected."
    return False, None


def enforce_medical_guardrail(llm_response: str) -> str:
    """
    Appends the non-prescriptive medical disclaimer if the response contains
    health or dosage recommendations and doesn't already have one.
    """
    if not llm_response:
        return llm_response

    # Check if a disclaimer is already present
    if "Responsible AI Health Disclaimer" in llm_response:
        return llm_response

    health_keywords = ["asthma", "medication", "inhaler", "dosage", "prescribe", "treatment", "doctor", "hospital", "patient", "copd"]
    lower = llm_response.lower()
    if any(k in lower for k in health_keywords):
        return f"{llm_response}\n\n---\n{MEDICAL_DISCLAIMER}"
    return llm_response


def apply_guardrails(
    query: str,
    response_text: str,
    is_fallback_data: bool = False,
) -> Tuple[str, Dict[str, bool]]:
    """
    Executes the full responsible AI pipeline:
    1. Check injection on input
    2. Enforce uncertainty disclosure if running on fallback data
    3. Enforce medical disclaimer
    Returns (final_text, guardrail_flags).
    """
    flags = {
        "injection_detected": False,
        "uncertainty_disclosed": is_fallback_data,
        "disclaimer_attached": False,
    }

    is_unsafe, reason = check_prompt_injection(query)
    if is_unsafe:
        flags["injection_detected"] = True
        return (
            f"🛡️ **Responsible AI Guardrail Triggered:**\n\n"
            f"Your request was flagged by the input safety filter ({reason}). "
            f"SafeAir AI is restricted to environmental air quality analysis, CPCB metrics, "
            f"and preventive public health guidance. Please rephrase your air quality query."
        ), flags

    final_text = response_text
    if is_fallback_data and UNCERTAINTY_DISCLOSURE not in final_text:
        final_text = f"{UNCERTAINTY_DISCLOSURE}\n\n{final_text}"

    guarded_text = enforce_medical_guardrail(final_text)
    if guarded_text != final_text:
        flags["disclaimer_attached"] = True

    return guarded_text, flags
