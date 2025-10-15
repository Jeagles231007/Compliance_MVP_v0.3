# =====================================================
# Cyphera AI Compliance Policy Generator
# Author: Joe Eagles
# =====================================================

# Importing of necessary libraries and functions from other file.
# Make sure to add .env to .gitignore, so it never gets pushed to GitHub.
# This is local only, so we need GitHub to ignore.

import streamlit as st
import tempfile
from policy_generator import generate_policy, save_to_docx, save_to_pdf

# -----------------------------------------------------
# PAGE CONFIG & BRANDING
# -----------------------------------------------------
st.set_page_config(
    page_title="Cyphera | AI Compliance Policy Generator",
    page_icon="🛡",
    layout="centered"
)

# -----------------------------------------------------
# CUSTOM CSS FOR MODERN UI
# -----------------------------------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .main-title {
            font-size: 2.2rem;
            font-weight: 700;
            color: #1C1C1C;
            text-align: center;
            margin-bottom: 0.3rem;
        }

        .subtitle {
            text-align: center;
            color: #5C5C5C;
            margin-bottom: 2rem;
        }

        .stTextInput>div>div>input, .stSelectbox>div>div>select {
            background-color: #F8F9FB !important;
            border-radius: 10px !important;
        }

        .stButton>button {
            background: linear-gradient(90deg, #2563EB, #1E40AF);
            color: white;
            border: none;
            padding: 0.6em 1.5em;
            border-radius: 10px;
            font-weight: 600;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #1E40AF, #2563EB);
            transform: scale(1.02);
            transition: 0.2s ease-in-out;
        }

        .stForm {
            background-color: white;
            border-radius: 15px;
            padding: 2rem 2.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
        }

        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# SIDEBAR BRANDING
# -----------------------------------------------------
with st.sidebar:
    st.image("cyphera.png", width=180)  # Add your logo in same folder as app.py
    st.markdown("### About Cyphera")
    st.write(
        "Cyphera helps organisations generate **AI-powered compliance documents** instantly. "
        "Built for startups, consultancies, and growing tech firms needing reliable documentation fast."
    )
    st.markdown("---")
    st.write("🛡️ *Disclaimer: Generated documents are for informational purposes only and should be reviewed by a qualified professional before use.*")

# -----------------------------------------------------
# MAIN PAGE HEADER
# -----------------------------------------------------
st.markdown('<div class="main-title">Cyphera Compliance Policy Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Generate legally sound policies tailored to your company and jurisdiction</div>', unsafe_allow_html=True)


# -----------------------------------------------------
# INPUT FORM
# -----------------------------------------------------
# st.title("AI Compliance Policy Generator")
with st.form("policy_form"):
    company_name = st.text_input("Company Name", placeholder="e.g. FinTech Solutions Ltd")
    industry = st.text_input("Industry", placeholder="e.g. Finance")
    jurisdiction = st.selectbox("Jurisdiction", ["UK", "EU", "USA"])
    size = st.text_input("Company Size", placeholder="e.g. Small startup, 50 employees")
    policy_type = st.selectbox(
        "Select Policy Type",
        ["Privacy Policy", "Data Protection Policy", "Acceptable Use Policy", "Incident Response Policy",
         "AI Governance Policy"]
    )
    submitted = st.form_submit_button("Generate Policy")

# -----------------------------------------------------
# POLICY GENERATION SECTION
# -----------------------------------------------------
if submitted:
    with st.spinner("🧠Generating your policy...please wait"):
        policy_text = generate_policy(
            company_name=company_name,
            industry=industry,
            jurisdiction=jurisdiction,
            size=size,
            policy_type=policy_type
        )

    st.success("✅Policy generated successfully!")
    st.text_area("Preview", policy_text, height=400)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:

        save_to_docx(policy_text, tmp_docx.name)
        save_to_pdf(policy_text, tmp_pdf.name)

        with open(tmp_docx.name, "rb") as f:
            st.download_button(
                label="📄Download Policy (.docx)",
                data=f,
                file_name=f"{company_name}_{policy_type.replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

        with open(tmp_pdf.name, "rb") as f:
            st.download_button(
                label="📘Download Policy (.pdf)",
                data=f,
                file_name=f"{company_name}_{policy_type.replace(' ', '_')}.pdf",
                mime="application/pdf",
            )
