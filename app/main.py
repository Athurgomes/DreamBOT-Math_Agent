import logging

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

#Carrega variáveis do arquivo .env antes de qualquer configuração do agente
load_dotenv()

from app.agent import create_agent  # noqa: E402

logger = logging.getLogger(__name__)

#Iniciar a api e poder acessar o swagger (documentação automatica)
app = FastAPI(title="API AGENTE IA")


#Pydantic, tanto no request do usuario quanto no response do agente de ia
#validamos os dados da API: mensagem precisa ser texto não vazio e de tamanho razoável
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    response: str


#Endpoint
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        #Instancia o agente sempre que é emitido um request, isso garante que o
        #prompt e a ferramenta estejam sempre configurados da forma correta
        agent = create_agent()
        #O Strands agente orquestra a chamada ao llm e então decide se usa ou não a tool
        response_text = agent(request.message)
        return ChatResponse(response=str(response_text).strip())
    #Loga o erro completo no servidor, mas não expõe detalhes internos ao cliente
    except Exception as e:
        logger.exception("Falha ao processar a mensagem")
        raise HTTPException(status_code=503, detail="Agente indisponível no momento.") from e


#Verificação para o Docker, queremos saber se o backend está pronto
@app.get("/health")
def health():
    return {"status": "ok"}
