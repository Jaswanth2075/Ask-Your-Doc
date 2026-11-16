import streamlit as st

st.title("Ask Your Doc")

uploaded_files = st.file_uploader(
    "Upload your Document",
    type = ["pdf","txt","xlsx","xls"],
    accept_multiple_files= True

)

if uploaded_files:
    st.success("Documents uploaded")