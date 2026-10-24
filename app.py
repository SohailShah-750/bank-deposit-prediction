
import streamlit as st
import pandas as pd
import joblib

model = joblib.load("bank_model.pkl")

st.title("Bank Deposit Prediction")
st.write("Enter customer details to predict whether they may subscribe to a deposit.")

age = st.number_input("Age", min_value=18, max_value=100, value=35)
job = st.selectbox("Job", [
    "admin.", "blue-collar", "entrepreneur", "housemaid",
    "management", "retired", "self-employed", "services",
    "student", "technician", "unemployed", "unknown"
])
marital = st.selectbox("Marital Status", ["married", "single", "divorced"])
education = st.selectbox("Education", [
    "primary", "secondary", "tertiary", "unknown"
])
default = st.selectbox("Credit Default", ["no", "yes"])
balance = st.number_input("Account Balance", value=1000)
housing = st.selectbox("Housing Loan", ["no", "yes"])
loan = st.selectbox("Personal Loan", ["no", "yes"])
contact = st.selectbox("Contact Type", ["cellular", "telephone", "unknown"])
day = st.number_input("Contact Day", min_value=1, max_value=31, value=15)
month = st.selectbox("Contact Month", [
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec"
])
duration = st.number_input("Call Duration (seconds)", min_value=0, value=150)
campaign = st.number_input("Contacts This Campaign", min_value=1, value=1)
pdays = st.number_input("Days Since Previous Contact (-1 if never)", value=-1)
previous = st.number_input("Previous Contacts", min_value=0, value=0)
poutcome = st.selectbox("Previous Campaign Outcome", [
    "unknown", "other", "failure", "success"
])

if st.button("Predict"):
    customer = pd.DataFrame([{
        "age": age,
        "job": job,
        "marital": marital,
        "education": education,
        "default": default,
        "balance": balance,
        "housing": housing,
        "loan": loan,
        "contact": contact,
        "day": day,
        "month": month,
        "duration": duration,
        "campaign": campaign,
        "pdays": pdays,
        "previous": previous,
        "poutcome": poutcome
    }])

    prediction = model.predict(customer)[0]
    st.subheader(f"Prediction: {prediction}")
