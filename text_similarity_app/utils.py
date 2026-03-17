import re
import nltk

# Ensure required NLTK resources are available
def init_nltk():
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")

    try:
        nltk.data.find("tokenizers/punkt_tab")
    except LookupError:
        nltk.download("punkt_tab")

    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords")

init_nltk()

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader
from docx import Document


# Initialize stopwords
stop_words = set(stopwords.words("english"))


# ---------------- TEXT PREPROCESSING ----------------
def preprocess_text(text):
    if not text:
        return ""

    text = text.lower()

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords and punctuation from tokens, not from original structure
    tokens = [word for word in tokens if word not in stop_words and word.isalnum()]

    return " ".join(tokens)


# ---------------- TEXT ANALYSIS ----------------
def analyze_text(clean_text, original_text=None):

    # Use original text to accurately count sentences, fallback to clean text if not provided
    text_to_analyze = original_text if original_text else clean_text
    
    sentences = sent_tokenize(text_to_analyze)
    sentence_count = len(sentences) if text_to_analyze.strip() else 0

    words = clean_text.split()

    return {
        "total_words": len(words),
        "unique_words": len(set(words)),
        "sentence_count": sentence_count
    }


# ---------------- KEYWORD EXTRACTION ----------------
def get_keywords(text, num_keywords=10):

    if not text.strip():
        return []

    try:
        vectorizer = TfidfVectorizer(stop_words="english")

        tfidf_matrix = vectorizer.fit_transform([text])

        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray().flatten()

        keyword_scores = dict(zip(feature_names, scores))

        sorted_keywords = sorted(
            keyword_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [word for word, score in sorted_keywords[:num_keywords]]

    except Exception:
        return list(set(text.split()))[:num_keywords]


# ---------------- DOCUMENT SIMILARITY ----------------
def similarity_score(doc1, doc2):

    if not doc1.strip() or not doc2.strip():
        return 0.0

    try:
        vectorizer = TfidfVectorizer(stop_words="english")

        tfidf = vectorizer.fit_transform([doc1, doc2])

        similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])

        return float(similarity[0][0])

    except Exception:
        return 0.0


# ---------------- FILE READERS ----------------
def read_txt(file):
    return file.read().decode("utf-8")


def read_pdf(file):

    try:
        reader = PdfReader(file)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text

    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def read_docx(file):

    try:
        doc = Document(file)

        text = ""

        for para in doc.paragraphs:
            text += para.text + "\n"

        return text

    except Exception as e:
        return f"Error reading DOCX: {str(e)}"