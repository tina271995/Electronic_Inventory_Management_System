from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base
class Registration(Base):
    __tablename__ = "registration"  # fixed typo: resgistration → registration
    id = Column(Integer, primary_key=True, index=True)
    Email = Column(String(200), nullable=False)
    Password = Column(String(200), nullable=False)
    Role = Column(Boolean, nullable=False)
    logins = relationship("Login", back_populates="registration")

    def to_dict(self):
        return {
            "id":{self.id},
            "Email":{self.Email},
            "Password":{self.Password},
            "Role":{self.Role}
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
    TimeStamp = Column(DateTime, nullable=False, default=func.now())
    price = Column(Integer)
    quantity = Column(Integer)
    inventory_record  = relationship("InventoryRecord", back_populates="product")
    sale_transaction = relationship("SaleTransaction", back_populates="product")
    inventory_record = relationship(
    "InventoryRecord", back_populates="product", cascade="all, delete"
    )
    sale_transaction = relationship(
        "SaleTransaction", back_populates="product", cascade="all, delete"
    )
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
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    quantity_sold = Column(Integer,nullable=True)
    restock = Column(Boolean,nullable=True)
    timestamp_sold = Column(DateTime,nullable=True,default=func.now())
    timestamp_restock = Column(DateTime,nullable=True,default=func.now())
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
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)

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