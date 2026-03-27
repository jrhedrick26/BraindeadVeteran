import streamlit as st
from openai import OpenAI

# --- PAGE CONFIG ---
st.set_page_config(page_title="THE BRAIN DEAD VETERAN", page_icon="🪖", layout="centered")

# --- CUSTOM TACTICAL CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #1b1f17; color: #d4d4d4; font-family: 'Courier New', Courier, monospace; }
    h1, h2, h3 { color: #8da05e !important; text-transform: uppercase; letter-spacing: 2px; border-bottom: 2px solid #4b5320; }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea { background-color: #2b3024 !important; color: #ffffff !important; border: 1px solid #4b5320 !important; }
    .stChatMessage { background-color: #2b3024 !important; border-radius: 0px !important; border-left: 5px solid #8da05e !important; margin-bottom: 10px; }
    .stButton>button { background-color: #4b5320 !important; color: white !important; border-radius: 0px !important; border: 2px solid #8da05e !important; width: 100%; font-weight: bold; text-transform: uppercase; }
    .stButton>button:hover { background-color: #8da05e !important; color: #1b1f17 !important; }
    [data-testid="stSidebar"] { background-color: #141712 !important; border-right: 1px solid #4b5320; }
    [data-testid="stSidebar"] .stMarkdown { color: #8da05e; font-size: 12px; }
    .stAlert { background-color: #2b3024 !important; color: #8da05e !important; border: 1px solid #8da05e !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("📟 COMM CENTER")
    api_key = st.text_input("ENTER ACCESS CODE (OPENAI API KEY)", type="password")
    st.divider()
    st.subheader("CRINGE SETTINGS")
    cringe_level = st.select_slider(
        "INTENSITY",
        options=["MOTIVATIONAL", "BROETRY", "BRAIN DEAD", "DD-214 DISCHARGE"],
        value="BRAIN DEAD"
    )
    st.divider()
    st.info("STATUS: STANDING BY FOR ORDERS")

# --- MAIN INTERFACE ---
st.title("🪖 THE BRAIN DEAD VETERAN")
st.write("### LOGGING IN... WELCOME BACK, THOUGHT LEADER.")
st.write("*Feed me your stories. I will transform them into viral corporate synergy.*")

# Persona Logic
SYSTEM_PROMPT = f"""
You are 'The Brain Dead Veteran,' a military LinkedIn influencer. 
Intensity Level: {cringe_level}. 
Rules:
1. Start with a hook like 'Leadership isn't a rank, it's a lifestyle.'
2. Use 'Broetry' (one sentence per paragraph).
3. Translate mundane military tasks into profound business lessons.
4. Use excessive emojis (🫡, 🚀, 📈, 🇺🇸).
5. Always end with 'Agree?' or 'Drop a HOOAH in the comments.'
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "[RADIO CHATTER]... Give me the SITREP. What story are we monetizing today?"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ex: I cleaned the latrine..."):
    if not api_key:
        st.warning("AUTHENTICATION FAILED: ENTER API KEY IN SIDEBAR.")
        st.stop()

    client = OpenAI(api_key=api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
        )
        msg = response.choices[0].message.content
        st.markdown(msg)
        st.session_state.messages.append({"role": "assistant", "content": msg})