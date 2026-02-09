import logging
import sys
from sqlalchemy import text
from utils.logger import setup_logging
from db.session import get_db_session

setup_logging()
logger = logging.getLogger(__name__)

def check_connection():
    logger.info("Тест соединения")
    try:
        db = get_db_session()
        result = db.execute(text("select 1"))
        
        if result.fetchone():
            logger.info("Соединение установлено")

        db.close()

    except Exception as e:
        logger.error(f"Ошибка {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_connection()