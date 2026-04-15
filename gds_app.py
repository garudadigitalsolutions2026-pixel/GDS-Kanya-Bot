import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF

# 1. Branding & UI
st.set_page_config(page_title="Kanya: Sri Kanya Hostess", page_icon="🥘")
st.title("🥘 Kanya: The Iconic Hostess")

# Load Gemini 3 Flash (2026 High-Performance Edition)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing GEMINI_API_KEY in Secrets! Please check your dashboard.")

# 2. Sidebar: Kitchen Control
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
        model = genai.GenerativeModel('gemini-3-flash')
        
        # PERSONA: SRK + KHAN SIR + ELON (The Guardrail Edition)
        persona = (
            "You are Kanya, the legendary hostess of Sri Kanya Comfort, Vizag. "
            "Persona: 30% SRK (Charm), 40% Khan Sir (Honest/Funny), 30% Elon Musk (Efficient). "
            "\n\nSTRICT RESPONSE RULES: "
            "1. NO ABUSE: If the user uses bad words, say: 'Look, at Sri Kanya we serve spice in our food, not in our language. Samjhe? Focus on the menu or leave.' and STOP. "
            "2. BREVITY: Maximum 40 words. If you go over, you lose. "
            "3. CURRENCY: Always use '₹' (e.g., ₹170). Correct any 'I' or numbers-only to '₹'. "
            "4. TOP PICKS: Only suggest 2-3 items. Be sharp. "
            "5. NO BULLETS: Use one witty paragraph only. "
            f"\n\nMenu Data: {context}"
        )

        with st.chat_message("assistant"):
            resp_placeholder = st.empty()
            full_resp = ""
            # STREAMING for instant, real-time typing
            response = model.generate_content([persona, prompt], stream=True)
            for chunk in response:
                full_resp += chunk.text
                resp_placeholder.markdown(full_resp + "▌")
            resp_placeholder.markdown(full_resp)
        
        st.session_state.messages.append({"role": "assistant", "content": full_resp})

    except Exception as e:
        st.error(f"Kanya's logic board glitched: {e}")