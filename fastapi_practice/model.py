# from sqlalchemy import Column, Integer, String, ForeignKey,Boolean
# from sqlalchemy.orm import relationship
# from database import Base

# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(50), unique=True, nullable=False)

#     posts = relationship("Post", back_populates="user")

# class Post(Base):
#     __tablename__ = 'posts'
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(50), nullable=False)
#     content = Column(String(100), nullable=False)
#     user_Id = Column(Integer, ForeignKey('users.id'))
#     user = relationship("User", back_populates="posts")


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
