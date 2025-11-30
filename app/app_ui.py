import streamlit as st
import requests
import os 

#Config da página, apenas o titulo e um icone
st.set_page_config(page_title="DreamBOT", page_icon="☁️")
st.title("☁️ DreamBOT")
st.caption("Agente inteligente com capacidade matemática")

#Mantém um historico das mensagens já enviadas, mas não tem persistencia, se reiniciar a aba ele apaga
if "messages" not in st.session_state:
    st.session_state["messages"] = []

#Carrega o historico de mensagens na tela (renderização)
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

#Lê a entrada do usuario
if prompt := st.chat_input("Peça ao DreamBOT"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    #Chama a API no backend
    try:
        #Busca a url da api de forma dinamica no .env (bom para alternar entre local e docker)
        api_base_url = os.getenv("API_URL")
        response = requests.post(f"{api_base_url}/chat", json={"message": prompt})     
        if response.status_code == 200:
            ai_response = response.json().get("response", "Erro na resposta.")
        else:
            ai_response = f"Erro na API: {response.status_code}"
    except Exception as e:
        ai_response = f"Erro de conexão: {e}"
    #Mostra e salva a resposta do agente
    st.session_state["messages"].append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(ai_response)