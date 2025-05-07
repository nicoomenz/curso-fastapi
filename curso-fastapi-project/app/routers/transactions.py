from sqlmodel import func, select
from models import *
from fastapi import APIRouter, HTTPException, Query, status
from typing import Any
from db import SessionDep

router = APIRouter(tags=['transactions'])


@router.post("/transactions/", status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    transaction_data_dict = transaction_data.model_dump() #obtenemos los datos de la transaccion
    customer = session.get(Customer, transaction_data_dict.get('customer_id')) #verificamos que el cliente exista
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer dosen't exists") #si no existe el cliente lanzamos una excepcion
    
    transaction_db = Transaction.model_validate(transaction_data_dict) #validamos los datos de la transaccion para guardarlo en el session de la db
    session.add(transaction_db) #agregamos la transaccion a la base de datos
    session.commit() #guardamos los cambios en la base de datos
    session.refresh(transaction_db) #refrescamos la transaccion para obtener el id
    return transaction_db


#skip es los numeros de registros a omitir y limit es el numero de registros a mostrar en el paginador
@router.get("/transactions/", response_model=dict[str, Any])
async def get_transactions(session: SessionDep, 
    skip: int = Query(0, description="Registros a omitir"), 
    limit: int=Query(5, description="Numero de registros")):

    total = session.exec(select(func.count()).select_from(Transaction)).one()
    totalpagination: int = (total + limit - 1) // limit #calculamos el total de paginas
    query = select(Transaction).offset(skip).limit(limit) #obtenemos los registros de la base de datos
    transactions = session.exec(query).all()
    
    response = {
        "total": totalpagination,
        "skip": skip,
        "limit": limit,
        "transactions": transactions
    }

    return response