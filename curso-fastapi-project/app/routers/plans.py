from sqlmodel import select
from models import *
from fastapi import APIRouter, HTTPException, status
from db import SessionDep

router = APIRouter(tags=['plans'])
@router.post("/plans/", status_code=status.HTTP_201_CREATED, response_model=Plan)
async def create_plan(plan_data: PlanCreate, session: SessionDep):
    plan = Plan.model_validate(plan_data.model_dump()) #obtenemos los datos del plan
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan

@router.get("/plans/", response_model=list[Plan])
async def get_plans(session: SessionDep):
    query = select(Plan)
    plans = session.exec(query).all()
    return plans

