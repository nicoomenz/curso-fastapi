from fastapi import APIRouter, HTTPException, Query, status
from fastapi import Depends
from sqlmodel import select
from models import *
from db import SessionDep

db_customers: list[Customer] = [] #base de datos en memoria

router = APIRouter(tags=['customers']) #creamos un router para agrupar los endpoints de clientes

@router.post("/customers/", response_model=Customer, status_code=status.HTTP_201_CREATED) #con que modelo vamos a responder
async def create_customer(customer_data: CustomerCreate, session: SessionDep): #con que modelo vamos a recibir
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer) #agregamos el cliente a la base de datos
    session.commit() #guardamos los cambios en la base de datos
    session.refresh(customer)

    return customer

@router.get("/customers/", response_model=list[Customer])
async def get_customers(session: SessionDep):
    return session.exec(select(Customer)).all() #obtenemos todos los clientes de la base de datos

@router.get("/customers/{customer_id}", response_model=Customer)
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id) #obtenemos el cliente de la base de datos
    if customer_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer_db

@router.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED) #actualizar un cliente
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

@router.delete("/customers/{customer_id}") #eliminar un cliente, si no le pongo un response_model no necesito devolver un modelo u objeto
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if customer_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    session.delete(customer_db)
    session.commit()
    return {"message": "Customer deleted"}

@router.post("/customers/{customer_id}/plans/{plan_id}", status_code=status.HTTP_201_CREATED)
async def subscribe_customer_to_plan(customer_id: int, plan_id: int, session: SessionDep, plan_status: StatusEnum = Query(),):
    customer_db = session.get(Customer, customer_id)

    if customer_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    plan_db = session.get(Plan, plan_id)
    if plan_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    
    customer_plan = CustomerPlan(customer_id=customer_id, plan_id=plan_id, status=plan_status)
    session.add(customer_plan)
    session.commit()
    session.refresh(customer_plan)
    return customer_plan

@router.get("/customers/{customer_id}/plans", response_model=list[Plan])
async def get_customer_plans(customer_id: int, session: SessionDep, plan_status: StatusEnum = Query()):
    customer_db = session.get(Customer, customer_id)
    if customer_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    query = select(CustomerPlan).where(CustomerPlan.customer_id == customer_id).where(CustomerPlan.status == plan_status)
    plans = session.exec(query).all()
    return plans