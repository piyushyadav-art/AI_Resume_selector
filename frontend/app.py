import sys
from pathlib import Path
import tempfile
import streamlit as st

# ==========================================================
# PATH CONFIGURATION
# ==========================================================
# Ensure project root is in sys.path so 'src' can be imported
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.pdf_parser import extract_text_from_pdf
from src.preprocessing import clean_resume_text
from src.resume_parser import extract_resume_sections
from src.embeddings import (
    create_resume_text,
    generate_embedding,
)
from src.similarity import (
    calculate_cosine_similarity,
    generate_match_score,
)
from src.skill_extractor import (
    extract_skills,
    find_missing_skills,
    format_skill_name,
)
from src.recommendations import recommend_skills


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="AI Resume Intelligence",
    page_icon="📄",
    layout="wide"
)


# ==========================================================
# CUSTOM CSS & STYLING
# ==========================================================

st.markdown(
    """
    <style>
    .main-title {
        font-size: 38px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 6px;
        letter-spacing: -0.5px;
    }

    .subtitle {
        text-align: center;
        color: #888888;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .score-card {
        padding: 24px 20px;
        border-radius: 12px;
        background: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.2);
        text-align: center;
        margin: 10px 0;
    }

    .score-card-label {
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #999999;
        margin-bottom: 6px;
    }

    .score-card-value {
        font-size: 44px;
        font-weight: 800;
        line-height: 1.1;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        margin-top: 24px;
        margin-bottom: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    '<div class="main-title">📄 AI Resume Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze candidate resumes against job descriptions using transformer embeddings & skill gap analysis'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================================
# INPUT SECTION
# ==========================================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload Resume")
    resume_file = st.file_uploader(
        "Upload your resume",
        type=["pdf"],
        help="Upload a candidate resume in PDF format (text-based PDF)"
    )

with col2:
    st.subheader("💼 Job Description")
    job_description = st.text_area(
        "Paste the job description",
        height=220,
        placeholder=(
            "Example:\n\n"
            "We are looking for a Machine Learning Engineer with Python, PyTorch, "
            "SQL, FastAPI, Docker, and LangChain experience..."
        )
    )


# ==========================================================
# ANALYZE BUTTON
# ==========================================================

st.write("")
analyze_button = st.button(
    "🔍 Analyze Resume",
    use_container_width=True,
    type="primary"
)


# ==========================================================
# ANALYSIS
# ==========================================================

if analyze_button:
    # --------------------------------------------
    # Validate input
    # --------------------------------------------
    if resume_file is None:
        st.warning("⚠️ Please upload a resume PDF.")
        st.stop()

    if not job_description.strip():
        st.warning("⚠️ Please enter a job description.")
        st.stop()

    # --------------------------------------------
    # Processing
    # --------------------------------------------
    temp_pdf_path = None
    with st.spinner("Analyzing resume and computing semantic match..."):
        try:
            # Save uploaded PDF temporarily
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:
                temp_file.write(resume_file.getvalue())
                temp_pdf_path = Path(temp_file.name)

            # PDF Extraction
            pdf_data = extract_text_from_pdf(temp_pdf_path)
            extracted_text = pdf_data.get("full_text", "").strip()

            if not extracted_text:
                st.error("⚠️ Could not extract text from the uploaded PDF. Please make sure it is a selectable text PDF, not a scanned image.")
                st.stop()

            # Text Preprocessing
            cleaned_text = clean_resume_text(extracted_text)

            # Resume Sections
            sections = extract_resume_sections(cleaned_text)

            # Create Resume Text
            resume_text = create_resume_text(sections)
            if not resume_text:
                resume_text = cleaned_text

            # Embeddings
            resume_embedding = generate_embedding(resume_text)
            job_embedding = generate_embedding(job_description)

            # Match Score
            similarity_score = calculate_cosine_similarity(
                resume_embedding,
                job_embedding
            )

            match_score = generate_match_score(
                resume_embedding,
                job_embedding
            )

            # Classification
            if match_score >= 70:
                classification = "Strong Match"
                badge_emoji = "🟢"
                score_color = "#4CAF50"
            elif match_score >= 50:
                classification = "Moderate Match"
                badge_emoji = "🟡"
                score_color = "#FFA726"
            else:
                classification = "Weak Match"
                badge_emoji = "🔴"
                score_color = "#EF5350"

            # Skill Extraction
            resume_skills = extract_skills(resume_text)
            job_skills = extract_skills(job_description)

            # Missing Skills
            missing_skills = find_missing_skills(
                resume_skills,
                job_skills
            )

            # Recommendations
            recommendations = recommend_skills(missing_skills)

        except Exception as e:
            st.error(f"Something went wrong during analysis: {e}")
            st.stop()

        finally:
            # Clean up temp file
            if temp_pdf_path and temp_pdf_path.exists():
                try:
                    temp_pdf_path.unlink()
                except Exception:
                    pass

    # ======================================================
    # RESULTS
    # ======================================================

    st.divider()

    st.markdown(
        '<div class="section-title">📊 Resume–Job Analysis Overview</div>',
        unsafe_allow_html=True
    )

    # Score Cards
    score_col1, score_col2 = st.columns(2)

    with score_col1:
        st.markdown(
            f"""
            <div class="score-card">
                <div class="score-card-label">Resume–Job Match Score</div>
                <div class="score-card-value" style="color: {score_color};">
                    {match_score:.1f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with score_col2:
        st.markdown(
            f"""
            <div class="score-card">
                <div class="score-card-label">Compatibility Status</div>
                <div class="score-card-value" style="font-size: 32px; color: {score_color};">
                    {badge_emoji} {classification}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ======================================================
    # SKILLS ANALYSIS
    # ======================================================

    st.markdown(
        '<div class="section-title">🛠️ Skills Analysis</div>',
        unsafe_allow_html=True
    )

    skill_col1, skill_col2 = st.columns(2)

    with skill_col1:
        st.subheader("👨‍💻 Resume Skills Found")
        if resume_skills:
            for skill in resume_skills:
                st.write(f"✅ **{format_skill_name(skill)}**")
        else:
            st.info("No known technical skills detected in the resume.")

    with skill_col2:
        st.subheader("💼 Required Skills (Job Description)")
        if job_skills:
            for skill in job_skills:
                st.write(f"🔹 **{format_skill_name(skill)}**")
        else:
            st.info("No specific technical skills detected in the job description.")

    # ======================================================
    # MISSING SKILLS & RECOMMENDATIONS
    # ======================================================

    st.markdown(
        '<div class="section-title">🔍 Skill Gap & Recommendations</div>',
        unsafe_allow_html=True
    )

    gap_col1, gap_col2 = st.columns(2)

    with gap_col1:
        st.subheader("⚠️ Missing Skills")
        if missing_skills:
            for skill in missing_skills:
                st.warning(f"**{format_skill_name(skill)}**")
        else:
            st.success("🎉 No missing skills detected! Perfect skill overlap.")

    with gap_col2:
        st.subheader("💡 Learning Recommendations")
        if recommendations:
            for skill, recommendation in recommendations.items():
                with st.expander(f"📚 {format_skill_name(skill)}"):
                    st.write(recommendation)
        else:
            st.success("✨ Candidate meets all identified skill requirements.")

    # ======================================================
    # RESUME SECTIONS
    # ======================================================

    st.divider()
    with st.expander("📑 View Extracted Resume Sections"):
        for section, content in sections.items():
            st.markdown(f"### {section.title()}")
            if content:
                st.text(content)
            else:
                st.write("_No content found for this section._")
