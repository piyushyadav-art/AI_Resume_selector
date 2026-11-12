import re


def clean_resume_text(extracted_text):
    """
    Cleans resume text while preserving line structure.
    """
    if not isinstance(extracted_text, str):
        return ""

    text = extracted_text.replace("\xa0", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    text = re.sub(
        r"page\s+\d+\s*(of\s+\d+)?",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Keep useful resume/programming characters.
    # Ampersands are intentionally removed, matching the expected cleaned output.
    text = re.sub(
        r"[^\w\s@.+#/\-:,()%]",
        " ",
        text
    )

    text = re.sub(r"[ \t]+", " ", text)

    lines = []
    for line in text.split("\n"):
        line = line.strip()
        if line:
            lines.append(line)

    return "\n".join(lines).strip()
