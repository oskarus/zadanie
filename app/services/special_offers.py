from fastapi import HTTPException
from fastapi.responses import JSONResponse
from db.utils import async_session
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from db.models import Laptop, PC, Printer
from routers.models import LaptopDetails, PCDetails, PrinterDetails
from decimal import Decimal
import csv

# Utility Functions
def format_product_details(product) -> dict:
    detail_classes = {
        Laptop: LaptopDetails,
        PC: PCDetails,
        Printer: PrinterDetails
    }

    detail_class = detail_classes.get(type(product))
    if detail_class:
        return detail_class.parse_obj(product.__dict__).dict()
    else:
        return {}

def calculate_discounted_price(*prices, discount_factor=Decimal(0.9)) -> float:
    return float(sum(prices) * discount_factor)

def create_special_offer(promotion_set, *products):
    return {
        'promotion_set': promotion_set,
        'products': {product.__class__.__name__.lower(): format_product_details(product) for product in products},
        'discounted_price': calculate_discounted_price(*(product.price for product in products))
    }

# Database Operations
async def fetch_single_product(session, model):
    result = await session.execute(select(model).limit(1).options(joinedload(model.product)))
    return result.scalar_one_or_none()

class SpecialOfferService:
    @staticmethod
    async def get_products_special_offers() -> JSONResponse:
        try:
            async with async_session() as session:
                pc = await fetch_single_product(session, PC)
                laptop = await fetch_single_product(session, Laptop)
                printer = await fetch_single_product(session, Printer)

                if not (pc and laptop and printer):
                    raise HTTPException(status_code=404, detail="Insufficient products for special offers")

                special_offers = [
                    create_special_offer('PC + Printer', pc, printer),
                    create_special_offer('Laptop + Printer', laptop, printer)
                ]

                return JSONResponse(status_code=200, content={"special_offers": special_offers})
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"error": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})

    @staticmethod
    async def export_special_offers_csv() -> JSONResponse:
        try:
            async with async_session() as session:
                pc = await fetch_single_product(session, PC)
                laptop = await fetch_single_product(session, Laptop)
                printer = await fetch_single_product(session, Printer)

                if not (pc and laptop and printer):
                    raise HTTPException(status_code=404, detail="Insufficient products for special offers")

                special_offers = [
                    create_special_offer('PC + Printer', pc, printer),
                    create_special_offer('Laptop + Printer', laptop, printer)
                ]

                csv_file_path = "outputs/special_offers.csv"

                with open(csv_file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Promotion Set', 'Products', 'Products Details', 'Discounted Price'])

                    for special_offer in special_offers:
                        product_names = ', '.join(special_offer['products'].keys())
                        product_details = '; '.join(
                            f"{name} - " + ', '.join(f'{key}: {value}' for key, value in details.items())
                            for name, details in special_offer['products'].items()
                        )
                        writer.writerow([
                            special_offer['special_offer_set'],
                            product_names,
                            product_details,
                            special_offer['discounted_price']
                        ])

                return JSONResponse(status_code=200, content={"filepath": csv_file_path})

        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"error": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
