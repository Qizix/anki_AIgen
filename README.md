# LLM-Based Flashcard Generator
## Description

This project was designed to address the challenge of creating high-quality flashcards for language learning in Anki. It
leverages a self-hosted LLM model to efficiently process and transform word lists into the desired flashcard format.
## Requirements
- Python 3.12 or later
- [Ollama](https://ollama.com/) service running locally (used to process and generate LLM output)
- Dependencies: Install using `pip`
``` bash
  pip install requests
```
## Installation
1. Clone the repository.
2. Install dependencies:
``` bash
   pip install -r requirements.txt
```
1. Ensure the Ollama service is running locally:
``` bash
   ollama serve
```
## Usage
1. **Prepare Input File**:
    - Place a text file with a list of words (one word per line) in the `input/word_lists/` directory, e.g., `custom_words.txt`.
    - Example:
``` 
     apple
     run
     love
```
1. **Run the Script**: Execute the program using:
``` bash
   python main.py
```
1. **Output**:
    - The program will generate an output file in the `output/` directory named `anki_cards.txt`.
    - Example output:
``` 
     Sentence with translated word1.;Original word1 (translated word1), synonym1, synonym2.
     Sentence with translated word2.;Original word2 (translated word2), synonym1, synonym2.
```
## Project Structure
``` 
.
├── main.py                     # Main script to execute the program
├── input/                      # Input directory containing word lists
│   └── word_lists/
│       └── custom_words.txt    # Example input file with words to process
├── output/                     # Output directory for results
│   └── anki_cards.txt          # Generated flashcards
├── README.md                   # Project documentation
└── requirements.txt            # Dependencies
```
## Configuration
- **Languages**: Update `language1` and `language2` variables in the `main()` function for custom language translation.
- **Batch Size**: Modify the `batch_size` parameter in the `LLMHandler.generate_cards` method for custom batch sizes.
- **Max Retries**: Adapt the `max_retries` parameter within the `LLMHandler` class for handling retries when contacting the LLM service.

## Error Handling
- If the input file does not exist or is improperly formatted, the program will notify the user and exit gracefully.
- If the Ollama service is not running, the program will display a message to start it:
``` bash
  $ ollama serve
```
## Example Use Case
If you want to build an English-to-Ukrainian vocabulary flashcard deck:
1. Add a list of English words to `custom_words.txt`.
2. Run the program to generate translations and synonyms.
3. Import the `anki_cards.txt` into Anki or a similar flashcard app.

Feel free to contribute or raise issues for further development ideas!
