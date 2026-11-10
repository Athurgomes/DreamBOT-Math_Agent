from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_chat_retorna_resposta_do_agente():
    with patch("app.main.create_agent") as fabrica:
        fabrica.return_value = lambda mensagem: f"  eco: {mensagem}\n"
        resp = client.post("/chat", json={"message": "Olá"})

    assert resp.status_code == 200
    assert resp.json() == {"response": "eco: Olá"}


def test_chat_rejeita_mensagem_vazia():
    assert client.post("/chat", json={"message": ""}).status_code == 422


def test_chat_nao_expoe_erro_interno():
    def agente_quebrado(_):
        raise RuntimeError("segredo interno: conexão com ollama recusada")

    with patch("app.main.create_agent", return_value=agente_quebrado):
        resp = client.post("/chat", json={"message": "Oi"})

    assert resp.status_code == 503
    assert "segredo" not in resp.text
