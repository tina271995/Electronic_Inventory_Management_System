from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/add_product", response_class=HTMLResponse)
def add_product(request: Request):
    return templates.TemplateResponse("add_product.html", {"request": request})

@app.get("/view-products", response_class=HTMLResponse)
def view_products(request: Request):
    return templates.TemplateResponse("view_products.html", {"request": request})

@app.get("/sell-product", response_class=HTMLResponse)
def sell_product(request: Request):
    return templates.TemplateResponse("sale_product.html", {"request": request})

@app.get("/restock-product", response_class=HTMLResponse)
def restock_product(request: Request):
    return templates.TemplateResponse("restock_product.html", {"request": request})

@app.get("/sales-history", response_class=HTMLResponse)
def sales_history(request: Request):
    return templates.TemplateResponse("sales_history.html", {"request": request})

@app.get("/sale-bill", response_class=HTMLResponse)
def sale_bill(request: Request):
    return templates.TemplateResponse("sale_bill.html", {"request": request})
