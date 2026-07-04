import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader
import glob

# 1. Web Page Configuration
st.set_page_config(page_title="AI Study Tutor", page_icon="📚", layout="centered")
st.title("📚 Personal AI Study Tutor")
st.write("Ask any question! The AI will search through your uploaded PDF books and notes.")

# 2. Initialize AI client securely using Streamlit Secrets
# This reads the key from a hidden vault instead of hardcoding it!
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

# 5. Upgraded Module-Specific PDF Scanning Engine
def load_module_pdfs(module_name):
    combined_text = ""
    # Map selection to specific workspace directory folders
    folder_map = {
        "Science": "science_books/*.pdf",
        "Social Science": "social_science_books/*.pdf",
        "Math": "math_books/*.pdf",
        "English": "english_books/*.pdf"
    }
    
    search_path = folder_map.get(module_name, "*.pdf")
    pdf_files = glob.glob(search_path)
    
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
            pass
            
    return combined_text

# 6. Sidebar Navigation Module Selector
with st.sidebar:
    st.markdown("### 📚 Learning Dashboard")
    selected_module = st.radio(
        "Select your Subject Module:",
        ["Science", "Social Science", "Math", "English"]
    )
    st.info(f"Active Module: {selected_module}")

# Synchronize textbook context data layers based on folder selection
with st.spinner(f"Loading {selected_module} reference materials..."):
    knowledge_base = load_module_pdfs(selected_module)

# 7. Dynamic Instruction Mapping Block
prompt_dictionary = {
    "Science": """You are an expert Science tutor. Explain concepts clearly using precise definitions, everyday physical analogies, and crisp, double-spaced bullet points. If requested to show exam strategy, outline the response using clear headings: Definition, Core Scientific Facts, and Diagram Descriptions.""",
    
    "Social Science": """You are an expert History and Civics tutor. Break down complex events, causes, and chronological timelines into structured bullet points. Keep explanations direct and factual. For exams, highlight key dates, major historical impacts, and core arguments cleanly.""",
    
    "Math": """You are a precise Mathematics mentor. Focus on clear, step-by-step logical derivations. You MUST use standard text formatting or basic structural equations without raw markdown symbols. For exam strategy, explicitly break down your response into: Given Data, Formula to Apply, Step-by-Step Solution, and Final Answer Box.""",
    
    "English": """You are a creative and sharp English Language and Literature tutor. Explain grammar rules, context, and chapter themes elegantly. Avoid markdown symbols. Provide clear, bulleted breakdowns for character sketches, thematic notes, or structural writing formats for exams."""
}

# Combine the core persona with your formatting constraints
tutor_instructions = f"""
{prompt_dictionary[selected_module]}

CRITICAL FORMATTING CONSTRAINTS (NO CODE SYMBOLS):
1. Do NOT use markdown symbols like asterisks (**), hashtags (#), or bullet dashes (-).
2. To build cleanly spaced lists, start each new line using a standard number or clear dot character (e.g., "• Point text" or "1. Point text").
3. Use double line breaks between points so it reads beautifully on smaller touch screens.
4. Always conclude your interaction with a short, motivating sentence!
"""

# 8. User Interface Display Fields
st.markdown(f'<p class="input-label">Ask your {selected_module} question or exam strategy objective:</p>', unsafe_allow_html=True)
student_question = st.text_input("", placeholder=f"e.g., Ask a question about your uploaded {selected_module} books...", label_visibility="collapsed")

# 6. Web Input Interface
student_question = st.text_input("What concept do you want me to explain today?", placeholder="Type your question here...")

# 7. Execution Button
if st.button("Ask Tutor", type="primary"):
    if not student_question.strip():
        st.warning("Please type a question first!")
    elif not knowledge_base:
        st.error("No PDF files found! Please drop your book or notes PDFs into the folder.")
    else:
        with st.spinner("Tutor is reading the materials and thinking... 🧠"):
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
                
                # Render beautifully as a clean informational box on the phone screen
                st.markdown("### 📖 Explanation:")
                st.info(response.text)
                
            except Exception as e:
                st.error(f"Connection Error: {e}")