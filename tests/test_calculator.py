import pytest

from app.tools.calculator import calculator_tool


@pytest.mark.parametrize(
    "expressao, esperado",
    [
        ("1234 * 5678", "7006652"),
        ("sqrt(144)", "12.0"),
        ("33 / 11", "3.0"),
        ("2 ** 10", "1024"),
        ("pi * 2", "6.283185307179586"),
    ],
)
def test_calcula_expressoes_validas(expressao, esperado):
    assert calculator_tool(expressao) == esperado


@pytest.mark.parametrize(
    "expressao",
    [
        "__import__('os').system('ls')",  # tentativa de injeção de código
        "open('/etc/passwd').read()",
        "2 ** 10000000",  # potência gigante bloqueada pelo simpleeval
        "1 / 0",
    ],
)
def test_bloqueia_expressoes_perigosas_ou_invalidas(expressao):
    assert calculator_tool(expressao).startswith("Erro ao calcular")
