import math
import re
from collections import Counter
import numpy as np


def tokenize(text):
    """
    Converts text into lowercase word tokens for similarity matching.
    """
    return re.findall(r"[a-z0-9]+", text.lower())


def text_to_vector(text):
    """
    Builds a simple bag-of-words vector from text.
    """
    return Counter(tokenize(text))


def cosine_similarity(first_text, second_text):
    """
    Calculates cosine similarity between two text strings using bag-of-words.
    Returns a value between 0.0 and 1.0.
    """
    first_vector = text_to_vector(first_text)
    second_vector = text_to_vector(second_text)

    common_words = set(first_vector) & set(second_vector)
    dot_product = sum(first_vector[word] * second_vector[word] for word in common_words)

    first_length = math.sqrt(sum(value * value for value in first_vector.values()))
    second_length = math.sqrt(sum(value * value for value in second_vector.values()))

    if first_length == 0 or second_length == 0:
        return 0.0

    return float(dot_product / (first_length * second_length))


def calculate_cosine_similarity(first_vector, second_vector):
    """
    Calculates cosine similarity between two numeric vectors.
    """
    first_arr = np.asarray(first_vector, dtype=float)
    second_arr = np.asarray(second_vector, dtype=float)

    dot_product = np.dot(first_arr, second_arr)
    first_norm = np.linalg.norm(first_arr)
    second_norm = np.linalg.norm(second_arr)

    if first_norm == 0 or second_norm == 0:
        return 0.0

    return float(dot_product / (first_norm * second_norm))


def calculate_similarity(resume_embedding, job_embedding):
    """
    Calculates similarity between resume and job embeddings using cosine similarity.
    """
    return calculate_cosine_similarity(resume_embedding, job_embedding)


def generate_match_score(resume_embedding, job_embedding):
    """
    Generates a percentage match score (0.0 to 100.0) rounded to 2 decimal places.
    """
    similarity = calculate_similarity(
        resume_embedding,
        job_embedding
    )
    score = round(float(similarity) * 100, 2)
    return max(0.0, min(100.0, score))


def format_match_result(score):
    """
    Formats a similarity score for console output.
    """
    return (
        "========== MATCH RESULT ==========\n\n"
        f"Cosine similarity: {score:.4f}\n"
        f"Semantic similarity: {score * 100:.2f} %"
    )