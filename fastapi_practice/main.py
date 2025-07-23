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
from model import InventoryRecord, Registration, Login,Product, SaleTransaction
from pydantic import BaseModel
import setup_db
from fastapi import Body
from typing import Optional


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
# @app.get("/GetAllInformation")
@app.get("/Dashboards", response_class=HTMLResponse)
async def Dashboards(request: Request, db: Session = Depends(get_db)):
    # Retrieve total products
    total_products = db.query(func.count(Product.id)).scalar() or 0
    print(total_products)
    # Retrieve total quantity sold
    total_quantity = db.query(func.sum(SaleTransaction.quantity_sold)).scalar() or 0
    # Retrieve total stock
    total_stock = db.query(func.sum(Product.quantity)).scalar() or 0
    # Retrieve total sales
    total_sales = db.query(func.sum(SaleTransaction.product_amt * SaleTransaction.quantity_sold)).scalar() or 0
    top_stock_products = db.query(Product.product_name,Product.quantity).order_by(Product.quantity.desc()).limit(5).all()

    # Convert to JSON-serializable format
    top_stock_data = [{"product_name": p[0], "quantity": p[1]} for p in top_stock_products]
    
    daily_sales = db.query(func.date(SaleTransaction.timestamp_sold).label("sale_date"),
        func.sum(SaleTransaction.quantity_sold).label("daily_quantity")
        ).group_by(func.date(SaleTransaction.timestamp_sold)).order_by(func.date(SaleTransaction.timestamp_sold)).all()


    daily_quantity_labels = [sale.sale_date.strftime("%Y-%m-%d") for sale in daily_sales] 
    daily_quantity_values = [int(sale.daily_quantity) for sale in daily_sales]
    db.close()
    return templates.TemplateResponse("diksha_dashboard.html", 
            {"request": request,
            "total_products": total_products,
            "total_quantity": total_quantity,
            "total_stock": total_stock,
            "total_sales": total_sales if total_sales else "0",
            "top_stock_data": top_stock_data,
            "daily_quantity_labels": daily_quantity_labels,
            "daily_quantity_values": daily_quantity_values})

@app.get("/sales-history", response_class=HTMLResponse)
async def sales_history(request: Request,db: Session = Depends(get_db)):
    products = db.query(SaleTransaction).all()
    return templates.TemplateResponse("diksha_sales_history.html", {"request": request,"products":products})

@app.get("/sales-reports", response_class=HTMLResponse)
async def get_sales_reports(request: Request, db: Session = Depends(get_db)):
    try:
        total_sales = db.query(func.sum(SaleTransaction.product_amt * SaleTransaction.quantity_sold)).scalar() or 0
        total_orders = db.query(func.count(SaleTransaction.id)).scalar() or 0
        
        top_product_result = db.query(Product.product_name)\
            .join(SaleTransaction, SaleTransaction.product_id == Product.id)\
            .group_by(Product.product_name)\
            .order_by(func.sum(SaleTransaction.quantity_sold).desc())\
            .first()
        
        top_product_name = top_product_result.product_name if top_product_result else "N/A"
        
        # Get top selling products for the bar chart (list of objects)
        top_products_for_chart = db.query(
            Product.product_name,
            func.sum(SaleTransaction.quantity_sold).label("total_quantity"))\
            .join(SaleTransaction, SaleTransaction.product_id == Product.id)\
            .group_by(Product.product_name)\
            .order_by(func.sum(SaleTransaction.quantity_sold).desc())\
            .limit(5).all()
        
        # Convert top_products_for_chart to a list of dictionaries for JSON serialization
        top_products_data = [
            {"product_name": p[0], "total_quantity": float(p[1])}  # Convert Decimal to float
            for p in top_products_for_chart
        ]

        # Last 3
        last_3 = db.query(Product.id,Product.product_name.label('name'), Product.quantity.label('quantity'),
            Product.price,Product.TimeStamp.label('timestamp')).order_by(Product.id.desc()).limit(3).all()        
        
        # Line chart
        daily_sales = db.query(
        func.date(SaleTransaction.timestamp_sold).label("sale_date"),
        func.sum(SaleTransaction.quantity_sold).label("daily_quantity")
        ).group_by(func.date(SaleTransaction.timestamp_sold)).order_by(func.date(SaleTransaction.timestamp_sold)).all()

        daily_quantity_labels = [sale.sale_date.strftime("%Y-%m-%d") for sale in daily_sales]  # Day name
        daily_quantity_values = [int(sale.daily_quantity) for sale in daily_sales]
        # daily_quantity = db.query(
        #     func.strftime('%Y-%m-%d', SaleTransaction.timestamp_sold).label("date"),
        #     func.sum(SaleTransaction.quantity_sold).label("daily_quantity")
        # ).group_by(func.strftime('%Y-%m-%d', SaleTransaction.timestamp_sold)).all()
        # daily_quantity_labels1 = [sale.sale_date.strftime("%Y-%m-%d") for sale in daily_quantity]

    
        return templates.TemplateResponse("diksha_sales_reports.html",
            {"request": request,
             "total_sales": float(total_sales),  # Convert to float
             "total_orders": total_orders,
             "top_product_name": top_product_name,
             "top_products": top_products_data,
             "daily_revenue": daily_quantity_values,
             "daily_quantity_labels": daily_quantity_labels,
             "daily_quantity_values": daily_quantity_values,
             "last3": last_3
            })
    except Exception as e:
        print(f"Error in get_sales_reports: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while generating sales reports.")

