from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import datetime
from sqlalchemy import text, func
from sqlalchemy.exc import SQLAlchemyError
from database import engine, Base, SessionLocal
from sqlalchemy.orm import Session
import bcrypt
from model import Registration, Login, Product, SaleTransaction, InventoryRecord
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import RedirectResponse
   
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="templates")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#For Checking the Database is connected or not
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


#Setting the Default Root
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

# User registration endpoint
@app.post("/registerName")
async def register_user(request: Request, db: Session = Depends(get_db), username: str = Form(...), email: str = Form(...), password: str = Form(...), confirm_password: str = Form(...), redirect_to_home: bool = Form(False)):
    try:
        # Check if user already exists
        existing_user = db.query(Registration).filter(Registration.Email == email).first()
        if existing_user:
            return templates.TemplateResponse("register.html", {"request": request, "error": "⚠️ Email already registered."})

        if confirm_password != password:
            return templates.TemplateResponse("register.html", {"request": request, "error": "⚠️ Passwords do not match."})
        existing_user = db.query(Registration).filter(Registration.username == username).first()
        if existing_user:
            return JSONResponse(status_code=400, content={"success": False, "message": "Username already exists"})
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # Create new user
        new_user = Registration(username=username, email=email, password=hashed_password.decode('utf-8'))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        # return templates.TemplateResponse(request=request, name="login.html")
        if redirect_to_home:
            # ✅ Redirect to /home
            return RedirectResponse(url="/loginuser", status_code=303)
        else:
            # 🧾 Render login.html
            return templates.TemplateResponse(
                "login.html",
                {
                    "request": request,
                    "email": email,
                    "username": username,
                    "password": password,
                    "confirm_password": password,
                }
            )
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        return JSONResponse(status_code=500, content={"success": False, "message": "Database error occurred during registration"})
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return JSONResponse(status_code=500, content={"success": False, "message": "An unexpected error occurred during registration"})

# User login endpoint
@app.post("/loginuser")
async def login_user(request: Request, db: Session = Depends(get_db), email: str = Form(...), password: str = Form(...)):
    user = db.query(Registration).filter(Registration.email == email).first()
    products = db.query(Product).all()
    # ✅ Verify password using bcrypt
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        login = Login(
            RegistrationID=user.id,
            LoginTimeStamp=datetime.datetime.now(),
            LoginStatus=True 
        )
        db.add(login)
        db.commit()
        # db.refresh()
        
    # Get all products
    products = db.query(Product).all()
    total_products = len(products)

    # Get recent product additions
    recent_additions = db.query(Product).order_by(Product.created_at.desc()).limit(5).all()
    recent_activities = []
    for product in recent_additions:
        recent_activities.append({
            "description": f"Added new product: {product.product_name} (Qty: {product.quantity})",
            "timestamp": product.created_at,
            "type": "add"
        })

    # Get recent sales
    recent_sales = db.query(SaleTransaction).order_by(SaleTransaction.timestamp_sold.desc()).limit(5).all()
    for sale in recent_sales:
        product = db.query(Product).filter(Product.id == sale.product_id).first()
        if product:
            recent_activities.append({
                "description": f"Sold {sale.quantity_sold} units of {product.product_name}",
                "timestamp": sale.timestamp_sold,
                "type": "sale"
            })

    # Get recent restocks
    recent_restocks = db.query(InventoryRecord)\
        .filter(InventoryRecord.restock == True)\
        .order_by(InventoryRecord.timestamp_restock.desc())\
        .limit(5).all()
    for restock in recent_restocks:
        product = db.query(Product).filter(Product.id == restock.product_id).first()
        if product:
            recent_activities.append({
                "description": f"Restocked {restock.quantity_sold} units of {product.product_name}",
                "timestamp": restock.timestamp_restock,
                "type": "restock"
            })

    # Sort activities by timestamp
    recent_activities.sort(key=lambda x: x["timestamp"], reverse=True)
    recent_activities = recent_activities[:5]

    # Example stats (replace with real queries as needed)
    todays_sales = db.query(SaleTransaction).filter(func.date(SaleTransaction.timestamp_sold) == datetime.date.today()).count()
    low_stock_count = db.query(Product).filter(Product.quantity < 5).count()
    
    return templates.TemplateResponse("dashboard.html", {"request": request, "username": user.email,"products": products,"total_products": total_products,"todays_sales": todays_sales,"low_stock_count": low_stock_count,"recent_activities": recent_activities})

