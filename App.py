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
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
    genai.configure(api_key=api_key)
else:
    st.error("❌ ERROR: GEMINI_API_KEY not found in Streamlit Secrets.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("📟 COMM CENTER")
    cringe_level = st.select_slider("INTENSITY", options=["MOTIVATIONAL", "BROETRY", "BRAIN DEAD", "DD-214 DISCHARGE"], value="BRAIN DEAD")
    st.divider()
    st.write("SEARCHING FOR SATELLITE UPLINK...")

# --- THE "MODEL SCOUT" (Fixes the 404 Error) ---
@st.cache_resource
def get_working_model():
    try:
        # This looks at YOUR account to see what Google actually calls the models for you
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Priority list: We want Flash 1.5, then Pro, then anything else
        target_models = ["models/gemini-1.5-flash", "models/gemini-pro", "models/gemini-1.0-pro"]
        
        for target in target_models:
            if target in available_models:
                return target
        
        # Fallback: Just take the first one that supports text generation
        return available_models[0] if available_models else None
    except Exception as e:
        st.sidebar.error(f"SATELLITE ERROR: {e}")
        return None

working_model_name = get_working_model()

if not working_model_name:
    st.error("🚨 CRITICAL FAILURE: Your API Key was accepted, but Google says you have no models available. Try creating a new API Key at aistudio.google.com.")
    st.stop()

st.sidebar.success(f"UPLINK ESTABLISHED: {working_model_name.split('/')[-1]}")

# --- PERSONA ---
SYSTEM_PROMPT = f"""You are 'The Brain Dead Veteran,' a military LinkedIn influencer. Intensity: {cringe_level}. 
Rules: 
1. Every sentence is its own paragraph. 
2. Use many emojis. 
3. Turn military stories into business leadership lessons. 
4. End with 'Agree?' or 'What's your 'Why'?'."""

model = genai.GenerativeModel(model_name=working_model_name, system_instruction=SYSTEM_PROMPT)

# --- MAIN UI ---
st.title("🪖 THE BRAIN DEAD VETERAN")
st.write("### STATUS: ONLINE. MISSION READY.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ex: I forgot my gear..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # We add a safety check for the response
            response = model.generate_content(prompt)
            if response.text:
                msg = response.text
                st.markdown(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
            else:
                st.warning("REDACTED: Google blocked that response for safety. Try a less 'intense' story.")
        except Exception as e:
            st.error(f"⚠️ COMMS ERROR: {str(e)}")
