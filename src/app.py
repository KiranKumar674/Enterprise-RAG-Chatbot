
import streamlit as st

from rag_pipeline import answer_question


st.set_page_config(
    page_title="Enterprise RAG Chatbot",
    page_icon="💬",
    layout="centered",
)

st.title("Enterprise RAG Chatbot")
st.caption("Ask questions about company policies.")

# Development-only role selector; not production authentication.
role = st.selectbox(
    "Select a test role",
    options=["general", "hr", "finance"],
    format_func=lambda value: {
        "general": "General Employee",
        "hr": "HR Employee",
        "finance": "Finance Employee",
    }[value],
)

# Keep conversation history separate for each selected role.
if "messages" not in st.session_state:
    st.session_state.messages = {}

role_messages = st.session_state.messages.setdefault(role, [])

for message in role_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Ask about company policies..."):
    role_messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching permitted company documents..."):
            try:
                answer = answer_question(question, role)
                st.markdown(answer)
            except Exception as error:
                st.error("Sorry, I couldn't process your question.")
                print(f"RAG error: {error}")
                answer = "Sorry, I couldn't process your question."

    role_messages.append({"role": "assistant", "content": answer})
