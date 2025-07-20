from json import JSONDecodeError
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

# VALIDATORS
from src.validators.exams import ExamValidBody

# LOGGER
from src.configs.logging_config import LOGGER as logger

# HTTP TYPES
from src.controllers.http_types.http_request import HttpRequest

# COMPOSER
from src.main.composer.create_exam_composer import create_exam_composer

router = APIRouter(
    prefix="/exams",
    tags=["Exams"],
    responses={
        201: {
            "description": "Exam created successfully",
            "content": {
                "application/json": {
                    "status": "success",
                    "message": "Prova criada com sucesso.",
                    "attributes": {
                        "subject": "subject_name",
                        "teacher_id": 1,
                        "time_stamp": "2023-10-01T12:00:00",
                        "correction_status": "Pendente"
                    }
                }
            }
        },
        400: {
            "description": "Bad Request - Invalid input data",
            "content": {
                "application/json": {
                    "detail": "Dados de entrada inválidos."
                }
            }
        },
        404: {
            "description": "Not Found - Resource not found",
            "content": {
                "application/json": {
                    "detail": "Recurso não encontrado."
                }
            }
        },
        422: {
            "description": "Unprocessable Entity - Validation error",
            "content": {
                "application/json": {
                    "detail": "Erro de validação."
                }
            }
        },
        500: {
            "description": "Internal Server Error - Unexpected error",
            "content": {
                "application/json": {
                    "detail": "Erro inesperado ocorreu."
                }
            }
        },
        503: {
            "description": "Service Unavailable - Service is currently unavailable",
            "content": {
                "application/json": {
                    "detail": "Serviço indisponível no momento."
                }
            }
        }
    }
)

@router.post("/create", response_class=JSONResponse, status_code=201)
async def create_exam_route(
    request: Request,
):
    try:
        body = await request.json()
        valid_body = ExamValidBody(**body)
        
        http_request = HttpRequest(
            body=valid_body
        )
        
        controller = create_exam_composer()
        
        http_response = await controller.handle(http_request)
        logger.info(f"Resposta do controlador: {http_response.body}")
        
        return JSONResponse(
            status_code=http_response.status_code,
            content=http_response.body
        )
    
    except JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON: {repr(e)}")
        raise HTTPException(
            status_code=400,
            detail="Corpo da requisição não contém um JSON válido ou está vazio."
        ) from e
    
    except ValidationError as e:
        
        errors = [
            {
            "campo": error["loc"],
            "mensagem": error["msg"],
            "valor": error["input"],
            "tipo": error["type"],
            }
            for error in e.errors()
        ]
        
        header_errors = {
            "codigo": 422,
            "descricao": "Erro de validação",
            "erros": errors
        }
        
        logger.error(f"Erro de validação: {header_errors}")
        raise HTTPException(status_code=422, detail={"erros": header_errors})
    
    except HTTPException  as e:
        logger.error(f"HTTPException: {e.status_code} Erro completo: {repr(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    except Exception as e:
        logger.error(f"Tipo de erro: {type(e)} Erro completo: {repr(e)}", exc_info=True, stack_info=True, extra={"request": request})
        raise HTTPException(status_code=500, detail=e)