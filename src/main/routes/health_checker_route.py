from fastapi import APIRouter

router = APIRouter (
    prefix="/health_checker",
    tags=["Heath Checker"],
    responses= {
        200: {
            "description": "Service is running",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ok",
                        "detail": "Service is running smoothly"
                    }
                }
            }
        },
        404: {
            "description": "Service not found",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "detail": "Service not found"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "detail": "Internal server error"
                    }
                }
            }
        },
        503: {
            "description": "Service unavailable",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "detail": "Service is currently unavailable"
                    }
                }
            }
        }
    }
)


@router.get("/", summary="Health Check")
async def health_check():
    """
    Endpoint para checar o estado do serviço.
    
    Returns:
    str: JSON com o status do serviço.
    """
    return {"status": "ok", "detail": "Service is running smoothly"}
