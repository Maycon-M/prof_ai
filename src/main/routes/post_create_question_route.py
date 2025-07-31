from json import JSONDecodeError
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

# VALIDADORES
from src.validators.questions import ValidQuestionsBody
from src.validators.get_headers import get_request_headers

# LOGGING
from src.configs.logging_config import LOGGER as logger

# HTTP TYPES
from src.controllers.http_types.http_request import HttpRequest 

# COMPOSER
from src.main.composer.create_questions_composer import create_questions_composer

router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
    responses={
        201: {
            "description": "Questions created successfully",
            "content": {
                "application/json": {
                    "status": "success",
                    "message": "Questões criadas com sucesso."
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
                    "detail": "Serviço indisponível."
                }
            }
        }
    }
)

@router.post("/create/{exam_id}", response_class=JSONResponse, status_code=201)
async def post_questions(exam_id: int, request: Request, headers: dict = Depends(get_request_headers)):

    """Rota para criar questões associadas a uma prova."""

    if not exam_id or exam_id <= 0:
        logger.error("ID da prova não fornecido.")
        raise HTTPException(
            status_code=400,
            detail="ID da prova não fornecido."
        )
    
    try:
        body = await request.json()
        valid_questions_body = ValidQuestionsBody(**body)
        
        http_request = HttpRequest(
            body=valid_questions_body.model_dump(),
            headers=headers,
            param={"exam_id": exam_id},
        )
        
        controller = create_questions_composer()
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
        
        errors = [
            {
                "campo": error["loc"],
                "mensagem": error["msg"],
                "valor": error["input"],
                "tipo": error["type"]
            }
            
            for error in e.errors()
        ]
        
        header_error = {
            "codigo": 422,
            "descricao": "Erro de validação",
            "erros": errors
        }
        
        logger.error(f"Erro de validação: {header_error}")
        raise HTTPException(status_code=422, detail=header_error)
    
    except HTTPException  as e:
        logger.error(f"HTTPException: {e.status_code} Erro completo: {repr(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    except Exception as e:
        logger.error(f"Tipo de erro: {type(e)} Erro completo: {repr(e)}")
        raise HTTPException(status_code=500, detail=e)
