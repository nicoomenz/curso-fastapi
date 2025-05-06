from datetime import datetime
from fastapi import FastAPI
import zoneinfo
from db import create_all_tables
from models import *
from .routers import customers, invoices, transactions, plans

app = FastAPI(lifespan=create_all_tables) #crea todas las tablas en la base de datos
app.include_router(customers.router) #incluimos el router de clientes
app.include_router(invoices.router) #incluimos el router de facturas
app.include_router(transactions.router) #incluimos el router de transacciones
app.include_router(plans.router) #incluimos el router de planes

@app.get("/")
async def root():
    return {"message": "Hola Nico"}

country_timezones = {
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "CL": "America/Santiago",
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
}

@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}
