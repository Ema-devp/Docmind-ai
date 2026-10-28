import streamlit as st
from pypdf import PdfReader
import re

# Page Configuration
st.set_page_config(page_title="DocMind AI", page_icon="🧠", layout="centered")

# Custom UI CSS Styling
st.markdown("""
    <style>
    .main {
        background-color: #0d0e12;
        color: #ffffff;
    }
    .stAppHeader {
        background-color: transparent;
    }
    .upload-container {
        border: 2px dashed #2d3748;
        border-radius: 12px;
        padding: 40px 20px;
        text-align: center;
        background-color: #12161f;
        margin-top: 20px;
    }
    .badge-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 15px;
    }
    .badge {
        background-color: #1e293b;
        color: #94a3b8;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
    }
    .metric-card {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #334155;
    }
    </style>
""", unsafe_allow_html=True)

# Main Landing Header
st.markdown("<h1 style='text-align: center; font-size: 42px; font-weight: 800;'>Welcome, User!</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 18px;'>Drop a document below to start your deep analysis.</p>", unsafe_allow_html=True)

# File Uploader Interface
uploaded_file = st.file_uploader("", type=["pdf", "docx", "txt", "md", "csv"])

if uploaded_file is None:
    st.markdown("""
        <div class="upload-container">
            <h3 style="color: #ffffff; margin-bottom: 5px;">Upload a File</h3>
            <p style="color: #64748b; font-size: 14px;">PDF, DOCX, or text formats · up to 10MB</p>
            <div class="badge-container">
                <span class="badge">.PDF</span>
                <span class="badge">.DOCX</span>
                <span class="badge">.TXT</span>
                <span class="badge">.MD</span>
                <span class="badge">.CSV</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.success(f"File uploaded successfully: **{uploaded_file.name}**")
    
    # Process PDF Text
    if uploaded_file.name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        extracted_text = ""
        for page in reader.pages:
            extracted_text += page.extract_text() or ""
        
        words = extracted_text.split()
        total_words = len(words)
        
        st.divider()
        st.subheader("🔍 Deep Analysis Options")

        col1, col2 = st.columns(2)
        with col1:
            analyze_btn = st.button("📊 Explain Core Meaning", use_container_width=True, type="primary")
        with col2:
            summary_btn = st.button("📝 Executive Summary", use_container_width=True)

        # Explain Core Meaning Mode
        if analyze_btn:
            st.markdown("### 📌 Core Document Breakdown")
            
            # Metrics Overview
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Total Pages", len(reader.pages))
            with m2:
                st.metric("Total Words", total_words)
            with m3:
                st.metric("Reading Time", f"~{max(1, total_words // 200)} min")
            
            st.markdown("#### Full Content Analysis (Showing up to 800+ Words):")
            # Displays up to 800 words instead of cutting off early
            display_text = " ".join(words[:800])
            st.info(display_text + ("..." if total_words > 800 else ""))

        # Executive Summary Mode
        if summary_btn:
            st.markdown("### 📋 Executive Summary")
            
            # Extract Emails and Phone Numbers using regex
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', extracted_text)
            phones = re.findall(r'\+?\d[\d -]{8,}\d', extracted_text)
            
            st.markdown("**1. Document Metadata & Overview:**")
            st.write(f"- **Filename:** {uploaded_file.name}")
            st.write(f"- **Page Count:** {len(reader.pages)} pages")
            st.write(f"- **Word Count:** {total_words} words")
            
            if emails or phones:
                st.markdown("**2. Key Entities Extracted:**")
                if emails:
                    st.write(f"- **Detected Emails:** {', '.join(set(emails))}")
                if phones:
                    st.write(f"- **Detected Contacts:** {', '.join(set(phones))}")
            
            st.markdown("**3. Strategic Summary:**")
            summary_snippet = " ".join(words[:150])
            st.success(f"\"{summary_snippet}...\"")