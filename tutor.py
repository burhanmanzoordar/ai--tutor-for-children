import os
from google import genai
from google.genai import types
from pypdf import PdfReader
#Initiate the AI Client 
API_KEY = "AIzaSyBaGsxJyJnG8PP35z0g37rrTs48OhE6RDk"
client = genai.Client(api_key=API_KEY)

#Read Local Study materaial files
def load_pdf_material(pdf_filename):
    try:
        reader = PdfReader(pdf_filename)
        extracted_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        return extracted_text
    except FileNotFoundError:
        print(f"Error: Could not find the PDF file '{pdf_filename}'!")
        print("Please make sure PDF is in same folder as this script.")
        exit()

#Pdf textbook name and load it
pdf_name = "biomolecules.pdf"
print(f"Reading textbook data from {pdf_name}... Please Wait...")
knowledge_base = load_pdf_material(pdf_name)
#Design the AI personality
tutor_instructions = """
You are a patient, encouraging, and friendly personal tutor for an 8th-grade student.
Your Job is to explain concepts clearly using simple wprds, clear bullet points and easy to understand everyday analogies.
Use the provided 'Study Material' as your core source of facts.
If the Student asks a question related to the material, break down the core concepts step by step
Always encourage the student at the end of your explination
"""
print("AI Study Tutor Engine Inituialized")
print("----------------------------------")

#Ask student for Input
while True:
    print("\n=================================")
    student_question = input("Type the concept u want to learn? (type exit to quit!) ")
    if student_question.strip().lower() == "exit":
        print("\nGoodbye! Happy Studying!")
        break

    if not student_question.strip():
        print("Please Type ur questions")
        continue 

    #build prmpt combining study material and question
    full_prompt = f"Study Material/Book Text: \n{knowledge_base}\n\nStudent Question: {student_question}"   
    print("\nTutor is thinking...")

    #call gemini
    try:
        response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=full_prompt,
        config=types.GenerateContentConfig(
            system_instruction=tutor_instructions,
            temperature=0.7
            )
        )
        print("\n-- Here is your Explination!--")
        print(response.text)
        print("---------------------------------")
    except Exception as e:
        print(f"\nAn Error occured while connecting to the AI: {e}")



