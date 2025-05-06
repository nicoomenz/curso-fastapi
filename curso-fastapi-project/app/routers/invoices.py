from models import *
from fastapi import APIRouter


router = APIRouter(tags=['invoices'])

@router.post("/invoices/")
async def create_invoice(invoice: Invoice):
    return invoice