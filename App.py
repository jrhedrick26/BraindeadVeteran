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
    .stButton>button { background-color: #4b5320 !important; color: white !important; border: 2px solid #8da05e !important; width: 100%; font-weight: bold; }
    [data-testid="stSidebar"] { background-color: #141712 !important; border-right: 1px solid #4b5320; }
    </style>
    """, unsafe_allow_html=True)

# --- SECURE API SETUP ---
# Check if key exists in secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"].strip() # .strip() removes accidental spaces
    genai.configure(api_key=api_key)
else:
    st.error("❌ ERROR: GEMINI_API_KEY not found in Streamlit Secrets.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("📟 COMM CENTER")
    cringe_level = st.select_slider("INTENSITY", options=["MOTIVATIONAL", "BROETRY", "BRAIN DEAD", "DD-214 DISCHARGE"], value="BRAIN DEAD")
    st.info("MODEL: GEMINI-1.5-FLASH")

# --- PERSONA ---
SYSTEM_PROMPT = f"""You are 'The Brain Dead Veteran,' a military LinkedIn influencer. Intensity: {cringe_level}. 
Rules: One sentence per paragraph. Use many emojis. Turn military tasks into business wins. End with 'Agree?'."""

# --- THE MODEL (Simplified for Stability) ---
try:
    # We use 1.5-flash as it is the most widely available free model globally
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )
    # TEST CALL: This checks if the key actually works
    model.generate_content("Testing connection.")
except Exception as e:
    st.error("🚨 MISSION FAILURE: GOOGLE REJECTED THE KEY")
    st.warning(f"DEBUG DATA: {str(e)}")
    st.stop()

# --- MAIN UI ---
st.title("🪖 THE BRAIN DEAD VETERAN")
st.write("### STATUS: ONLINE. STANDING BY.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ex: I cleaned the motorpool..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            msg = response.text
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            st.error(f"⚠️ COMMS ERROR: {str(e)}")
