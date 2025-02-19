import streamlit as st
import pandas as pd
import datetime
import warnings
import json
import sys
import os
import io
from crew import HostipalMs
from PyPDF2 import PdfReader

def show_admission_page():
    # Initialize session state
    if "dr_prescription" not in st.session_state:
        st.session_state.dr_prescription = ""

    st.header("Patient Admission")

    # File uploader (only accepts PDF)
    uploaded_file = st.file_uploader("Upload your Prescription here", type=["pdf"])

    if uploaded_file is not None:
        pdf_reader = PdfReader(uploaded_file)
        extracted_text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        
        st.session_state.dr_prescription = extracted_text
        
        st.subheader("Extracted Prescription Content:")
        st.text_area("Doctor's Prescription", value=st.session_state.dr_prescription, height=300)

        # CrewAI Integration
        if st.button("Admit Patient", type="primary"):
            with st.spinner("Loading Agents..."):
                inputs = {'dr_prescription': st.session_state.dr_prescription}
                results = HostipalMs().admit_crew().kickoff(inputs=inputs)
                st.markdown(results.raw)
        
            
            
    
    
    