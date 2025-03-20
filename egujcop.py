import streamlit as st
from docx import Document
import re
from googletrans import Translator

#remove special characters
def remove_special_characters(text):
    return re.sub(r"[.,\"\/\\()\?!;:\[\]{}@#$%^&*“”_+’‘''=|<>`-]", '', text)

#translate Gujarati to Englishs
def translate_to_english(text):
    translator = Translator()
    translated_text = translator.translate(text, src='gu', dest='en')
    return translated_text.text

#process a Word document
def process_word_document(input_path, output_path):
    doc = Document(input_path)
    for para in doc.paragraphs:
        cleaned_gujarati = remove_special_characters(para.text)  # Clean Gujarati
        translated_text = translate_to_english(para.text)  # Translate to English
        cleaned_english = remove_special_characters(translated_text)  # Clean English

        para.text = f"Gujarati: {cleaned_gujarati}\nEnglish: {cleaned_english}"  # Update document
        
    doc.save(output_path)

# Streamlit App
st.title("e-GujCop Gujarati-English Text")

# Option selection: File Upload or Text Input
option = st.radio("Choose Input Method:", ("Upload Word File", "Enter Text Directly"))

if option == "Upload Word File":
    uploaded_file = st.file_uploader("Upload a Word (.docx) file", type=["docx"])
    
    if uploaded_file is not None:
        input_path = "input.docx"
        output_path = "output_cleaned.docx"
        
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Process file
        process_word_document(input_path, output_path)
        
        st.success("Processing complete! Download your cleaned file below.")
        
        with open(output_path, "rb") as f:
            st.download_button("Download Cleaned File", f, file_name="cleaned_output.docx")

elif option == "Enter Text Directly":
    text_input = st.text_area("Enter your Gujarati paragraph here:")
    
    if st.button("Process Text"):
        if text_input:
            cleaned_gujarati = remove_special_characters(text_input)  #Clean Gujarati
            translated_text = translate_to_english(text_input)  #Translate to English
            cleaned_english = remove_special_characters(translated_text)  #Clean English

            # Display only 2 required fields
            st.subheader("Cleaned Gujarati (No Special Characters):")
            st.text_area("Gujarati Cleaned:", cleaned_gujarati, height=150)

            st.subheader("Final Cleaned English Text:")
            st.text_area("English Cleaned:", cleaned_english, height=150)
        else:
            st.warning("Please enter some text!")

