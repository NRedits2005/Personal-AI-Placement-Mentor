import logging
from backend.database import engine, Base
from backend.models import *

logger = logging.getLogger(__name__)

def init_db():
    """Initializes the database tables if they do not exist."""
    logger.info("Initializing database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_db()
