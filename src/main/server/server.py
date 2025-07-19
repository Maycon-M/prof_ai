from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

# ROTAS
from src.main.routes.health_checker_route import router as health_checker_router

# LOGGING
from src.configs.logging_config import LOGGER as logger

app = FastAPI (
    title="API - Prof AI",
    description= "",
    version="1.0.0",    
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware(middleware_type="https")
async def log_requests(request: Request, call_next):
    if request.method != "GET":
        logger.info(f"Recebendo requisição: {request.method} {request.url.path}")
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Erro não tratado durante a requisição: {e}")
        raise
    if request.method != "GET":
        logger.info(f"Respondendo requisição: {request.method} {request.url.path} -> Status {response.status_code}")
    return response

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    error_message = str(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": error_message}
    )
    

app.include_router(health_checker_router)
