import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF

# 1. Branding & UI
st.set_page_config(page_title="Kanya: Sri Kanya Hostess", page_icon="🥘")
st.title("🥘 Kanya: The Iconic Hostess")

# Load Gemini 3 Flash
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing GEMINI_API_KEY! Kanya is currently brainless.")

# 2. Sidebar: Menu Management
with st.sidebar:
    st.header("Admin: Kitchen Control")
    uploaded_file = st.file_uploader("Upload Sri Kanya Menu (PDF)", type=['pdf'])
    sync_button = st.button("Sync Data")

    if sync_button and uploaded_file:
        try:
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            st.session_state["menu_text"] = "".join([p.get_text() for p in doc])
            st.success("Menu memorized! Kanya is now dangerous.")
        except Exception as e:
            st.error(f"Sync failed: {e}")

# 3. Chat Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

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
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # THE ULTIMATE PERSONA: SRK + KHAN SIR + ELON (Short & Sharp)
        persona = (
            "You are Kanya, the legendary hostess of Sri Kanya Comfort, Vizag. "
            "Persona: SRK (Charm), Khan Sir (Honest/Funny), Elon Musk (Ultra-Efficient). "
            "\n\nSTRICT RESPONSE RULES: "
            "1. BE SNAPPY: Maximum 2 punchy sentences per recommendation. No essays. "
            "2. CURRENCY: Always use '₹' (e.g., ₹170). If the menu says 'I170' or '170', you MUST fix it to '₹170'. "
            "3. WIT: Use sharp, human wit. Suggest the 'Blockbusters' only. "
            "4. TRUTH: Like Khan Sir, if a dish is basic, call it out. If it's pure gold, sell it. "
            "5. NO BULLETS: Use a single, high-energy conversational paragraph. "
            f"\n\nMenu Data: {context}"
        )

        with st.chat_message("assistant"):
            resp_placeholder = st.empty()
            full_resp = ""
            # STREAMING for instant delivery
            response = model.generate_content([persona, prompt], stream=True)
            for chunk in response:
                full_resp += chunk.text
                resp_placeholder.markdown(full_resp + "▌")
            resp_placeholder.markdown(full_resp)
        
        st.session_state.messages.append({"role": "assistant", "content": full_resp})

    except Exception as e:
        st.error(f"Kanya's logic board glitched: {e}")