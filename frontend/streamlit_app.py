import streamlit as st
import requests

# Configuração da API
API_URL = "http://127.0.0.1:8000/chat"

# Configuração do Streamlit
st.set_page_config(page_title="Chatbot dev", layout="wide")

st.title("Chatbot dev")

# Inicializa o histórico de mensagens corretamente
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Sidebar - Configurações
st.sidebar.title("⚙️ Configurações")
max_length = st.sidebar.slider("Comprimento máximo da resposta:", 64, 8192, 4096)
temperature = st.sidebar.slider("Temperatura (criatividade):", 0.1, 1.0, 0.7)

# Botão para limpar a conversa
if st.sidebar.button("🗑 Limpar Conversa"):
    st.session_state["messages"] = []
    st.experimental_rerun()

# Função para detectar a linguagem do código
def detect_language(code):
    if "def " in code or "import " in code or "print(" in code:
        return "python"
    elif "function " in code or "console.log(" in code:
        return "javascript"
    elif "#include" in code or "int main()" in code:
        return "cpp"
    elif "SELECT " in code.upper() or "FROM " in code.upper():
        return "sql"
    else:
        return "plaintext"

# Exibir o histórico de mensagens
chat_container = st.container()
with chat_container:
    for message in st.session_state["messages"]:
        role = message["role"]
        content = message["content"]

        with st.container():
            st.markdown('<div class="chat-bubble">', unsafe_allow_html=True)
            if role == "Chatbot":
                language = detect_language(content)
                st.code(content, language=language)  # Exibe código corretamente
            else:
                st.markdown(f"<b>{role}:</b> {content}", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# Entrada do usuário
user_input = st.chat_input("Digite seu código ou pergunta sobre programação...")

if user_input:
    # Adiciona a mensagem do usuário ao histórico corretamente
    st.session_state["messages"].append({"role": "Você", "content": user_input})

    # Exibir a mensagem do usuário instantaneamente
    with st.container():
        st.markdown('<div class="chat-bubble">', unsafe_allow_html=True)
        st.markdown(f"<b>Você:</b> {user_input}", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Indicador de carregamento
    with st.spinner("Pensando..."):
        try:
            response = requests.post(
                API_URL,
                json={"prompt": user_input, "max_length": max_length, "temperature": temperature},
                timeout=300,
            )
            response.raise_for_status()
            bot_response = response.json().get("response", "Erro ao processar a resposta.")
        except requests.RequestException as e:
            bot_response = f"Erro ao conectar ao backend: {e}"

    # Adicionar resposta do chatbot ao histórico
    st.session_state["messages"].append({"role": "Chatbot", "content": bot_response})

    # Exibir resposta do chatbot com código destacado
    with st.container():
        st.markdown('<div class="chat-bubble">', unsafe_allow_html=True)
        language = detect_language(bot_response)
        st.code(bot_response, language=language)  # Exibe código corretamente
        st.markdown('</div>', unsafe_allow_html=True)
