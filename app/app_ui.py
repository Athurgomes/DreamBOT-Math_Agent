import streamlit as st
import requests
import os 

st.set_page_config(page_title="DreamBOT - Teste Técnico", page_icon="☁️")
st.title("☁️ DreamBOT")
st.caption("Agente inteligente com capacidade matemática")

if "messages" not in st.session_state:
    st.session_state["messages"] = []
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
if prompt := st.chat_input("Peça ao DreamBOT"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    try:
        api_base_url = os.getenv("API_URL")
        response = requests.post(f"{api_base_url}/chat", json={"message": prompt})     
        if response.status_code == 200:
            ai_response = response.json().get("response", "Erro na resposta.")
        else:
            ai_response = f"Erro na API: {response.status_code}"
    except Exception as e:
        ai_response = f"Erro de conexão: {e}"
    st.session_state["messages"].append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(ai_response)