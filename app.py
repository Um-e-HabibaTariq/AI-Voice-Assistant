import streamlit as st
import time


from modules.stt import speech_to_text
from modules.llm import ask_gemini
from modules.tts import speak

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------------------------------
# MODERN DARK THEME
# ----------------------------------------------------

st.markdown("""
<style>

/* App background */
.stApp{
    background: linear-gradient(135deg,#0B1120,#111827,#1E293B);
    color:#F9FAFB;
}

/* Hide Streamlit default UI */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Page spacing */
.block-container{
    max-width:1200px;
    padding-top:2rem;
    padding-bottom:2rem;
}

/* Title */
.main-title{
    font-size:52px;
    font-weight:800;
    background:linear-gradient(90deg,#3B82F6,#06B6D4,#10B981);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-bottom:0.2rem;
}

/* Subtitle */
.subtitle{
    color:#CBD5E1;
    font-size:18px;
    margin-bottom:1rem;
}

/* User bubble */
.user-box{
    background:#2563EB;
    color:white;
    padding:18px;
    border-radius:18px;
    margin:12px 0 12px 120px;
    box-shadow:0 8px 20px rgba(37,99,235,.35);
}

/* Assistant bubble */
.ai-box{
    background:#1F2937;
    color:white;
    padding:18px;
    border-radius:18px;
    margin:12px 120px 12px 0;
    border:1px solid #374151;
    box-shadow:0 8px 20px rgba(0,0,0,.30);
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#111827;
    border-right:1px solid #374151;
}

/* Buttons */
.stButton>button{
    width:100%;
    height:54px;
    border-radius:14px;
    background:#2563EB;
    color:white;
    font-size:16px;
    font-weight:600;
    border:none;
    transition:all .2s ease;
}

.stButton>button:hover{
    background:#1D4ED8;
    transform:translateY(-1px);
}

/* Download button */
.stDownloadButton>button{
    width:100%;
    height:50px;
    border-radius:14px;
}

/* Metrics */
[data-testid="metric-container"]{
    background:#1F2937;
    border:1px solid #374151;
    border-radius:16px;
    padding:18px;
}

/* Tabs */
button[data-baseweb="tab"]{
    font-size:16px;
    font-weight:700;
}

/* Divider */
hr{
    border-color:#374151;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# SESSION STATE
# ----------------------------------------------------

if "chat" not in st.session_state:
    st.session_state.chat = []

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

with st.sidebar:

    st.title("AI Voice Assistant")
    st.caption("Version 1.0")

    st.divider()

    st.subheader("Technology Stack")

    st.success("Python")
    st.success("Whisper")
    st.success("Gemini API")
    st.success("Google Text-to-Speech")
    st.success("Streamlit")

    st.divider()

    st.subheader("System Status")
    st.success("Ready")

    st.divider()

    if st.button("Clear Conversation"):
        st.session_state.chat = []
        st.rerun()

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------

st.markdown(
    """
    <div class='main-title'>AI Voice Assistant</div>
    <div class='subtitle'>
    Speak naturally or type your message to interact with an AI assistant powered by Whisper, Gemini and Google Text-to-Speech.
    </div>
    """,
    unsafe_allow_html=True
)

# Feature cards
c1, c2, c3 = st.columns(3)

with c1:
    st.info("**Speech Recognition**\n\nWhisper AI")

with c2:
    st.info("**Language Model**\n\nGoogle Gemini")

with c3:
    st.info("**Speech Synthesis**\n\nGoogle Text-to-Speech")

st.divider()

# ----------------------------------------------------
# TABS
# ----------------------------------------------------

chat_tab, voice_tab = st.tabs(["Text Chat", "Voice Assistant"])

# ====================================================
# TEXT CHAT TAB
# ====================================================

with chat_tab:

    st.subheader("Chat with Assistant")

    # Show current conversation
    for sender, message in st.session_state.chat:

        if sender == "You":
            st.markdown(
                f"""
                <div class='user-box'>
                <b>You</b><br><br>
                {message}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class='ai-box'>
                <b>Assistant</b><br><br>
                {message}
                </div>
                """,
                unsafe_allow_html=True
            )

    user_input = st.chat_input("Type your message...")

    if user_input:

        st.session_state.chat.append(("You", user_input))

        start = time.time()

        with st.spinner("AI is thinking..."):
            ai_response = ask_gemini(user_input)

        response_time = round(time.time() - start, 2)

        st.session_state.chat.append(("Assistant", ai_response))

        # Speak response (ignore audio errors)
        try:
            speak(ai_response)
        except Exception:
            pass

        st.success(f"Response generated in {response_time} sec")

        st.rerun()

# ====================================================
# VOICE ASSISTANT TAB
# ====================================================
try:
    from modules.recorder import record_audio
    voice_available = True
except Exception:
    voice_available = False

if not voice_available:
    st.error("Voice recording is not available on the deployed server.")
    st.stop()

record_audio()

with voice_tab:

    st.subheader("Voice Assistant")

    st.write("Click the button below and speak naturally into your microphone.")

    if st.button("Start Recording", use_container_width=True):

        status = st.empty()
        start = time.time()

        try:

            # Record
            status.info("Recording your voice...")
            record_audio()

            # Speech to text
            status.info("Transcribing speech...")
            user_text = speech_to_text()

            if not user_text or user_text.strip() == "":
                st.warning("No speech detected.")
                st.stop()

            st.session_state.chat.append(("You", user_text))

            # LLM
            status.info("AI is thinking...")
            ai_response = ask_gemini(user_text)

            st.session_state.chat.append(("Assistant", ai_response))

            # Show response
            st.markdown(
                f"""
                <div class='ai-box'>
                <b>Assistant</b><br><br>
                {ai_response}
                </div>
                """,
                unsafe_allow_html=True
            )

            # TTS
            status.info("Generating speech...")
            speak(ai_response)

            total_time = round(time.time() - start, 2)
            status.success(f"Completed in {total_time} sec")

        except Exception as e:
            st.error(f"Error: {e}")

# ====================================================
# CONVERSATION HISTORY
# ====================================================

st.divider()
st.subheader("Conversation History")

if len(st.session_state.chat) == 0:

    st.info("No conversation yet.")

else:

    conversation = ""

    for sender, message in st.session_state.chat:

        if sender == "You":
            st.markdown(
                f"""
                <div class='user-box'>
                <b>You</b><br><br>
                {message}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class='ai-box'>
                <b>Assistant</b><br><br>
                {message}
                </div>
                """,
                unsafe_allow_html=True
            )

        conversation += f"{sender}: {message}\n\n"

    st.download_button(
        label="Download Conversation",
        data=conversation,
        file_name="conversation.txt",
        mime="text/plain",
        use_container_width=True
    )

# ====================================================
# SESSION STATISTICS
# ====================================================

st.divider()
st.subheader("Session Statistics")

m1, m2, m3 = st.columns(3)

with m1:
    st.metric("Total Messages", len(st.session_state.chat))

with m2:
    user_count = len([m for m in st.session_state.chat if m[0] == "You"])
    st.metric("User Messages", user_count)

with m3:
    ai_count = len([m for m in st.session_state.chat if m[0] == "Assistant"])
    st.metric("AI Responses", ai_count)

# ====================================================
# FOOTER
# ====================================================

st.divider()

st.markdown(
    """
    <div style='text-align:center;color:#9CA3AF;padding:10px 0'>
        Built with <b>Python</b> • <b>Whisper</b> •
        <b>Gemini API</b> • <b>Google Text-to-Speech</b> •
        <b>Streamlit</b>
    </div>
    """,
    unsafe_allow_html=True
)
