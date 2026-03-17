import streamlit as st
from utils import preprocess_text, analyze_text, get_keywords, similarity_score
from utils import read_txt, read_pdf, read_docx
import time
try:
    import nltk
except ImportError:
    st.error("The `nltk` package is not installed. "
             "Run `pip install nltk` in your environment.")
    raise

# make sure the corpora are available
for pkg in ('punkt', 'stopwords'):
    try:
        nltk.data.find(pkg)
    except LookupError:
        nltk.download(pkg)

st.set_page_config(
    page_title="Text Analysis & Similarity Detection",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #000000 100%);
    color: #f8fafc;
}

section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.6) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

[data-testid="stHeader"] {
    background-color: transparent !important;
}

section[data-testid="stSidebar"] [data-testid="stText"] {
    color: #e2e8f0;
}

div[role="radiogroup"] > label {
    padding: 10px 15px;
    border-radius: 12px;
    margin-bottom: 8px;
    transition: all 0.3s ease;
    cursor: pointer;
}

div[role="radiogroup"] > label:hover {
    background: rgba(255, 255, 255, 0.05);
}

div[role="radiogroup"] p {
    color: #e2e8f0 !important;
    font-weight: 500;
    font-size: 1.1rem;
    margin: 0;
}

div[role="radiogroup"] > label:hover p {
    color: #ffffff !important;
}

div[role="radiogroup"] input[type="radio"] {
    display: none;
}

div[role="radiogroup"] label[data-checked="true"],
div[role="radiogroup"] [aria-checked="true"] {
    background: rgba(239, 68, 68, 0.1) !important; /* Light Red transparent */
    border-left: 4px solid #ef4444 !important;
}

div[role="radiogroup"] label[data-checked="true"] p,
div[role="radiogroup"] [aria-checked="true"] p,
div[role="radiogroup"] [aria-checked="true"] + div p {
    color: #ef4444 !important;
    font-weight: 600 !important;
}

.stRadio div[role="radiogroup"] > label > div:first-child {
    display: none;
}

.main-title {
    font-size: 4rem;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, #fca5a5 0%, #ef4444 50%, #b91c1c 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
}

.subtitle {
    font-size: 1.25rem;
    color: #94a3b8;
    margin-bottom: 3rem;
    font-weight: 300;
}

.glass-card {
    background: rgba(30, 41, 59, 0.4);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    height: 100%;
}

.glass-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(239, 68, 68, 0.15);
    border-color: rgba(239, 68, 68, 0.3);
}

.card-icon {
    font-size: 2.5rem;
    margin-bottom: 15px;
    color: #ef4444;
}

.card-title {
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 10px;
    color: #f8fafc;
}

.card-text {
    font-size: 1rem;
    color: #94a3b8;
    line-height: 1.5;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(15, 23, 42, 0.6);
    color: #f8fafc;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 1rem;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #ef4444;
    box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.2);
}

label {
    color: #cbd5e1 !important;
    font-weight: 500 !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 30px;
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    transition: all 0.3s ease;
    width: 100%;
    margin-top: 10px;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(239, 68, 68, 0.5);
    border: none;
    color: white;
}

div.stButton > button:active {
    transform: translateY(0);
}

/* File Uploader Container Framework */
[data-testid="stFileUploader"] section,
[data-testid="stFileUploadDropzone"],
.stFileUploader > div > div {
    background-color: rgba(30, 41, 59, 0.4) !important;
    border: 1px dashed rgba(255, 255, 255, 0.2) !important;
    border-radius: 16px !important;
    padding: 10px !important;
    transition: all 0.3s ease;
}

[data-testid="stFileUploader"] section:hover,
[data-testid="stFileUploadDropzone"]:hover,
.stFileUploader > div > div:hover {
    border-color: #ef4444 !important;
    background-color: rgba(30, 41, 59, 0.6) !important;
}

/* Browse Files Button - Forced Dark Mode */
.stFileUploader button,
[data-testid="stFileUploader"] button,
[data-testid="stFileUploadDropzone"] button {
    background-color: #ef4444 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 6px 16px !important;
    opacity: 1 !important;
    transition: all 0.3s ease;
}

/* Ensure inner text is forced to white */
.stFileUploader button *,
[data-testid="stFileUploader"] button *,
[data-testid="stFileUploadDropzone"] button * {
    color: #ffffff !important;
}

.stFileUploader button:hover,
[data-testid="stFileUploader"] button:hover,
[data-testid="stFileUploadDropzone"] button:hover {
    background-color: #dc2626 !important;
}

/* File Uploader Texts */
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploadDropzone"] span,
[data-testid="stFileUploadDropzone"] p {
    color: #f8fafc !important;
    font-size: 1rem !important;
}

[data-testid="stFileUploader"] small,
[data-testid="stFileUploadDropzone"] small {
    color: #94a3b8 !important;
}

