def is_valid_paragraph(text: str, min_words: int) -> bool:
    """
    Validates if a paragraph has the required minimum number of words.
    """
    if not text or not text.strip():
        return False
        
    words = text.split()
    return len(words) >= min_words
