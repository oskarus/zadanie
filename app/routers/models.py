from pydantic import BaseModel
from typing import Union, List


class ProductDetails(BaseModel):
    code: int
    model: str
    price: float

    class Config:
        orm_mode = True
        from_attributes = True

class LaptopDetails(ProductDetails):
    speed: int
    ram: int
    hd: int
    screen: int

class PCDetails(ProductDetails):
    speed: int
    ram: int
    hd: int
    cd: str

class PrinterDetails(ProductDetails):
    color: str
    type: str

class Products(BaseModel):
    pc: Union[PCDetails, None] = None
    laptop: Union[LaptopDetails, None] = None
    printer: Union[PrinterDetails, None] = None

class ProductSpecialOfferResult(BaseModel):
    special_offer_set: str
    products: Products
    discounted_price: float

class ProductSpecialOfferResponse(BaseModel):
    special_offers: List[ProductSpecialOfferResult]

class ProfitabilityResult(BaseModel):
    model_name: str
    profitability: float

class ProfitabilityResponse(BaseModel):
    profitability_values: List[ProfitabilityResult]
