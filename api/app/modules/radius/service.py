from datetime import datetime
from sqlalchemy import text
from app.core.database import SessionLocal
from app.shared.constants import (
    FREE_SESSION_SECONDS,
    FREE_RATE_LIMIT,
    PAID_RATE_LIMIT
)


def radius_auth(username: str, mac: str, ip: str):
    db = SessionLocal()

    # 1. Get or create user
    user = db.execute(
        text("SELECT id FROM users WHERE username=:u"),
        {"u": username}
    ).fetchone()

    if not user:
        db.execute(
            text("INSERT INTO users (username, mac_address) VALUES (:u, :m)"),
            {"u": username, "m": mac}
        )
        db.commit()
        user = db.execute(
            text("SELECT id FROM users WHERE username=:u"),
            {"u": username}
        ).fetchone()

    user_id = user.id

    # 2. Paid session?
    paid = db.execute(text("""
        SELECT * FROM sessions
        WHERE user_id=:uid
        AND is_active=true
        AND session_type='paid'
    """), {"uid": user_id}).fetchone()

    if paid:
        return {
            "allow": True,
            "timeout": 3600,
            "rate": PAID_RATE_LIMIT
        }

    # 3. Free session?
    free = db.execute(text("""
        SELECT * FROM sessions
        WHERE user_id=:uid
        AND is_active=true
        AND session_type='free'
    """), {"uid": user_id}).fetchone()

    if free:
        elapsed = (datetime.utcnow() - free.start_time).total_seconds()
        remaining = FREE_SESSION_SECONDS - int(elapsed)

        if remaining > 0:
            return {
                "allow": True,
                "timeout": remaining,
                "rate": FREE_RATE_LIMIT
            }
        else:
            db.execute(
                text("UPDATE sessions SET is_active=false WHERE id=:id"),
                {"id": free.id}
            )
            db.commit()

    # 4. Create new free session
    db.execute(text("""
        INSERT INTO sessions (user_id, session_type, ip_address, mac_address)
        VALUES (:uid, 'free', :ip, :mac)
    """), {"uid": user_id, "ip": ip, "mac": mac})
    db.commit()

    return {
        "allow": True,
        "timeout": FREE_SESSION_SECONDS,
        "rate": FREE_RATE_LIMIT
    }
