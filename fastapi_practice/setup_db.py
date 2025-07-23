from database import engine
from model import Base


Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
