# MODELS
from src.models.settings.postegres_connection import pg_connection_handler
from src.models.repositories.questions_repository import QuestionsRepository

# SERVICES
from src.services.create_questions import CreateQuestionsService

# CONTROLLERS
from src.controllers.create_questions_controller import CreateQuestionsController

def create_questions_composer() -> CreateQuestionsController:
    model = QuestionsRepository(pg_connection_handler)
    service = CreateQuestionsService(model)
    controller = CreateQuestionsController(service)
    return controller
