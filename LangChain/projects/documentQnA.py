# Application in user user can upload any pdf file and will able to query that document

import streamlit as st


pdf=st.sidebar.file_uploader("Upload PDF file:", type='pdf')