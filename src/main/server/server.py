from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from src.models.settings.postegres_connection import pg_connection_handler

# ROTAS
from src.main.routes.health_checker_route import router as health_checker_router
from src.main.routes.post_create_exam_route import router as post_create_exam_router
from src.main.routes.post_create_question_route import router as post_question_router
from src.main.routes.get_questions_by_exam_id_route import router as get_questions_router
from src.main.routes.post_create_students_route import router as post_students_router
from src.main.routes.post_create_answer_route import router as post_answers_router

# LOGGING
from src.configs.logging_config import LOGGER as logger


pg_connection_handler.connect_to_db()

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
app.include_router(post_create_exam_router)
app.include_router(post_question_router)
app.include_router(get_questions_router)
app.include_router(post_students_router)
app.include_router(post_answers_router)
