# randomcontent/generators/text_generator.py

import random

def generate_text(type="sentence", length=10, words=None):
    """
    Generate random text.
    """
    if words is None:
        words = ["the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog"]
    if type == "sentence":
        return " ".join(random.choices(words, k=length)).capitalize() + "."
    elif type == "paragraph":
        return " ".join(
            generate_text(type="sentence", length=length, words=words) for _ in range(5)
        )
    else:
        raise ValueError("Invalid type. Use 'sentence' or 'paragraph'.")


