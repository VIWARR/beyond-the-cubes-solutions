import time
import logging
from app.db.session import get_db_session
from app.services.orchestrator import Orchestrator
from app.utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def main():
    logger.info("Воркер запущен")
    while True:
        try:
            with get_db_session() as session:
                orchestrator = Orchestrator(session)
                orchestrator.process_pending_tasks()
                session.commit()
        except Exception as e:
            logger.error(f"Ошибка в цикле: {e}")

        time.sleep(10)

if __name__ == "__main__":
    main()