from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

# VALIDADORES
from src.validators.get_headers import get_request_headers

# LOGGING
from src.configs.logging_config import LOGGER as logger

# HTTP TYPES
from src.controllers.http_types.http_request import HttpRequest 

# COMPOSER
from src.main.composer.get_answer_by_id_composer import get_answer_by_id_composer

router = APIRouter(
    prefix="/answers",
    tags=["Answers"],
    responses={
        200: {
            "description": "OK",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "text": "Resposta correta para a pergunta.",
                        "question_id": 1,
                        "created_at": "2025-07-20T13:00:13"
                    }
                }
            }
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "ID da resposta não fornecido."
                    }
                }
            }
        },
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Resposta não encontrada."
                    }
                }
            }
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Erro interno do servidor."
                    }
                }
            }
        },
        503: {
            "description": "Service Unavailable",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Serviço temporariamente indisponível."
                    }
                }
            }
        }
    }
)

@router.get("/id/{answer_id}", response_class=JSONResponse, status_code=200)
async def get_answer_by_id(answer_id: int, headers: dict = Depends(get_request_headers)):
    """Rota para obter uma resposta pelo ID."""
    
    try:
        request = HttpRequest(param={"answer_id": answer_id}, headers=headers)
        controller = get_answer_by_id_composer()
        response = await controller.handle(request)
        

        return JSONResponse(status_code=response.status_code, content=response.body)
    
    except HTTPException as e:
        logger.error(f"HTTPException: {e.status_code} - {e.detail}")
        raise e
    
    except Exception as e:
        logger.error(f"Erro ao obter resposta: {e}", exc_info=True, stack_info=True)
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")
