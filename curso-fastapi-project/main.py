from datetime import datetime
from fastapi import FastAPI, HTTPException, status
import zoneinfo
from db import SessionDep, create_all_tables
from models import *
from sqlmodel import select



app = FastAPI(lifespan=create_all_tables) #crea todas las tablas en la base de datos

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

db_customers: list[Customer] = [] #base de datos en memoria

@app.post("/customers/", response_model=Customer) #con que modelo vamos a responder
async def create_customer(customer_data: CustomerCreate, session: SessionDep): #con que modelo vamos a recibir
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer) #agregamos el cliente a la base de datos
    session.commit() #guardamos los cambios en la base de datos
    session.refresh(customer)

    return customer

@app.get("/customers/", response_model=list[Customer])
async def get_customers(session: SessionDep):
    return session.exec(select(Customer)).all() #obtenemos todos los clientes de la base de datos

@app.get("/customers/{customer_id}", response_model=Customer)
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id) #obtenemos el cliente de la base de datos
    if customer_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer_db

@app.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED) #actualizar un cliente
async def update_customer(customer_id: int, customer_data: CustomerUpdate, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if customer_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    customer_data_dict = customer_data.model_dump(exclude_unset=True) #obtenemos los datos del cliente
    customer_db.sqlmodel_update(customer_data_dict) #actualizamos el cliente
    session.add(customer_db) #agregamos el cliente a la base de datos
    session.commit()
    session.refresh(customer_db)
    return customer_db

@app.delete("/customers/{customer_id}") #eliminar un cliente, si no le pongo un response_model no necesito devolver un modelo u objeto
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if customer_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    session.delete(customer_db)
    session.commit()
    return {"message": "Customer deleted"}

@app.post("/transactions/")
async def create_transaction(transaction: Transaction):
    return transaction

@app.post("/invoices/")
async def create_invoice(invoice: Invoice):
    return invoice
