import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="THE BRAIN DEAD VETERAN", page_icon="🪖", layout="centered")

# --- CUSTOM TACTICAL CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #1b1f17; color: #d4d4d4; font-family: 'Courier New', Courier, monospace; }
    h1, h2, h3 { color: #8da05e !important; text-transform: uppercase; letter-spacing: 2px; border-bottom: 2px solid #4b5320; }
    .stChatMessage { background-color: #2b3024 !important; border-radius: 0px !important; border-left: 5px solid #8da05e !important; margin-bottom: 10px; }
    .stChatInputContainer { padding-bottom: 20px; }
    .stButton>button { background-color: #4b5320 !important; color: white !important; border: 2px solid #8da05e !important; border-radius: 0px !important; width: 100%; font-weight: bold; }
    [data-testid="stSidebar"] { background-color: #141712 !important; border-right: 1px solid #4b5320; }
    [data-testid="stSidebar"] .stMarkdown { color: #8da05e; font-size: 12px; }
    .stAlert { background-color: #2b3024 !important; color: #8da05e !important; border: 1px solid #8da05e !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SECURE API SETUP ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ ERROR: MISSING ACCESS CODE. Go to Streamlit Settings > Secrets and add GEMINI_API_KEY.")
    st.stop()

# --- SIDEBAR (COMM CENTER) ---
with st.sidebar:
    st.title("📟 COMM CENTER")
    st.subheader("CRINGE SETTINGS")
    cringe_level = st.select_slider(
        "INTENSITY",
        options=["MOTIVATIONAL", "BROETRY", "BRAIN DEAD", "DD-214 DISCHARGE"],
        value="BRAIN DEAD"
    )
    st.divider()
    st.info("ENCRYPTION: ACTIVE\nMODEL: GEMINI-2.0-TACTICAL")
    st.write("v2.1 // THE BRAIN DEAD VETERAN")

# --- PERSONA LOGIC ---
SYSTEM_PROMPT = f"""
You are 'The Brain Dead Veteran,' a military LinkedIn influencer. 
Intensity Level: {cringe_level}. 
Rules:
1. Start with a hook like 'Leadership is a combat sport' or 'The motorpool taught me more than Harvard.'
2. Every single sentence MUST be its own paragraph (LinkedIn 'Broetry' style).
3. Translate mundane military tasks (sweeping, lines, filling forms) into massive corporate synergy wins.
4. Use at least 5 military/business emojis per post (🫡, 🚀, 📈, 🇺🇸, ⚓).
5. Always end with a question: 'Agree?' or 'What is your mission today?'
"""

# --- MODEL INITIALIZATION WITH AUTO-REPAIR ---
@st.cache_resource
def load_tactical_model():
    # We try 2.0 first, then 1.5, then 1.0. This fixes the 'NotFound' error.
    for model_name in ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-pro"]:
        try:
            m = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=SYSTEM_PROMPT
            )
            # Test it briefly
            m.generate_content("test")
            return m
        except Exception:
            continue
    return None

model = load_tactical_model()

if not model:
    st.error("🚨 CRITICAL FAILURE: No AI models found. Check your API key or regional availability.")
    st.stop()

# --- MAIN INTERFACE ---
st.title("🪖 THE BRAIN DEAD VETERAN")
st.write("### STATUS: ONLINE. STANDING BY FOR STORY.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Ex: I spent 4 hours at CIF today..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # We use the chat feature for better "memory"
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            msg = response.text
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            st.error(f"⚠️ COMMS INTERRUPTED: {str(e)}")
