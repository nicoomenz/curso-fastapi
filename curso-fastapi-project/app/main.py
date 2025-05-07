from fastapi import FastAPI
from app.core.config import settings
from app.core.lifespan import lifespan_handler
from app.core.middleware import add_middlewares
from app.core.routes import include_routes


app = FastAPI(lifespan=lifespan_handler)

include_routes(app)
add_middlewares(app)



# import time
# from datetime import datetime
# from typing import Annotated, Callable
# from fastapi import Depends, FastAPI, HTTPException, Request
# import zoneinfo

# from fastapi.security import HTTPBasic, HTTPBasicCredentials
# from db import create_all_tables
# from models import *
# from .routers import customers, invoices, transactions, plans
# from fastapi import status
# import os
# from dotenv import load_dotenv

# load_dotenv()

# app = FastAPI(lifespan=create_all_tables) #crea todas las tablas en la base de datos
# app.include_router(customers.router) #incluimos el router de clientes
# app.include_router(invoices.router) #incluimos el router de facturas
# app.include_router(transactions.router) #incluimos el router de transacciones
# app.include_router(plans.router) #incluimos el router de planes

# @app.middleware("http")
# async def log_request_time(request: Request, call_next: Callable):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     print(f"Request: {request.url} - completed in: {process_time:.4f} seconds")
#     return response

# @app.middleware("http")
# async def log_request_headers(request: Request, call_next: Callable):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     print(f"Request: {request.headers} - completed in: {process_time:.4f} seconds")
#     return response

# security = HTTPBasic()

# ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
# ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# @app.get("/")
# async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
#     if credentials.username != ADMIN_USERNAME or credentials.password != ADMIN_PASSWORD:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
#     return {"message": f"Hola {credentials.username}!"}

# country_timezones = {
#     "AR": "America/Argentina/Buenos_Aires",
#     "BR": "America/Sao_Paulo",
#     "CL": "America/Santiago",
#     "CO": "America/Bogota",
#     "MX": "America/Mexico_City",
# }

# @app.get("/time/{iso_code}")
# async def get_time_by_iso_code(iso_code: str):
#     iso = iso_code.upper()
#     timezone_str = country_timezones.get(iso)
#     tz = zoneinfo.ZoneInfo(timezone_str)
#     return {"time": datetime.now(tz)}
