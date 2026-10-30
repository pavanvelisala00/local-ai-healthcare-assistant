"""Simple educational input/output checks; not clinically validated."""

import re
from typing import Tuple

MAX_INPUT_LENGTH = 1200

EMERGENCY_PATTERNS = (
    r"chest pain",
    r"can't breathe",
    r"cannot breathe",
    r"trouble breathing",
    r"severe bleeding",
    r"unconscious",
    r"stroke symptoms",
    r"suicid(?:e|al)",
)

INJECTION_PATTERNS = (
    r"ignore (?:all )?(?:previous|prior) instructions",
    r"reveal (?:your )?(?:system prompt|hidden instructions)",
    r"act as (?:an? )?(?:unrestricted|uncensored)",
)

MEDICATION_PATTERNS = (
    r"tell me (?:the )?exact dose",
    r"what dose should i take",
    r"how much medication should i take",
)

UNSAFE_OUTPUT_PATTERNS = (
    r"stop taking your prescribed medication",
    r"you definitely have (?:cancer|a heart attack|a stroke)",
    r"take a dangerous amount",
)


def _matches(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def check_input(text: str) -> Tuple[bool, str]:
    """Return (allowed, message) for a user's prompt."""
    if not isinstance(text, str) or not text.strip():
        return False, "Please enter a question."
    if len(text) > MAX_INPUT_LENGTH:
        return False, "The question is too long. Please shorten it."
    if _matches(text, EMERGENCY_PATTERNS):
        return False, (
            "This may describe an emergency. Contact local emergency services "
            "or seek urgent medical attention now. Do not rely on this prototype."
        )
    if _matches(text, INJECTION_PATTERNS):
        return False, "The request was blocked by the prompt-injection check."
    if _matches(text, MEDICATION_PATTERNS):
        return False, (
            "For personal medication dosing, consult a qualified clinician or "
            "pharmacist who knows your medical history."
        )
    return True, ""


def check_output(text: str) -> Tuple[bool, str]:
    """Block selected unsafe response patterns; this is not comprehensive."""
    if not isinstance(text, str) or not text.strip():
        return False, "The model returned an empty response."
    if _matches(text, UNSAFE_OUTPUT_PATTERNS):
        return False, "The response matched a configured safety rule."
    return True, ""
