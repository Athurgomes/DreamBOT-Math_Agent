import os
from strands import Agent
from strands.models.ollama import OllamaModel
from app.tools.calculator import calculator_tool

def load_system_prompt():
    path = os.path.join(os.path.dirname(__file__), "prompts/system_prompt.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def create_agent():
    system_prompt = load_system_prompt()
    
    model = OllamaModel(
        host=os.getenv("OLLAMA_HOST"),
        model_id=os.getenv("OLLAMA_MODEL")
    )

    return Agent(
        model=model,
        tools=[calculator_tool],
        system_prompt=system_prompt,
    )