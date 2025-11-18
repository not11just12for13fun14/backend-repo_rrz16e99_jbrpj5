from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone

app = FastAPI(title="1bena API", version="1.0.0")

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

@app.get("/stats")
def get_stats():
    # Static demo metrics; can be wired to MongoDB later
    return {
        "users": 24567,
        "completed_deliveries": 183420,
        "active_drivers": 850,
        "partner_merchants": 320,
        "cities": ["Banjul", "Serrekunda", "Brikama", "Bakau"],
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
