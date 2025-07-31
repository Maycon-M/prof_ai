# MODEL
from src.models.settings.postegres_connection import pg_connection_handler
from src.models.repositories.exams_repository import ExamsRepository

# SERVICE
from src.services.create_exam import CreateExam

# CONTROLLER
from src.controllers.create_exam_controller import CreateExamController

def create_exam_composer ():
    model = ExamsRepository(pg_connection_handler)
    service = CreateExam(model)
    controller = CreateExamController(service)
    
    return controller
