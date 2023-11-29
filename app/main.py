from fastapi import FastAPI
from settings import config
from db.utils import engine, database, Base
from routers import profitability, special_offers

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(special_offers.router)
app.include_router(profitability.router)
