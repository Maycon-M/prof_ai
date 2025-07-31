# MODELS
from src.models.settings.postegres_connection import pg_connection_handler
from src.models.repositories.students_repository import StudentsRepository

# SERVICE
from src.services.create_student import CreateStudent

# CONTROLLER
from src.controllers.create_student_controller import CreateStudentController

def create_student_composer() -> CreateStudentController:
    """Factory function to create an instance of CreateStudentController.
    Returns:
        CreateStudentController: An instance of CreateStudentController.
    """
        
    model = StudentsRepository(pg_connection_handler)
    service = CreateStudent(model)
    controller = CreateStudentController(service)
    return controller
