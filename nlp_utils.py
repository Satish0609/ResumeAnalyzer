import nltk
import spacy
from nltk.corpus import stopwords
import string

# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")

# Download NLTK stopwords (if not already)
nltk.download('stopwords')
nltk.download('punkt')

# Set of stopwords
stop_words = set(stopwords.words("english"))

def clean_text(text):
    """
    Cleans and preprocesses the input text: lowercasing, removing stopwords, punctuation, and lemmatizing.
    """
    doc = nlp(text.lower())

    tokens = []
    for token in doc:
        if (token.text not in stop_words and
            token.text not in string.punctuation and
            token.is_alpha):
            tokens.append(token.lemma_)

    return ' '.join(tokens)

# Test
if __name__ == "__main__":
    sample = "Experience with Python, Flask, and SQL databases is required!"
    print("Cleaned:", clean_text(sample))
