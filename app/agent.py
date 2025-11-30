import os
from strands import Agent
from strands.models.ollama import OllamaModel
from app.tools.calculator import calculator_tool

#Leitura do prompt na pasta de prompts externa, para facilidar o controle de versões
def load_system_prompt():
    path = os.path.join(os.path.dirname(__file__), "prompts/system_prompt.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

#Criação e configuração de uma nova instancia do agente
def create_agent():
    system_prompt = load_system_prompt()
    
    #A conexão com o ollama é feita usando o .env, podendo alternar entre local ou docker
    model = OllamaModel(
        host=os.getenv("OLLAMA_HOST"),
        model_id=os.getenv("OLLAMA_MODEL")
    )

    #Retorna o agente configurado com a tool de calcular
    return Agent(
        model=model,
        tools=[calculator_tool],
        system_prompt=system_prompt,
    )