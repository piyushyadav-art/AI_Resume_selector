from pathlib import Path

_MODEL_CACHE = {}


def get_embedding_model(model_name="all-MiniLM-L6-v2", local_files_only=True):
    """
    Returns a cached SentenceTransformer model instance to avoid reloading weights repeatedly.
    """
    cache_key = (model_name, local_files_only)
    if cache_key in _MODEL_CACHE:
        return _MODEL_CACHE[cache_key]

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise ImportError(
            "sentence-transformers is not installed. Install it before using "
            "generate_embedding(), or use src.similarity.cosine_similarity()."
        ) from exc

    try:
        model = SentenceTransformer(model_name, local_files_only=local_files_only)
    except Exception:
        # Fallback to downloading if local files only was requested but not found
        model = SentenceTransformer(model_name, local_files_only=False)

    _MODEL_CACHE[cache_key] = model
    return model


def create_resume_text(sections):
    """
    Combines parsed resume sections into one text block for matching.
    """
    section_order = [
        "skills",
        "education",
        "experience",
        "projects",
        "certifications",
        "achievements",
    ]

    parts = []
    for section in section_order:
        content = sections.get(section, "")
        if content:
            parts.append(f"{section.title()}:\n{content}")

    return "\n\n".join(parts).strip()


def generate_embedding(text, model_name="all-MiniLM-L6-v2", local_files_only=True):
    """
    Generates a normalized sentence-transformer embedding.
    """
    if not text or not text.strip():
        text = " "

    model = get_embedding_model(model_name=model_name, local_files_only=local_files_only)
    return model.encode(text, normalize_embeddings=True)


def generate_embeddings(text, model_name="all-MiniLM-L6-v2", local_files_only=True):
    """
    Backward-compatible plural alias.
    """
    return generate_embedding(text, model_name, local_files_only)


def read_job_description(file_path):
    """
    Reads a job description text file.
    """
    return Path(file_path).read_text(encoding="utf-8")
