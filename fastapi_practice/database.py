from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base



DATABASE_URL = "mysql+pymysql://root:redhat@localhost/fastapi_db"
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=30)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
