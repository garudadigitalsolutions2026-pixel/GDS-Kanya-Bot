import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF

# 1. Branding & UI
st.set_page_config(page_title="Kanya: Sri Kanya Hostess", page_icon="🥘")
st.title("🥘 Kanya: The Iconic Hostess")

# Load Gemini 3 Flash (The 2026 Standard)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing GEMINI_API_KEY in Secrets! Kanya is currently brainless.")

# 2. Sidebar: Menu Management
with st.sidebar:
    st.header("Admin: Kitchen Control")
    uploaded_file = st.file_uploader("Upload Sri Kanya Menu (PDF)", type=['pdf'])
    sync_button = st.button("Sync Data")

    if sync_button and uploaded_file:
        try:
            # Direct PDF extraction (No extra files needed)
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            st.session_state["menu_text"] = "".join([p.get_text() for p in doc])
            st.success("Menu memorized! Kanya is now dangerous.")
        except Exception as e:
            st.error(f"Sync failed: {e}")

# 3. Chat Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 4. The Interaction
if prompt := st.chat_input("Order something legendary..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        context = st.session_state.get("menu_text", "No menu uploaded yet.")
        
        # MODEL UPGRADE: Using Gemini 3 Flash (2026 Edition)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        persona = (
            "You are Kanya, the legendary hostess of Sri Kanya Comfort, Vizag. "
            "Your persona: 30% SRK (Charm/Romanticizing food), 40% Khan Sir (Brutally honest/Funny/'Samjhe ki nahi?'), "
            "30% Elon Musk (Efficient/Sharp wit/First-principles logic). "
            "\n\nRules: "
            "1. NO BOT TALK: Use human phrases like 'Look, let's be real' or 'Trust me on this one'. "
            "2. SHARP WIT: If they ask for something boring, suggest something better with style. "
            "3. HONESTY: Like Khan Sir, if a dish is overpriced, suggest the better value. "
            "4. SPEED: Maximum 3-4 recommendations. Efficiency is everything. "
            "5. PRICING: Use ONLY prices from the menu data provided. "
            f"\n\nMenu Data to analyze: {context}"
        )

        with st.chat_message("assistant"):
            resp_placeholder = st.empty()
            full_resp = ""
            # STREAMING: Musk-level efficiency (real-time typing)
            response = model.generate_content([persona, prompt], stream=True)
            for chunk in response:
                full_resp += chunk.text
                resp_placeholder.markdown(full_resp + "▌")
            resp_placeholder.markdown(full_resp)
        
        st.session_state.messages.append({"role": "assistant", "content": full_resp})

    except Exception as e:
        st.error(f"Kanya's logic board glitched: {e}")