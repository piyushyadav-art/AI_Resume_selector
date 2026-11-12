import re

SKILL_DISPLAY_NAMES = {
    "aws": "AWS",
    "azure": "Azure",
    "c#": "C#",
    "c++": "C++",
    "css": "CSS",
    "django": "Django",
    "docker": "Docker",
    "fastapi": "FastAPI",
    "flask": "Flask",
    "git": "Git",
    "github": "GitHub",
    "html": "HTML",
    "java": "Java",
    "javascript": "JavaScript",
    "kubernetes": "Kubernetes",
    "langchain": "LangChain",
    "langgraph": "LangGraph",
    "matplotlib": "Matplotlib",
    "mongodb": "MongoDB",
    "mysql": "MySQL",
    "nlp": "NLP",
    "node.js": "Node.js",
    "numpy": "NumPy",
    "pandas": "Pandas",
    "postgresql": "PostgreSQL",
    "pytorch": "PyTorch",
    "react": "React",
    "scikit-learn": "scikit-learn",
    "sql": "SQL",
    "tensorflow": "TensorFlow",
    "typescript": "TypeScript",
}

KNOWN_SKILLS = [
    # Programming & Web Development
    "python",
    "java",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "html",
    "css",
    "react",
    "node.js",
    "fastapi",
    "flask",
    "django",
    "web development",

    # Databases & Cloud / DevOps
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "git",
    "github",

    # AI, Data Science & Machine Learning
    "numpy",
    "pandas",
    "matplotlib",
    "scikit-learn",
    "pytorch",
    "tensorflow",
    "machine learning",
    "deep learning",
    "nlp",
    "natural language processing",
    "computer vision",
    "langchain",
    "langgraph",
    "data analysis",

    # Mechanical, Maintenance & Industrial Operations
    "centrifugal pumps",
    "preventive maintenance",
    "routine greasing",
    "greasing",
    "filter cleaning",
    "strainer filter cleaning",
    "lube oil filling",
    "troubleshooting",
    "oil and gas",
    "logbook management",
    "equipment maintenance",
    "plant operations",
    "pumps",
    "valves",
    "compressors",
    "hydraulic systems",
    "pneumatic systems",

    # Soft Skills & Management
    "team collaboration",
    "problem solving",
    "project management",
    "innovative thinking",
]


def format_skill_name(skill):
    """
    Formats a skill name into its standard capitalized/branded display name.
    """
    return SKILL_DISPLAY_NAMES.get(skill.lower(), skill.title())


def skill_pattern(skill):
    """
    Creates a regex pattern matching whole words or phrases for a given skill.
    """
    escaped = re.escape(skill)
    if skill[0].isalnum() and skill[-1].isalnum():
        return rf"\b{escaped}\b"
    return rf"(?<![a-zA-Z0-9]){escaped}(?![a-zA-Z0-9])"


def extract_skills(text):
    """
    Extracts known skills from the provided text using case-insensitive matching.
    Returns a list of lowercase skill names.
    """
    if not text:
        return []

    text_lower = text.lower()
    found_skills = []

    for skill in KNOWN_SKILLS:
        if re.search(skill_pattern(skill), text_lower):
            found_skills.append(skill)

    return found_skills


def find_missing_skills(resume_skills, job_skills):
    """
    Finds skills that are required by the job but missing from the resume.
    """
    resume_set = {s.lower() for s in resume_skills}
    job_set = {s.lower() for s in job_skills}

    missing_skills = job_set - resume_set
    return sorted(list(missing_skills))