from fastapi import FastAPI
from db.utils import engine, database, Base, migrate, migrate, migrate_test_data
from routers import profitability, special_offers

app = FastAPI()


@app.on_event("startup")
async def startup():
    await migrate()
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(special_offers.router)
app.include_router(profitability.router)
