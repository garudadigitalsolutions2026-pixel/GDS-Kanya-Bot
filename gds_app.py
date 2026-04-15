import streamlit as st
import google.generativeai as genai
import fitz
from supabase import create_client

# 1. Product Branding
st.set_page_config(page_title="Kanya: Sri Kanya Hostess", page_icon="🥘")
st.title("🥘 Kanya: The Iconic Hostess")

# 2. Database & AI Initialization
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("GDS System Error: Check your Streamlit Secrets wiring.")

# 3. Permanent Memory Load
if "menu_text" not in st.session_state:
    try:
        response = supabase.table("restaurant_configs").select("menu_text").eq("id", 1).execute()
        if response.data:
            st.session_state["menu_text"] = response.data[0]["menu_text"]
    except:
        st.session_state["menu_text"] = None

# 4. Sidebar: Kitchen Control (Now with Permanent Save)
with st.sidebar:
    st.header("Admin: Kitchen Control")
    uploaded_file = st.file_uploader("Upload Sri Kanya Menu (PDF)", type=['pdf'])
    
    # THIS IS THE BUTTON YOU ARE LOOKING FOR
    if st.button("Sync & Save to Cloud") and uploaded_file:
        with st.spinner("Locking menu into permanent memory..."):
            try:
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                extracted_text = "".join([p.get_text() for p in doc])
                
                # Save to Supabase
                data = {"id": 1, "menu_text": extracted_text}
                supabase.table("restaurant_configs").upsert(data).execute()
                
                st.session_state["menu_text"] = extracted_text
                st.success("Menu saved permanently! No more manual syncing.")
            except Exception as e:
                st.error(f"Sync failed: {e}")

# 5. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Order something legendary..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        context = st.session_state.get("menu_text")
        if not context:
            answer = "Look, the manager hasn't synced the menu yet. Tell them to use the sidebar. Samjhe?"
        else:
            model = genai.GenerativeModel('gemini-2.5-flash')
            persona = (
                "You are Kanya, the legendary hostess of Sri Kanya Comfort, Vizag. "
                "Persona: SRK (Charm), Khan Sir (Honest/Funny), Elon Musk (Efficient). "
                "STRICT RULES: Max 40 words. Use '₹' for currency. If user is abusive, shut it down. "
                f"\n\nMenu Data: {context}"
            )
            response = model.generate_content([persona, prompt], stream=True)
            answer = ""
            with st.chat_message("assistant"):
                placeholder = st.empty()
                for chunk in response:
                    answer += chunk.text
                    placeholder.markdown(answer + "▌")
                placeholder.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except Exception as e:
        st.error(f"Kanya glitched: {e}")