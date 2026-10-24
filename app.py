
import streamlit as st
import pandas as pd
import joblib



# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Bank AI | Deposit Prediction",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ---------------- GOOGLE LOGIN ----------------
if not st.user.is_logged_in:
    st.title("🏦 Bank Deposit Prediction")
    st.write("Please sign in with your Google account to continue.")

    if st.button("Login with Google"):
        st.login("google")

    st.stop()

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    return joblib.load("bank_model.pkl")

model = load_model()

# ---------------- DARK NAVY + TEAL DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #07111f 0%, #0b1929 100%);
    color: #e8f1fa;
}
.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
header[data-testid="stHeader"] {
    background: transparent;
}
h1, h2, h3, p, label, span {
    color: #e8f1fa;
}
.hero {
    background: linear-gradient(120deg, #10283b, #123c43);
    border: 1px solid #24535b;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 24px;
}
.hero-tag {
    color: #53e0c0;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
}
.hero-title {
    color: #ffffff;
    font-size: 34px;
    font-weight: 800;
    margin: 10px 0;
}
.hero-subtitle {
    color: #b7cbd9;
    font-size: 16px;
}
.section-card {
    background: #101f30;
    border: 1px solid #263b50;
    border-radius: 16px;
    padding: 20px;
    margin: 8px 0 18px 0;
}
.section-title {
    color: #56e2c1;
    font-size: 19px;
    font-weight: 700;
    margin-bottom: 6px;
}
div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background-color: #14283a;
}
div[data-testid="stNumberInput"] input {
    color: white;
}
div.stButton > button {
    background: linear-gradient(90deg, #14b8a6, #2dd4bf);
    color: #06201f;
    font-weight: 800;
    border: none;
    border-radius: 10px;
    padding: 13px 20px;
    min-height: 50px;
    width: 100%;
    transition: 0.2s;
}
div.stButton > button:hover {
    background: #5eead4;
    color: #06201f;
    border: none;
}
.result-card {
    background: #10283b;
    border: 1px solid #2b5367;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    margin-top: 18px;
}
.result-yes {
    color: #5eead4;
    font-size: 30px;
    font-weight: 800;
}
.result-no {
    color: #fbbf24;
    font-size: 30px;
    font-weight: 800;
}
.small-note {
    color: #9fb4c7;
    font-size: 13px;
}
hr {
    border-color: #263b50;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
    <div class="hero-tag">AI POWERED • MACHINE LEARNING</div>
    <div class="hero-title">🏦 Bank Deposit Intelligence</div>
    <div class="hero-subtitle">
        Predict whether a customer may subscribe to a term deposit.
        Enter customer information to generate a model prediction.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("## Customer Profile")
st.caption("Enter the customer details below, then run the prediction.")

# ---------------- INPUT FORM ----------------
with st.form("customer_form"):

    st.markdown("""
    <div class="section-card">
        <div class="section-title">👤 Personal Information</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        age = st.number_input(
            "Customer Age", min_value=18, max_value=100, value=35
        )
        job = st.selectbox("Job", [
            "admin.", "blue-collar", "entrepreneur", "housemaid",
            "management", "retired", "self-employed", "services",
            "student", "technician", "unemployed", "unknown"
        ])

    with c2:
        marital = st.selectbox(
            "Marital Status", ["married", "single", "divorced"]
        )
        education = st.selectbox(
            "Education", ["primary", "secondary", "tertiary", "unknown"]
        )

    with c3:
        default = st.selectbox("Credit Default", ["no", "yes"])
        balance = st.number_input(
            "Account Balance", value=1000, step=100
        )

    st.markdown("---")
    st.markdown("## 💳 Loans & Contact Details")

    c4, c5, c6 = st.columns(3)

    with c4:
        housing = st.selectbox("Housing Loan", ["no", "yes"])
        loan = st.selectbox("Personal Loan", ["no", "yes"])

    with c5:
        contact = st.selectbox(
            "Contact Type", ["cellular", "telephone", "unknown"]
        )
        day = st.number_input(
            "Last Contact Day", min_value=1, max_value=31, value=15
        )

    with c6:
        month = st.selectbox("Contact Month", [
            "jan", "feb", "mar", "apr", "may", "jun",
            "jul", "aug", "sep", "oct", "nov", "dec"
        ])
        duration = st.number_input(
            "Call Duration (seconds)", min_value=0, value=150
        )

    st.markdown("---")
    st.markdown("## 📊 Campaign History")

    c7, c8, c9 = st.columns(3)

    with c7:
        campaign = st.number_input(
            "Contacts This Campaign", min_value=1, value=1
        )

    with c8:
        pdays = st.number_input(
            "Days Since Previous Contact (-1 = never)",
            value=-1
        )

    with c9:
        previous = st.number_input(
            "Previous Contacts", min_value=0, value=0
        )

    poutcome = st.selectbox(
        "Previous Campaign Outcome",
        ["unknown", "other", "failure", "success"]
    )

    submitted = st.form_submit_button(
        "✨ Predict Deposit Subscription",
        use_container_width=True
    )

# ---------------- PREDICTION ----------------
if submitted:
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

    try:
        prediction = model.predict(customer)[0]

        st.markdown("---")
        st.markdown("## 🔎 Prediction Result")

        if str(prediction).lower() == "yes":
            st.markdown("""
            <div class="result-card">
                <div class="result-yes">✓ Likely to Subscribe: YES</div>
                <p class="small-note">
                    The model predicts that this customer may subscribe
                    to a term deposit.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-card">
                <div class="result-no">Predicted Subscription: NO</div>
                <p class="small-note">
                    The model predicts that this customer may not
                    subscribe to a term deposit.
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Optional model probability
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(customer)[0]
            classes = list(model.classes_)

            if "yes" in classes:
                yes_probability = probabilities[classes.index("yes")]

                st.markdown("### Model-estimated subscription probability")
                st.progress(float(yes_probability))
                st.metric(
                    "Estimated probability",
                    f"{yes_probability * 100:.1f}%"
                )

        st.caption(
            "This is a machine-learning estimate, not a guarantee. "
            "Call duration is known only after a call ends, so this "
            "feature may not be available before contacting a customer."
        )

        with st.expander("View submitted customer data"):
            st.dataframe(customer, use_container_width=True)

    except Exception as error:
        st.error("Prediction failed. Please check the model and feature columns.")
        st.code(str(error))

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<p class='small-note'>Bank Deposit Intelligence · "
    "Built with Python, Scikit-learn and Streamlit</p>",
    unsafe_allow_html=True
)

