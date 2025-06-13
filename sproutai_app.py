import streamlit as st
import random

# --------------------------
# THEME SETUP
# --------------------------
st.set_page_config(page_title="SproutAI 🌱", page_icon="🌼")

# --------------------------
# SESSION STATE INITIALIZATION
# --------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "quiz_mode" not in st.session_state:
    st.session_state.quiz_mode = False

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# --------------------------
# THEME SELECTOR
# --------------------------
st.sidebar.title("🌼 SproutAI Settings")
st.sidebar.markdown("Customize your chatbot experience:")

theme = st.sidebar.selectbox("Choose a Theme", ["Light", "Dark", "Nature"])
st.session_state.theme = theme

if theme == "Dark":
    st.markdown("<style>body { background-color: #1e1e1e; color: white; }</style>", unsafe_allow_html=True)
elif theme == "Nature":
    st.markdown(
        """
        <style>
            body { background-color: #eafbe0; }
            .stTextInput, .stTextArea, .stButton, .stSelectbox, .stSlider, .stCheckbox { background-color: #f0fff0; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# --------------------------
# RESET CHAT BUTTON
# --------------------------
if st.sidebar.button("🔄 Reset Chat"):
    st.session_state.messages = []
    st.success("Chat cleared!")

# --------------------------
# STEM QUIZ MODE TOGGLE
# --------------------------
st.session_state.quiz_mode = st.sidebar.toggle("🧠 STEM Quiz Mode")

# --------------------------
# STATIC RESOURCES
# --------------------------
bird_audio_url = "https://www.fesliyanstudios.com/play-mp3/387"
flower_img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Spring_flowers_in_a_field.jpg/640px-Spring_flowers_in_a_field.jpg"

# --------------------------
# SIMULATED RESPONSES
# --------------------------
chat_responses = {
    "flower": ["🌸 Tulips, daffodils, and cherry blossoms bloom in spring!", "🌼 Peonies, irises, and hyacinths love spring sunshine."],
    "bee": ["🐝 Bees pollinate over 70% of crops — they're spring heroes!", "Bees can visit 5,000+ flowers a day!"],
    "rain": ["🌦️ Rain helps flowers grow and fills rivers in spring!", "Rain in spring softens the soil for new plants."],
    "bird": ["🕊️ Birds migrate back in spring to find mates and build nests."],
    "sound": ["🎶 Enjoy this relaxing spring sound!"],
    "image": ["Here’s a picture of spring flowers!"],
    "default": ["Spring is amazing! Try asking about bees, flowers, or birds!"],
}

quiz_questions = [
    {"q": "What gas do plants produce during photosynthesis?", "a": "Oxygen"},
    {"q": "Which season comes after spring?", "a": "Summer"},
    {"q": "Which part of the plant conducts photosynthesis?", "a": "Leaves"},
    {"q": "Which animal is a major pollinator?", "a": "Bee"},
]

# --------------------------
# REPLY GENERATOR
# --------------------------
def get_reply(input_text):
    input_text = input_text.lower()
    for key in chat_responses:
        if key in input_text:
            return random.choice(chat_responses[key]), key
    return random.choice(chat_responses["default"]), "default"

# --------------------------
# DISPLAY OLD MESSAGES
# --------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🌱" if msg["role"] == "assistant" else "🙂"):
        st.markdown(msg["content"])
        if msg.get("type") == "image":
            st.image(flower_img_url, caption="Spring blooms 🌷", use_column_width=True)
        elif msg.get("type") == "sound":
            st.audio(bird_audio_url)

# --------------------------
# CHAT INPUT HANDLER
# --------------------------
if prompt := st.chat_input("Type your message or ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🙂"):
        st.markdown(prompt)

    # --------------------------
    # QUIZ MODE
    # --------------------------
    if st.session_state.quiz_mode:
        question = random.choice(quiz_questions)
        answer = question["a"]
        bot_reply = f"🧠 Quiz Time!\n**{question['q']}**\n\n*(Correct Answer: {answer})*"
        reply_type = "text"
    else:
        bot_reply, reply_type = get_reply(prompt)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply, "type": reply_type})

    with st.chat_message("assistant", avatar="🌱"):
        st.markdown(bot_reply)
        if reply_type == "image":
            st.image(flower_img_url, caption="Spring blooms 🌷", use_column_width=True)
        elif reply_type == "sound":
            st.audio(bird_audio_url)
