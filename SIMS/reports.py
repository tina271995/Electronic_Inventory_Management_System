import csv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from model import SaleTransaction

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
  
@router.get("/download_sales_report")
def download_sales_report(db: Session = Depends(get_db)):
    try:
        # Fetch data from SaleTransaction table
        sales = db.query(SaleTransaction).all()

        # Define CSV file path
        file_path = "sales_report.csv"

        # Write data to CSV file
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Sale ID", "Product ID", "Product Amount", "Quantity Sold", "Timestamp Sold", "User"])
            for sale in sales:
                writer.writerow([
                    sale.id,
                    sale.product_id,
                    sale.product_amt,
                    sale.quantity_sold,
                    sale.timestamp_sold,
                    sale.user
                ])

        return FileResponse(file_path, media_type="text/csv", filename="sales_report.csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating sales report: {str(e)}")
