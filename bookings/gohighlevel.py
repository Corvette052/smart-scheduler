import os
import base64
import json
import logging
import requests

logger = logging.getLogger(__name__)

GHL_API_KEY = os.getenv("GHL_API_KEY")
API_BASE = "https://rest.gohighlevel.com/v1"
GHL_LOCATION_ID = os.getenv("GHL_LOCATION_ID")

headers = None
if GHL_API_KEY:
    headers = {
        "Authorization": f"Bearer {GHL_API_KEY}",
        "Content-Type": "application/json",
    }
    if not GHL_LOCATION_ID and "." in GHL_API_KEY:
        try:
            # decode the JWT payload to extract the location id
            payload_part = GHL_API_KEY.split(".")[1]
            padding = "=" * (-len(payload_part) % 4)
            data = json.loads(base64.urlsafe_b64decode(payload_part + padding))
            GHL_LOCATION_ID = data.get("location_id") or data.get("locationId")
        except Exception as exc:
            logger.warning("Failed to decode GHL location id from API key: %s", exc)
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
    if GHL_LOCATION_ID:
        payload["locationId"] = GHL_LOCATION_ID
    else:
        logger.warning("GHL_LOCATION_ID not configured; contact may fail to be created")
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
