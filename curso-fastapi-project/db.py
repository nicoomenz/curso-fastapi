from typing import Annotated
from fastapi import Depends, FastAPI

from sqlmodel import Session, create_engine, SQLModel

sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_url)

def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine) #crea todas las tablas en la base de datos
    yield #cedemos el control a la aplicacion a fastapi
    
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)] # registrando la session para todos nuestros endpoints
# para que no tengamos que estar creando la session en cada endpoint