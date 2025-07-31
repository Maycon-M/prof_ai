# MODELS
from src.models.settings.postegres_connection import pg_connection_handler
from src.models.repositories.answers_repository import AnswersRepository

# SERVICE
from src.services.create_answers import CreateAnswers

# CONTROLLER
from src.controllers.create_answers_controller import CreateAnswersController

def create_answers_composer() -> CreateAnswersController:
    """Composer para criar o controller de respostas."""
    model = AnswersRepository(pg_connection_handler)
    service = CreateAnswers(model)
    controller = CreateAnswersController(service)
    return controller
