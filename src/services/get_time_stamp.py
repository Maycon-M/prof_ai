from datetime import datetime

class GetTimeStamp:
    """Classe responsável por obter o timestamp atual."""
    
    @staticmethod
    def get_current_time_stamp() -> str:
        """Obtém o timestamp atual no formato 'YYYY-MM-DD HH:MM:SS'."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
