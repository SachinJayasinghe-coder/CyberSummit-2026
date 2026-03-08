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

input[type="text"], input[type="email"], textarea, select {
    background-color: rgba(25,0,40,0.85) !important;
    color: #F3E8FF !important;
    border: 1.5px solid #A855F7 !important;
    border-radius: 12px !important;
}

input::placeholder, textarea::placeholder {
    color: #C084FC !important;
}

.success-box {
    background: rgba(40, 0, 60, 0.9);
    border: 1px solid #C084FC;
    border-radius: 18px;
    padding: 30px;
    box-shadow: 0 0 35px rgba(168,85,247,0.6);
    margin-top: 30px;
}
/* ===== FORCE RADIO TEXT PURE WHITE (FINAL FIX) ===== */
[data-baseweb="radio"] label,
[data-baseweb="radio"] div,
[data-baseweb="radio"] span {
    color: #FFFFFF !important;
    opacity: 1 !important;
}
/* Keep radio circle purple */
input[type="radio"]:checked {
    accent-color: #A855F7 !important;
}
/* Remove weird red selection */
input[type="radio"]:checked {
    accent-color: #A855F7 !important;
}
/* ===== STYLE SELECTBOX TO MATCH THEME ===== */
[data-baseweb="select"] > div {
    background-color: rgba(25,0,40,0.85) !important;
    color: #F3E8FF !important;
    border: 1.5px solid #A855F7 !important;
    border-radius: 12px !important;
}

/* Dropdown text */
[data-baseweb="select"] span {
    color: #F3E8FF !important;
}

/* Dropdown arrow */
[data-baseweb="select"] svg {
    fill: #F3E8FF !important;
}
/* ===== FIX DROPDOWN MENU (Selectbox Options) ===== */

/* Dropdown container */
[data-baseweb="popover"] {
    background-color: rgba(25,0,40,0.98) !important;
}
/* ===== FORCE STREAMLIT SELECT DROPDOWN DARK THEME ===== */

/* Dropdown portal layer */
div[data-baseweb="layer"] {
    background-color: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
# ---------------- HEADER ----------------
st.markdown("""
<div class="header-pill">
    <div class="header-pill-text">🔒 Participant Registration</div>
</div>
""", unsafe_allow_html=True)

# 👇 ADD PARAGRAPH HERE
st.markdown("""
<p style="
    text-align:center;
    font-size:16px;
    color:#E9D5FF;
    margin-bottom:25px;
">
Welcome to the official registration form for <b>Cyber Summit 2026</b>, the flagship cybersecurity event organized by the ISACA Student Group of the University of Sri Jayewardenepura.
</p>
""", unsafe_allow_html=True)

# -------- BASIC DETAILS --------
full_name = st.text_input("1. First & Last Name *")
email = st.text_input("2. Email Address *")
phone = st.text_input("3. Contact Number *")

# -------- ACADEMIC STATUS --------
academic_status = st.radio(
    "4. Current Academic Status *",
    [
        "University Undergraduate",
        "Advanced Level Student",
        "School Student",
        "Other"
    ],
    horizontal=False
)

# initialize variables
university_name = ""
other_university = ""
school_name = ""
other_status = ""

# -------- CONDITIONAL INSTITUTION FIELD --------
if academic_status == "University Undergraduate":

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

    university_name = st.selectbox("🎓 University *", universities, index=None)

    if university_name == "Other":
        other_university = st.text_input("✍️ Specify University *")

elif academic_status in ["Advanced Level Student", "School Student"]:
    school_name = st.text_input("🏫 Name of School *")

elif academic_status == "Other":
    other_status = st.text_input("✍️ Please specify *")

# -------- PREVIOUS EVENT --------
previous_event_attended = st.radio(
    "5. Have you previously attended a cybersecurity event? *",
    ["Yes", "No"],
    horizontal=False
)

# -------- KNOWLEDGE LEVEL --------
cyber_knowledge_level = st.radio(
    "6. How would you rate your knowledge of cybersecurity? *",
    ["No prior knowledge", "Beginner", "Intermediate", "Advanced"],
    horizontal=False
)

# -------- HEARD ABOUT EVENT --------
hear_about_event = st.text_input(
    "7. How did you hear about Cyber Summit'26? (Optional)"
)

# -------- FOOD PREFERENCE --------
food_preference = st.radio(
    "8. Food Preference *",
    ["Veg", "Non-Veg"],
    horizontal=False
)

# -------- CONSENT --------
consent_updates = st.radio(
    "9. I agree to receive event updates via Whatsapp and Email *",
    ["Yes", "No"],
    horizontal=False
)

# -------- MESSAGE --------
message = st.text_area("10. Any message / query (optional)")

# -------- SUBMIT BUTTON --------
submit = st.button("🚀 Submit Registration", type="primary")

# ---------------- SAVE TO GOOGLE SHEETS ----------------
if submit:

    # -------- VALIDATION --------
    if not full_name.strip() or not email.strip() or not phone.strip():
        st.error("⚠️ Please fill all mandatory fields.")

    elif "@" not in email or "." not in email:
        st.error("⚠️ Please enter a valid email address.")

    elif academic_status == "University Undergraduate" and university_name == "Other" and not other_university.strip():
        st.error("⚠️ Please specify your university.")

    elif academic_status == "University Undergraduate" and not university_name:
        st.error("⚠️ Please select your university.")

    elif academic_status in ["Advanced Level Student", "School Student"] and not school_name:
        st.error("⚠️ Please enter your school name.")

    elif academic_status == "Other" and not other_status.strip():
        st.error("⚠️ Please specify your status.")

    elif consent_updates != "Yes":
        st.error("⚠️ You must agree to receive updates to complete registration.")

    else:

        # -------- FINAL INSTITUTION LOGIC --------
        if academic_status == "University Undergraduate":
            final_institution = other_university if university_name == "Other" else university_name
        elif academic_status in ["Advanced Level Student", "School Student"]:
            final_institution = school_name
        else:
            final_institution = other_status

        try:
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]

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
                academic_status,
                final_institution,
                previous_event_attended,
                cyber_knowledge_level,
                hear_about_event,
                food_preference,
                consent_updates,
                message
            ])

            st.success("✅ Registration Successful!")
            st.balloons()
            st.success("📢 Join our official WhatsApp group for event updates!")
            st.markdown(
                """
                <a href="https://chat.whatsapp.com/IBXaMMkkQ0T3AvhxZkJqnr?mode=gi_t" target="_blank">
                    <button style="
                        background-color:#25D366;
                        color:white;
                        padding:12px 25px;
                        border:none;
                        border-radius:8px;
                        font-size:16px;
                        cursor:pointer;">
                        Join WhatsApp Group
                    </button>
                </a>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"❌ Error saving data: {e}")
