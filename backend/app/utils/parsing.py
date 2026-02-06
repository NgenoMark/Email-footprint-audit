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
    if (
        "receipt" in text
        or "invoice" in text
        or "payment" in text
        or "charged" in text
        or "billing" in text
        or "statement" in text
        or "subscription" in text
    ):
        return "receipt"
    if (
        "security alert" in text
        or "new login" in text
        or "login detected" in text
        or "sign-in" in text
        or "sign in" in text
        or "suspicious" in text
    ):
        return "login"
    if (
        "otp" in text
        or "verification code" in text
        or "two-factor" in text
        or "2fa" in text
        or "one-time" in text
        or "security code" in text
    ):
        return "otp"
    if "newsletter" in text or "digest" in text or "weekly" in text:
        return "newsletter"
    if "support" in text or "ticket" in text or "case" in text:
        return "support"
    return "other"
