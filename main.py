from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from typing import Dict, Any

# Database helper
from database import db

app = FastAPI(title="1bena API", version="1.1.0")

# CORS (allow frontend dev server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
def test():
    return {"ok": True, "service": "1bena-api", "time": datetime.now(timezone.utc).isoformat()}


def _fallback_stats() -> Dict[str, Any]:
    return {
        "users": 24567,
        "completed_deliveries": 183420,
        "active_drivers": 850,
        "partner_merchants": 320,
        "cities": ["Banjul", "Serrekunda", "Brikama", "Bakau"],
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "source": "fallback",
    }

@app.get("/stats")
def get_stats():
    """
    Aggregate key metrics. If MongoDB is configured and collections exist, return live counts.
    Collections used (optional): user, delivery, driver, merchant
    """
    # If DB not configured, or any error occurs, return fallback demo metrics
    try:
        if db is None:
            return _fallback_stats()

        # Count documents if collections exist; if not, default to 0 for each
        users = db["user"].count_documents({}) if "user" in db.list_collection_names() else 0
        deliveries = db["delivery"].count_documents({}) if "delivery" in db.list_collection_names() else 0
        drivers = db["driver"].count_documents({}) if "driver" in db.list_collection_names() else 0
        merchants = db["merchant"].count_documents({}) if "merchant" in db.list_collection_names() else 0
        cities = [c.get("name", "") for c in db["city"].find({}, {"name": 1})] if "city" in db.list_collection_names() else [
            "Banjul", "Serrekunda", "Brikama", "Bakau"
        ]

        data = {
            "users": users or 0,
            "completed_deliveries": deliveries or 0,
            "active_drivers": drivers or 0,
            "partner_merchants": merchants or 0,
            "cities": cities,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "source": "database",
        }

        # If the database is empty (all zeros), fall back to demo values for a better preview experience
        if sum([data["users"], data["completed_deliveries"], data["active_drivers"], data["partner_merchants"]]) == 0:
            return _fallback_stats()

        return data
    except Exception:
        return _fallback_stats()
