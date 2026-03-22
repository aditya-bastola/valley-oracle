import streamlit as st
from rag import chain

st.set_page_config(page_title="ValleyOracle", page_icon="⛰️")
st.title("ValleyOracle")
st.caption("Startup advice grounded in Paul Graham's essays.")

if "messages" not in st.session_state:
    st.session_state.messages = []


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask a startup question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(chain.stream(prompt))

    st.session_state.messages.append({"role": "assistant", "content": response})



    