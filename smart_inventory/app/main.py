from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")



# Set up Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

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

# Route for adding a product
@app.get("/add-product", response_class=HTMLResponse)
def add_product(request: Request):
    return templates.TemplateResponse("add_product.html", {"request": request})

# Route for viewing products
@app.get("/view-products", response_class=HTMLResponse)
def view_products(request: Request, search: str = ""):
    filtered_products = products
    
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

# Route for sales history
@app.get("/sales-history", response_class=HTMLResponse)
def sales_history(request: Request):
    return templates.TemplateResponse("sales_history.html", {"request": request})

# Route for sale bill
@app.get("/sale-bill", response_class=HTMLResponse)
def sale_bill(request: Request):
    return templates.TemplateResponse("sale_bill.html", {"request": request})