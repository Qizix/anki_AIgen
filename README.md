# LLM-Based Flashcard Generator
## Updated Description
This project allows the creation of high-quality flashcards for language learning in Anki. It leverages a self-hosted LLM model to efficiently process and transform word lists into flashcard format. Users can now specify the source (`lang1`) and target (`lang2`) languages directly from the terminal during script execution.

Additionally, a new script `generate_word_list.py` is included for generating unique and optimized word lists for language learning.

---

## Requirements
- Python 3.12 or later
- [Ollama](https://ollama.com/) service running locally (used to process and generate LLM output)
- Dependencies: Install using `pip`
```bash
  pip install requests
```

---

## Installation
1. Clone the repository.
2. Install dependencies:
```bash
   pip install -r requirements.txt
```
3. Ensure the Ollama service is running locally:
```bash
   ollama serve
```

---

## Usage

### Generating Word Lists using the `#symbol:generate_word_list.py` Script
The `generate_word_list.py` script is designed to generate structured, diverse, and useful word lists for language learners. This tool ensures no duplicates in the final output through an automated cleaning process.

**Steps to Use:**
1. Run the script in the terminal with optional parameters for the desired source language and the total number of words.
   - **Source language**: Specify the language for which the word list is generated (default: `english`).
   - **Word count**: Total number of words to be generated (default: `50`).

   **Examples**:
   - Generating 100 English words:
     ```bash
     python generate_word_list.py english 100
     ```

   - Using default settings (50 English words):
     ```bash
     python generate_word_list.py
     ```

2. The output will be saved as `generated_words.txt` in the `input/word_lists/` directory.

---

### Features of the Word Generation Script:
- **Automatic Duplicate Removal**:
  - After generating each batch of words, the script ensures uniqueness by removing any repeated entries.
  - This feature is integrated into the script and requires no manual action.
  
- **Diverse Word Lists**:
  - Words represent a range of categories such as nouns, verbs, adjectives, and adverbs.
  - Useful for conversations and progressive learning.

- **Customizable**:
  - Adjust parameters for the total word count and source language as needed.

---

### Workflow for the Full Flashcard Generation:
1. **Using `generate_word_list.py`**:
   - Generate a unique word list for the desired source language.
   - The cleaned list is saved in the `input/word_lists/` folder.

2. **Using the Main Script (`main.py`)**:
   - Feed the generated word list into `main.py` to create flashcards.
   - Specify the source (`lang1`) and target (`lang2`) languages for flashcard generation.

---

### Example Workflow:
1. Generate 100 English words using `generate_word_list.py`:
   ```bash
   python generate_word_list.py english 100
   ```

2. Use the generated word list to create English-to-Spanish flashcards:
   ```bash
   python main.py english spanish
   ```

3. The flashcards are saved in the `output` directory as `anki_cards.txt`.

---

## Project Structure
```plaintext
.
├── main.py                     # Main script to execute the program
├── generate_word_list.py        # Script to generate and clean word lists
├── input/                      # Input directory containing word lists
│   └── word_lists/
│       └── generated_words.txt # File with generated unique word lists
├── output/                     # Output directory for results
│   └── anki_cards.txt          # Generated flashcards
├── README.md                   # Project documentation
└── requirements.txt            # Dependencies
```

---

## Notes
Feel free to contribute or raise issues for further development ideas!