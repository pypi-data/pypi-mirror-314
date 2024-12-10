# File: textinfo.py

import re
from collections import Counter

class WordLyzer:
    """A simple library for text analysis."""

    def __init__(self, text):
        self.text = text
        self.words = self._get_words()
        self.sentences = self._get_sentences()
        self.paragraphs = self._get_paragraphs()

    def _get_words(self):
        """Extract words from the text."""
        return re.findall(r'\b\w+\b', self.text.lower())

    def _get_sentences(self):
        """Split the text into sentences."""
        return re.split(r'[.!?]+', self.text)

    def _get_paragraphs(self):
        """Split the text into paragraphs."""
        return self.text.split('\n\n')

    def word_count(self):
        """Count the total number of words."""
        return len(self.words)

    def sentence_count(self):
        """Count the total number of sentences."""
        return len([s for s in self.sentences if s.strip()])

    def paragraph_count(self):
        """Count the total number of paragraphs."""
        return len([p for p in self.paragraphs if p.strip()])

    def character_count(self):
        """Count the total number of characters (excluding spaces)."""
        return len(re.findall(r'\S', self.text))

    def most_common_words(self, n=5):
        """Find the most frequently used words."""
        return Counter(self.words).most_common(n)

    def average_word_length(self):
        """Calculate the average length of words."""
        if not self.words:
            return 0
        return sum(len(word) for word in self.words) / len(self.words)

    def average_sentence_length(self):
        """Calculate the average sentence length in words."""
        sentence_lengths = [len(re.findall(r'\b\w+\b', s)) for s in self.sentences if s.strip()]
        if not sentence_lengths:
            return 0
        return sum(sentence_lengths) / len(sentence_lengths)
