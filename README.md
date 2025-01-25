# README.md

# Anki Dataset Generator

This project is designed to generate language datasets for Anki using an open-source LLM model. The application takes user input for two languages and optional custom words, processes this input, and outputs a text file formatted for Anki.

## Project Structure

```
anki-dataset-generator
├── src
│   ├── main.py                # Entry point of the application
│   ├── models
│   │   └── llm_handler.py     # Interacts with the LLM model
│   ├── utils
│   │   ├── anki_formatter.py   # Formats generated cards for Anki
│   │   └── language_processor.py # Processes input words and validates languages
│   └── config
│       └── model_config.py     # Configuration settings for the LLM model
├── input
│   └── word_lists
│       └── custom_words.txt    # Custom words for processing
├── output
│   └── anki_cards.txt          # Output file with generated Anki cards
├── requirements.txt             # Project dependencies
├── .env                         # Environment variables
└── README.md                    # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd anki-dataset-generator
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables in the `.env` file.

## Usage

1. Prepare your custom words in `input/word_lists/custom_words.txt`.
2. Run the application:
   ```
   python src/main.py
   ```
3. The generated Anki cards will be saved in `output/anki_cards.txt`.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.