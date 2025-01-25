# LLM-Based Flashcard Generator
## Updated Description
This project allows the creation of high-quality flashcards for language learning in Anki. It leverages a self-hosted LLM model to efficiently process and transform word lists into flashcard format. Users can now specify the source (`lang1`) and target (`lang2`) languages directly from the terminal during script execution.
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
1. **Run the Script**:
    - To run the program, specify the source language (`lang1`) and target language (`lang2`) in the terminal **or** fall back to default values.
    - Examples:
        - **With specified languages**:
``` bash
        python main.py english spanish
```
- **With default languages** (`english` as `lang1`, `ukrainian` as `lang2`):
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
- **Languages**: Now, you can specify the source (`lang1`) and target (`lang2`) languages during script execution as shown above.
- **Batch Size**: Modify the `batch_size` parameter in the `LLMHandler.generate_cards` method for custom batch sizes.
- **Max Retries**: Adjust the `max_retries` parameter within the `LLMHandler` class to handle retries when contacting the LLM service.

## Error Handling
- If the input file does not exist or is improperly formatted, the program will notify the user and exit gracefully.
- If the Ollama service is not running, the program will display a message to start it:
``` bash
  $ ollama serve
```
## Example Use Case
To create an English-to-Spanish vocabulary flashcard deck:
1. Add a list of English words to `custom_words.txt`.
2. Run the program with specified languages:
``` bash
   python main.py english spanish
```
1. Import the `anki_cards.txt` into Anki or another flashcard application.

## Notes
Feel free to contribute or raise issues for further development ideas!
