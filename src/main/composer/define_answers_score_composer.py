# MODELS
from src.models.settings.postegres_connection import pg_connection_handler
from src.models.repositories.answers_repository import AnswersRepository

# SERVICE
from src.services.define_answers_score import DefineAnswersScore

# CONTROLLER
from src.controllers.define_answers_score_controller import DefineAnswersScoreController

def define_answers_score_composer() -> DefineAnswersScoreController:
    """Compositor para criar o controller de definição de pontuação de respostas.
    
    Returns:
        controller (DefineAnswersScoreController): Instância do controller configurado.
    """
    
    model = AnswersRepository(pg_connection_handler)
    service = DefineAnswersScore(model)
    controller = DefineAnswersScoreController(service)
    
    return controller
