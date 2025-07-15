import datetime
from typing import Union
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI,Request,Depends, HTTPException
from sqlalchemy import *
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import SQLAlchemyError
from database import engine, Base, SessionLocal
from fastapi import FastAPI,Request, Form,Depends
from sqlalchemy.orm import Session
from database import *
import bcrypt
from model import InventoryRecord, Registration, Login,Product
import datetime
from pydantic import BaseModel
import setup_db

##Calling the FastAPI creating an insance app
app = FastAPI()

#For knwoing the static Directory for getting all the static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

#For knowing the Templates Directory for getting all the Templates Files
templates = Jinja2Templates(directory="templates")

#For Creating Session opeing and Closing the Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#For Checking the Database is connected or not
#{
def check_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "Database connected ✅"}
    except SQLAlchemyError as e:
        print("Error:", str(e))  # Prints to console
        raise HTTPException(status_code=500, detail=f"DB connection failed: {str(e)}")
    
@app.get("/healthcheck")
def healthcheck():
    return check_db_connection()
#}

#Setting the Defult Root
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return  templates.TemplateResponse(request=request, name="login.html")

#Setting the route for Registation Page
@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

#Setting the route for Login Page
@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

#For Registation of the table
@app.post("/registerName", response_class=HTMLResponse)
async def register(
    request: Request, 
    db: Session = Depends(get_db),
    email: str = Form(...), 
    username: str = Form(...), 
    password: str = Form(...), 
    confirm_password: str = Form(...), 
    role: str = Form(...)
):
    existing_user = db.query(Registration).filter(Registration.Email == email).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {"request": request, "error": "⚠️ Email already registered."})

    if confirm_password != password:
        return templates.TemplateResponse("register.html", {"request": request, "error": "⚠️ Passwords do not match."})

    # ✅ Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    registration = Registration(
        Email=email,
        Password=hashed_password.decode('utf-8'),  # store as string
        Role=bool(int(role)) 
    )
    db.add(registration)
    db.commit()
    db.refresh(registration)

    return templates.TemplateResponse(request=request, name="login.html")


@app.post("/loginuser", response_class=HTMLResponse)
async def login_form(
    request: Request, 
    db: Session = Depends(get_db),
    email: str = Form(...), 
    password: str = Form(...)
):
    
    user = db.query(Registration).filter(Registration.Email == email).first()
    print(user.Role)
    products = db.query(Product).all()
    # ✅ Verify password using bcrypt
    if user and bcrypt.checkpw(password.encode('utf-8'), user.Password.encode('utf-8')):
        login = Login(
            RegistrationID=user.id,
            LoginTimeStamp=datetime.datetime.now(),
            LoginStatus=True 
        )
        db.add(login)
        db.commit()
        # if staff logs in -> staff dashboard & if admin logs in -> admin dashboard
        if user.Role:
            return templates.TemplateResponse("diksha_dashboard.html", {"request": request, "username": user.Email,"products": products})
        else:
            return templates.TemplateResponse("dashboard.html", {"request": request, "username": user.Email,"products": products})
    
    return templates.TemplateResponse("login.html", {"request": request, "error": "❌ Invalid credentials"})

# Product  endpoints
class ProductCreate(BaseModel):
    name: str
    description: str = ""
    price: float
    quantity: int

class ProductUpdate(BaseModel):
    name: str = None
    description: str = None
    price: float = None
    quantity: int = None



# Add product(Staff)
@app.post("/products", response_class=HTMLResponse)
async def add_product(
    request: Request,
    user_id: int = Form(...),
    ProductName: str = Form(...),
    productDesc: str = Form(...),
    quantity: int = Form(...),
    price: int = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(Registration).filter(Registration.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    products = db.query(Product).all()
    new_product = Product(
        product_name=ProductName,
        description=productDesc,
        price=price,
        quantity=quantity
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    last_ele = db.query(Product).order_by(Product.id.desc()).first()
    Inventory_Record = InventoryRecord(
        product_id = last_ele.id,
        quantity_sold=None,
        restock=None,
        timestamp_sold=None,
        timestamp_restock=None
    )

    db.add(Inventory_Record)
    db.commit()
    db.refresh(Inventory_Record)
    products = db.query(Product).all()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "products": products
    })


