from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from app.agent import create_agent

#Carrega variáveis do arquivo .env para rodar localmente
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="API AGENTE IA")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        agent = create_agent()
        response_text = agent(request.message)
        return ChatResponse(response=str(response_text))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}