from json import JSONDecodeError
from fastapi import HTTPException, APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

# VALIDADORES
from src.validators.teachers import TeacherValidationBody
from src.validators.get_headers import get_request_headers

# LOGGING
from src.configs.logging_config import LOGGER as logger

# HTTP TYPES
from src.controllers.http_types.http_request import HttpRequest

# COMPOSER
from src.main.composer.create_teacher_composer import create_teacher_composer

router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"],
    responses={
        201: {
            "description": "Teacher created successfully",
            "content": {
                "application/json": {
                    "status": "success",
                    "message": "Professor criado com sucesso.",
                    "attributes": {
                        "name": "nome completo do professor",
                        "email": "email do professor",
                        "time_stamp": "2025-10-01T12:00:00",
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
                    "detail": "Erro interno do servidor."
                }
            }
        },
        503: {
            "description": "Service Unavailable - Service is currently unavailable",
            "content": {
                "application/json": {
                    "detail": "Serviço temporariamente indisponível."
                }
            }
        }
    }
)

@router.post("/create", response_class=JSONResponse, status_code=201)
async def create_teacher(request: Request, headers: dict = Depends(get_request_headers)):
    """Rota para criar um novo professor."""
    try:
        body = await request.json()
        validated_body = TeacherValidationBody(**body)
        http_request = HttpRequest(body=validated_body.model_dump(), headers=headers)
        
        controller = create_teacher_composer()
        response = await controller.handle(http_request)
        
        return JSONResponse(status_code=response.status_code, content=response.body)
    
    except JSONDecodeError:
        logger.error("Erro ao decodificar o JSON da requisição.")
        raise HTTPException(status_code=400, detail="Dados de entrada inválidos.")
    
    except ValidationError as ve:
        logger.error(f"Erro de validação: {ve.errors()}")
        raise HTTPException(status_code=422, detail="Erro de validação dos dados de entrada.")
    
    except HTTPException as http_exc:
        logger.error(f"HTTP Exception: {http_exc.detail}", exc_info=True)
        raise http_exc
    
    except Exception as e:
        logger.error(f"Erro inesperado ao criar professor: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")
