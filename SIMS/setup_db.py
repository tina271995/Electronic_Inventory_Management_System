from database import engine
from model import Base, Registration, Login, Product, SaleTransaction, InventoryRecord  # Ensure models are imported

# Drop all tables to handle schema changes
Base.metadata.drop_all(bind=engine)
# Recreate all tables with updated schema
Base.metadata.create_all(bind=engine)
print("✅ Database tables recreated successfully!")
