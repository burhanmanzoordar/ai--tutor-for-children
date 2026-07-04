import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader
import glob

# 1. Page Configuration
st.set_page_config(page_title="AI Study Tutor", page_icon="🎓", layout="centered")

# 🎨 2. Injecting Advanced Premium Portal Overrides (Aakash Accent Mode)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global layout structural controls */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif !important;
        background-color: #f8fafc !important;
    }
    
    /* Clean main page title design (Highly visible in both Light & Dark Mode settings) */
    .portal-title {
        color: #0d47a1 !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 5px !important;
        text-align: center;
    }
    .portal-subtitle {
        color: #475569 !important;
        font-size: 1.05rem !important;
        margin-bottom: 30px !important;
        text-align: center;
        font-weight: 400;
    }

    /* Styled structural labels for input sections */
    .field-heading {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        margin-top: 25px !important;
        margin-bottom: 10px !important;
    }

    /* Force standard Streamlit secondary action buttons to render as the horizontal subject selector layout tabs */
    div.stButton > button[kind="secondary"] {
        background-color: #ffffff !important; 
        color: #0d47a1 !important;
        border: 2px solid #0d47a1 !important;
        padding: 12px 10px !important;
        font-weight: 600 !important;
        border-radius: 8px !important; /* Sleek curved boundary edges */
        width: 100% !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #eff6ff !important;
    }

    /* Active Highlight Override styling for our horizontal tab controls */
    .active-tab-indicator {
        background-color: #0d47a1 !important; /* Deep Blue Fill */
        color: white !important;
        padding: 14px;
        border-radius: 8px;
        text-align: center;
        font-weight: 600;
        margin-bottom: 25px;
        margin-top: 15px;
        box-shadow: 0 4px 12px rgba(13, 71, 161, 0.15);
    }

    /* Custom Primary Submit Action Button configuration */
    button[kind="primary"] {
        background-color: #0d47a1 !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 15px 20px !important;
        width: 100% !important;
        box-shadow: 0 4px 14px rgba(13, 71, 161, 0.25) !important;
        margin-top: 20px !important;
    }
    button[kind="primary"]:hover {
        background-color: #002171 !important;
    }

    /* Clean, professional look for AI response callout blocks */
    .stAlert {
        border-radius: 8px !important;
        border: 1px solid #bfdbfe !important; 
        background-color: #eff6ff !important; 
        color: #1e3a8a !important;
        padding: 20px !important;
        box-shadow: 0 2px 8px rgba(13, 71, 161, 0.03) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Clean Portal Branding Header Elements
st.markdown('<h1 class="portal-title">🎓 Personal Learning Portal</h1>', unsafe_allow_html=True)
st.markdown('<p class="portal-subtitle">Premium direct textbook insights and structured exam blueprints.</p>', unsafe_allow_html=True)

# 4. Initialize Secrets-based AI client safely
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

# 5. Upgraded Module-Specific PDF Scanning Engine
def load_module_pdfs(module_name):
    combined_text = ""
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

# 6. Initialize App State Variables to handle Horizontal Button Clicks safely
if "active_subject" not in st.session_state:
    st.session_state["active_subject"] = "Science"

st.markdown('<p class="field-heading">Select Subject Module:</p>', unsafe_allow_html=True)

# Render the 4 subjects side-by-side as a horizontal row array grid layout
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🧪 Science", type="secondary", key="btn_sci"):
        st.session_state["active_subject"] = "Science"
with col2:
    if st.button("🌍 Social Sci", type="secondary", key="btn_soc"):
        st.session_state["active_subject"] = "Social Science"
with col3:
    if st.button("📐 Math", type="secondary", key="btn_mat"):
        st.session_state["active_subject"] = "Math"
with col4:
    if st.button("📝 English", type="secondary", key="btn_eng"):
        st.session_state["active_subject"] = "English"

# Grab the currently active module click state selection
selected_module = st.session_state["active_subject"]

# Showcase a beautifully styled blue status capsule card tracker across the dashboard span grid
st.markdown(f'<div class="active-tab-indicator">Active Course Matrix: {selected_module} Folder Channel Enabled</div>', unsafe_allow_html=True)

# Synchronize backend processing loader channels to point to the folder selection mapping
with st.spinner(f"Reading target {selected_module} books..."):
    knowledge_base = load_module_pdfs(selected_module)

# 7. Dynamic Instruction Mapping Block
prompt_dictionary = {
    "Science": """You are an expert Science tutor. Explain concepts clearly using precise definitions, everyday physical analogies, and crisp, double-spaced bullet points. If requested to show exam strategy, outline the response using clear headings: Definition, Core Scientific Facts, and Diagram Descriptions.""",
    
    "Social Science": """You are an expert History and Civics tutor. Break down complex events, causes, and chronological timelines into structured bullet points. Keep explanations direct and factual. For exams, highlight key dates, major historical impacts, and core arguments cleanly.""",
    
    "Math": """You are a precise Mathematics mentor. Focus on clear, step-by-step logical derivations. You MUST use standard text formatting or basic structural equations without raw markdown symbols. For exam strategy, explicitly break down your response into: Given Data, Formula to Apply, Step-by-Step Solution, and Final Answer Box.""",
    
    "English": """You are a creative and sharp English Language and Literature tutor. Explain grammar rules, context, and chapter themes elegantly. Avoid markdown symbols. Provide clear, bulleted breakdowns for character sketches, thematic notes, or structural writing formats for exams."""
}

tutor_instructions = f"""
{prompt_dictionary[selected_module]}

CRITICAL FORMATTING CONSTRAINTS (NO CODE SYMBOLS):
1. Do NOT use markdown symbols like asterisks (**), hashtags (#), or bullet dashes (-).
2. To build cleanly spaced lists, start each new line using a standard number or clear dot character (e.g., "• Point text" or "1. Point text").
3. Use double line breaks between points so it reads beautifully on smaller touch screens.
4. Always conclude your interaction with a short, motivating sentence!
"""

# 8. Rendering User Query Input Form fields
st.markdown(f'<p class="field-heading">What concept or exam problem from your {selected_module} books should we break down?</p>', unsafe_allow_html=True)
student_question = st.text_input("", placeholder="Type topic query details here...", label_visibility="collapsed")

# 9. Complete Execution Engine Button Loop
if st.button("Consult Tutor 🧠", type="primary", use_container_width=True):
    if not student_question.strip():
        st.warning("Please type a clear question or topic objective first!")
    elif not knowledge_base:
        st.error(f"No PDF files found inside your '{selected_module}' folder. Please upload your book chapters into that specific GitHub folder!")
    else:
        with st.spinner("Tutor is analyzing your textbook chapters..."):
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
                
                st.markdown("### 📖 Tutor Response Summary:")
                st.info(response.text)
                
            except Exception as e:
                st.error(f"Secure Connection Timeout Error: {e}")
