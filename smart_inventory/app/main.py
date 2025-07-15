from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")



# Set up Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

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
def view_products(request: Request):
    return templates.TemplateResponse("view_products.html", {"request": request})

# Route for selling a product
@app.get("/sell-product", response_class=HTMLResponse)
def sell_product(request: Request):
    return templates.TemplateResponse("sale_product.html", {"request": request})


# Route for restocking a product
@app.get("/restock-product", response_class=HTMLResponse)
def restock_product(request: Request):
    return templates.TemplateResponse("restock_product.html", {"request": request})

# @app.post("/restock-product", response_class=HTMLResponse)
# def restock_product(request: Request, product_id: str = Form(None), product_name: str = Form(None), product_desc: str = Form(None)):
#     product = None
#     if product_id:
#         product = {
#             "id": product_id,
#             "name": product_name,
#             "desc": product_desc
#         }
    # return templates.TemplateResponse("restock_product.html", {"request": request, "product": product})

# Route for generating restock
# @app.post("/generate-restock")
# def generate_restock(restockProductId: str = Form(...), restockQuantity: int = Form(...), restockPrice: float = Form(...)):
#     # Logic to handle the restock process
#     return {"message": f"Restocked Product ID: {restockProductId} with Quantity: {restockQuantity} and New Price: ₹{restockPrice}"}

# Route for sales history
@app.get("/sales-history", response_class=HTMLResponse)
def sales_history(request: Request):
    return templates.TemplateResponse("sales_history.html", {"request": request})

# Route for sale bill
@app.get("/sale-bill", response_class=HTMLResponse)
def sale_bill(request: Request):
    return templates.TemplateResponse("sale_bill.html", {"request": request})