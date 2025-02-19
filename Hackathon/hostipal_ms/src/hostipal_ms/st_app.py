import streamlit as st
import pandas as pd
import datetime

# Title of the app


# Initialize session state if not set
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Apply custom CSS for better button styling

# Home Page Content
if st.session_state.page == "Home":
    st.markdown(
        """
        <style>
        div.stButton > button {
            margin-top: 2rem;
            width: 220px;
            height: 220px;
            font-size: 30px !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            transition: 0.3s;
            color: #054ADA
        }
        div.stButton > button:hover {
            background-color: #054ADA !important; 
            color: white;
            font-weight: bold !important;
            
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<h1 style='text-align: center; font-size: 50px; color: #054ADA;'>Welcome to CareAI </h1>",unsafe_allow_html=True )

    # Add some spacing
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Create three columns for navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("OPD Consultation"):
            st.session_state.page = "OPD"
            st.rerun()

    with col2:
        if st.button("Patient Admission"):
            st.session_state.page = "Admission"
            st.rerun()

    with col3:
        if st.button("Billing"):
            st.session_state.page = "Billing"
            st.rerun()


# Import reception.py dynamically after clicking "OPD Consultation"
if st.session_state.page == "OPD":
    from reception import show_reception_form
    show_reception_form()  # Call function from reception.py

    
if st.session_state.page == "Admission":
    import admission
    # Call a function inside admission.py to ensure Streamlit updates only the UI
    admission.show_admission_page()
    
if st.session_state.page == "Billing":
    import billing
    # Call a function inside admission.py to ensure Streamlit updates only the UI
    billing.show_billing()
    
    


