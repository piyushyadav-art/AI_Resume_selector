from pathlib import Path

from src.pdf_parser import extract_text_from_pdf
from src.preprocessing import clean_resume_text
from src.resume_parser import extract_resume_sections, format_resume_sections
from src.embeddings import (
    create_resume_text,
    generate_embedding,
    read_job_description,
)
from src.similarity import calculate_cosine_similarity,generate_match_score
from src.skill_extractor import extract_skills, find_missing_skills
from src.recommendations import recommend_skills

BASE_DIR = Path(__file__).resolve().parent
pdf_path = BASE_DIR / "data" / "resume" / "Piyush_Yadav_Resume_Modern.pdf"
# pdf_path = BASE_DIR / "data" / "resume" / "Ashish_resume3.pdf"
job_path = BASE_DIR / "data" / "jobs" / "job_002.txt"

# 1. Ensure job description file exists
if not job_path.exists():
    job_path.parent.mkdir(parents=True, exist_ok=True)
    job_path.write_text(
        "Required Skills: Maintenance of centrifugal pumps, logbook management, "
        "preventive maintenance, and oil and gas equipment operation.",
        encoding="utf-8",
    )
    print(f"Created missing job description at: {job_path}")

# 2. Extract & Preprocess Resume
print("Starting PDF extraction...")
pdf_data = extract_text_from_pdf(pdf_path)
cleaned_text = clean_resume_text(pdf_data["full_text"])

print("\n========== CLEANED RESUME TEXT ==========\n")
# print(cleaned_text)

sections = extract_resume_sections(cleaned_text)

print("\n========== PARSED RESUME SECTIONS ==========\n")
print(format_resume_sections(sections))

# 3. Create combined resume text & generate embedding
resume_text = create_resume_text(sections)
resume_embedding = generate_embedding(resume_text)

print("\n========== RESUME EMBEDDING ==========\n")
print("Embedding type:", type(resume_embedding))
print("Embedding shape:", resume_embedding.shape)
print("First 10 values:", resume_embedding[:10])

# 4. Load Job Description & generate embedding
job_text = read_job_description(job_path)

print("\n========== JOB DESCRIPTION ==========\n")
print(job_text)

job_embedding = generate_embedding(job_text)

print("\n========== JOB EMBEDDING ==========\n")
print("Embedding shape:", job_embedding.shape)
print("First 10 values:", job_embedding[:10])

# 5. Calculate Similarity & Output Match Result
similarity_score = calculate_cosine_similarity(resume_embedding, job_embedding)

print("\n========== MATCH RESULT ==========\n")
print(f"Cosine similarity: {float(similarity_score):.4f}")
print(f"Semantic similarity: {float(similarity_score) * 100:.2f} %")

def classify_candidate(similarity_score):
    if similarity_score >= 0.7:
        return "Strong Match"
    elif similarity_score >= 0.5:
        return "Moderate Match"
    else:
        return "Weak Match"

print("Classification: ", classify_candidate(similarity_score))


# ================================ADDITIONAL====================================
match_score = generate_match_score(
    resume_embedding,
    job_embedding
)

print("\n========== MATCH SCORE ==========")
print(f"Resume - Job Match Score: {match_score}%")


resume_skills = extract_skills(resume_text)
print("\n========== RESUME SKILLS ==========")
if resume_skills:
    for skill in resume_skills:
        print("-", skill)
else:
    print("(No known skills detected in resume)")

job_skills = extract_skills(job_text)
print("\n========== JOB REQUIRED SKILLS ==========")
if job_skills:
    for skill in job_skills:
        print("-", skill)
else:
    print("(No known skills detected in job description)")

missing_skills = find_missing_skills(
    resume_skills,
    job_skills
)
print("\n========== MISSING SKILLS ==========")
if missing_skills:
    for skill in missing_skills:
        print("-", skill)
else:
    print("(No missing skills - perfect skill match!)")

recommendations = recommend_skills(missing_skills)
print("\n========== SKILL RECOMMENDATIONS ==========")
if recommendations:
    for skill, recommendation in recommendations.items():
        print(f"\n{skill.upper()}:")
        print(recommendation)
else:
    print("(No recommendations needed)")

    