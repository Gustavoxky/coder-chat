import streamlit as st
import requests

# Configurações
API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="Chatbot com Mistral 7B", layout="wide")
st.title("Chatbot com Mistral 7B 🚀")

# Interface de conversa
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Formulário de entrada
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Digite sua mensagem:", "")
    max_length = st.slider("Comprimento máximo da resposta:", 64, 512, 128)
    temperature = st.slider("Temperatura (criatividade):", 0.1, 1.0, 0.7)
    submit_button = st.form_submit_button("Enviar")

# Lidar com envio
if submit_button and user_input.strip():
    try:
        # Requisição para o backend
        response = requests.post(
            API_URL,
            json={
                "prompt": user_input,
                "max_length": max_length,
                "temperature": temperature,
            },
        )
        response.raise_for_status()
        bot_response = response.json().get("response", "Erro ao processar a resposta.")

        # Atualizar o histórico
        st.session_state["messages"].append(("Você", user_input))
        st.session_state["messages"].append(("Chatbot", bot_response))
    except requests.RequestException as e:
        st.error(f"Erro ao conectar ao backend: {e}")
else:
    if not user_input.strip() and submit_button:
        st.warning("Por favor, insira uma mensagem antes de enviar.")

# Mostrar histórico de mensagens
for sender, message in st.session_state["messages"]:
    if sender == "Você":
        st.markdown(f"**{sender}:** {message}")
    else:
        st.markdown(f"**{sender}:** {message}")

# Informações adicionais
st.sidebar.title("Configurações")
st.sidebar.write("Configure os parâmetros do chatbot.")
st.sidebar.markdown("Criado com [Streamlit](https://streamlit.io) e Mistral 7B.")
