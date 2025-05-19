from sqlalchemy.orm import Session

from app.models.system_log import SystemLog


def log_action(db: Session, user_id: int = None, action: str = '', detail: str = ''):
    log_entry = SystemLog(
        user_id=user_id,
        action=action,
        detail=detail
    )
    db.add(log_entry)
    db.commit()
