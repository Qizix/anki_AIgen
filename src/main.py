import os

import matplotlib.pyplot as plt
import requests
import json
import time
from pathlib import Path

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
        for word in words:
            retries = 0
            while retries < self.max_retries:
                try:
                    response = requests.post(
                        self.api_url,
                        json={
                            "model": "phi4",  # Changed from phi4 to phi
                            "prompt": f"""
                            Take the word "{word}" in "{lang1}" (first language) and "{lang2}" (second language). Create one strict output in the following format:
                            "Sentence with the word translated in brackets.,Original word (translated word in {lang2}), synonym1, synonym2."
                            
                            Instructions:
                            - Write a short sentence in {lang1} using the word "{word}" but translate "{word}" into {lang2} and place it in brackets.
                            - After the sentence, write the original word from {lang1} and its translation in {lang2}, then list a few synonyms separated by commas.
                            - Do not output anything else, strictly follow the exact format.
                            
                            Example:
                            
                            Input:
                            word = go, lang1 = English, lang2 = Ukrainian
                            
                            Output:
                            We decided to [піти] for a walk in the park.,Go (піти), move, proceed, travel.
                            
                            Input:
                            word = see, lang1 = English, lang2 = Ukrainian
                            
                            Output:
                            He [бачив] a strange bird in the garden.,See (бачив), watch, look, observe.
                            """,
                            "stream": False
                        },
                        verify=False  # Disable SSL verification
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        generated_text = result.get('response', '')
                        if generated_text:
                            cards.append(generated_text)
                            break
                    retries += 1
                    time.sleep(1)
                    
                except requests.exceptions.RequestException as e:
                    print(f"Error processing word '{word}' (attempt {retries + 1}/{self.max_retries}): {str(e)}")
                    retries += 1
                    time.sleep(1)
                    
            if retries == self.max_retries:
                print(f"Failed to process word '{word}' after {self.max_retries} attempts")
                
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
    
    # Fixed languages for this use case
    language1 = 'english'
    language2 = 'ukrainian'
    
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
    print(f"Generating cards for {len(words_to_process)} words...")
    generated_cards = llm_handler.generate_cards(words_to_process, language1, language2)
    
    # Save output
    if generated_cards:
        save_output(generated_cards, output_file)
        print(f"Generated {len(generated_cards)} cards. Saved to {output_file}")
    else:
        print("No cards were generated.")

if __name__ == "__main__":
    main()