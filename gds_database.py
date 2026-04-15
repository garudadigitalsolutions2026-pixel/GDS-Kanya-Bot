import fitz  # PyMuPDF
import streamlit as st

def ingest_pdf(file_input):
    """Extracts text from PDF. Handles both file objects and file paths."""
    try:
        # Check if we got a file object (has .read) or a path string
        if hasattr(file_input, 'read'):
            file_input.seek(0)
            doc = fitz.open(stream=file_input.read(), filetype="pdf")
        else:
            # It's a path string (like 'SriKanya_Menu_Catalogue.pdf')
            doc = fitz.open(file_input)
        
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def search_database(query, top_n=15):
    """
    Lightweight version. 
    Returns a LIST of dictionaries to match what gds_app.py expects.
    """
    # Grab the menu text from memory
    menu_data = st.session_state.get("menu_text", "Menu data not found. Please upload and sync.")
    
    # Wrap it in the 'chunk' format Kanya expects
    return [{"chunk": menu_data}]