#  Dashboard route
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    # Get all products
    
    products = db.query(Product).all()
    total_products = len(products)

    # Get recent product additions
    recent_additions = db.query(Product).order_by(Product.created_at.desc()).limit(5).all()
    recent_activities = []
    for product in recent_additions:
        recent_activities.append({
            "description": f"Added new product: {product.product_name} (Qty: {product.quantity})",
            "timestamp": product.created_at,
            "type": "add"
        })

    # Get recent sales
    recent_sales = db.query(SaleTransaction).order_by(SaleTransaction.timestamp_sold.desc()).limit(5).all()
    for sale in recent_sales:
        product = db.query(Product).filter(Product.id == sale.product_id).first()
        if product:
            recent_activities.append({
                "description": f"Sold {sale.quantity_sold} units of {product.product_name}",
                "timestamp": sale.timestamp_sold,
                "type": "sale"
            })

    # Get recent restocks
    recent_restocks = db.query(InventoryRecord)\
        .filter(InventoryRecord.restock == True)\
        .order_by(InventoryRecord.timestamp_restock.desc())\
        .limit(5).all()
    for restock in recent_restocks:
        product = db.query(Product).filter(Product.id == restock.product_id).first()
        if product:
            recent_activities.append({
                "description": f"Restocked {restock.quantity_sold} units of {product.product_name}",
                "timestamp": restock.timestamp_restock,
                "type": "restock"
            })

    # Sort activities by timestamp
    recent_activities.sort(key=lambda x: x["timestamp"], reverse=True)
    recent_activities = recent_activities[:5]

    # Example stats (replace with real queries as needed)
    todays_sales = db.query(SaleTransaction).filter(func.date(SaleTransaction.timestamp_sold) == datetime.date.today()).count()
    low_stock_count = db.query(Product).filter(Product.quantity < 5).count()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "products": products,
            "total_products": total_products,
            "todays_sales": todays_sales,
            "low_stock_count": low_stock_count,
            "recent_activities": recent_activities
        }
    )


# Product models for API validation
class ProductCreate(BaseModel):
    product_name: str
    description: str = ""
    price: float
    quantity: int

class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

# Add product endpoint (Staff)
@app.post("/products")
async def add_product(
    request: Request,
    db: Session = Depends(get_db),
    product_name: str = Form(...),
    description: str = Form(...),
    quantity: int = Form(...),
    price: float = Form(...)
):
    try:
        # Validate inputs
        if not product_name.strip() or not description.strip():
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Product name and description are required"}
            )
            
        if quantity < 0:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Quantity cannot be negative"}
            )
            
        if price < 0:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Price cannot be negative"}
            )
            
        # Create new product
        new_product = Product(
            product_name=product_name.strip(),
            description=description.strip(),
            price=price,
            quantity=quantity
        )
        
        # Add to database
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return JSONResponse(content={"success": True, "message": f"Product '{product_name}' added successfully!", "product": {"id": new_product.id, "name": new_product.product_name, "description": new_product.description, "price": new_product.price, "quantity": new_product.quantity}})
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Database error occurred while adding product"}
        )
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "An unexpected error occurred"}
        )
    
# List products
@app.get("/get_products", response_class=HTMLResponse)
async def list_products(request: Request, view_type: str = "table", db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return templates.TemplateResponse(
        "dashboard.html", 
        {
            "request": request, 
            "products": products,
            "view_type": view_type,
            "total_products": len(products)
        }
    )

# Delete product
@app.post("/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    del_query = db.query(Product).filter(Product.id == product_id).first()
    if not del_query:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(del_query)
    db.commit()
    return {"msg": "Product deleted"}

@app.get("/sales_history", response_class=HTMLResponse)
async def sales_history(request: Request, db: Session = Depends(get_db)):
    sales = db.query(SaleTransaction).order_by(SaleTransaction.timestamp_sold.desc()).all()
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "sales_history": sales
        }
    )

@app.get("/restock_history", response_class=HTMLResponse)
async def restock_history(request: Request, db: Session = Depends(get_db)):
    restocks = db.query(InventoryRecord).filter(InventoryRecord.restock == True).order_by(InventoryRecord.timestamp_restock.desc()).all()
    return templates.TemplateResponse(
        "templates/dashboard.html",
        {
            "request": request,
            "restock_history": restocks
        }
    )

@app.get("/sell_products", response_class=HTMLResponse)
async def sell_products(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.quantity > 0).all()
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "sellable_products": products
        }
    )
