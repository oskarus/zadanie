from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from databases import Database
from settings import config



database = Database(config.database_url)
Base = declarative_base()

engine = create_async_engine(config.database_url, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

test_data = {
    "products":[
        {"model":'Printer1', "maker":'MakerA',"type": 'Printer'},
        {"model":'Printer2', "maker":'MakerA',"type": 'Printer'},
        {"model":'PC1', "maker":'MakerB',"type": 'PC'},
        {"model":'PC2', "maker":'MakerB',"type": 'PC'},
        {"model":'Laptop1', "maker":'MakerC',"type": 'Laptop'},
        {"model":'Laptop2', "maker":'MakerC',"type": 'Laptop'},
    ],
    "printers":[
        {"model":"Printer1","color": "Y","type": "Laser","price": 150.0},
        {"model":"Printer2","color": "N","type": "Inkjet","price": 120.0},
    ],
    "personal_computers":[
        {"model": "PC1", "speed": 3200, "ram": 8, "hd": 500, "cd":"DVD", "price":450.00},
        {"model": "PC2", "speed": 3400, "ram": 16, "hd": 1000, "cd":"Blu-ray", "price":550.00},
    ],
    "laptops":[
        {"model": "PC1", "speed": 2500, "ram": 16, "hd": 1000, "price":800.00, "screen": 15},
        {"model": "PC1", "speed": 2600, "ram": 8, "hd": 750, "price":700.00, "screen": 13},
    ]
}

async def migrate():
    from db.models import Laptop, PC, Printer, Product
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def migrate_test_data():
    from db.models import Laptop, PC, Printer, Product
    async with async_session() as session:
        session.add_all([Product(**data) for data in test_data["products"]])
        session.add_all([Printer(**data) for data in test_data["printers"]])
        session.add_all([PC(**data) for data in test_data["personal_computers"]])
        session.add_all([Laptop(**data) for data in test_data["laptops"]])
        await session.commit()
