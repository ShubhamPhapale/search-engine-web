import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Specify the directory for NLTK data
nltk_data_dir = "/Users/shubhamsarjeraophapale/IR Assignment 5/nltk_data"
# Append the directory to the NLTK data path
nltk.data.path.append(nltk_data_dir)

# Check if the necessary NLTK packages are already downloaded
def download_nltk_data():
    required_data = {
        'punkt': 'tokenizers/punkt',
        'stopwords': 'corpora/stopwords',
        'wordnet': 'corpora/wordnet',
        'punkt_tab': 'tokenizers/punkt_tab'
    }
    
    for data, path in required_data.items():
        data_path = os.path.join(nltk_data_dir, path)
        try:
            # Check if data is already downloaded
            if not os.path.exists(data_path):
                print(f"Downloading {data}...")
                nltk.download(data, download_dir=nltk_data_dir)
            else:
                print(f"{data} already exists. Skipping download.")
        except LookupError:
            print(f"Error: {data} not found. Attempting download.")
            nltk.download(data, download_dir=nltk_data_dir)

# Download NLTK data if not already present
download_nltk_data()

class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, text):
        # Tokenize text
        tokens = word_tokenize(text.lower())
        # Remove punctuation and stopwords
        tokens = [word for word in tokens if word.isalnum() and word not in self.stop_words]
        # Lemmatize tokens
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
        return ' '.join(tokens)
