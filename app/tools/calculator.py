import math
import logging
from simpleeval import SimpleEval
from strands import tool

#Monitoramente da tool 
logger = logging.getLogger(__name__)

@tool
def calculator_tool(expression: str) -> str:
    """
    Calcula expressões matemáticas.
    """
    #Remoção dos espaços da entrada
    expression = expression.replace(" ", "")
    logger.info(f"Calculando: {expression}")

    try:
        #Criação do avaliador seguro, evitar injenção de código malicioso
        evaluator = SimpleEval()

        #Carrega dinamicamente todas as funções da biblioteca 'math'
        #permitindo calculos complexos sem risco de segurança.
        math_funcs = {name: getattr(math, name) for name in dir(math) if not name.startswith("__")}
        evaluator.functions.update(math_funcs)

        #Executa o calculo
        result = evaluator.eval(expression)
        return str(result)
    except Exception as e:
        logger.error(f"Erro no cálculo: {e}")
        return f"Erro ao calcular: {str(e)}"