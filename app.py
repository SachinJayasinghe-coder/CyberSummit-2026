import streamlit as st
from datetime import date
from pathlib import Path
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
# Detect screen width
screen_width = streamlit_js_eval(
    js_expressions="window.innerWidth",
    key="SCREEN_WIDTH",
    want_output=True,
)

# Store in session state
if screen_width:
    st.session_state["screen_width"] = screen_width

is_mobile = st.session_state.get("screen_width", 1000) < 768

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Exo+2:wght@400;600;700;800;900&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ---------------- CYBER THEME ----------------
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(
        135deg,
        #0f051d 0%,
        #240046 35%,
        #5a189a 70%,
        #10002b 100%
    ) !important;
    color: #F3E8FF;
}
   
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@400;600;700;800;900&display=swap');
            
/* ===== REMOVE STREAMLIT HEADER (TOP BAR) ===== */
header[data-testid="stHeader"] {
    display: none;
}
            
/* ===== REMOVE STREAMLIT FOOTER (BOTTOM AREA) ===== */
footer {
    display: none;
}

/* ===== REMOVE MAIN MENU (three dots menu) ===== */
#MainMenu {
    visibility: hidden;
}

/* Remove extra padding at top */
.main .block-container {
    padding-top: 1rem;
}
            
/* Headings */
h1, h2, h3 {
    color: #A855F7;
    text-shadow: 0 0 15px rgba(168,85,247,0.7);
    text-align: center;
}
            
/* Remove Sidebar Completely */
section[data-testid="stSidebar"] {
    display: none !important;
}

/* Expand main content full width */
div[data-testid="stAppViewContainer"] {
    margin-left: 0 !important;
}
            
/* Align Streamlit columns vertically (THIS IS THE FIX) */
[data-testid="column"] {
    display: flex;
    align-items: center;
    justify-content: center;
}
            
