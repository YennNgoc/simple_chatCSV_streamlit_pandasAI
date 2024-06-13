import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
import matplotlib.pyplot as plt
import os
# from pandasai.llm.local_llm import LocalLLM 
# use openai token
from pandasai.llm import OpenAI

st.title("simple demo")

### for keep history
# st.session_state.openai_key = ""
# st.session_state.prompt_history = []

### for keep state on imported dataframe
st.session_state.df = None


# if "openai_key" in st.session_state:
if st.session_state.df is None:
    uploaded_file = st.file_uploader(
        "Choose a valid CSV file",
        type="csv",
    )
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df

    if st.session_state.df is not None:
        st.subheader("Current dataframe:")
        st.write(st.session_state.df)

    with st.form("Question"):
        question = st.text_input("Question", value="", type="default")
        submitted = st.form_submit_button("Submit")
        if submitted:
            with st.spinner():
                ### use local LLM
                # ollama_llm = LocalLLM(api_base="http://localhost:11434/v1", model="llama3:8b")
                # pandas_ai = SmartDataframe(st.session_state.df, config={"llm": ollama_llm, "save_charts": True})

                ### openAI key
                llm = OpenAI(api_token="api_key_here")
                pandas_ai = SmartDataframe(st.session_state.df, config={"llm": llm, "save_charts": True})

                x = pandas_ai.chat(question)
                print(x)
               
                # check output path is file
                if type(x) == str and os.path.isfile(x):
                    im = plt.imread(x)
                    st.image(im)
                    os.remove(x)
                else:
                    st.write(x)

                ### keep history
                # st.session_state.prompt_history.append(question)


if st.button("Clear"):
    st.session_state.df = None
