from json import JSONDecodeError
from fastapi import HTTPException, APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

# VALIDADORES
from src.validators.students import StudentValidationBody
from src.validators.get_headers import get_request_headers

# LOGGING
from src.configs.logging_config import LOGGER as logger

# HTTP TYPES
from src.controllers.http_types.http_request import HttpRequest

# COMPOSER
from src.main.composer.create_student_composer import create_student_composer

router = APIRouter(
    prefix="/students",
    tags=["Students"],
    responses={
        201: {
            "description": "Student created successfully",
            "content": {
                "application/json": {
                    "status": "success",
                    "message": "Estudante criado com sucesso.",
                    "attributes": {
                        "full_name": "nome completo do aluno",
                        "registration_number": "número de matrícula",
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
                    "detail": "Erro inesperado ocorreu."
                }
            }
        }
    }
)


@router.post("/create", response_class=JSONResponse, status_code=201)
async def post_students(request: Request, headers: dict = Depends(get_request_headers)):
    """Rota para criar um novo estudante."""

    try:
        body = await request.json()
        valid_student_body = StudentValidationBody(**body)

        http_request = HttpRequest(
            body=valid_student_body.model_dump(),
            headers=headers,
        )

        controller = create_student_composer()
        http_response = await controller.handle(http_request)

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
        logger.error(f"Erro de validação: {repr(e)}")
        raise HTTPException(
            status_code=422,
            detail=e.errors()
        ) from e

    except HTTPException as e:
        logger.error(f"Erro HTTP: {repr(e)}")
        raise e
    
    except Exception as e:
        logger.error(f"Erro inesperado: {repr(e)}")
        raise HTTPException(
            status_code=500,
            detail="Ocorreu um erro inesperado ao processar a requisição."
        ) from e
