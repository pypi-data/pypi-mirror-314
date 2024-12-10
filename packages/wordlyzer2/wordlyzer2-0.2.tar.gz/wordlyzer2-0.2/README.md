# Wordlyzer

Wordlyzer is a powerful Python library for text analysis, providing comprehensive insights into text metrics and properties.

## Installation

Install Wordlyzer using pip:

```bash
pip install wordlyzer==0.2
```

## Features

- Word count analysis
- Sentence count calculation
- Paragraph count detection
- Character count measurement
- Most common words identification
- Average word length computation
- Average sentence length calculation

## Quick Start

```python
# File: main.py
from wordlyzer import WordLyzer

# Example text for analysis
text = """Python is an amazing programming language. It's widely used for web development, data analysis, and AI.

This is a second paragraph."""

# Create analyzer object
analyzer = WordLyzer(text)

# Display analysis results
print("Word Count:", analyzer.word_count())
print("Sentence Count:", analyzer.sentence_count())
print("Paragraph Count:", analyzer.paragraph_count())
print("Character Count:", analyzer.character_count())
print("Most Common Words:", analyzer.most_common_words())
print("Average Word Length:", analyzer.average_word_length())
print("Average Sentence Length:", analyzer.average_sentence_length())
```

## Methods

### `word_count()`
Returns the total number of words in the text.

### `sentence_count()`
Returns the number of sentences in the text.

### `paragraph_count()`
Returns the number of paragraphs in the text.

### `character_count()`
Returns the total number of characters in the text.

### `most_common_words(n=5)`
Returns the `n` most frequently occurring words in the text.
- Default is top 5 words
- Optional parameter to specify number of words

### `average_word_length()`
Calculates the average length of words in the text.

### `average_sentence_length()`
Calculates the average number of words per sentence.

## Requirements

- Python 3.7+
- No external dependencies

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

[Nurico Vicyyanto]

## Support

For issues or questions, please open an issue on our GitHub repository.
