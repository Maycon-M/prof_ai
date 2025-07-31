# MODELS
from src.models.settings.postegres_connection import pg_connection_handler
from src.models.repositories.answers_repository import AnswersRepository

# SERVICES
from src.services.get_answers_by_student_id import GetAnswersByStudentId

# CONTROLLERS
from src.controllers.get_answers_by_student_id_controller import GetAnswersByStudentIdController


def get_answers_by_student_id_composer() -> GetAnswersByStudentIdController:
    """Composer para criar o controller de obtenção de respostas por ID do estudante.
    
    Returns:
        controller (GetAnswersByStudentIdController): Instância do controller configurado.
    """
    
    model = AnswersRepository(pg_connection_handler)
    service = GetAnswersByStudentId(model)
    controller = GetAnswersByStudentIdController(service)
    return controller
