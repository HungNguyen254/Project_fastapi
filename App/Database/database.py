from sqlalchemy.orm import Session,sessionmaker,declarative_base
from sqlalchemy import create_engine
DATABASE_URL = 'mysql+pymysql://root:25042006@localhost:3306/Project_fastapi'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()