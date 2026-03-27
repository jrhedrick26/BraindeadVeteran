import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="THE BRAIN DEAD VETERAN", 
    page_icon="🪖", 
    layout="centered"
)

# --- ACCESSIBILITY-FIRST TACTICAL CSS ---
# Improved contrast for Safari Mobile and OLED screens
st.markdown("""
    <style>
    /* Main background - Darker for better contrast */
    .stApp { 
        background-color: #0a0c08; 
        color: #FFFFFF; 
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
    }
    
    /* Headers - Bright 'Night Vision' Green */
    h1, h2, h3 { 
        color: #a3cf62 !important; 
        text-transform: uppercase; 
        letter-spacing: 1.5px; 
    }

    /* Description text - Ensuring high visibility on Safari */
    .mission-text {
        background-color: #1a1d14;
        padding: 15px;
        border-left: 4px solid #a3cf62;
        margin-bottom: 20px;
        color: #FFFFFF !important;
        line-height: 1.6;
    }

    /* Chat Messages - High contrast white text */
    .stChatMessage { 
        background-color: #1a1d14 !important; 
        border: 1px solid #333 !important;
        color: #FFFFFF !important;
    }
    
    /* Chat Input - Fixed for mobile visibility */
    .stChatInputContainer input {
        color: #FFFFFF !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] { 
        background-color: #050505 !important; 
        border-right: 1px solid #a3cf62; 
    }
    
    /* Buttons */
    .stButton>button { 
        background-color: #a3cf62 !important; 
        color: #000000 !important; 
        font-weight: bold; 
        text-transform: uppercase;
        border-radius: 4px;
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
    st.write("v2.5 // MOBILE OPTIMIZED")

# --- MODEL SCOUT LOGIC ---
@st.cache_resource
def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_models = ["models/gemini-1.5-flash", "models/gemini-pro", "models/gemini-1.0-pro"]
        for target in target_models:
            if target in available_models:
                return target
        return available_models[0] if available_models else None
    except:
        return None

working_model_name = get_working_model()

# --- PERSONA ---
SYSTEM_PROMPT = f"""You are 'The Brain Dead Veteran,' a military LinkedIn influencer. Intensity: {cringe_level}. 
Rules: 
1. Every sentence is its own paragraph. 
2. Use many military and corporate emojis. 
3. Turn military stories into profound 'Thought Leadership' LinkedIn posts. 
4. Translate boring tasks into corporate jargon. 
5. End with 'Agree?' or 'What is your Why?'."""

# --- MAIN UI ---
st.title("🪖 THE BRAIN DEAD VETERAN")

# NEW: Onboarding / Instructions
st.markdown(f"""
    <div class="mission-text">
        <strong>MISSION OVERVIEW:</strong><br>
        This tool transforms your mundane military service stories (like cleaning the motorpool or losing your ID card) into 
        <strong>cringe-worthy LinkedIn "Thought Leadership" posts.</strong><br><br>
        <strong>SOP:</strong> Type a short story below, and I'll generate the viral "Broetry" for you to copy-paste.
    </div>
    """, unsafe_allow_html=True)

if not working_model_name:
    st.error("🚨 SATELLITE UPLINK FAILED. Check API Key or region availability.")
    st.stop()

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(f'<span style="color: #FFFFFF;">{msg["content"]}</span>', unsafe_allow_html=True)

# User Input
if prompt := st.chat_input("Ex: I forgot my PT belt and got smoked..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f'<span style="color: #FFFFFF;">{prompt}</span>', unsafe_allow_html=True)

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel(model_name=working_model_name, system_instruction=SYSTEM_PROMPT)
            response = model.generate_content(prompt)
            
            if response.text:
                msg = response.text
                st.markdown(f'<span style="color: #FFFFFF;">{msg}</span>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": msg})
                
                # Useful feature: One-click copy helper
                st.info("⬆️ Copy the text above and paste it into LinkedIn to confuse your civilian peers.")
            else:
                st.warning("REDACTED: Google safety filters caught that story. Try a slightly cleaner version.")
        except Exception as e:
            st.error(f"⚠️ COMMS ERROR: {str(e)}")
