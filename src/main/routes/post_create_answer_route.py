from json import JSONDecodeError
from fastapi import HTTPException, APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

# HTTP Types
from src.controllers.http_types.http_request import HttpRequest

# COMPOSER
from src.main.composer.create_answers_composer import create_answers_composer

# LOGGER
from src.configs.logging_config import LOGGER

# VALIDATORS
from src.validators.get_headers import get_request_headers
from src.validators.answers import AnswersValidBody

router = APIRouter(
    prefix="/answers",
    tags=["Answers"],
    responses= {
        201: {
            "description": "Answer created successfully",
            "content": {
                "application/json": {
                    "status": "success",
                    "message": "Respostas criadas com sucesso."
                }
            }
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
        422: {
            "description": "Unprocessable Entity - Validation error",
            "content": {
                "application/json": {
                    "detail": "Validation error."
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

@router.post("/create", response_class=JSONResponse, status_code=201)
async def create_answers(request: Request, 
                         headers: dict = Depends(get_request_headers)) -> JSONResponse:
    """Endpoint para criar respostas de uma prova."""
    try:
        body = await request.json()
        valid_body = AnswersValidBody(**body)
        
        http_request = HttpRequest(body=valid_body.model_dump(), headers=headers)
        controller = create_answers_composer()
        response = await controller.handle(http_request)
        return JSONResponse(status_code=response.status_code, content=response.body)
    
    except JSONDecodeError:
        LOGGER.error("Invalid JSON format in request body.")
        raise HTTPException(status_code=400, detail="Invalid JSON format.")
    
    except ValidationError as ve:
        LOGGER.error(f"Validation error: {ve.errors()}")
        raise HTTPException(status_code=422, detail=ve.errors())
    
    except HTTPException as http_exc:
        LOGGER.error(f"HTTP Exception: {http_exc.detail}")
        raise http_exc
    
    except Exception as e:
        LOGGER.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
