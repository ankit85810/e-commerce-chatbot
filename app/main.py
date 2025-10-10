import streamlit as st
from router import router
from faq import ingest_faq_data, faq_chain
from pathlib import Path
from sql import sql_chain
from chit_chat import generate_answer

faqs_path = Path(__file__).parent / "resources" / "faq_data.csv"
ingest_faq_data(faqs_path)

def ask(query: str) -> str:
    route = router(query).name
    if route == 'faq':
        return faq_chain(query)
    elif route == 'sql':
        return sql_chain(query)
    elif route == 'chit_chat':
        return generate_answer(query)
    else:
        return "This route is not implemented yet.(only shoes and faq related queries are supported now :))"

st.title("E -commerce Chatbot")

st.write("Welcome to the E-commerce Chatbot! How can I assist you today?")

query = st.chat_input("Type your message here...")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

for message in st.session_state['messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"]) 

if query:
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state['messages'].append({"role": "user", "content": query})

    response = ask(query)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state['messages'].append({"role": "assistant", "content": response})
