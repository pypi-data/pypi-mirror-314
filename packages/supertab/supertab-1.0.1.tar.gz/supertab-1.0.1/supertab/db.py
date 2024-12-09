from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def init_engine(database_url, pool_size):
    return create_engine(
        database_url,
        echo=False,
        pool_recycle=360,
        pool_size=pool_size,
        max_overflow=10,
        pool_timeout=30,
        pool_pre_ping=True,
    )

def get_session(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
