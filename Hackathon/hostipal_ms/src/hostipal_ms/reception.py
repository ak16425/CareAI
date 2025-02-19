#!/usr/bin/env python
import streamlit as st
import pandas as pd
import datetime
import warnings
import json
import sys
import os
import io
from crew import HostipalMs

def show_reception_form():

    if "patient_data" not in st.session_state:
        st.session_state.patient_data = None
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False
    if "kickoff_clicked" not in st.session_state:
        st.session_state.kickoff_clicked = False    
    

    if not st.session_state.kickoff_clicked:
        st.header("Enter Patient Details")
        with st.form("patient_form"):
            name = st.text_input("Patient Name", value=st.session_state.get("name", ""))
            age = st.number_input("Age", min_value=0, max_value=120, step=1, value=st.session_state.get("age", 0))
            gender = st.selectbox("Gender", ("Male", "Female", "Other"), index=None, placeholder="Choose an option")
            date_of_visit = st.date_input("Date of Visit", st.session_state.get("date_of_visit", datetime.date.today()))
            date_of_visit_str = date_of_visit.strftime("%Y-%m-%d") 
            symptoms = st.text_area("Symptoms", value=st.session_state.get("symptoms", ""))
            contact_number = st.text_input("Contact Number", value=st.session_state.get("contact_number", ""))

            submitted = st.form_submit_button("Submit")

        if submitted:
            st.session_state.patient_data = {
                "Name": name,
                "Age": age,
                "Gender": gender,
                "Date of Visit": date_of_visit_str,
                "Symptoms": symptoms,
                "Contact Number": contact_number,
            }
            st.session_state.form_submitted = True
            st.rerun()

        if st.session_state.form_submitted:
            st.success("Patient details submitted successfully!")
            if st.button("Search Available Doctors", type="primary"):
                st.session_state.kickoff_clicked = True
                st.rerun()
                      
    else:
        with st.spinner("Loading Agents..."):
            
            def run(patient_data):
                """
                Run the crew.
                """
                inputs = {
                    'patient_data': patient_data,
                }
                results = HostipalMs().opd_crew().kickoff(inputs=inputs)
                return results
            
            if st.session_state.patient_data:
                patient_data = st.session_state.patient_data
                results = run(patient_data)
    
                st.markdown(results.raw)
               
            
                
            else:
                st.error("No patient data found. Please submit the form first.")

    
    

    
