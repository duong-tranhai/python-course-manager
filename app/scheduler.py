from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.routers.attendance import mark_absent_for_expired_sessions

def start_scheduler():
    scheduler = BackgroundScheduler()

    def job():
        print("🔄 Running daily attendance auto-mark task...")
        db = SessionLocal()
        mark_absent_for_expired_sessions(db=db, current_user=None)
        db.close()

    # Schedule to run once every 24 hours
    scheduler.add_job(job, 'interval', hours=24)

    scheduler.start()
