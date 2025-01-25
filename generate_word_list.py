import sys
import time
from pathlib import Path

import requests


class WordListGenerator:
    def __init__(self):
        self.port = 11435
        self.api_url = f"http://localhost:{self.port}/api/generate"
        self.max_retries = 3
        self.generated_words = set()  # Зберігання всіх згенерованих слів

    def check_ollama_service(self):
        try:
            response = requests.get(f"http://localhost:{self.port}/api/tags")
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False

    def generate_word_list(self, prompt: str, output_file: str):
        if not self.check_ollama_service():
            print("Error: Ollama service is not running. Please start it with 'ollama serve'")
            return

        retries = 0
        while retries < self.max_retries:
            try:
                response = requests.post(
                    self.api_url,
                    json={
                        "model": "phi4",
                        "prompt": prompt,
                        "stream": False
                    },
                    verify=False  # Disable SSL verification
                )

                if response.status_code == 200:
                    result = response.json()
                    words = result.get('response', '').strip().splitlines()
                    unique_words = [word for word in words if word not in self.generated_words]
                    self.generated_words.update(unique_words)  # Додаємо унікальні слова до списку
                    if unique_words:
                        self.save_to_file(unique_words, output_file)
                        print(f"Word list generated and saved to {output_file}")
                        return
                retries += 1
                time.sleep(1)

            except requests.exceptions.RequestException as e:
                print(f"Error generating word list (attempt {retries + 1}/{self.max_retries}): {str(e)}")
                retries += 1
                time.sleep(1)

        print("Failed to generate word list after multiple attempts.")

    @staticmethod
    def save_to_file(words: list, file_path: str):
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'a', encoding='utf-8') as f:
            for word in words:
                f.write(f"{word}\n")

def remove_duplicates(file_path: str):
    """
    Removes duplicate words from the given file and overwrites it with a unique word list.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            words = f.readlines()

        # Use a set to eliminate duplicates while maintaining order
        unique_words = list(dict.fromkeys(word.strip() for word in words))

        with open(file_path, 'w', encoding='utf-8') as f:
            for word in unique_words:
                f.write(f"{word}\n")

        print(f"Duplicates removed. Final unique word count: {len(unique_words)}")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred while removing duplicates: {e}")


def main():
    # Set up the output file location
    output_file = "input/word_lists/generated_words.txt"
    language1 = sys.argv[1] if len(sys.argv) > 1 else 'english'
    words_count = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    batches = (words_count + 49) // 50  # Calculate the number of batches of 50 words each
    # Initialize the generator
    generator = WordListGenerator()
    for batch in range(batches):
        # Define a prompt for each batch
        prompt = f"""
        You are both a **Language Dictionary** and an experienced **Language Teacher** specializing in crafting optimized vocabulary lists for language learners. Your task is to generate a word list perfect for learning.
        
        1. **Words**: Provide exactly 50 commonly used words in the specified language. These words should:
           - Be **useful for everyday conversations**.
           - Represent **diverse categories** (nouns, verbs, adjectives, adverbs).
           - Contain a mix of both **simple** and **slightly advanced words** to support progressive learning.
        
        2. **Strict Requirements**:
           - Do NOT number the words or group them into categories.
           - Do NOT add titles, headers, bullet points, or any extra structure or formatting.
           - Avoid any additional commentary, notes, or explanations.
        
        3. **Output Format**:
           - Provide the words as a **plain text list**, with each word or short phrase on a **new line**.
           - Example of the required output for English:
             ```
             apple
             run
             beautiful
             quickly
             good morning
             thanks
             ...
             ```
        
        4. **Avoid Repetition**:
           - Do not repeat any of the following words: {', '.join(generator.generated_words)}.
        
        Just list the words or phrases in the correct format. No categories, no decoration—only the plain list, as shown in the example.
        Donot add any additional information or comments. Do not add any extra sentences. Do not ask questions. Do not add notes.
        """
        # Generate the word list for the current batch
        generator.generate_word_list(prompt, output_file)
        remove_duplicates(output_file)


if __name__ == "__main__":
    main()