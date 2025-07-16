from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
import csv
import io
app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")


# Set up Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

# Sample sales data
sales_data = [
    {"sale_id": 501, "sale_date": "2025-07-13", "name": "iPhone 15", "description": "Latest Apple model", "quantity": 2, "total_cost": 179998},
]

# Sample product data
products = [
    {"id": 101, "date": "2025-07-13", "name": "iPhone 15", "desc": "Latest Apple model", "quantity": 10, "price": 89999},
    {"id": 102, "date": "2025-07-14", "name": "Samsung Galaxy S23", "desc": "Latest Samsung model", "quantity": 5, "price": 74999},
    {"id": 103, "date": "2025-07-15", "name": "Google Pixel 7", "desc": "Latest Google model", "quantity": 8, "price": 59999},
    {"id": 104, "date": "2025-07-16", "name": "OnePlus 11", "desc": "Flagship killer", "quantity": 7, "price": 54999},
    {"id": 105, "date": "2025-07-17", "name": "Xiaomi 13 Pro", "desc": "Chinese flagship", "quantity": 12, "price": 49999},
]

# Route for the dashboard
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Logout route
@app.post("/logout")
def logout(request: Request):
    # Here you would clear the user's session or token
    # For example, if using sessions:
    # request.session.clear()  # Clear the session
    return RedirectResponse(url="/", status_code=303)

# Route for adding a product
@app.get("/add-product", response_class=HTMLResponse)
def add_product(request: Request):
    return templates.TemplateResponse("add_product.html", {"request": request})

# Route for viewing products
@app.get("/view-products", response_class=HTMLResponse)
def view_products(request: Request, search: str = ""):
    filtered_products = products
    
    # searching products
    if search:
        filtered_products = [
            product for product in products 
            if search.lower() in product["name"].lower() or 
               search in str(product["id"])
        ]
    
    return templates.TemplateResponse(
        "view_products.html", 
        {
            "request": request, 
            "products": filtered_products, 
            "search": search,
            "products_count": len(filtered_products)
        }
    )


# Route for selling a product
@app.get("/sell-product", response_class=HTMLResponse)
def sell_product(request: Request):
    return templates.TemplateResponse("sale_product.html", {"request": request})


# Route for restocking a product
@app.get("/restock-product", response_class=HTMLResponse)
def restock_product(request: Request):
    return templates.TemplateResponse("restock_product.html", {"request": request})


# Route for sale bill
@app.get("/sale-bill", response_class=HTMLResponse)
def sale_bill(request: Request):
    return templates.TemplateResponse("sale_bill.html", {"request": request})


# Route for sales history

# @app.get("/sales-history", response_class=HTMLResponse)
# def sales_history(request: Request):
#     return templates.TemplateResponse("sales_history.html", {"request": request})

@app.get("/sales_history", response_class=HTMLResponse)
async def sales_history(request: Request):
    return templates.TemplateResponse("sales_history.html", {"request": request, "sales_data": sales_data})

@app.get("/export_sales", response_class=StreamingResponse)
async def export_sales():
    # Create a CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Sale ID", "Sale Date", "Name", "Description", "Quantity", "Total Cost"])  # Header

    for sale in sales_data:
        writer.writerow([sale["sale_id"], sale["sale_date"], sale["name"], sale["description"], sale["quantity"], sale["total_cost"]])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=sales_history.csv"})
