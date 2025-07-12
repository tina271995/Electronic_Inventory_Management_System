from typing import Union
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI,Request,Depends, HTTPException
from sqlalchemy import *
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import SQLAlchemyError
from database import engine, Base, SessionLocal
from fastapi import FastAPI,Request, Form

from database import *
app = FastAPI()
Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return  templates.TemplateResponse(request=request, name="login.html")

# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}

# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse(
#         request=request, name="item.html", context={"id": id}
#     )
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


@app.get("/db-check")
def db_check():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "✅ Connected to MySQL database"}
    except OperationalError as e:
        raise HTTPException(status_code=500, detail=f"❌ Connection failed: {str(e)}")
    
@app.get("/Connection")
def root():
    return {"message": "Hello from FastAPI + SQLAlchemy + MySQL"}

Base.metadata.create_all(bind=engine)
print("✅ Tables created with FastAPI app startup")




@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    print("Rakeshhhhhhhhhhhhhhhhhh")
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/registerName", response_class=HTMLResponse)
async def register(
    request: Request, 
    email: str=Form(...), 
    username: str = Form(...), 
    password : str =Form(...), 
    confirm_password : str =Form(...), 
    role: str =Form(...)
):
    print("Rakeshhssshshshsshshhs")
    
    print(f"Email: {email}, Username: {username}, Password: {password}, Role: {role}")
    
    return templates.TemplateResponse(request= request, name="login.html")


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    print("aakssssssssssssssssssssssssshhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/loginuser", response_class=HTMLResponse)
async def login_form(
    request: Request, 
    email: str=Form(...), 
    password: str =Form(...)
):
    print("Asksksksssssssssssssssssssssssss")
    
    print(f"Email: {email}, Password: {password}")
    
    return templates.TemplateResponse(request= request, name="login.html")