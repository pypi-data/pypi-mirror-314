import argparse
import importlib
import logging
import sys
import warnings

from dotenv import load

try:
    if not load('.env'):
        raise Exception("Não localizou variáveis de ambiente")
except:
    warnings.warn(
        "Não foi possível carregar as variáveis de ambiente através. Não esqueça de carregá-las antes de executar a aplicação",
        ImportWarning
    )

from .library.notification import (
    MailNotification as MAIL
)

# Configuração básica do logging
logging.basicConfig(
    level=logging.DEBUG,  # Define o nível mínimo de log a ser registrado (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Define o formato da mensagem de log
    datefmt='%Y-%m-%d %H:%M:%S',  # Define o formato da data/hora
    handlers=[
        #logging.FileHandler('app.log'),  # Registra as mensagens de log em um arquivo
        logging.StreamHandler()  # Registra as mensagens de log no console
    ]
)

logger = logging.getLogger(__name__)

class PipelineArgument:
    
    def __init__(self):
        self.pipeline = []
        self.company = ""
        self.load_full = "N"

def run_pipeline(**kwargs):
    """
    Executar o pipeline
    """
    arguments = kwargs.get("arguments")
    pipelines : list = arguments.pipeline
    company : str = arguments.company
    load_full = (arguments.load_full == "S" or arguments.load_full == "Y") if not arguments.load_full is None else False

    if pipelines is None or len(pipelines) == 0:
        raise Exception("Parameter pipeline is required")

    error_list = []

    for pipeline in pipelines:
        
        module_name = f".pipes.{company}.etl_{pipeline}"
        
        logger.debug(f"Loading module {module_name} ...")

        module = importlib.import_module(module_name, package="pronexus")
        
        if "run_pipeline" not in dir(module):
            raise Exception("Method run_pipeline not found")
        
        module_arguments = { "pipeline": pipeline, "companies": company, "load_full": load_full, "logger": logger }

        execution_with_error = False

        try:
            logger.debug(f"Running {pipeline} ...")
            module.run_pipeline(**module_arguments)

        except Exception as error:
            execution_with_error = True
            error_list.append({ "pipeline": pipeline, "error": error })
        
        finally:
            if execution_with_error:
                logger.debug(f"Finished {pipeline} with error!")
            else:
                logger.debug(f"Finished {pipeline} successful!")

    if len(error_list) > 0:
        raise Exception(error_list)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Executar o pipeline')
    parser.add_argument('-pipeline', required=True, nargs='+', type=str, help='Nome do pipeline')
    parser.add_argument('-company', required=True, type=str, help="Nome do cliente Bonanza")
    parser.add_argument('-load_full', required=False, type=str, default="N", help="Carga completa S=Sim ou N=Não")
    arguments = parser.parse_args()

    try:
        logger.debug(f"Starting pipeline(s): {arguments}")
        run_pipeline(arguments=arguments)
        sys.exit(0)

    except Exception as error:
        logger.error(f"Error in pipeline {error}")

        try:
            logger.debug(f"Sending notification ...")
            MAIL.send_mail(
                f"Failed run_pipeline {arguments}",
                f"Failed details: {error}"
            )

        except Exception as mail_error:
            logger.error(f"Error sending notification {mail_error}")

        sys.exit(1)

    finally:
        logger.debug(f"Finished all pipeline(s)!")
