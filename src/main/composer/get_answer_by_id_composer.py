# MODELS
from src.models.settings.postegres_connection import pg_connection_handler
from src.models.repositories.answers_repository import AnswersRepository

# SERVICE
from src.services.get_answer_by_id import GetAnswerById

# CONTROLLER
from src.controllers.get_answer_by_id_controller import GetAnswerByIdController


def get_answer_by_id_composer() -> GetAnswerByIdController:
    """Composer para o controlador de obter resposta por ID.
    
    Returns:
        GetAnswerByIdController: Instância do controlador configurado.
    """
    
    model = AnswersRepository(pg_connection_handler)
    
    service = GetAnswerById(model)
    
    controller = GetAnswerByIdController(service)
    
    return controller
