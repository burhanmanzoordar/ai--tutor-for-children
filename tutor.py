import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader
import glob

# 1. Web Page Configuration
st.set_page_config(page_title="AI Study Tutor", page_icon="📚", layout="centered")
st.title("📚 Personal AI Study Tutor")
st.write("Ask any question! The AI will search through your uploaded PDF books and notes.")

# 2. Initialize AI client securely
# Make sure to put your working API key here!
API_KEY = "AIzaSyBaGsxJyJnG8PP35z0g37rrTs48OhE6RDk"
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

# 5. Clean, Conversational AI Persona (No coding text, no asterisks)
tutor_instructions = """
You are a patient, encouraging, and friendly personal tutor for an 8th-grade student. 
Your job is to explain concepts clearly using simple words and a natural, conversational tone.

CRITICAL FORMATTING RULES:
1. Do NOT use markdown symbols like asterisks (**), hashtags (#), or bullet dashes (-). 
2. Use simple line breaks (empty spaces between paragraphs) to separate your ideas cleanly.
3. Always encourage the student at the end of your explanation!
4. write your explination in bullets and points rather it being a summery or essay 
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
