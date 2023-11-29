from fastapi import APIRouter
from fastapi.responses import FileResponse
from services.profitability import ProfitabilityService
from routers.models import ProfitabilityResponse

router = APIRouter(prefix="/api/products")


@router.get("/profitability", response_model=ProfitabilityResponse)
async def get_products_profitability():
    return await ProfitabilityService.get_products_profitability()


@router.get("/profitability/export-csv", response_class=FileResponse)
async def export_profitability_csv():
    return await ProfitabilityService.export_csv
