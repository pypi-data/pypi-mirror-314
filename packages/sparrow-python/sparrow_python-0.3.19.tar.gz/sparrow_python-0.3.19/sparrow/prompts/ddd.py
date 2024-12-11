import streamlit as st

from file_chat_input import file_chat_input
from streamlit_float import float_init


# float_init()

st.write("laskdjf")
st.sidebar.write("laskdjf")
container = st.container()
with container:
    message = file_chat_input("Type a message...")
    print(f"{type(message)}")
    print(message)

if message:
    st.write(message)


# container.float("bottom: 0")