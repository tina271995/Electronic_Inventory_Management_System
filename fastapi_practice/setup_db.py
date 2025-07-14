from database import engine
from model import Base, Registration, Login  # Ensure models are imported

Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
