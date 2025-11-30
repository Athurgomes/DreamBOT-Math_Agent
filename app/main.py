from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from app.agent import create_agent

#Carrega variáveis do arquivo .env para rodar localmente
from dotenv import load_dotenv
load_dotenv()
#Iniciar a api e poder acessar o swagger (documentação automatica)
app = FastAPI(title="API AGENTE IA")

#Pydantic, tanto no request do usuario quanto no responde do agente de ia
#validamos os dados da API, sé é string
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

#Endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        #Instancia o agente sempre que é emetido um request, isso garante que o 
        #prompt e a ferramenta estejam sempre configurados da forma correta
        agent = create_agent()
        #O Strands agente orquestra a chamada ao llm e então decide se usa ou não a tool
        response_text = agent(request.message)
        return ChatResponse(response=str(response_text))
    #Tratamento de erro apenas para não quebrar o cliente
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Verificação para o Docker, queremos saber se o backend está pronto
@app.get("/health")
def health():
    return {"status": "ok"}