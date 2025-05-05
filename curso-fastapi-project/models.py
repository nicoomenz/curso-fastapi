from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field

class CustomerBase(SQLModel): #para validad el tipado de los datos
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None)

class CustomerCreate(CustomerBase): #para crear un cliente
    pass

class CustomerUpdate(CustomerBase): #para actualizar un cliente
    pass

class Customer(CustomerBase, table=True): #para mostrar un cliente
    id: int | None = Field(default=None, primary_key=True) #para que sea el id de la tabla

class Transaction(BaseModel):
    id: int
    amount: int
    description: str | None

class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property  #decorador para definir una variable de clase
    def amount_total(self):
        return sum(transaction.amount for transaction in self.transactions)