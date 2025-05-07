import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session
from app.main import app
from db import get_session
from models import Customer

sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_url, # para crear la base de datos en sqlite
                       connect_args={"check_same_thread": False}, # para que no de error de conexion
                       poolclass=StaticPool
) # StaticPool es para que no se cree una nueva conexion cada vez que se hace una consulta

@pytest.fixture(name="session")
def session_fixture(): # lo que retorne con pytest que puede ser una prueba u otro fixture
    SQLModel.metadata.create_all(engine) # crea todas las tablas en la base de datos
    with Session(engine) as session: # crea una nueva session
        yield session # cedemos el control al proximo fixture, cuando vuelve sigue ejecutando
    SQLModel.metadata.drop_all(engine) # elimina todas las tablas en la base de datos

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override # sobreescribimos la dependencia de la session para que use la session del fixture y usar los metodos del router
    client = TestClient(app) # creamos un cliente de prueba
    yield client # cedemos el control al proximo fixture
    app.dependency_overrides.clear() # limpiamos las dependencias sobreescritas

@pytest.fixture(name="customer")
def customer_data_fixture(session: Session):
    customer = Customer(name="Nico Perez", email="nicoperez@gmail.com", age=30) # creamos un cliente de prueba
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@pytest.fixture(name="plan")
def plan_data_fixture(session: Session):
    from models import Plan
    plan = Plan(name="Plan 1", price=100, description="Plan de prueba")
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan
    