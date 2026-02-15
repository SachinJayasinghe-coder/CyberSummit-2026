import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Register | CYBERSUMMIT 2026",
    page_icon="🛡️",
    layout="centered"
)

# ---------------- STYLES ----------------
st.markdown("""
<style>
header[data-testid="stHeader"] { display: none; }
footer { display: none; }
#MainMenu { visibility: hidden; }
.main .block-container { padding-top: 1rem; }

.stApp {
    background: radial-gradient(circle at top, #140025, #000000 80%);
    color: #F3E8FF;
}

.header-pill {
    width: 100%;
    background: linear-gradient(180deg, rgba(30,0,50,0.95), rgba(15,0,35,0.95));
    border: 2px solid #A855F7;
    border-radius: 45px;
    padding: 26px;
    text-align: center;
    margin: 40px 0 35px 0;
    box-shadow: 0 0 30px rgba(168,85,247,0.7);
}

.header-pill-text {
    font-size: 28px;
    font-weight: 700;
    color: #F3E8FF;
    text-shadow: 0 0 14px rgba(168,85,247,1);
}

label {
    color: #E9D5FF !important;
    font-weight: 600;
}

input, textarea, select {
    background-color: rgba(25,0,40,0.85) !important;
    color: #F3E8FF !important;
    border: 1.5px solid #A855F7 !important;
    border-radius: 12px !important;
}

input::placeholder, textarea::placeholder {
    color: #C084FC !important;
}

/* Submit Button */
button[data-testid="stFormSubmitButton"] {
    background-color: #A855F7 !important;
    color: #ffffff !important;
    font-size: 18px !important;
    font-weight: 800 !important;
    padding: 15px !important;
    border-radius: 35px !important;
    border: none !important;
    width: 100% !important;
    box-shadow: 0 0 25px rgba(168,85,247,0.8) !important;
    transition: all 0.3s ease !important;
}

button[data-testid="stFormSubmitButton"]:hover {
    background-color: #7E22CE !important;
    box-shadow: 0 0 40px rgba(168,85,247,1) !important;
    transform: scale(1.04);
}

.success-box {
    background: rgba(40, 0, 60, 0.9);
    border: 1px solid #C084FC;
    border-radius: 18px;
    padding: 30px;
    box-shadow: 0 0 35px rgba(168,85,247,0.6);
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

    # Default = Sri Jayewardenepura (index 1)
    university = st.selectbox("🎓 University *", universities, index=1)

    other_university = ""
    if university == "Other":
        other_university = st.text_input("✍️ Specify University *")

    message = st.text_area(
        "💬 Any message / query (optional)",
        placeholder="Leave empty if not needed"
    )

    submit = st.form_submit_button("🚀 Submit Registration")

# ---------------- SAVE TO GOOGLE SHEETS ----------------
if submit:
    if not full_name or not email or not phone:
        st.error("⚠️ Please fill all mandatory fields.")
    elif university == "Other" and not other_university:
        st.error("⚠️ Please specify your university.")
    else:
        final_university = other_university if university == "Other" else university

        try:
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]

            # 🔐 Using Streamlit Secrets
            creds = ServiceAccountCredentials.from_json_keyfile_dict(
                st.secrets["gcp_service_account"],
                scope
            )

            client = gspread.authorize(creds)
            sheet = client.open("CyberSummit 2026 Registrations").sheet1

            sheet.append_row([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                full_name,
                email,
                phone,
                final_university,
                message
            ])

            st.markdown("""
                <div class="success-box">
                    <h3>✅ Registration Successful!</h3>
                    <p>You are now registered for <b>CYBERSUMMIT 2026</b>.</p>
                    <p style="margin-top:15px;font-size:18px;">
                        📲 Join our Official WhatsApp Group:
                    </p>
                    <a href="https://chat.whatsapp.com/YOUR_GROUP_LINK"
                       target="_blank"
                       style="
                            display:inline-block;
                            margin-top:10px;
                            padding:12px 25px;
                            background:#25D366;
                            color:white;
                            font-weight:bold;
                            border-radius:30px;
                            text-decoration:none;
                            box-shadow:0 0 20px rgba(37,211,102,0.7);
                       ">
                       👉 Join WhatsApp Group
                    </a>
                </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error saving data: {e}")
