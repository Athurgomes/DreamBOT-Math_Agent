from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import create_agent
from app.utils.detectors import is_math_expression
from app.tools.calculator import calculator_tool

app = FastAPI(title="API AGENTE IA")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    agent = create_agent()

    if is_math_expression(request.message):
        result = calculator_tool(request.message)
        return ChatResponse(response=result)

    response = agent(request.message)
    return ChatResponse(response=str(response))

@app.get("/health")
def health():
    return {"status": "ok"}