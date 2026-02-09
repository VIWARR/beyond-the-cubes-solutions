import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tenacity import retry, stop_after_attempt, wait_fixed, before_sleep_log
from config import settings

logger = logging.getLogger(__name__)

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@retry(
    stop=stop_after_attempt(10),
    wait=wait_fixed(2),
    before_sleep=before_sleep_log(logger, logging.WARNING)
)
def get_db_session():
    with engine.connect() as conn:
        return SessionLocal()