import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader
import glob

# 1. Page Configuration
st.set_page_config(page_title="AI Study Tutor", page_icon="🎓", layout="centered")

# 🎨 2. Injecting Custom Styling Elements to beautify the UI
st.markdown("""
    <style>
    /* Styling the main background header block */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .main-header h1 {
        margin: 0;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .main-header p {
        margin: 10px 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    /* Adding styling to the user question indicator container */
    .input-label {
        font-weight: 600;
        color: #e0e0e0;
        margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Render the newly styled top header card banner
st.markdown("""
    <div class="main-header">
        <h1>🎓 Personal AI Study Companion</h1>
        <p>Smart, direct textbook insights and exam strategies customized for you.</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Initialize Secrets-based AI client safely
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

# 5. Automated PDF Engine scanning loop
def load_all_pdf_materials():
    combined_text = ""
    pdf_files = glob.glob("*.pdf")
    
    if not pdf_files:
        return None
        
    for pdf_file in pdf_files:
        try:
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    combined_text += text + "\n"
        except Exception:
            pass  # Fail silently to avoid interrupting web app runtime
            
    return combined_text

# Ingestion loader phase tracking
with st.spinner("Syncing core textbook data channels..."):
    knowledge_base = load_all_pdf_materials()

# 6. Optimized Dual Mode AI Prompts Architecture (With Bullet Points Formatting)
tutor_instructions = """
You are a highly capable personal tutor for a student. 
Your tone shifts dynamically depending on what the student is asking:

MODE 1: CONCEPT EXPLANATION
If the student wants to understand a topic or concept, be patient, encouraging, and friendly. 
Break down the topic into an easy-to-read list of core points. 
Start with a quick introductory sentence, followed by clear, spaced-out conceptual points.

MODE 2: EXAM WRITING STRATEGY (CRITICAL)
If the student asks how to write a concept in an exam, how to score marks, or requests an exam blueprint:
1. Instantly drop all friendly chitchat, conversational filler, and preachiness.
2. Structure the answer exactly as it should look on an exam sheet to secure full marks.
3. Use clear section headers like: Definition, Key Points, and Formulae. Under each header, present the information in precise, high-scoring bulleted facts.

CRITICAL FORMATTING RULES FOR ALL MODES (NO CODE SYMBOLS):
- Do NOT use markdown symbols like asterisks (**), hashtags (#), or bullet dashes (-).
- To create bullet points or lists without markdown, start each point on a new line using a clean number or a standard character emoji like a small arrow or dot (e.g., "• Point text" or "1. Point text").
- Use double line breaks (empty vertical space) between points so they don't bunch up together on a mobile screen.
- Always encourage the student at the end of your explanation!
"""

# 7. Rendering the Input Control Form Fields
st.markdown('<p class="input-label">What concept or exam strategy do you want to explore today?</p>', unsafe_allow_html=True)
student_question = st.text_input("", placeholder="e.g., Explain lipids or How to answer structural cell layouts in exams...", label_visibility="collapsed")

st.write("") # Adds an elegant empty layout spacing block row

# 8. Evaluation Button Click Loop
if st.button("Consult Tutor 🧠", type="primary", use_container_width=True):
    if not student_question.strip():
        st.warning("Please type a clear question or topic objective first!")
    elif not knowledge_base:
        st.error("No PDF reference materials found inside the workspace repository folder structure.")
    else:
        with st.spinner("Tutor is parsing reference material layers..."):
            full_prompt = f"Study Material/Book Text:\n{knowledge_base}\n\nStudent Question: {student_question}"
            
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=tutor_instructions,
                        temperature=0.7,
                    )
                )
                
                # Render response in a distinct visual block callout element box wrapper
                st.markdown("### 📖 Tutor Response Summary:")
                st.info(response.text)
                
            except Exception as e:
                st.error(f"Secure Connection Timeout Error: {e}")
