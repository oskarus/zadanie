from fastapi import HTTPException
from fastapi.responses import JSONResponse
from db.utils import async_session
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from db.models import Laptop, PC, Printer, Product
from routers.models import LaptopDetails, PCDetails, PrinterDetails
from decimal import Decimal
import csv

async def calculate_profitability(product):
    if product.laptops:
        laptop = product.laptops[0]
        index = (laptop.ram + laptop.hd) / (laptop.price * laptop.speed)
        return {"model": product.model, "type": "Laptop", "index": index}

    elif product.personal_computers:
        pc = product.personal_computers[0]
        index = (pc.ram + pc.hd) / (pc.price * pc.speed)
        return {"model": product.model, "type": "Personal Computer", "index": index}

    return None

async def fetch_products(session):
    result = await session.execute(select(Product))
    return result.scalars().all()
    
class ProfitabilityService:
    @staticmethod
    async def get_products_profitability() -> JSONResponse:
        try:
            async with async_session() as session:
                products = await fetch_products(session)
                results = [await calculate_profitability(product) for product in products if product]
                return JSONResponse(status_code=200, content={"profitability": results})
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"error": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})

    @staticmethod
    async def export_profitability_csv() -> JSONResponse:
        try:
            async with async_session() as session:
                csv_file_path = "outputs/profitability.csv"

                with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Model', 'Type', 'Profitability Index'])

                    products = await fetch_products(session)
                    for product in products:
                        info = await calculate_profitability(product)
                        if info:
                            writer.writerow([info['model'], info['type'], info['index']])

                return JSONResponse(content={"filepath": csv_file_path})
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"error": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
