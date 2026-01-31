import streamlit as st
import csv
import os
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Register | CYBERSUMMIT 2026",
    page_icon="🛡️",
    layout="centered"
)

# ---------------- STYLES ----------------
st.markdown("""
<style>
/* Background */
.stApp {
    background: radial-gradient(circle at top, #0b1020, #000000 80%);
    color: #E0F7FA;
}

/* Header pill */
.header-pill {
    width: 100%;
    background: linear-gradient(180deg, rgba(5,25,35,0.95), rgba(5,15,25,0.95));
    border: 2px solid #00ffff;
    border-radius: 45px;
    padding: 26px;
    text-align: center;
    margin: 40px 0 35px 0;
    box-shadow: 0 0 30px rgba(0,255,255,0.6);
}

.header-pill-text {
    font-size: 28px;
    font-weight: 700;
    color: #E0F7FA;
    text-shadow: 0 0 14px rgba(0,255,255,1);
}

/* Labels */
label {
    color: #E0F7FA !important;
    font-weight: 600;
}

/* Inputs & selectbox */
input, textarea, select {
    background-color: rgba(0,0,0,0.75) !important;
    color: #E0F7FA !important;
    border: 1.5px solid #00ffff !important;
    border-radius: 12px !important;
}

/* Placeholder */
input::placeholder, textarea::placeholder {
    color: #9ee7e7 !important;
}

/* Submit button (PURE WHITE) */
div.stButton > button {
    background-color: #ffffff !important;
    color: #000000 !important;
    font-size: 18px !important;
    font-weight: 800 !important;
    padding: 15px !important;
    border-radius: 35px !important;
    border: none !important;
    width: 100% !important;
    box-shadow: 0 0 25px rgba(255,255,255,0.6) !important;
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    background-color: #e6faff !important;
    box-shadow: 0 0 40px rgba(0,255,255,0.9) !important;
    transform: scale(1.04);
}

/* Success box */
.success-box {
    background: rgba(0, 90, 80, 0.9);
    border: 1px solid #1DE9B6;
    border-radius: 18px;
    padding: 30px;
    box-shadow: 0 0 35px rgba(29,233,182,0.6);
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="header-pill">
    <div class="header-pill-text">🔒 Participant Registration</div>
</div>
""", unsafe_allow_html=True)

# ---------------- FORM ----------------
with st.form("registration_form"):

    full_name = st.text_input("👤 Full Name *")
    email = st.text_input("📧 Email Address *")
    phone = st.text_input("📱 Contact Number *")

    universities = [
        "University of Colombo",
        "University of Sri Jayewardenepura",
        "University of Peradeniya",
        "University of Moratuwa",
        "University of Kelaniya",
        "University of Ruhuna",
        "Eastern University",
        "South Eastern University",
        "Rajarata University",
        "Wayamba University",
        "Sabaragamuwa University",
        "Uva Wellassa University",
        "Open University of Sri Lanka",
        "Other"
    ]

    university = st.selectbox("🎓 University *", universities)

    other_university = ""
    if university == "Other":
        other_university = st.text_input("✍️ Specify University *")

    # OPTIONAL MESSAGE (FIXED)
    message = st.text_area(
        "💬 Any message / query (optional)",
        placeholder="You may leave this empty if you have no message"
    )

    submit = st.form_submit_button("🚀 Submit Registration")

# ---------------- VALIDATION & SAVE ----------------
if submit:
    if not full_name or not email or not phone:
        st.error("⚠️ Please fill all mandatory fields.")
    elif university == "Other" and not other_university:
        st.error("⚠️ Please specify your university.")
    else:
        final_university = other_university if university == "Other" else university

        file_exists = os.path.isfile("registrations.csv")
        with open("registrations.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow([
                    "Timestamp",
                    "Name",
                    "Email",
                    "Phone",
                    "University",
                    "Message"
                ])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                full_name,
                email,
                phone,
                final_university,
                message
            ])

        st.markdown(
            """
            <div class="success-box">
                <h3>✅ Registration Successful!</h3>
                <p>You are now registered for <b>CYBERSUMMIT 2026</b>.</p>
                <a href="https://chat.whatsapp.com/YOUR_WHATSAPP_LINK"
                   target="_blank"
                   style="color:#25D366;font-size:20px;font-weight:bold;">
                   👉 Join Official WhatsApp Group
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