@app.get("/InventoryRecords", response_class=HTMLResponse)
async def inventory_reports(request: Request,db: Session = Depends(get_db)):
    products = db.query(InventoryRecord).all()
    return templates.TemplateResponse("diksha_inventory_reports.html", {"request": request,"products": products})

@app.get("/ProductRecords", response_class=HTMLResponse)
async def Product_reports(request: Request,db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return templates.TemplateResponse("diksha_Product_reports.html", {"request": request,"products": products})

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
        return templates.TemplateResponse("dashboard.html", {"request": request, "error": "⚠️ Email already registered."})

    if confirm_password != password:
        return templates.TemplateResponse("dashboard.html", {"request": request, "error": "⚠️ Passwords do not match."})


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
    password: str = Form(...),
    
):
    
    user = db.query(Registration).filter(Registration.Email == email).first()
    LowQuantity = db.query(Product).filter(Product.quantity < 11).all()
    inventory_history = db.query(InventoryRecord).all()
    Low = len(LowQuantity)
    products = db.query(Product).all()
    SaleTransactions = db.query(SaleTransaction).all()
    TotalProducs = len(products)
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
            return templates.TemplateResponse("dashboard.html", {"request": request, "username": user.Email,"products": products,"TotalProducts":TotalProducs,"LowInQuantity":Low,"SaleTransactions":SaleTransactions,"inventory_history": inventory_history})
    
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
    product = db.query(Product).filter(Product.id == last_ele.id).first()
    LowQuantity = db.query(Product).filter(Product.quantity < 11).all()
    inventory_history = db.query(InventoryRecord).all()
    Low = len(LowQuantity)
    products = db.query(Product).all()
    SaleTransactions = db.query(SaleTransaction).all()
    TotalProducs = len(products)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "products": products,
        "username": user.Email,
        "TotalProducts":TotalProducs,
        "LowInQuantity":Low,
        "SaleTransactions":SaleTransactions,
        "inventory_history": inventory_history
    })
# Add product(Staff)

# @app.post("/products/{product_id}")
# async def add_product(
#     request: Request,
#     product_id: int,
#     user_id: int = Form(...),
#     ProductName: str = Form(...),
#     productDesc: str = Form(...),
#     quantity: int = Form(...),
#     price: int = Form(...),
#     db: Session = Depends(get_db)
# ):
#     print("Incoming Data:")
#     print(f"product_id: {product_id}")
#     print(f"user_id: {user_id}")
#     print(f"ProductName: {ProductName}")
#     print(f"productDesc: {productDesc}")
#     print(f"quantity: {quantity}")
#     print(f"price: {price}")

#     # ✅ You can now safely update the product here
#     # product = db.query(Product).filter(Product.id == product_id).first()
#     # if product:
#     #     product.product_name = ProductName
#     #     product.description = productDesc
#     #     product.quantity = quantity
#     #     product.price = price
#     #     db.commit()

#     products = db.query(Product).all()
#     return templates.TemplateResponse("dashboard.html", {"request": request, "products": products})

