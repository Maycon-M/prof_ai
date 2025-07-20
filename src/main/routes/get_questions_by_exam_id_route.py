from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

# VALIDADORES
from src.validators.get_headers import get_request_headers

# LOGGING
from src.configs.logging_config import LOGGER as logger

# HTTP TYPES
from src.controllers.http_types.http_request import HttpRequest 

# COMPOSER
from src.main.composer.get_questions_by_exam_id_composer import get_questions_by_exam_id_composer

router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
    responses= {
        200: {
            "description": "OK",
            "content": {
                "application/json": {
                    "example": {
                    "questions": [
                            {
                            "id": 1,
                            "number": 1,
                            "text": "Em que ano começou a segunda guerra mundial?",
                            "correction_status": "Pendente",
                            "exam_id": 1,
                            "created_at": "2025-07-20T13:00:13"
                            },
                            {
                            "id": 2,
                            "number": 2,
                            "text": "Quando começou a revolução russa?",
                            "correction_status": "Pendente",
                            "exam_id": 1,
                            "created_at": "2025-07-20T13:00:16"
                            }
                        ]
                    }
                }
            }
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "ID da prova não fornecido."
                    }
                }
            }
        },
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "example": {
                        "message": "404: Nenhuma questão encontrada para o exame fornecido."
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

@router.get("/{exam_id}", response_class=JSONResponse, status_code=200)
async def get_questions_by_exam_id(exam_id: int, headers: dict = Depends(get_request_headers)):
    """Rota para obter questões associadas a uma prova."""
    
    if not exam_id or exam_id <= 0:
        logger.error("ID da prova não fornecido.")
        raise HTTPException(
            status_code=400,
            detail="ID da prova não fornecido."
        )
    
    try:
        http_request = HttpRequest(
            body=None,
            headers=headers,
            param={"exam_id": exam_id},
        )
        
        controller = get_questions_by_exam_id_composer()
        http_response = await controller.handle(http_request)
        
        return JSONResponse(
            status_code=http_response.status_code,
            content=http_response.body
        )
        
    except HTTPException as e:
        logger.error(f"HTTPException: {e.status_code} Erro completo: {repr(e)}")
        raise e
    
    except Exception as e:
        logger.error(f"Tipo de erro: {type(e)} Erro completo: {repr(e)}")
        raise HTTPException(status_code=500, detail=e)
