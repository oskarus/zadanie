from fastapi import HTTPException
from fastapi.responses import JSONResponse
from db.utils import async_session
from db.models import Product
from sqlalchemy import select


class ProfitabilityService:
    @staticmethod
    async def get_products_profitability() -> JSONResponse:
        try:
            async with async_session() as session:
                result = await session.execute(select(Product).limit(1)) 
                products = result.scalars().all()
            return JSONResponse(status_code=200, content={"products": products})
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"error": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})

    @staticmethod
    async def export_profitability_csv() -> JSONResponse:
        try:
            return JSONResponse(status_code=200, content={"msg": "placeholder"})
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"error": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
