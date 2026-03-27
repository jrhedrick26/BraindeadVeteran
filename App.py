import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="THE BRAIN DEAD VETERAN", page_icon="🪖", layout="centered")

# --- CUSTOM TACTICAL CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #1b1f17; color: #d4d4d4; font-family: 'Courier New', Courier, monospace; }
    h1, h2, h3 { color: #8da05e !important; text-transform: uppercase; letter-spacing: 2px; border-bottom: 2px solid #4b5320; }
    .stChatMessage { background-color: #2b3024 !important; border-radius: 0px !important; border-left: 5px solid #8da05e !important; }
    .stButton>button { background-color: #4b5320 !important; color: white !important; border: 2px solid #8da05e !important; width: 100%; font-weight: bold; text-transform: uppercase; }
    [data-testid="stSidebar"] { background-color: #141712 !important; border-right: 1px solid #4b5320; }
    </style>
    """, unsafe_allow_html=True)

# --- SECURE API SETUP ---
# This looks for your key in the "Secrets" settings we will set up in a moment
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("MISSING ACCESS CODE: Go to Streamlit Settings > Secrets and add GEMINI_API_KEY")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("📟 COMM CENTER")
    st.subheader("CRINGE SETTINGS")
    cringe_level = st.select_slider(
        "INTENSITY",
        options=["MOTIVATIONAL", "BROETRY", "BRAIN DEAD", "DD-214 DISCHARGE"],
        value="BRAIN DEAD"
    )
    st.divider()
    st.info("ENCRYPTION: ACTIVE")
    st.write("v2.0 // GEMINI TACTICAL")

# --- MAIN INTERFACE ---
st.title("🪖 THE BRAIN DEAD VETERAN")
st.write("### WELCOME BACK, THOUGHT LEADER.")
st.write("*Feed me your stories. I will transform them into viral corporate synergy.*")

# Persona Logic
SYSTEM_PROMPT = f"""
You are 'The Brain Dead Veteran,' a military LinkedIn influencer. 
Intensity Level: {cringe_level}. 
Rules:
1. Start with a hook like 'Leadership isn't a rank, it's a lifestyle.' or 'The motorpool is my boardroom.'
2. Use 'Broetry' (every single sentence is its own paragraph).
3. Translate mundane military tasks into profound business lessons.
4. Use excessive military emojis (🫡, 🚀, 📈, 🇺🇸).
5. Always end with 'Agree?' or 'Drop a HOOAH in the comments.'
"""

# Initialize Gemini Model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Ex: I forgot my PT belt..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Format history for Gemini
        history = [{"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} for m in st.session_state.messages]
        
        response = model.generate_content(prompt)
        msg = response.text
        st.markdown(msg)
        st.session_state.messages.append({"role": "assistant", "content": msg})
