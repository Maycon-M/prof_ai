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
    tags=["questions"]
)

@router.get("/{exam_id}")
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
