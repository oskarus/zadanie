from fastapi import APIRouter
from services.special_offers import SpecialOfferService
from routers.models import ProductSpecialOfferResponse

router = APIRouter(prefix="/api/products")


@router.get("/special-offers", response_model=ProductSpecialOfferResponse)
async def get_products_special_offers():
    return await SpecialOfferService.get_products_special_offers()


@router.post("/special-offers/export-csv")
async def export_special_offers_csv():
    return await SpecialOfferService.export_special_offers_csv()
