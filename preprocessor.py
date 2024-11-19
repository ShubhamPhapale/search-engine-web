import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, text):
        # Ensure text is a string before processing
        if isinstance(text, list):
            text = ' '.join(text)  # Convert list to string
        elif not isinstance(text, str):
            raise ValueError(f"Unexpected type for text: {type(text)}") # why it is not string???

        # Tokenize text
        tokens = word_tokenize(text.lower())
        # Remove punctuation and stopwords
        tokens = [word for word in tokens if word.isalnum() and word not in self.stop_words]
        # Lemmatize tokens
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
        return ' '.join(tokens)
