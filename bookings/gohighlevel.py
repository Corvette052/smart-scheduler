import os
import base64
import json
import logging
import requests

logger = logging.getLogger(__name__)

API_BASE = "https://rest.gohighlevel.com/v1"


def _get_api_key() -> str | None:
    """Return the GoHighLevel API key stripped of whitespace."""
    key = os.getenv("GHL_API_KEY", "").strip()
    return key or None


def _get_location_id(api_key: str | None) -> str | None:
    """Return the location ID either from env or decoded from the API key."""
    loc = os.getenv("GHL_LOCATION_ID")
    if loc:
        return loc.strip()

    if api_key and "." in api_key:
        try:
            payload_part = api_key.split(".")[1]
            padding = "=" * (-len(payload_part) % 4)
            data = json.loads(base64.urlsafe_b64decode(payload_part + padding))
            return data.get("location_id") or data.get("locationId")
        except Exception as exc:
            logger.warning("Failed to decode GHL location id from API key: %s", exc)
    return None


def _get_headers(api_key: str | None) -> dict | None:
    """Return headers for the GHL API or ``None`` if the key is missing."""

    if not api_key:
        print("⚠️  GHL_API_KEY not set; GoHighLevel integration disabled.")
        return None
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def create_contact(full_name: str, email: str | None = None, phone: str | None = None):
    """Create a contact in GoHighLevel.

    The function looks for ``GHL_API_KEY`` and optionally ``GHL_LOCATION_ID`` in
    the environment.  If ``GHL_LOCATION_ID`` isn't provided it will attempt to
    decode it from the JWT-formatted API key.  When the API key is missing the
    call is skipped entirely and ``None`` is returned.
    """
    api_key = _get_api_key()
    headers = _get_headers(api_key)
    if not headers:
        return None
    location_id = _get_location_id(api_key)

    parts = full_name.strip().split()
    first_name = parts[0]
    last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

    payload = {
        "firstName": first_name,
        "lastName": last_name,
    }
    if location_id:
        payload["locationId"] = location_id
    else:
        logger.warning("GHL_LOCATION_ID not configured; contact may fail to be created")
    if email:
        payload["email"] = email
    if phone:
        payload["phone"] = phone

    try:
        resp = requests.post(
            f"{API_BASE}/contacts/",
            json=payload,
            headers=headers,
            timeout=10,
        )
        resp.raise_for_status()
        print(
            f"✅ Created GoHighLevel contact (status {resp.status_code})"
        )
        return resp.json()
    except requests.HTTPError as exc:
        detail = exc.response.text if exc.response else str(exc)
        print(f"❌ Failed to create GoHighLevel contact: {detail}")
        return None
    except Exception as exc:
        print(f"❌ Error creating GoHighLevel contact: {exc}")
        return None
