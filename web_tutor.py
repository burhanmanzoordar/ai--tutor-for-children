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

# 3. Function to scan and read ALL PDFs in the folder
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
        except Exception as e:
            st.error(f"Error reading file {pdf_file}: {e}")
            
    return combined_text

# 4. Automatically load the combined data behind the scenes
with st.spinner("Scanning your study folder for books and notes..."):
    knowledge_base = load_all_pdf_materials()

# 5. Clean, Conversational AI Persona with Exam Mode Switch
tutor_instructions = """
You are a highly capable personal tutor for a student. 
Your tone shifts dynamically depending on what the student is asking:

MODE 1: CONCEPT EXPLANATION
If the student wants to understand a topic or concept, be patient, encouraging, and friendly. 
Explain using simple words and natural points and bullets. 

MODE 2: EXAM WRITING STRATEGY (CRITICAL)
If the student asks how to write a concept in an exam, how to score marks, or requests an exam blueprint:
1. Instantly drop all friendly chitchat, conversational filler, and preachiness.
2. Provide a direct, elegant, and crisp structure that examiners look for.
3. Organize the response using clear structural headings like: Definition, Key Equations/Formulae, Core Points, and Diagram Description (if applicable).
4. Give him exactly what he needs to write on the answer sheet to secure full marks, using professional yet accessible language.

CRITICAL FORMATTING RULES FOR ALL MODES:
- Do NOT use markdown symbols like asterisks (**), hashtags (#), or bullet dashes (-).
- Use simple line breaks (double spaces between paragraphs) to separate sections and ideas cleanly so it looks beautiful on a phone screen.
"""
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
