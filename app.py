import streamlit as st
import pandas as pd
import joblib
import numpy as np

st.title("Loan Application")

no_of_dependents = st.number_input("Enter No.of Dependentes", min_value=0, step=1)
education = st.selectbox("Education", ["Graduate", "Not Graduate"])
self_employed = st.selectbox("Self Employed", ["Yes", "No"])
income_annum = st.number_input("Enter Income Annual", min_value=0)
loan_amount = st.number_input("Enter Loan Amount", min_value=1)
loan_term = st.number_input("Enter Loan Term", min_value=1)
credit_score = st.number_input("Enter Credit Score", min_value=300, max_value=900)
total_asset = st.number_input("Enter Total Asset Value", min_value=0)   # FIXED name

if st.button("Apply Loan"):
    dataset = {
        "no_of_dependents": no_of_dependents,
        "education": 0 if education == "Graduate" else 1,
        "self_employed": 0 if self_employed == "No" else 1,
        "income_annum": np.log(income_annum),
        "loan_amount": np.log(loan_amount),
        "loan_term": loan_term,
        "credit_score": credit_score,
        "total_asset": np.log(total_asset),   # FIXED name
    }

    df = pd.DataFrame([dataset])

    my_model = joblib.load("model.pkl")
    y_predict = my_model.predict(df)

    st.write("Loan Status:", "Approved" if y_predict == 1 else "Rejected")
