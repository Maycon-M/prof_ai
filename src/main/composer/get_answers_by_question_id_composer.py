# MODELS
from src.models.settings.postegres_connection import pg_connection_handler
from src.models.repositories.answers_repository import AnswersRepository

# SERVICE
from src.services.get_answers_by_question_id import GetAnswersByQuestionId

# CONTROLLER
from src.controllers.get_answers_by_question_id_controller import GetAnswersByQuestionIdController

def get_answers_by_question_id_composer() -> GetAnswersByQuestionIdController:
    """Composer para criar o controller de obter respostas por question_id.
    
    Returns:
        controller (GetAnswersByQuestionIdController): Instância do controller configurada com o serviço necessário.
    """
    model = AnswersRepository(pg_connection_handler)
    service = GetAnswersByQuestionId(model)
    controller =  GetAnswersByQuestionIdController(service) 
    return controller