@app.post("/update_products/{product_id}")
async def update_product(
    request: Request,
    product_id: int,
    quantity: int = Form(...),
    price: int = Form(...),
    name: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "error": "Product not found."
        })

    # Update only the fields that were edited
    product.quantity = quantity  # Add to existing quantity
    product.price = price         # Overwrite price
    product.product_name = name
    product.description = description
    print(product.price,product.quantity,product.product_name,product.description,'proddddddddddddddddddddddddddddddddddddddddd')
    db.commit()

    # Optionally reload product list
    products = db.query(Product).all()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "products": products,
        "message": "Product updated successfully!"
    })



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



class InvoiceData(BaseModel):
    product_id: int
    user: str
    quantity_sold: int
    product_amt: int

@app.post("/save_invoice/")
async def save_invoice(data: InvoiceData = Body(...), db: Session = Depends(get_db)):
    sale = SaleTransaction(
        product_id=data.product_id,
        user=data.user,
        quantity_sold=data.quantity_sold,
        product_amt=data.product_amt,
        # timestamp_sold=datetime.now()
    )
   
    db.add(sale)
    db.flush()  # Ensures the insert happens before querying product
    Inventory_Record = InventoryRecord(
        product_id = data.product_id,
        quantity_sold=data.quantity_sold,
        restock=0
    )

    db.add(Inventory_Record)
    db.commit()
    db.refresh(Inventory_Record)

    # Optional: update product quantity
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if product:
        product.quantity -= data.quantity_sold
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.quantity < data.quantity_sold:
        raise HTTPException(status_code=400, detail="Not enough stock")


    db.commit()
    return {"message": "Invoice saved successfully"}


@app.get("/restock_products", response_class=HTMLResponse)
async def restock_products(request: Request, db: Session = Depends(get_db)):
    
    restock = db.query(Product).filter(Product.quantity < Product.restock_threshold).all()  
    
    restock_product = InventoryRecord(
        product_id = restock.id,
        restock = True,
        quantity_sold = restock.quantity
    )
    db.add(restock_product)
    db.commit()
    # db.refresh(restock_product)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "restockable_products": restock
        }
    )

class RestockData(BaseModel):
    product_id: int
    quantity:int
@app.post("/save_restock/")
async def save_restock(data: RestockData, db: Session = Depends(get_db)):
    restock_entry = InventoryRecord(
        product_id=data.product_id,
        quantity_sold = data.quantity,
        restock=True
    )
    db.add(restock_entry)
    db.commit()
    db.refresh(restock_entry)
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if product:
        product.quantity += data.quantity
    # if not product:
    #     raise HTTPException(status_code=404, detail="Product not found")
    # if product.quantity < data.quantity_sold:
    #     raise HTTPException(status_code=400, detail="Not enough stock")


    db.commit()
    return {"message": "Restock successful", "id": restock_entry.id}

@app.get("/sale_history", response_class=HTMLResponse)
async def sale_history(request: Request, db: Session = Depends(get_db)):
    
    sale_history = db.query(SaleTransaction).all()
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "sale_history": sale_history
        }
    )
    
@app.get("/get_sales_history/")
async def get_sales_history(request: Request, db: Session = Depends(get_db)):
    try:
        # Get all sales with related product information
        sales = db.query(SaleTransaction)\
            .join(Product)\
            .options(joinedload(SaleTransaction.product))\
            .all()
            
        # Convert to JSON serializable format
        sales_data = []
        for sale in sales:
            sales_data.append({
                "id": sale.id,
                "timestamp_sold": sale.timestamp_sold.strftime("%Y-%m-%d"),
                "quantity_sold": sale.quantity_sold,
                "product_amt": sale.product_amt,
                "product": {
                    "product_name": sale.product.product_name,
                    "description": sale.product.description
                }
            })
        return sales_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/inventory_history", response_class=HTMLResponse)
async def inventory_history(request: Request, db: Session = Depends(get_db)):
    
    inventory_history = db.query(InventoryRecord).all()
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "inventory_history": inventory_history
        }
    )

@app.post("/delete-product/{product_id}", response_class=HTMLResponse)
async def delete_product(request: Request,product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    inventory_history = db.query(InventoryRecord).all()
    products = db.query(Product).all()
    SaleTransactions = db.query(SaleTransaction).all()
    TotalProducs = len(products)
    if Product:
        db.delete(product)
        db.commit()
    products = db.query(Product).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "products": products,"request": request,"TotalProducts":TotalProducs,"SaleTransactions":SaleTransactions,"inventory_history": inventory_history})
