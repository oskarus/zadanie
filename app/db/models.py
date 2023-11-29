from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship,declared_attr, declarative_mixin
from db.utils import Base


@declarative_mixin
class BaseDeviceModel(object):
    code = Column(Integer, primary_key=True)
    price = Column(Numeric)

    @declared_attr
    def model(cls):
        return Column(String(50), ForeignKey('products.model'))

    @declared_attr
    def product(cls):
        return  relationship("Product", back_populates=f"{cls.__name__.lower()}s")



class BaseComputerModel(BaseDeviceModel):
    speed = Column(Integer)
    ram = Column(Integer)
    hd = Column(Integer)


class Laptop(Base, BaseComputerModel):
    __tablename__ = "laptops"

    screen = Column(Integer)


class PC(Base, BaseComputerModel):
    __tablename__ = "personal_computers"

    cd = Column(String(10))


class Printer(Base, BaseDeviceModel):
    __tablename__ = "printers"

    color = Column(String(1))
    type = Column(String(10))


class Product(Base):
    __tablename__ = "products"

    model = Column(String(50), primary_key=True)
    maker = Column(String(10))
    type = Column(String(50))

    laptops = relationship("Laptop", back_populates="product")
    pcs = relationship("PC", back_populates="product")
    printers = relationship("Printer", back_populates="product")
