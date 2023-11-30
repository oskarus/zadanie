from fastapi import HTTPException
from fastapi.responses import JSONResponse
from db.utils import async_session
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from db.models import Laptop, PC, Printer, Product
from routers.models import LaptopDetails, PCDetails, PrinterDetails
from decimal import Decimal
import csv
import os

class ProfitabilityService:
    @staticmethod
    async def fetch_and_calculate_profitability(session) -> list:
        results = []
        # Fetch and calculate profitability for Laptops and PCs
        laptops = await session.execute(select(Laptop).options(joinedload(Laptop.product)))
        pcs = await session.execute(select(PC).options(joinedload(PC.product)))

        for laptop in laptops.scalars():
            profitability_index = ((laptop.ram + laptop.hd) / (laptop.price)) * laptop.speed
            results.append({
                "model": laptop.product.model,
                "type": "Laptop",
                "profitability_index": float(profitability_index)
            })

        for pc in pcs.scalars():
            profitability_index = ((pc.ram + pc.hd) / (pc.price)) * pc.speed
            results.append({
                "model": pc.product.model,
                "type": "PC",
                "profitability_index": float(profitability_index)
            })

        return results

    @staticmethod
    async def get_products_profitability() -> JSONResponse:
        try:
            async with async_session() as session:
                results = await ProfitabilityService.fetch_and_calculate_profitability(session)
                return JSONResponse(status_code=200, content={"profitability": results})
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"error": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})

    @staticmethod
    async def export_profitability_csv() -> JSONResponse:
        try:
            async with async_session() as session:
                products_profitability = await ProfitabilityService.fetch_and_calculate_profitability(session)

                csv_file_path = 'outputs/profitability.csv'
                with open(csv_file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Model', 'Type', 'Profitability Index'])

                    for item in products_profitability:
                        writer.writerow([item['model'], item['type'], item['profitability_index']])

                return JSONResponse(content={"filepath": csv_file_path})
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"error": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
