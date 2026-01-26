import re
from email.utils import parseaddr


def extract_domain(from_address: str) -> str:
    _, addr = parseaddr(from_address)
    target = addr or from_address
    match = re.search(r"@([A-Za-z0-9.-]+)$", target.strip())
    if not match:
        return ""
    return match.group(1).lower()


def classify_evidence_type(subject: str) -> str:
    text = subject.lower()
    if "welcome" in text:
        return "welcome"
    if "verify" in text or "confirm your email" in text or "confirm email" in text:
        return "verify"
    if "password reset" in text or "reset your password" in text:
        return "reset"
    if "receipt" in text or "invoice" in text or "payment" in text:
        return "receipt"
    if "new login" in text or "login detected" in text:
        return "login"
    if "otp" in text or "verification code" in text or "two-factor" in text:
        return "otp"
    return "other"
