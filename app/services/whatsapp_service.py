import os
import sys
from dotenv import load_dotenv

# Windows isolation fix: ensure User Roaming site-packages are in path
user_site = os.path.expanduser("~") + r"\AppData\Roaming\Python\Python310\site-packages"
if user_site not in sys.path:
    sys.path.append(user_site)

load_dotenv()

# ── Twilio credentials (loaded from .env) ────────────────────────────────────
ACCOUNT_SID    = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN     = os.getenv("TWILIO_AUTH_TOKEN")
FROM_WHATSAPP  = os.getenv("TWILIO_FROM_WHATSAPP", "whatsapp:+14155238886")  # Twilio sandbox default
OFFICER_PHONE  = os.getenv("OFFICER_PHONE", "8589958840")   # contact number shown in message


def send_match_alert(
    complainant_phone: str,
    missing_name: str,
    match_distance: float = 0.0,
    case_id: int = None,
    location: str = "Unknown Location",
    officer_no: str = "0000000000"
) -> dict:
    """
    Send a WhatsApp alert to `complainant_phone` when a missing person is spotted.

    Args:
        complainant_phone : phone number of the complainant, e.g. '9876543210' or '+919876543210'
        missing_name      : name of the missing person
        match_distance    : cosine distance from the recognition result (lower = better)
        case_id           : optional case ID from the database

    Returns:
        dict with 'success' bool and 'sid' or 'error' keys.
    """
    print(f"[WhatsApp] DEBUG: send_match_alert called for {missing_name} to {complainant_phone}")
    
    if not ACCOUNT_SID or not AUTH_TOKEN:
        print("[WhatsApp] ERROR: Twilio credentials missing in .env")
        raise EnvironmentError(
            "TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN must be set in .env"
        )

    # Normalise phone → WhatsApp format
    to_number = _normalise_phone(complainant_phone)

    similarity_pct = max(0, round((1 - match_distance) * 100, 1))

    case_ref = f"Case #{case_id}" if case_id else "a reported case"

    message_body = (
        f"🚨 *Missing Person Found*\n\n"
        f"Your dear one (*{missing_name}*) is here!\n\n"
        f"📍 Location: *{location}*\n"
        f"📊 Match confidence: *{similarity_pct}%*\n"
        f"📞 Kindly call the officer at: *+91 {officer_no}* for more information.\n\n"
        f"— National Missing Person Support System"
    )

    try:
        print("[WhatsApp] DEBUG: Importing twilio...")
        from twilio.rest import Client
        print("[WhatsApp] DEBUG: Initializing Twilio Client...")
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        print(f"[WhatsApp] DEBUG: Sending message from {FROM_WHATSAPP} to {to_number}...")
        message = client.messages.create(
            from_=FROM_WHATSAPP,
            to=to_number,
            body=message_body,
        )
        print(f"[WhatsApp] Message sent ✔  SID: {message.sid}  →  {to_number}")
        return {"success": True, "sid": message.sid}

    except Exception as e:
        print(f"[WhatsApp] Failed to send message: {e}")
        return {"success": False, "error": str(e)}


def send_report_confirmation(
    complainant_phone: str,
    complainant_name: str,
    missing_name: str,
    case_id: int
) -> dict:
    """
    Send a WhatsApp confirmation to the complainant when they report a missing person.

    Args:
        complainant_phone : phone number of the complainant
        complainant_name  : name of the complainant
        missing_name     : name of the missing person
        case_id          : the case ID assigned

    Returns:
        dict with 'success' bool and 'sid' or 'error' keys.
    """
    if not ACCOUNT_SID or not AUTH_TOKEN:
        return {"success": False, "error": "Twilio credentials not configured"}

    to_number = _normalise_phone(complainant_phone)

    message_body = (
        f"✅ *Report Registered*\n\n"
        f"Dear *{complainant_name}*,\n\n"
        f"Your missing person report for *{missing_name}* has been registered successfully.\n\n"
        f"📋 Case ID: *#{case_id}*\n\n"
        f"You will receive a WhatsApp alert if our system identifies a match.\n\n"
        f"— National Missing Person Support System"
    )

    try:
        from twilio.rest import Client
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            from_=FROM_WHATSAPP,
            to=to_number,
            body=message_body,
        )
        print(f"[WhatsApp] Report confirmation sent ✔  SID: {message.sid}  →  {to_number}")
        return {"success": True, "sid": message.sid}
    except Exception as e:
        print(f"[WhatsApp] Failed to send report confirmation: {e}")
        return {"success": False, "error": str(e)}


def _normalise_phone(phone: str) -> str:
    """
    Convert a raw phone number to 'whatsapp:+91XXXXXXXXXX' format.
    If already starts with '+', use as-is (just prepend whatsapp:).
    """
    phone = phone.strip().replace(" ", "").replace("-", "")
    if phone.startswith("whatsapp:"):
        return phone
    if phone.startswith("+"):
        return f"whatsapp:{phone}"
    if phone.startswith("91") and len(phone) == 12:
        return f"whatsapp:+{phone}"
    # assume Indian number
    return f"whatsapp:+91{phone}"
