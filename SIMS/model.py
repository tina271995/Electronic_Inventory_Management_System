from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base
  
class Registration(Base):
    __tablename__ = "registration"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(200), nullable=False, unique=True)
    email = Column(String(200), nullable=False)
    password = Column(String(200), nullable=False)
    role = Column(Boolean, nullable=False, default=False)
    logins = relationship("Login", back_populates="registration")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role
        }
      
class Login(Base):
    __tablename__ = "login"
    id = Column(Integer, primary_key=True, index=True)
    RegistrationID = Column(Integer, ForeignKey("registration.id"), nullable=False)
    LoginTimeStamp = Column(DateTime, nullable=False, default=func.now())
    LoginStatus = Column(Boolean, nullable=False)
    registration = relationship("Registration", back_populates="logins")

    def to_dict(self):
        return {
            "id":{self.id},
            "RegistrationID":{self.RegistrationID},
            "LoginTimeStamp":{self.LoginTimeStamp},
            "LoginStatus":{self.LoginStatus}
        }

class Product(Base):
    __tablename__= 'product'
    id = Column(Integer,primary_key=True,index=True)
    product_name = Column(String(200),nullable=False)
    description = Column(String(200),nullable=False)
    price = Column(Integer)
    quantity = Column(Integer)
    created_at = Column(DateTime, nullable=False, default=func.now())
    inventory_record  = relationship("InventoryRecord", back_populates="product")
    sale_transaction = relationship("SaleTransaction", back_populates="product")

    def to_dict(self):
        return{
            "id":{self.id},
            "product_name":{self.product_name},
            "description":{self.description},
            "price":{self.price},
            "quantity":{self.quantity}
        }

class InventoryRecord(Base):
    __tablename__ = 'inventory_record'
    id = Column(Integer,primary_key=True,index=True)
    product_id = Column(Integer,ForeignKey("product.id"),nullable=False)
    quantity_sold = Column(Integer,nullable=False)
    restock = Column(Boolean,nullable=False)
    timestamp_sold = Column(DateTime,nullable=False,default=func.now())
    timestamp_restock = Column(DateTime,nullable=False,default=func.now())
    product = relationship("Product", back_populates="inventory_record")
    
    def to_dict(self):
        return{
            "id":{self.id},
            "product_id":{self.product_id},
            "quantity_sold":{self.quantity_sold},
            "restock":{self.restock},
            "timestamp_sold":{self.timestamp_sold},
            "timestamp_restock":{self.timestamp_restock}
        }

class SaleTransaction(Base):
    __tablename__ = 'sale_transaction'
    id = Column(Integer,primary_key=True,index=True)
    product_id = Column(Integer,ForeignKey("product.id"),nullable=False)
    product_amt = Column(Integer,nullable=False)
    quantity_sold = Column(Integer,nullable=False)
    timestamp_sold = Column(DateTime,nullable=False,default=func.now())
    user = Column(String(200),nullable=False)
    product = relationship("Product", back_populates="sale_transaction")

    def to_dict(self):
        return{
            "id":{self.id},
            "product_id":{self.product_id},
            "product_amt":{self.product_amt},
            "quantity_sold":{self.quantity_sold},
            "timestamp_sold":{self.timestamp_sold},
            "user":{self.user},
        }