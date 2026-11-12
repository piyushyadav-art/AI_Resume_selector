import re
from src.skill_extractor import KNOWN_SKILLS, format_skill_name, skill_pattern


SECTION_NAMES = {
    "skills": [
        "skills",
        "technical skills",
        "technical skill",
        "core skills",
        "key skills",
        "key deliverables"
    ],

    "education": [
        "education",
        "education and training",
        "academic background",
        "academic qualification",
        "acadmic qualification",
        "qualifications"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "responsibilities"
    ],

    "projects": [
        "projects",
        "personal projects",
        "academic projects",
        "project experience"
    ],

    "certifications": [
        "certifications",
        "certificates",
        "licenses"
    ],

    "achievements": [
        "achievements",
        "accomplishments",
        "awards"
    ],

    "other": [
        "summary",
        "career objective",
        "personal profile",
        "declaration",
        "declleration"
    ]
}

OUTPUT_SECTIONS = ["skills", "education", "projects", "experience"]


def normalize_heading(text):
    return re.sub(r"[^a-z0-9\s]", "", text.lower()).strip()


def detect_section(line):
    normalized_line = normalize_heading(line)
    for section, keywords in SECTION_NAMES.items():
        for keyword in keywords:
            normalized_keyword = normalize_heading(keyword)
            if normalized_line == normalized_keyword:
                return section

    return None


def extract_known_skills(text):
    """
    Finds known technical skills mentioned in cleaned resume text.
    """
    normalized_text = text.lower()
    found_skills = [
        format_skill_name(skill)
        for skill in KNOWN_SKILLS
        if re.search(skill_pattern(skill), normalized_text)
    ]

    return found_skills


def normalize_content(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def deduplicate_lines(lines):
    deduplicated_lines = []
    seen_lines = set()

    for line in lines:
        normalized_line = normalize_content(line)
        if normalized_line and normalized_line not in seen_lines:
            deduplicated_lines.append(line)
            seen_lines.add(normalized_line)

    return deduplicated_lines


def extract_resume_sections(text):
    """
    Splits cleaned resume text into important resume sections.
    """
    sections = {section: [] for section in OUTPUT_SECTIONS}
    current_section = None

    for line in text.splitlines():
        detected_section = detect_section(line)

        if detected_section:
            current_section = detected_section
            continue

        if current_section in sections:
            sections[current_section].append(line)

    known_skills = extract_known_skills(text)
    if known_skills:
        sections["skills"] = deduplicate_lines(known_skills + sections["skills"])

    return {
        section: "\n".join(lines).strip()
        for section, lines in sections.items()
    }


def format_resume_sections(sections):
    """
    Formats parsed resume sections for console output.
    """
    output = []

    for section in OUTPUT_SECTIONS:
        content = sections.get(section, "")
        output.append(f"===== {section.upper()} =====")
        output.append("")
        output.append(content if content else "No content found.")
        output.append("")

    return "\n".join(output).strip()


def extract_skills(text):
    """
    Backward-compatible wrapper for earlier versions.
    """
    return {
        "skills": "\n".join(extract_known_skills(text))
    }
