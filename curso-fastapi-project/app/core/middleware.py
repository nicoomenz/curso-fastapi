import time
from fastapi import Request
from typing import Callable

def add_middlewares(app):
    @app.middleware("http")
    async def log_request_time(request: Request, call_next: Callable):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        print(f"Request: {request.url} - completed in: {process_time:.4f} seconds")
        return response

    @app.middleware("http")
    async def log_request_headers(request: Request, call_next: Callable):
        response = await call_next(request)
        print(f"Headers: {request.headers}")
        return response