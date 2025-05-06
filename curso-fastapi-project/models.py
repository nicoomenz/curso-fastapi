from pydantic import BaseModel, EmailStr, field_validator
from sqlmodel import SQLModel, Field, Relationship, Session, select
from enum import Enum
from db import engine

class PlanBase(SQLModel): #para crear la tabla de planes
    name: str = Field(default=None)
    price: int = Field(default=None)
    description: str | None = Field(default=None)
    
class PlanCreate(PlanBase): #para crear un plan
    pass

class PlanUpdate(PlanBase): #para actualizar un plan
    pass

class StatusEnum(str, Enum): #para crear un enum de los estados
    ACTIVE = "active"
    INACTIVE = "inactive"

class CustomerPlan(SQLModel, table=True): #para crear la tabla de clientes y planes
    id: int | None = Field(default=None, primary_key=True) #para que sea el id de la tabla
    customer_id: int = Field(foreign_key="customer.id") #para que sea el id del cliente
    plan_id: int = Field(foreign_key="plan.id") #para que sea el id del plan
    status: StatusEnum = Field(default=StatusEnum.ACTIVE) #para que sea el estado del plan

class Plan(PlanBase, table=True): #para mostrar un plan
    id: int | None = Field(default=None, primary_key=True) #para que sea el id de la tabla
    customers: list["Customer"] = Relationship(back_populates="plans", link_model=CustomerPlan) #para que sea una relacion uno a muchos

class CustomerBase(SQLModel): #para validad el tipado de los datos
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None)
    
    # esto se podria hacer con un unique en la bd, pero por aprendizaje lo hacemos aqui
    @field_validator("email") #decorador para validar el email
    @classmethod
    def validate_email(cls, value): #validamos el email
        session = Session(engine)
        query = select(Customer).where(Customer.email == value) #verificamos que el email no exista
        result = session.exec(query).first()
        if result:
            raise ValueError("Email already exists")
        return value

class CustomerCreate(CustomerBase): #para crear un cliente
    pass

class CustomerUpdate(CustomerBase): #para actualizar un cliente
    pass

class Customer(CustomerBase, table=True): #para mostrar un cliente
    id: int | None = Field(default=None, primary_key=True) #para que sea el id de la tabla
    transactions: list["Transaction"] = Relationship(back_populates="customer") #para que sea una relacion uno a muchos
    plans: list[Plan] = Relationship(back_populates="customers", link_model=CustomerPlan) #para que sea una relacion uno a muchos

class TransactionBase(SQLModel): #para validad el tipado de los datos
    amount: int = Field(default=None)
    description: str | None = Field(default=None)

class Transaction(TransactionBase, table=True): #para mostrar una transaccion
    id: int | None = Field(default=None, primary_key=True) #para que sea el id de la tabla
    customer_id: int = Field(foreign_key="customer.id") #para que sea el id del cliente
    customer: Customer = Relationship(back_populates="transactions") #para que sea una relacion uno a muchos

class TransactionCreate(TransactionBase): #para crear una transaccion
    customer_id: int = Field(foreign_key="customer.id") #para que sea el id del cliente

class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property  #decorador para definir una variable de clase
    def amount_total(self):
        return sum(transaction.amount for transaction in self.transactions)