"""
Server-Driven UI Endpoint
Returns dynamic UI JSON based on client context:
- App version
- Patch ID (A/B test, hotfix)
- Location (campus, country)
- Time (morning/evening, events)
"""
from fastapi import APIRouter, Request, HTTPException
from datetime import datetime
from typing import Dict, Any
import pytz

router = APIRouter(prefix="/ui", tags=["ui"])

# Mock UI configurations per version/patch/location/time
UI_CONFIGS = {
    "v1.0": {
        "default": {
            "tabs": [
                {"id": "home", "label": "Home", "icon": "home", "route": "/"},
                {"id": "sparks", "label": "Sparks", "icon": "bolt", "route": "/sparks"},
                {"id": "routines", "label": "Routines", "icon": "calendar", "route": "/routines"},
                {"id": "profile", "label": "Profile", "icon": "user", "route": "/profile"}
            ],
            "theme": "dark",
            "features": ["sparks", "routines"],
            "welcomeMessage": "Welcome to Blip!"
        },
        "patch-welcome-video": {
            "welcomeMessage": "🎉 Welcome! Watch our quick tour?",
            "showTutorial": True,
            "tutorialVideoUrl": "https://example.com/tutorial.mp4"
        }
    },
    "v1.5": {
        "default": {
            "tabs": [
                {"id": "home", "label": "Home", "icon": "home", "route": "/"},
                {"id": "clusters", "label": "Clusters", "icon": "users", "route": "/clusters"},
                {"id": "sparks", "label": "Sparks", "icon": "bolt", "route": "/sparks"},
                {"id": "routines", "label": "Routines", "icon": "calendar", "route": "/routines"},
                {"id": "profile", "label": "Profile", "icon": "user", "route": "/profile"}
            ],
            "theme": "dark",
            "features": ["clusters", "sparks", "routines", "matching"],
            "welcomeMessage": "Welcome back! Ready to connect?"
        },
        "patch-match-poll": {
            "poll": {
                "question": "How are you feeling today?",
                "options": ["🔥 Fired Up", "😊 Good", "😴 Tired", "🌧️ Low"],
                "expiresAt": (datetime.now() + timedelta(hours=24)).isoformat()
            }
        }
    }
}

# Location-based banners
LOCATION_BANNERS = {
    "new york": {"text": "🎉 BlipNYU Launch Week! Join the welcome event.", "type": "event", "pin": True},
    "los angeles": {"text": "☀️ BlipUCLA Hackathon starts tomorrow!", "type": "event", "pin": True},
    "london": {"text": "🎉 BlipImperial Meetup — RSVP now!", "type": "event", "pin": True},
}

# Time-based greetings
def get_greeting(time: datetime):
    hour = time.hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 21:
        return "Good evening"
    else:
        return "Hey there"

@router.get("")
async def get_ui_config(request: Request) -> Dict[str, Any]:
    """
    Returns dynamic UI JSON based on headers
    """
    version = request.headers.get("X-App-Version", "1.0").strip()
    patch_id = request.headers.get("X-Patch-ID", "").strip()
    location = request.headers.get("X-Location", "").lower().strip()
    time_str = request.headers.get("X-Time")

    # Parse time
    try:
        if time_str:
            client_time = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        else:
            client_time = datetime.now(pytz.utc)
    except Exception:
        client_time = datetime.now(pytz.utc)

    # Localize time to user's timezone if available in location
    timezone = None
    if "new york" in location:
        timezone = pytz.timezone("America/New_York")
    elif "los angeles" in location:
        timezone = pytz.timezone("America/Los_Angeles")
    elif "london" in location:
        timezone = pytz.timezone("Europe/London")
    elif "india" in location or "mumbai" in location or "delhi" in location:
        timezone = pytz.timezone("Asia/Kolkata")

    if timezone:
        client_time = client_time.astimezone(timezone)

    # Select config based on version
    version_key = f"v{version.split('.')[0]}.{version.split('.')[1]}"
    base_config = UI_CONFIGS.get(version_key, UI_CONFIGS["v1.0"])["default"]

    # Override with patch config
    if patch_id and patch_id in UI_CONFIGS.get(version_key, {}):
        patch_config = UI_CONFIGS[version_key][patch_id]
        base_config = {**base_config, **patch_config}

    # Add location banner
    if location:
        for loc in LOCATION_BANNERS:
            if loc in location:
                base_config["banner"] = LOCATION_BANNERS[loc]
                break

    # Add greeting
    base_config["greeting"] = get_greeting(client_time)

    # Add server time
    base_config["serverTime"] = datetime.now(pytz.utc).isoformat()
    base_config["timezone"] = str(timezone) if timezone else "UTC"

    # Add metadata
    base_config["metadata"] = {
        "version": version,
        "patchId": patch_id or None,
        "location": location or None,
        "clientTime": time_str,
        "responseTime": datetime.now(pytz.utc).isoformat()
    }

    return base_config
