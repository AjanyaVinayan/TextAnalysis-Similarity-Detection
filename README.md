# 🚀 Text Analysis and Similarity Detection System

A modern **Streamlit-based web application** for analyzing textual data and detecting similarity between documents using **Natural Language Processing (NLP)** techniques.

---

## 📌 Project Overview

This application allows users to:

* 📄 Upload or paste text documents (`.txt`, `.pdf`, `.docx`)
* 📊 Analyze document statistics (word count, unique words, sentence count)
* 🔍 Extract important keywords using **TF-IDF**
* 🔗 Compare two documents using **cosine similarity**
* 📈 View similarity percentage with an intuitive UI

The system is designed as an **academic NLP-based document analysis tool** built completely from scratch.

---

## 🧠 Key Features

* ✔ Text preprocessing (tokenization, stopword removal, normalization)
* ✔ Keyword extraction using TF-IDF
* ✔ Document similarity detection using cosine similarity
* ✔ Multi-format file support (TXT, PDF, DOCX)
* ✔ Clean and interactive UI using Streamlit

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit** (Frontend UI)
* **NLTK** (Text preprocessing)
* **Scikit-learn** (TF-IDF & similarity)
* **pypdf** (PDF reading)
* **python-docx** (DOCX reading)

---

## 📂 Project Structure

```
text-similarity-app/
│
├── app.py              # Streamlit UI and main logic
├── utils.py            # NLP processing and core functions
├── requirements.txt    # Dependencies
└── .streamlit/
      └── config.toml   # UI theme configuration (optional)
```

---

## ⚙️ Installation & Setup

### 1️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Download NLTK Data (Optional)

```bash
python -m nltk.downloader punkt stopwords
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

Then open:
👉 http://localhost:8501

---

## 🌐 Deployment (Streamlit Cloud)

1. Push your project to GitHub
2. Go to 👉 https://share.streamlit.io
3. Create a new app
4. Select:

   * Repository
   * Branch: `main`
   * File: `app.py`
5. Click **Deploy**

---

## 📊 How It Works

```
User Input (Upload / Paste Text)
        ↓
Text Preprocessing (NLTK)
        ↓
Feature Extraction (TF-IDF)
        ↓
Analysis / Similarity Computation
        ↓
Results Display (Streamlit UI)
```

---

## ⚠️ Limitations

* Works on textual similarity only (no deep semantic understanding)
* Performance depends on document size and content quality

---

## 🔮 Future Enhancements

* 🔍 Plagiarism detection report
* 🤖 Integration with advanced NLP models (BERT)
* 📊 Visualization (charts/graphs)
* 🌐 Multi-language support

---

## 🎓 Academic Relevance

This project demonstrates:

* Natural Language Processing (NLP)
* Feature extraction using TF-IDF
* Cosine similarity computation
* Web application development using Streamlit

---

## 👨‍💻 Author

Developed as part of an academic project for learning **Python-based NLP and Web Applications**.