/* HERO CENTERING FIX */
.hero-container {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.hero-title {
    font-family: 'Exo 2', sans-serif !important;
    margin: 0;
    font-size: 60px;
    font-weight: 900;
    letter-spacing: 10px;
    text-transform: uppercase;
    text-align: center;
 font-family: 'Exo 2', sans-serif;

    background: linear-gradient(90deg,#60A5FA,#C084FC);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 8px 40px rgba(59,130,246,0.5);
}

/* Notice Cards */
.notice-card {
    background: rgba(168,85,247,0.08);
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 0 25px rgba(168,85,247,0.35);
    transition: 0.3s ease;
    padding: 0;
}

.notice-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 0 40px rgba(168,85,247,0.7);
}

.notice-text {
    padding: 15px;
    text-align: center;
    font-weight: 500;
}

/* Contact Cards */
.contact-card {
    background: rgba(168,85,247,0.08);
    border: 1px solid rgba(168,85,247,0.4);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 0 25px rgba(168,85,247,0.35);
    text-align: center;
}

/* Image inside card */
.flyer-image img {
    border-radius: 0;                 /* remove double rounding */
    display: block;
}

/* Text area */
.flyer-text {
    padding: 15px;
    text-align: center;
    font-weight: 500;
    font-size: 15px;
}

/* Timeline */
.timeline {
    background: rgba(0,0,0,0.7);
    border-left: 4px solid #A855F7;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 10px;
}

.flyer-box {
    height: 180px;
    border: 2px dashed #A855F7;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #A855F7;
    margin-bottom: 10px;
}

.avatar {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    border: 2px dashed #A855F7;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 38px;
    margin: auto;
}

/* Button */
div.stButton > button {
    background: linear-gradient(90deg, #A855F7, #7E22CE);
    color: #ffffff;
    font-size: 18px;
    font-weight: bold;
    padding: 14px 40px;
    border-radius: 30px;
    border: none;
    box-shadow: 0 0 22px rgba(168,85,247,0.8);
    transition: 0.3s ease;
}

div.stButton > button:hover {
    box-shadow: 0 0 40px rgba(168,85,247,1);
    transform: scale(1.05);
}
.bottom-wrapper {
    display: none;
}
.top-wrapper {
    display: block;           
}           
@media (max-width: 768px) {

    /* Stack columns vertically */
    [data-testid="column"] {
        display: block !important;
        width: 100% !important;
        text-align: center !important;
        margin-bottom: 15px;
    }

    /* Center Streamlit image wrapper */
    [data-testid="column"] div[data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
    }

    /* Resize images */
    [data-testid="column"] img {
        width: 100px !important;
        max-width: 100% !important;
    }

    /* Center title */
    h1 {
        font-size: 64px !important;
        text-align: center !important;
        white-space: normal !important;
    }
}        
/* Footer */
.footer {
    text-align: center;
    color: #C084FC;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
col1, col2, col3 = st.columns([1,3,1], gap="small")

with col1:
    st.image("project_logo.png", use_container_width=True)

with col2:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">
            CYBER<br>SUMMIT<br>2026
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if not is_mobile:
        st.markdown('<br><br><br>', unsafe_allow_html=True)
        st.image("ISACA_logo.png", width=480)
st.divider()

st.markdown("""
<div class="cyber-card">
<b>CYBERSUMMIT 2026</b> is <b>the flagship event of ISACA Student Group of
University of Sri Jayewardenepura</b>, proudly organized for <b>third consecutive
year</b> in <b>March 2026</b>. This one day summit brings together the passionate
students and experienced professionals from Cyber Security industry.<br><br>
The event will feature insightful, interactie and engaging sessions conducted
by industry experts, offering participants a real world perspective on Cyber Security,
risk, governance and emerging digital threats.<br><br>
<h2>What You Can Gain from Cyber Summit 2026 ?</h2>           
<ul>
<li>Industry Level Exposure - Interact with professionals and understand real-world Cyber Security Practices</li>
<li>Advance Technology - Explore latest trends in Digital Security, Risk assessment & AI</li>
<li>Skill development - Enhance critical thinking</li>
<li>Career Advantage - Strengthen your CV with summit participation and practical insights</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------- TIMELINE ----------------
st.markdown("<h2>🗓️ Event Timeline</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="timeline"><b>📢 Registration Opens</b><br>26 February 2026</div>
<div class="timeline"><b>⏳ Registration Closes</b><br>6 March 2026 </div>
<div class="timeline"><b>🎓 Workshop Day</b><br>14 March 2026</div>
<div class="timeline"><b>🏁 Event Ends</b><br>14 March 2026</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------- REGISTER (THIS PART MATTERS) ----------------
st.markdown("<h2>📝 Ready to Join?</h2>", unsafe_allow_html=True)

left, center, right = st.columns([1, 2, 1])

with center:
    if st.button("🚀 Register Now", use_container_width=True):
        st.switch_page("pages/registration.py")


st.divider()

# ---------------- NOTICE BOARD ----------------
st.markdown("<h2>📢 Notice Board</h2>", unsafe_allow_html=True)

def notice_card(image_path, text):
    st.markdown('<div class="notice-card">', unsafe_allow_html=True)

    st.image(image_path, use_container_width=True)

    st.markdown(
        f"<div class='notice-text'>{text}</div>",
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

n1, n2, n3 = st.columns(3)

with n1:
    notice_card("flyer1.png", "🚀 Registrations are now open. Secure your seat today!")

with n2:
    notice_card("flyer2.png", "📜 Digital certificates will be provided to all participants.")

with n3:
    notice_card("flyer3.png", "⚠️ Limited seats available. Register before deadline.")

st.divider()

# ---------------- CONTACT PERSONS ----------------
st.markdown("<h2>📞 Contact Persons</h2>", unsafe_allow_html=True)

p1, p2, p3 = st.columns(3)

def contact_card(icon, name, phone, email):
    st.markdown(f"""
    <div class="contact-card">
        <div class="avatar">{icon}</div><br>
        <b>{name}</b><br><br>
        📱 {phone}<br>
        📧 {email}
    </div>
    """, unsafe_allow_html=True)

with p1: 
    contact_card("👨‍💻", "Kasun Perera", "077 123 4567", "kasun@email.com") 
with p2: 
    contact_card("👩‍💻", "Nimali Fernando", "071 234 5678", "nimali@email.com") 
with p3: 
    contact_card("🧑‍💻", "Ravindu Silva", "075 345 6789", "ravindu@email.com")

st.divider()

# ---------------- MOBILE ISACA ----------------
col1, col2, col3 = st.columns([1,1,1], gap="small")

with col2:
    if is_mobile:
       st.image("ISACA_logo.png", width=220)

# ---------------- FOOTER ----------------
st.markdown(f"""
<div class="footer">
Developed by <b>Sachin Jayasinghe</b><br>
Created Date: {date.today().strftime("%d %B %Y")}<br>
© CYBERSUMMIT 2026
</div>
""", unsafe_allow_html=True)