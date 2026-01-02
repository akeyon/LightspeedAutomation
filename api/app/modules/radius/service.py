from sqlalchemy import text
from app.core.database import SessionLocal


def radius_auth(mac: str, ip: str):
    mac = mac.lower()
    db = SessionLocal()

    try:
        # 1. Resolve router (for now, single-router lab setup)
        router = db.execute(
            text("SELECT id FROM routers WHERE is_active=true LIMIT 1")
        ).fetchone()

        if not router:
            return {"allow": False}

        router_id = router.id

        # 2. Get or create device
        device = db.execute(
            text("SELECT id FROM devices WHERE mac_address=:m"),
            {"m": mac}
        ).fetchone()

        if not device:
            db.execute(
                text("INSERT INTO devices (mac_address) VALUES (:m)"),
                {"m": mac}
            )
            db.commit()

            device = db.execute(
                text("SELECT id FROM devices WHERE mac_address=:m"),
                {"m": mac}
            ).fetchone()

        device_id = device.id

        # 3. Check active access grant
        grant = db.execute(text("""
            SELECT *
            FROM access_grants
            WHERE device_id=:did
              AND router_id=:rid
              AND is_active=true
              AND start_at <= NOW()
              AND expires_at > NOW()
            ORDER BY expires_at DESC
            LIMIT 1
        """), {"did": device_id, "rid": router_id}).fetchone()

        if not grant:
            return {"allow": False}

        # 4. Grant access
        return {
            "allow": True,
            "session_timeout": grant.session_timeout,
            "rate_limit": grant.rate_limit
        }

    finally:
        db.close()
