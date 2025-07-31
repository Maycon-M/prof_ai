# MODELS
from src.models.settings.postegres_connection import pg_connection_handler
from src.models.repositories.teachers_repository import TeachersRepository

# SERVICE
from src.services.create_teacher import CreateTeacher

# CONTROLLER
from src.controllers.create_teacher_controller import CreateTeacherController

def create_teacher_composer() -> CreateTeacherController:
    """Compositor para criar o controller de criação de professores.
    
    Retorna:
        controller (CreateTeacherController): Instância do controller configurado.
    """
    model = TeachersRepository(db_conn_handler=pg_connection_handler)
    service = CreateTeacher(teachers_repository=model)
    controller = CreateTeacherController(create_teacher_service=service)

    return controller
