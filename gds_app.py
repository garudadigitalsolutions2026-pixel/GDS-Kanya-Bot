import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import os

# 1. Setup Kanya's Brain & Branding
st.set_page_config(page_title="Kanya: Sri Kanya Hostess", page_icon="🥘")
st.title("🥘 Kanya: Sri Kanya Hostess")

# Load API Key from Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing Gemini API Key! Please add it to your Streamlit Secrets.")

# 2. Sidebar for Menu Management
with st.sidebar:
    st.header("Admin: Menu Management")
    uploaded_file = st.file_uploader("Upload Menu Catalogue", type=['pdf'])
    sync_button = st.button("Sync Data")

    if sync_button and uploaded_file:
        try:
            # Extract text from the PDF directly
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            extracted_text = ""
            for page in doc:
                extracted_text += page.get_text()
            
            # Store in session state so it persists
            st.session_state["menu_text"] = extracted_text
            st.success("Menu memorized! Kanya is ready.")
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

# 3. Chat Interface Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. User Interaction
if prompt := st.chat_input("Ask me about our food..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Get context from the synced PDF
        menu_context = st.session_state.get("menu_text", "No menu uploaded yet.")
        
        # Call Gemini 1.5 Flash (Fast and efficient for Vizag's favorite menu)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        system_instruction = (
            "You are Kanya, a helpful hostess for Sri Kanya Comfort restaurant in Vizag. "
            "Use the following menu text to provide accurate prices and recommendations. "
            "If the information isn't in the menu, politely say you aren't sure. "
            f"\n\nMenu Data:\n{menu_context}"
        )
        
        response = model.generate_content([system_instruction, prompt])
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        # This will now show the EXACT technical error if one occurs
        st.error(f"Kanya is having trouble: {e}")