/* Metrics Styling */
div[data-testid="stMetricValue"] {
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    color: #f8fafc !important;
}

div[data-testid="stMetricLabel"] {
    font-size: 1.1rem !important;
    font-weight: 500 !important;
    color: #94a3b8 !important;
}

/* Keyword Tags (Red Pills) */
.keyword-tag {
    display: inline-block;
    background: rgba(239, 68, 68, 0.15);
    color: #fca5a5;
    border: 1px solid rgba(239, 68, 68, 0.3);
    padding: 8px 16px;
    border-radius: 20px;
    margin: 6px 6px 6px 0;
    font-size: 0.95rem;
    font-weight: 500;
    transition: all 0.3s ease;
}

.keyword-tag:hover {
    background: rgba(239, 68, 68, 0.25);
    transform: translateY(-2px);
}

.stProgress > div > div > div > div {
    background-color: #ef4444;
}

h1, h2, h3 {
    color: #f8fafc !important;
    font-weight: 700 !important;
}

h2 {
    font-size: 2.2rem !important;
    margin-bottom: 1.5rem !important;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    padding-bottom: 0.5rem;
}

.output-metrics {
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 20px;
    margin-top: 20px;
}

hr {
    border-color: rgba(255,255,255,0.1);
}

/* Custom Success/Warning/Info Boxes using st.markdown to bypass default styling if needed, but we'll style default alerts too */
div[data-testid="stAlert"] {
    background: rgba(30, 41, 59, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #f8fafc !important;
    border-radius: 12px;
    backdrop-filter: blur(10px);
}

</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="margin-bottom: 30px; padding: 10px 0;">
        <h2 style="font-size: 1.8rem; font-weight: 800; background: linear-gradient(135deg, #f8fafc, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; border: none; padding: 0; margin: 0;">System</h2>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio(
        "Navigation",
        ["Home", "Analyze", "Compare"],
        label_visibility="collapsed"
    )

def read_uploaded_file(uploaded_file):
    if not uploaded_file: return ""
    ext = uploaded_file.name.split('.')[-1].lower()
    if ext == "txt": return read_txt(uploaded_file)
    elif ext == "pdf": return read_pdf(uploaded_file)
    elif ext == "docx": return read_docx(uploaded_file)
    return ""


if menu == "Home":

    st.markdown('<h1 class="main-title">Text Analysis &<br>Similarity Detection System</h1>', unsafe_allow_html=True)
    
    st.markdown('<p class="subtitle">An advanced, AI-powered toolkit for deep document analysis, keyword extraction, and contextual similarity mapping.</p>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('''
        <div class="glass-card">
            <div class="card-icon">📊</div>
            <div class="card-title">Document Insights</div>
            <div class="card-text">Instantly break down complex documents. Get crucial metrics like word density, vocabulary diversity, and structural analysis in milliseconds.</div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''
        <div class="glass-card">
            <div class="card-icon">🎯</div>
            <div class="card-title">Keyword Detection</div>
            <div class="card-text">Leverage TF-IDF algorithms to cut through the noise and automatically surface the most critical terms and themes within your text.</div>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        st.markdown('''
        <div class="glass-card">
            <div class="card-icon">🔄</div>
            <div class="card-title">Similarity Analysis</div>
            <div class="card-text">Compare documents head-to-head. Our vector space model computes precise cosine similarity to detect overlap and plagiarism.</div>
        </div>
        ''', unsafe_allow_html=True)


elif menu == "Analyze":

    st.markdown('<h2>Document Analyzer</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        uploaded_file = st.file_uploader("Upload Document (TXT / PDF / DOCX)", type=["txt","pdf","docx"])
    
    with col2:
        text_input = st.text_area("Or Paste Text Iteratively", height=130, placeholder="Paste your text here...")

    text = ""
    if uploaded_file:
        text = read_uploaded_file(uploaded_file)
    elif text_input:
        text = text_input

    st.markdown("<br>", unsafe_allow_html=True)
    
    _, center_btn, _ = st.columns([1, 2, 1])
    with center_btn:
        analyze_clicked = st.button("Generate Insights")

    if analyze_clicked:
        if not text or text.strip() == "":
            st.error("Please provide text to analyze.")
        else:
            # Animated progress indicator
            progress_bar = st.progress(0, text="Initializing analysis engine...")
            time.sleep(0.2)
            
            progress_bar.progress(25, text="Normalizing text data...")
            clean = preprocess_text(text)
            time.sleep(0.3)
            
            progress_bar.progress(60, text="Computing document statistics...")
            stats = analyze_text(clean, original_text=text)
            time.sleep(0.3)
            
            progress_bar.progress(85, text="Extracting TF-IDF keywords...")
            keywords = get_keywords(text)
            time.sleep(0.3)
            
            progress_bar.progress(100, text="Analysis complete!")
            time.sleep(0.2)
            progress_bar.empty()

            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown('<div class="output-metrics">', unsafe_allow_html=True)
            m_col1, m_col2, m_col3 = st.columns(3)
            
            with m_col1:
                st.metric("Total Words", f"{stats['total_words']:,}")
            with m_col2:
                st.metric("Unique Words", f"{stats['unique_words']:,}")
            with m_col3:
                st.metric("Sentences", f"{stats['sentence_count']:,}")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<h3 style="font-size: 1.4rem; font-weight: 600; margin-bottom: 1rem; color: #f8fafc;">Extracted Entities & Keywords</h3>', unsafe_allow_html=True)

            tags_html = ""
            for k in keywords:
                tags_html += f'<span class="keyword-tag">{k}</span>'
            
            st.markdown(f'<div style="padding: 10px 0;">{tags_html}</div>', unsafe_allow_html=True)


elif menu == "Compare":

    st.markdown('<h2>Similarity Scanner</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div style="color: #94a3b8; font-weight: 600; margin-bottom: 10px;">Source Document A</div>', unsafe_allow_html=True)
        file1 = st.file_uploader("Upload File A", type=["txt","pdf","docx"], key="doc1")
        text1_input = st.text_area("Or paste text for A", height=180, key="ta1")
        
        text1 = read_uploaded_file(file1) if file1 else text1_input

    with col2:
        st.markdown('<div style="color: #94a3b8; font-weight: 600; margin-bottom: 10px;">Target Document B</div>', unsafe_allow_html=True)
        file2 = st.file_uploader("Upload File B", type=["txt","pdf","docx"], key="doc2")
        text2_input = st.text_area("Or paste text for B", height=180, key="ta2")
        
        text2 = read_uploaded_file(file2) if file2 else text2_input

    st.markdown("<br>", unsafe_allow_html=True)
    
    _, center_btn, _ = st.columns([1, 2, 1])
    with center_btn:
        compare_clicked = st.button("Run Comparison Analysis")

    if compare_clicked:
        if not text1.strip() or not text2.strip():
            st.error("Please provide content for both documents to compare.")
        else:
            # Animated progress indicator
            progress_bar = st.progress(0, text="Loading documents into semantic space...")
            time.sleep(0.2)
            
            progress_bar.progress(40, text="Vectorizing text parameters...")
            time.sleep(0.3)
            
            progress_bar.progress(70, text="Computing cosine similarity...")
            score = similarity_score(text1, text2)
            percent = round(score * 100, 2)
            time.sleep(0.4)
            
            progress_bar.progress(100, text="Match percentage calculated!")
            time.sleep(0.2)
            progress_bar.empty()

            st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)
            
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 1.2rem; color: #94a3b8; margin-bottom: 5px;'>Match Percentage</p>", unsafe_allow_html=True)
            
            color = "#ef4444" # High - Red (Danger/High similarity in this context usually means match)
            if percent <= 40:
                color = "#10b981" # Low - Green (Safe)
            elif percent <= 70:
                color = "#f59e0b" # Moderate - Yellow

            st.markdown(f"<h1 style='font-size: 5rem; color: {color} !important; margin: 0; line-height: 1;'>{percent}%</h1>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Custom colored progress bar approximation using HTML/CSS
            st.markdown(f"""
            <div style="width: 100%; background-color: rgba(255,255,255,0.1); border-radius: 10px; height: 12px; margin-bottom: 20px;">
                <div style="width: {percent}%; background-color: {color}; height: 100%; border-radius: 10px; transition: width 1s ease-in-out;"></div>
            </div>
            """, unsafe_allow_html=True)

            if percent > 70:
                st.markdown(f"""
                <div style="background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; padding: 15px; border-radius: 8px;">
                    <div style="color: #fca5a5; font-weight: 600; font-size: 1.1rem;">⚠️ High Similarity Detected</div>
                    <div style="color: #cbd5e1; font-size: 0.95rem; margin-top: 5px;">These documents show significant overlap. Manual review is recommended.</div>
                </div>
                """, unsafe_allow_html=True)
            elif percent > 40:
                st.markdown(f"""
                <div style="background: rgba(245, 158, 11, 0.1); border-left: 4px solid #f59e0b; padding: 15px; border-radius: 8px;">
                    <div style="color: #fcd34d; font-weight: 600; font-size: 1.1rem;">⚡ Moderate Similarity</div>
                    <div style="color: #cbd5e1; font-size: 0.95rem; margin-top: 5px;">Some common phrases and structures were found.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; padding: 15px; border-radius: 8px;">
                    <div style="color: #6ee7b7; font-weight: 600; font-size: 1.1rem;">✅ Low Similarity</div>
                    <div style="color: #cbd5e1; font-size: 0.95rem; margin-top: 5px;">Documents appear to be largely independent.</div>
                </div>
                """, unsafe_allow_html=True)