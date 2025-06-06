import streamlit as st
import re
import PyPDF2

st.set_page_config(page_title="Resume Shortlister - Flexible Skill Extractor", layout="centered")

st.title("📄 Smart Resume Shortlister - Flexible Skill Extractor")
st.write("Upload your resume (`.pdf` or `.txt`), and the app will extract your skills from any format and check company requirements.")

def extract_skills(text):
    skills = []

    # 1. Extract multiline skill sections (header line ending with ':' + multiline content until empty line or next header)
    multiline_pattern = r'([A-Za-z &]+):\s*\n([^:]+?)(?:\n\s*\n|$)'
    multiline_matches = re.findall(multiline_pattern, text, flags=re.DOTALL)

    for label, content in multiline_matches:
        if any(keyword in label.lower() for keyword in [
            'skill', 'development', 'technology', 'language', 'tool', 'infrastructure', 'framework', 'protocol']):
            items = re.split(r'[,\n]+', content)
            items = [item.strip() for item in items if item.strip()]
            skills.extend(items)

    # 2. Extract single line skill declarations (e.g. "Skills: Python, Java")
    singleline_pattern = r'([A-Za-z &]+):\s*([^\n]+)'
    singleline_matches = re.findall(singleline_pattern, text)

    for label, content in singleline_matches:
        if any(keyword in label.lower() for keyword in [
            'skill', 'development', 'technology', 'language', 'tool', 'infrastructure', 'framework', 'protocol']):
            items = re.split(r'[,\n]+', content)
            items = [item.strip() for item in items if item.strip()]
            skills.extend(items)

    # Deduplicate and lowercase normalize skills
    skills = list(set([s.strip() for s in skills if s.strip()]))

    return skills

uploaded_file = st.file_uploader("Upload your resume file", type=["pdf", "txt"])

if uploaded_file is not None:
    # Read file text
    if uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        file_text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                file_text += page_text + "\n"
    else:
        file_text = uploaded_file.getvalue().decode("utf-8")

    # Extract candidate info
    lines = file_text.splitlines()
    tokens = re.split(r'[,\n:;()\s]+', file_text)
    tokens = [t.strip() for t in tokens if t.strip()]

    # Name extraction - first non-empty line
    name = next((line.strip() for line in lines if line.strip()), None)

    # Email extraction
    email_match = re.search(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', file_text)
    email = email_match.group() if email_match else None

    # Phone extraction - simple 10 digit number pattern
    phone_match = re.search(r'\b\d{10}\b', file_text)
    phone = phone_match.group() if phone_match else None

    # Experience extraction
    if "intern" in file_text.lower():
        ex = "Internship"
        years = 0
    else:
        exp_match = re.search(r'(\d+)\s+years?', file_text.lower())
        years = int(exp_match.group(1)) if exp_match else 0
        ex = f"{years} years" if exp_match else "Not found"

    # Extract skills flexibly
    extracted_skills = extract_skills(file_text)

    # If no skills found by flexible method, fallback to token scanning after 'skills' keyword
    if not extracted_skills:
        skills = []
        collecting = False
        skip_tokens = {'technical', 'skills', '-'}
        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token.lower() in skip_tokens:
                i += 1
                continue

            if ':' in token:
                collecting = True
                i += 1
                continue

            if collecting:
                if i < len(tokens) and (':' in tokens[i] or tokens[i].lower() in skip_tokens):
                    collecting = False
                    continue

                clean_token = token.strip(',').strip()
                if clean_token:
                    skills.append(clean_token)

            i += 1

        extracted_skills = list(set(skills)) if skills else extracted_skills

    # Company Requirements Input
    st.subheader("🏢 Company Requirements")
    required_skills = st.text_input("Enter required skills (comma-separated)", "Python, React")
    min_experience = st.number_input("Enter minimum experience (in years)", min_value=0, max_value=50, value=1)

    if st.button("🔍 Check Resume"):
        required_skills_list = [s.strip().lower() for s in required_skills.split(',')]
        candidate_skills_lower = [s.lower() for s in extracted_skills]

        # Matching logic
        skill_match_count = sum(1 for s in required_skills_list if s in candidate_skills_lower)
        skills_matched = skill_match_count == len(required_skills_list)
        experience_matched = years >= min_experience
        shortlisted = skills_matched and experience_matched

        # Display extracted resume data
        st.subheader("📑 Extracted Resume Data")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**👤 Name:** {name or 'Not found'}")
            st.markdown(f"**📧 Email:** {email or 'Not found'}")
            st.markdown(f"**📞 Phone:** {phone or 'Not found'}")
        with col2:
            st.markdown(f"**💼 Experience:** {ex or 'Not found'} ({years} years)")
            st.markdown(f"**🧠 Skills:** {', '.join(extracted_skills) if extracted_skills else 'Not found'}")

        st.subheader("🎯 Result")
        if shortlisted:
            st.success("✅ Resume is **Shortlisted** based on company criteria.")
        else:
            st.error("❌ Resume is **Rejected**. Does not meet all requirements.")
