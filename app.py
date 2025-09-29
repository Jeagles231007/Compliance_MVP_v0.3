# Importing of necessary libraries and functions from other file.
# Make sure to add .env to .gitignore, so it never gets pushed to GitHub.
# This is local only, so we need GitHub to ignore.
import streamlit as st
import tempfile
from policy_generator import generate_policy, save_to_docx, save_to_pdf

st.title("AI Compliance Policy Generator")

with st.form("policy_form"):
    company_name = st.text_input("Company Name", placeholder="e.g. FinTech Solutions Ltd")
    industry = st.text_input("Industry", placeholder="e.g. Finance")
    jurisdiction = st.selectbox("Jurisdiction", ["UK", "EU", "USA"])
    size = st.text_input("Company Size", placeholder="e.g. Small startup, 50 employees")
    policy_type = st.selectbox(
        "Select Policy Type",
        ["Privacy Policy", "Data Protection Policy", "Acceptable Use Policy", "Incident Response Policy"]
    )
    submitted = st.form_submit_button("Generate Policy")

if submitted:
    st.info("Generating your policy...please wait")
    policy_text = generate_policy(
        company_name=company_name,
        industry=industry,
        jurisdiction=jurisdiction,
        size=size,
        policy_type=policy_type
    )
    st.success("Policy generated successfully!")

    st.text_area("Preview", policy_text, height=400)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:

        save_to_docx(policy_text, tmp_docx.name)
        save_to_pdf(policy_text, tmp_pdf.name)

        with open(tmp_docx.name, "rb") as f:
            st.download_button(
                label="Download Policy (.docx)",
                data=f,
                file_name=f"{company_name}_{policy_type.replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

        with open(tmp_pdf.name, "rb") as f:
            st.download_button(
                label="Download Policy (.pdf)",
                data=f,
                file_name=f"{company_name}_{policy_type.replace(' ', '_')}.pdf",
                mime="application/pdf",
            )
