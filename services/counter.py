from sqlalchemy.orm import Session
from datetime import datetime
from models import GlobalQueryCount

def get_global_query_count(db: Session):
    today = datetime.now().date()
    query_count = db.query(GlobalQueryCount).filter_by(date=today).first()
    if not query_count:
        query_count = GlobalQueryCount(date=today, count=0)
        db.add(query_count)
        db.commit()
    return query_count

def increment_global_query_count(db: Session):
    query_count = get_global_query_count(db)
    query_count.count += 1
    db.commit()

def check_global_limit(db: Session):
    query_count = get_global_query_count(db)
    return query_count.count < 50
