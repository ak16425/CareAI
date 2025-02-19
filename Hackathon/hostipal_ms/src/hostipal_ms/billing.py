import streamlit as st
import pandas as pd
import datetime
import warnings
import json
import sys
import os
import io
from crew import HostipalMs

def show_billing():
    
    st.header("Billing ")
    
    if "patient_data" not in st.session_state:
        st.session_state.patient_data = None
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False
        
    if not st.session_state.form_submitted:
        with st.form("patient_form"):
            patient_id = st.text_input("Patient ID", value=st.session_state.get("patient_id", ""))
            date_of_admission = st.text_input("Date of Admission", value=st.session_state.get("date_of_admission", ""))
            
            submitted = st.form_submit_button("Generate Bill")
            
        if submitted:
            st.session_state.patient_data = {
                "PatientID": patient_id,
                "DOA": date_of_admission
            }
            st.session_state.form_submitted = True
            
        if st.session_state.form_submitted:
            with st.spinner("Loading Agents..."):
                def run(patient_data):
                    """
                    Run the crew.
                    """
                    inputs = {
                        'patient_data': patient_data,
                    }
                    results = HostipalMs().bill_crew().kickoff(inputs=inputs)
                    return results
                
                if st.session_state.patient_data:
                    patient_data = st.session_state.patient_data
                    results = run(patient_data)
        
                    st.markdown(results.raw)
                