import os
import requests

GHL_API_KEY = os.getenv("GHL_API_KEY")
API_BASE = "https://rest.gohighlevel.com/v1"

headers = None
if GHL_API_KEY:
    headers = {
        "Authorization": f"Bearer {GHL_API_KEY}",
        "Content-Type": "application/json",
    }
else:
    print("⚠️  GHL_API_KEY not set; GoHighLevel integration disabled.")


def create_contact(full_name: str, email: str | None = None, phone: str | None = None):
    """Create a contact in GoHighLevel.

    If `GHL_API_KEY` is missing the function simply logs a warning and
    returns ``None``.
    """
    if not headers:
        return None

    parts = full_name.strip().split()
    first_name = parts[0]
    last_name = "".join(parts[1:]) if len(parts) > 1 else ""

    payload = {
        "firstName": first_name,
        "lastName": last_name,
    }
    if email:
        payload["email"] = email
    if phone:
        payload["phone"] = phone

    try:
        resp = requests.post(f"{API_BASE}/contacts/", json=payload, headers=headers)
        resp.raise_for_status()
        print("✅ Created GoHighLevel contact")
        return resp.json()
    except Exception as exc:
        print(f"❌ Failed to create GoHighLevel contact: {exc}")
        return None
