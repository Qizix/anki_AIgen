def process_input_words(input_words):
    # Process and format the input words for Anki
    processed_words = [word.strip() for word in input_words if word.strip()]
    return processed_words

def validate_languages(language1, language2):
    # Validate the provided languages
    valid_languages = ['English', 'Spanish', 'French', 'German', 'Chinese', 'Japanese', 'Russian']
    if language1 not in valid_languages or language2 not in valid_languages:
        raise ValueError(f"Languages must be one of the following: {', '.join(valid_languages)}")
    return True