import time
from pathlib import Path

import requests
import sys


class LLMHandler:
    def __init__(self):
        self.port = 11435
        self.api_url = f"http://localhost:{self.port}/api/generate"  # Changed from https to http
        self.max_retries = 1

    def check_ollama_service(self):
        try:
            response = requests.get(f"http://localhost:{self.port}/api/tags")
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False

    def generate_cards(self, words: list, lang1: str, lang2: str) -> list:
        if not self.check_ollama_service():
            print("Error: Ollama service is not running. Please start it with 'ollama serve'")
            return []

        cards = []
        batch_size = 15
        epochs = len(words) // batch_size + 1
        print(f"Generating cards for {len(words)} words in {epochs} epochs...")

        for epoch in range(epochs):
            batch = words[epoch * batch_size: (epoch + 1) * batch_size]
            retries = 0
            while retries < self.max_retries:
                try:
                    response = requests.post(
                        self.api_url,
                        json={
                            "model": "phi4",
                            "prompt": f"""
                            Take the following list of words in "{lang1}" and translate them to "{lang2}". For each word, perform the following steps:
                            1. Write a short sentence in "{lang1}" using the word, but translate the word into "{lang2}" and place it in brackets.
                            2. After the sentence, write the original word from "{lang1}" and its translation in "{lang2}", followed by a few synonyms separated by commas.
                            Follow this structure:
                            '''
                            Sentence with translated word1.;Original word (translated word1), synonym1, synonym2.
                            Sentence with translated word2.;Original word (translated word2), synonym1, synonym2.
                            Sentence with translated word3.;Original word (translated word3), synonym1, synonym2.
                            '''
                            Generate output strictly. Leave nothing else except for the structure. Do not add any additional information. Do not add any extra sentences. Do not ask questions.
                            Input:
                            Words = {[batch]}
                            Lang1 = {lang1}
                            Lang2 = {lang2}
                            """,
                            "stream": False
                        },
                        verify=False  # Disable SSL verification
                    )

                    if response.status_code == 200:
                        result = response.json()
                        generated_text = result.get('response', '')
                        if generated_text:
                            cards.extend(generated_text.strip().splitlines())  # Ensure cards are processed as lines
                            break
                    retries += 1
                    time.sleep(1)

                except requests.exceptions.RequestException as e:
                    print(
                        f"Error processing batch '{epoch + 1}/{epochs}' (attempt {retries + 1}/{self.max_retries}): {str(e)}")
                    retries += 1
                    time.sleep(1)
        return cards

def read_input_words(file_path: str) -> list:
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Input file not found: {file_path}")
        return []

def save_output(cards: list, file_path: str):
    with open(file_path, 'w', encoding='utf-8') as f:
        for card in cards:
            f.write(f"{card}\n")

def main():
    # Setup paths
    input_file = "input/word_lists/custom_words.txt"
    output_file = "output/anki_cards.txt"
    
    # Create directories if they don't exist
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Language selection via terminal arguments
    language1 = sys.argv[1] if len(sys.argv) > 1 else 'english'
    language2 = sys.argv[2] if len(sys.argv) > 2 else 'ukrainian'

    # Read input words
    words_to_process = read_input_words(input_file)
    if not words_to_process:
        print("No words to process. Exiting.")
        return
    
    # Initialize LLM handler
    llm_handler = LLMHandler()
    if not llm_handler.check_ollama_service():
        print("Please start Ollama service with:\n$ ollama serve")
        return
    
    # Generate cards
    generated_cards = llm_handler.generate_cards(words_to_process, language1, language2)
    
    # Save output
    if generated_cards:
        save_output(generated_cards, output_file)
        print(f"Generated {len(generated_cards)} cards. Saved to {output_file}")
    else:
        print("No cards were generated.")

if __name__ == "__main__":
    main()