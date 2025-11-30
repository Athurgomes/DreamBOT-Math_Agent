import math
import logging
from simpleeval import SimpleEval
from strands import tool

logger = logging.getLogger(__name__)

@tool
def calculator_tool(expression: str) -> str:
    """
    Calcula expressões matemáticas.
    """
    expression = expression.replace(" ", "")
    logger.info(f"Calculando: {expression}")

    try:
        evaluator = SimpleEval()
        math_funcs = {name: getattr(math, name) for name in dir(math) if not name.startswith("__")}
        evaluator.functions.update(math_funcs)
        result = evaluator.eval(expression)
        return str(result)
    except Exception as e:
        logger.error(f"Erro no cálculo: {e}")
        return f"Erro ao calcular: {str(e)}"