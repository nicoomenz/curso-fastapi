from fastapi import FastAPI
from ..routers import customers, invoices, transactions, plans
from ..auth.basic_auth import basic_root_route, get_time_by_iso_code

def include_routes(app: FastAPI):
    app.include_router(customers.router)
    app.include_router(invoices.router)
    app.include_router(transactions.router)
    app.include_router(plans.router)

    app.add_api_route("/", basic_root_route, methods=["GET"])
    app.add_api_route("/time/{iso_code}", get_time_by_iso_code, methods=["GET"])
