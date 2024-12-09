# randomcontent/generators/text_generator.py
import random
import string

def generate_text(type="sentence", length=10, words=None, num_lines=5):
    """
    Generate random text of different types.
    
    Parameters:
        type (str): Type of text to generate ('sentence', 'paragraph', 'word', 'random_text', 'letter', 'poem', etc.).
        length (int): Length of the sentence or number of words in a sentence (used for 'sentence' and 'random_text').
        words (list): Custom list of words for sentence generation.
        num_lines (int): Number of lines for a paragraph (used for 'paragraph' and 'poem').
        
    Returns:
        Generated text based on the specified type.
    """
    if words is None:
        words = ["the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog"]
    
    # Generate a random sentence
    if type == "sentence":
        return " ".join(random.choices(words, k=length)).capitalize() + "."
    
    # Generate a random paragraph
    elif type == "paragraph":
        return " ".join(generate_text(type="sentence", length=length, words=words) for _ in range(num_lines))
    
    # Generate a single random word
    elif type == "word":
        return random.choice(words)
    
    # Generate random text (sequence of words)
    elif type == "random_text":
        return " ".join(random.choices(words, k=length))
    
    # Generate a random letter (uppercase or lowercase)
    elif type == "letter":
        return random.choice(string.ascii_letters)
    
    # Generate a simple poem (random lines with some rhyme pattern or randomness)
    elif type == "poem":
        poem_lines = []
        for _ in range(num_lines):
            line = " ".join(random.choices(words, k=length))
            poem_lines.append(line.capitalize())
        return "\n".join(poem_lines)
    
    # Generate a random title (capitalized sentence)
    elif type == "title":
        return generate_text(type="sentence", length=length).capitalize()
    
    # Generate a sentence with special characters (random punctuation added)
    elif type == "sentence_with_special_characters":
        sentence = " ".join(random.choices(words, k=length)).capitalize()
        punctuation = random.choice([".", "!", "?", "...", "-"])
        return sentence + punctuation
    
    # Generate a paragraph with line breaks
    elif type == "paragraph_with_formatting":
        return "\n".join(generate_text(type="sentence", length=length, words=words) for _ in range(num_lines))
    
    else:
        raise ValueError("Invalid type. Use 'sentence', 'paragraph', 'word', 'random_text', 'letter', 'poem', 'title', 'sentence_with_special_characters', or 'paragraph_with_formatting'.")
