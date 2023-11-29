from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from db.utils import Base



class BaseDeviceModel:
    code = Column(Integer, primary_key=True)
    model = Column(String(50), ForeignKey('products.model'))
    price = Column(Numeric)


class BaseComputerModel(BaseDeviceModel):
    speed = Column(Integer)
    ram = Column(Integer)
    hd = Column(Integer)


class Laptop(BaseComputerModel):
    __tablename__ = "laptops"

    screen = Column(Integer)

    product = relationship("Product", back_populates="laptops")


class PC(BaseComputerModel):
    __tablename__ = "personal_computers"

    cd = Column(String(10))

    product = relationship("Product", back_populates="personal_computers")


class Printer(BaseDeviceModel):
    __tablename__ = "printers"

    color = Column(String(1))
    type = Column(String(10))

    product = relationship("Product", back_populates="printers")



class Product(Base):
    __tablename__ = "products"

    model = Column(String(50), primary_key=True)
    maker = Column(String(10))
    type = Column(String(50))

    laptops = relationship("Laptop", back_populates="product")
    personal_computers = relationship("PC", back_populates="product")
    printers = relationship("Printer", back_populates="product")
