from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

# VALIDADORES
from src.validators.get_headers import get_request_headers

# LOGGING
from src.configs.logging_config import LOGGER as logger

# HTTP TYPES
from src.controllers.http_types.http_request import HttpRequest 

# COMPOSER
from src.main.composer.get_answers_by_student_id_composer import get_answers_by_student_id_composer

router = APIRouter(
    prefix="/answers",
    tags=["Answers"],
    responses={
        200: {
            "description": "OK",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "question_id": 1,
                            "student_id": 1,
                            "answer_text": "Resposta correta para a pergunta.",
                            "created_at": "2025-07-20T13:00:13",
                            "correction_status": "CORRECT"
                        }
                    ]
                }
            }
        },
         400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "ID da pergunta não fornecido."
                    }
                }
            }
        },
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Nenhuma resposta encontrada para o question_id fornecido."
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

@router.get("/student/{student_id}", response_model=list, status_code=200)
async def get_answers_by_student_id(
    student_id: int,
    request: HttpRequest = Depends(get_request_headers)
):
    """Rota para obter respostas de um estudante pelo ID do estudante.
    
    Args:
        student_id (int): ID do estudante cujas respostas serão recuperadas.
        request (HttpRequest): Requisição HTTP contendo os headers necessários.
        
    Returns:
        JSONResponse: Resposta JSON contendo a lista de respostas do estudante.
    
    Raises:
        HTTPException: Se ocorrer um erro ao obter as respostas, retornando o status 404 ou 500.
    
    """
    try:
        controller = get_answers_by_student_id_composer()
        request.param = {"student_id": student_id}
        response = await controller.handle(request)
        return JSONResponse(status_code=response.status_code, content=response.body)
    
    except HTTPException as e:
        logger.error(f"HTTPException: {e.status_code} - {e.detail}")
        raise e
    
    except Exception as e:
        logger.error(f"Erro ao obter respostas do estudante {student_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")
