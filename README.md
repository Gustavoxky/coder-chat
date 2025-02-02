huggingface-cli login


# Chatbot dev

Este projeto é um chatbot desenvolvido para auxiliar programadores em perguntas sobre código, fornecendo sugestões e explicações utilizando o modelo **DeepSeek-Coder 6.7B**. O frontend foi criado com **Streamlit** e o backend com **FastAPI**.

## 📌 Funcionalidades
- Interface interativa para conversar sobre programação
- Suporte a múltiplas linguagens de código (Python, JavaScript, C++, SQL, etc.)
- Respostas geradas por IA com ajuste de temperatura e comprimento
- Destacamento de código para melhor visualização
- Otimização para rodar em GPUs como a **RTX 4050**

---

## 🚀 Tecnologias Utilizadas
- **Streamlit** (Interface gráfica)
- **FastAPI** (Backend da API)
- **Transformers** (Modelo DeepSeek-Coder 6.7B)
- **PyTorch** (Execução do modelo na GPU/CPU)
- **Requests** (Comunicação entre frontend e backend)

---

## 🛠️ Configuração e Execução

### 1️⃣ Clonar o repositório
```sh
  git clone https://github.com/seu-usuario/chatbot-programacao.git
  cd chatbot-programacao
```

### 2️⃣ Criar e ativar um ambiente virtual (opcional, mas recomendado)
```sh
  python -m venv venv
  source venv/bin/activate  # Linux/macOS
  venv\Scripts\activate  # Windows
```

### 3️⃣ Instalar dependências
```sh
  pip install -r requirements.txt
```

### 4️⃣ Configurar variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto e adicione:
```sh
HF_AUTH_TOKEN=seu_token_huggingface
```

Faça login no huggingface com o seu token: 
```sh
huggingface-cli login
```

### 5️⃣ Iniciar o backend (FastAPI)
```sh
 uvicorn api:app --reload
```

### 6️⃣ Iniciar o frontend (Streamlit)
```sh
  streamlit run frontend/streamlit_app.py

```

---

## 🔧 Ajustes e Configurações
### ⚙️ Parâmetros disponíveis no frontend (Sidebar)
- **Comprimento máximo da resposta**: Define quantos tokens a IA pode gerar.
- **Temperatura**: Controla a criatividade das respostas (valores mais baixos geram respostas mais determinísticas).
- **Botão de limpar conversa**: Apaga o histórico de mensagens.

---

## 📌 Estrutura do Projeto
```
chatbot-programacao/
│── app/
│   ├── chatbot.py  # Lógica do modelo AI (DeepSeek-Coder)
│   ├── main.py     # API FastAPI
│── frontend/
│   ├── app.py      # Interface Streamlit
│── requirements.txt  # Dependências do projeto
│── .env.example  # Exemplo do arquivo .env
│── README.md  # Documentação do projeto
```

---

## 🏗️ Futuras Melhorias
- Adicionar suporte a múltiplos modelos de IA
- Melhorar a exibição das mensagens no frontend
- Implementar autenticação para controle de acesso

---

## 📜 Licença
Este projeto é distribuído sob a **MIT License**.

## 🤝 Contribuição
Sinta-se à vontade para abrir issues e pull requests!

---

### 🎯 Criado por: [Seu Nome]

