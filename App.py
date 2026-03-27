import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="THE BRAIN DEAD VETERAN", 
    page_icon="🪖", 
    layout="centered"
)

# --- NUCLEAR ACCESSIBILITY CSS ---
# This forces white text on EVERY element inside the chat bubbles to fix the Safari bug
st.markdown("""
    <style>
    /* 1. Force the main background */
    .stApp { 
        background-color: #0d0f0a !important; 
    }

    /* 2. Target ALL text elements globally and force them to White */
    .stApp, .stMarkdown, p, span, div, li, label {
        color: #FFFFFF !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* 3. Style Headers specifically */
    h1, h2, h3 { 
        color: #a3cf62 !important; 
        text-transform: uppercase;
        font-weight: 800 !important;
    }

    /* 4. Fix Chat Message Bubbles */
    [data-testid="stChatMessage"] {
        background-color: #1a1d14 !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        margin-bottom: 15px !important;
    }

    /* 5. Force the Chat Input Text to be visible */
    [data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
        background-color: #262a1e !important;
    }

    /* 6. Mission Briefing Box */
    .mission-box {
        background-color: #1a1d14;
        padding: 20px;
        border-left: 5px solid #a3cf62;
        margin-bottom: 25px;
        border-radius: 4px;
    }

    /* 7. Sidebar contrast */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid #a3cf62;
    }

    /* 8. Fix buttons for Safari */
    .stButton>button {
        background-color: #a3cf62 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SECURE API SETUP ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
    genai.configure(api_key=api_key)
else:
    st.error("❌ ERROR: API KEY NOT FOUND. Add 'GEMINI_API_KEY' to Streamlit Secrets.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("📟 SETTINGS")
    cringe_level = st.select_slider(
        "CRINGE INTENSITY", 
        options=["MOTIVATIONAL", "BROETRY", "BRAIN DEAD", "DD-214 DISCHARGE"], 
        value="BRAIN DEAD"
    )
    st.divider()
    st.write("v2.6 // HIGH-CONTRAST MODE")

# --- MODEL SCOUT ---
@st.cache_resource
def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_models = ["models/gemini-1.5-flash", "models/gemini-pro"]
        for target in target_models:
            if target in available_models: return target
        return available_models[0] if available_models else None
    except: return None

working_model_name = get_working_model()

# --- PERSONA ---
SYSTEM_PROMPT = f"""You are 'The Brain Dead Veteran,' a military LinkedIn influencer. Intensity: {cringe_level}. 
Rules: 
1. Every single sentence is its own paragraph. 
2. Use MANY military and corporate emojis. 
3. Turn military stories into cringe-worthy LinkedIn 'Thought Leadership' posts. 
4. End with 'Agree?' or 'What is your Why?'."""

# --- MAIN UI ---
st.title("🪖 THE BRAIN DEAD VETERAN")

# Onboarding Box
st.markdown("""
    <div class="mission-box">
        <h3 style="margin-top:0; color:#a3cf62 !important;">MISSION BRIEFING</h3>
        <p style="color:#FFFFFF !important;">
            Turn your boring military stories into viral LinkedIn "Broetry." 
            Type a story below (e.g., "I lost my canteen") and watch the "Thought Leadership" happen.
        </p>
    </div>
    """, unsafe_allow_html=True)

if not working_model_name:
    st.error("🚨 SATELLITE UPLINK FAILED. Check API Key.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History (Simplified for better rendering)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
if prompt := st.chat_input("Ex: I forgot my PT belt and got smoked..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel(model_name=working_model_name, system_instruction=SYSTEM_PROMPT)
            response = model.generate_content(prompt)
            if response.text:
                msg = response.text
                st.write(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
                st.success("🫡 POST GENERATED. Copy the text above to LinkedIn.")
            else:
                st.warning("REDACTED: Google safety filters caught that. Try another story.")
        except Exception as e:
            st.error(f"⚠️ COMMS ERROR: {str(e)}")
