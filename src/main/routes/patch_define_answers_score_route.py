from fastapi import HTTPException, APIRouter, Depends, Query, Response

# HTTP Types
from src.controllers.http_types.http_request import HttpRequest

# COMPOSER
from src.main.composer.define_answers_score_composer import define_answers_score_composer

# LOGGER
from src.configs.logging_config import LOGGER

# VALIDATORS
from src.validators.get_headers import get_request_headers

router = APIRouter(
    prefix="/answers",
    tags=["Answers"],
    responses={
        204: {
            "description": "Answer score updated successfully",
        },
        400: {
            "description": "Bad Request - Invalid input data",
            "content": {
                "application/json": {
                    "detail": "Invalid input data."
                }
            }
        },
        404: {
            "description": "Not Found - Resource not found",
            "content": {
                "application/json": {
                    "detail": "Resource not found."
                }
            }
        },
        500: {
            "description": "Internal Server Error - Unexpected error",
            "content": {
                "application/json": {
                    "detail": "Unexpected error occurred."
                }
            }
        },
        503: {
            "description": "Service Unavailable - Service is currently unavailable",
            "content": {
                "application/json": {
                    "detail": "Service is currently unavailable."
                }
            }
        }
    }
)

@router.patch("/score/", response_model=None)
async def patch_define_answers_score_route(
    answer_id: int = Query(..., description="ID of the answer whose score will be defined"),
    score: float = Query(ge = 0, le = 10, description="Score to be assigned to the answer"),
    headers: dict = Depends(get_request_headers)
) -> Response:
    """Rota para definir a pontuação de uma resposta.
    
    Args:
        answer_id (int): ID da resposta cuja pontuação será definida.
        score (float): Pontuação a ser atribuída à resposta.
        headers (dict): Cabeçalhos da requisição.
    
    Returns:
        Response: Resposta HTTP com status 204 se a operação for bem-sucedida.
    
    Raises:
        HTTPException: Se ocorrer um erro ao definir a pontuação, retornando o status 404 ou 500.
    """
    try:
        service = define_answers_score_composer()
        http_request = HttpRequest(param={"answer_id": answer_id, "score": score}, headers=headers)
        response = await service.handle(http_request)
        return Response(status_code=response.status_code)
    
    except HTTPException as e:
        LOGGER.error(f"HTTPException: {e.status_code} - {e.detail}")
        raise e
    
    except Exception as e:
        LOGGER.error(f"Erro ao definir pontuação da resposta: {e}", exc_info=True, stack_info=True)
        raise HTTPException(status_code=500, detail=str(e)) from e
