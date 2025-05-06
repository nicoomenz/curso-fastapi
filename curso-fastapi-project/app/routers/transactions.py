from sqlmodel import select
from models import *
from fastapi import APIRouter, HTTPException, status
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



@router.get("/transactions/", response_model=list[Transaction])
async def get_transactions(session: SessionDep):
    query = select(Transaction)
    transactions = session.exec(query).all()
    return transactions