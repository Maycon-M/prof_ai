# MODELS
from src.models.settings.postegres_connection import pg_connection_handler
from src.models.repositories.questions_repository import QuestionsRepository

# SERVICES
from src.services.get_questions_by_exam_id import GetQuestionsByExamId

# CONTROLLER
from src.controllers.get_questions_by_exam_id_controller import GetQuestionsByExamIdController

def get_questions_by_exam_id_composer() -> GetQuestionsByExamIdController:
    """Compositor para criar o controller de obtenção de questões por ID de exame."""

    model = QuestionsRepository(pg_connection_handler)
    service = GetQuestionsByExamId(model)
    controller = GetQuestionsByExamIdController(service)
    
    return controller
