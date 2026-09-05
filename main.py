from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import employees, auth
from config import settings

import time
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())

    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    response.headers["X-Request-ID"] = request_id

    print(
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        process_time
    )

    return response



app.include_router(employees.router)
app.include_router(auth.router)

