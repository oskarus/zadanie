from fastapi import APIRouter
from fastapi.responses import FileResponse
from services.special_offers import SpecialOfferService
from routers.models import ProductSpecialOfferResponse

router = APIRouter(prefix="/api/products")


@router.get("/special_offers", response_model=ProductSpecialOfferResponse)
async def get_products_special_offers():
    return await SpecialOfferService.get_products_special_offers()


@router.post("/special_offers/export-csv", response_class=FileResponse)
async def export_special_offers_csv():
    return await SpecialOfferService.export_scpecial_offers_csv()
