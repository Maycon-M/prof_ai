import sys
import logging

def setup_logging():
    """
    Configura o logger para registrar mensagens em um arquivo rotativo.
    """
    
    logger = logging.getLogger("uvicorn")
    
    logger.setLevel(logging.INFO)
    
    log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    # filtra só registros abaixo de ERROR
    stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)
    stdout_handler.setFormatter(log_format)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(log_format)

    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)
    
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("uvicorn.error").setLevel(logging.ERROR)
    
    
    return logger


LOGGER = setup_logging()