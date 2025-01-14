import streamlit as st

if "messages" not in st.session_state:
    st.session_state["messages"] = []


def paint_history():
    for message in st.session_state["messages"]:
        send_message(message["message"], message["role"], False)

def save_message(message, role):
    st.session_state["messages"].append({"message" : message, "role" : role})

def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
        if save:
            save_message(message, role)

def clear_session_message():
    st.session_state["messages"] = []