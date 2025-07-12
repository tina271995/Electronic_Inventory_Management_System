from database import engine
from model import Base, User, Post  # Ensure models are imported

Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
