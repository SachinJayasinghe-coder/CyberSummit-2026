import streamlit as st
from datetime import date
from pathlib import Path
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CYBERSUMMIT 2026",
    page_icon="🔐",
    layout="wide"
)

# ---------------- CYBER THEME ----------------
st.markdown("""
<style>

/* Remove Streamlit header & footer */
header[data-testid="stHeader"] { display: none; }
footer { display: none; }
#MainMenu { visibility: hidden; }

.main .block-container { padding-top: 1rem; }

.stApp {
    background: radial-gradient(circle at top, #140025, #000000 60%);
    color: #F3E8FF;
}

h1, h2, h3 {
    color: #A855F7;
    text-shadow: 0 0 15px rgba(168,85,247,0.7);
    text-align: center;
}

/* Cards */
.cyber-card {
    background: rgba(168,85,247,0.08);
    border: 1px solid rgba(168,85,247,0.4);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 0 25px rgba(168,85,247,0.35);
}

.timeline {
    background: rgba(0,0,0,0.7);
    border-left: 4px solid #A855F7;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 10px;
}

/* Responsive header control */
.desktop-header { display: block; }
.mobile-header { display: none; }

@media (max-width: 768px) {

    .desktop-header { display: none; }

    .mobile-header {
        display: block;
        text-align: center;
    }

    .mobile-header img {
        display: block;
        margin: 10px auto;
    }

    .mobile-header h1 {
        font-size: 32px;
        margin: 10px 0;
    }

}

.footer {
    text-align: center;
    color: #C084FC;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- RESPONSIVE HEADER ----------------

# -------- DESKTOP VERSION --------
st.markdown('<div class="desktop-header">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,5,1])

with col1:
    st.image("project_logo.png", width=120)

with col2:
    st.markdown("""
        <h1 style="
            margin:0;
            font-size:60px;
            font-weight:700;
            letter-spacing:4px;
            white-space:nowrap;
            text-align:center;
        ">
            CYBER SUMMIT 2026
        </h1>
    """, unsafe_allow_html=True)

with col3:
    st.image("ISACA_logo.png", width=120)

st.markdown('</div>', unsafe_allow_html=True)


# -------- MOBILE VERSION --------
st.markdown('<div class="mobile-header">', unsafe_allow_html=True)

st.image("project_logo.png", width=100)
st.markdown("<h1>CYBER SUMMIT 2026</h1>", unsafe_allow_html=True)
st.image("ISACA_logo.png", width=90)

st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ---------------- ABOUT ----------------
st.markdown("<h2>🔍 What is CYBERSUMMIT 2026?</h2>", unsafe_allow_html=True)

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

n1, n2, n3 = st.columns(3)

def notice_card(text):
    st.markdown(f"""
    <div class="cyber-card">
        <div class="flyer-box">FLYER IMAGE</div>
        <p>{text}</p>
    </div>
    """, unsafe_allow_html=True)

with n1:
    notice_card("🚀 Registrations are now open. Secure your seat today!")

with n2:
    notice_card("📜 Digital certificates will be provided to all participants.")

with n3:
    notice_card("⚠️ Limited seats available. Register before deadline.")

st.divider()

# ---------------- CONTACT PERSONS ----------------
st.markdown("<h2>📞 Contact Persons</h2>", unsafe_allow_html=True)

p1, p2, p3 = st.columns(3)

def contact_card(icon, name, phone, email):
    st.markdown(f"""
    <div class="cyber-card" style="text-align:center;">
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

# ---------------- FOOTER ----------------
st.markdown(f"""
<div class="footer">
Developed by <b>Sachin Jayasinghe</b><br>
Created Date: {date.today().strftime("%d %B %Y")}<br>
© CYBERSUMMIT 2026
</div>
""", unsafe_allow_html=True)