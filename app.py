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
import os
import requests


# ==============================
# Gumroad License Verification
# ==============================
def verify_license(license_key: str) -> bool:
    """Verifies a Gumroad license key using the Gumroad API."""
    GUMROAD_PRODUCT_ID = st.secrets["gumroad_product_id"]  # Add this to your Streamlit Secrets
    url = "https://api.gumroad.com/v2/licenses/verify"
    payload = {
        "product_permalink": GUMROAD_PRODUCT_ID,
        "license_key": license_key,
    }
    try:
        response = requests.post(url, data=payload)
        result = response.json()
        return result.get("success", False)
    except requests.RequestException:
        st.error("Network Error during Verification.")
        return False
    except ValueError:
        st.error("Unexpected response from Gumroad.")
        return False


def check_license():
    """Prompts user for license key and verifies it."""
    if st.session_state.get("authenticated"):
        return True

    st.title("🔐 Cyphera Access Portal")
    st.write("Enter your Gumroad license key to access the AI Compliance Generator.")

    license_key = st.text_input(
        "License Key",
        placeholder="e.g. GUMROAD-XXXX-XXXX-XXXX",
        type="password"
    )
    remember_me = st.checkbox("Remember me on this device")

    if st.button("Verify License"):
        if verify_license(license_key):
            st.session_state["authenticated"] = True
            if remember_me:
                st.session_state["cached_license"] = license_key
            st.success("✅ License verified successfully. Welcome to Cyphera.")
            st.rerun()
        else:
            st.error("❌ Invalid or inactive license key. Please check your Gumroad account.")

    st.stop()


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

        .logout-button > button {
            background: none !important;
            color: #6B7280 !important;  /* grey text */
            border: none !important;
            font-size: 0.9rem !important;
            text-decoration: underline;
            padding: 0 !important;
            margin-top: 10px;
        }

        .logout-button > button:hover {
            color: #1E3A8A !important;  /* hover blue */
            text-decoration: none;
            transform: none !important;
        }
    </style>
""", unsafe_allow_html=True)


def main():
    # -----------------------------------------------------
    # PAGE CONFIG & BRANDING
    # -----------------------------------------------------
    st.set_page_config(
        page_title="Cyphera | AI Compliance Policy Generator",
        page_icon="🛡",
        layout="centered"
    )

    # License Gate
    if not st.session_state.get("authenticated"):
        check_license()
        return

    # -----------------------------------------------------
    # SIDEBAR BRANDING
    # -----------------------------------------------------
    with st.sidebar:
        st.image("cyphera.png", width=180)
        st.markdown("### About Cyphera")
        st.write(
            "Cyphera helps organisations generate **AI-powered compliance documents** instantly. "
            "Built for startups, consultancies, and growing tech firms needing reliable documentation fast."
        )
        st.markdown("---")
        if st.button("Log out", key="logout", help="End this session"):
            st.session_state.clear()
            st.rerun()
        st.write("🛡️ *Disclaimer: Generated documents are for informational purposes only and should be reviewed by a qualified professional before use.*")

    # -----------------------------------------------------
    # MAIN PAGE HEADER
    # -----------------------------------------------------
    st.markdown('<div class="main-title">Cyphera Compliance Policy Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Generate legally sound policies tailored to your company and jurisdiction</div>', unsafe_allow_html=True)

    # -----------------------------------------------------
    # INPUT FORM
    # -----------------------------------------------------
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


if __name__ == "__main__":
    main()

