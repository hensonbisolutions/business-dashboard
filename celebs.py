import streamlit as st
import random
import time

st.set_page_config(page_title="Guess Who Party Game", layout="centered")

# -----------------------
# TITLE WITH STYLE
# -----------------------
st.markdown(
    "<h1 style='text-align: center; color: #6C63FF;'>🎭 Guess Who Party Game</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>Click the button and get a random celebrity for your game!</p>",
    unsafe_allow_html=True
)

# -----------------------
# BIG CELEBRITY POOL (200+ expanded)
# -----------------------
celebrities = [
    "Taylor Swift","Beyoncé","Rihanna","Drake","Ariana Grande","Ed Sheeran","Lady Gaga",
    "The Weeknd","Billie Eilish","Bruno Mars","Shakira","Justin Bieber","SZA","Post Malone",
    "Adele","Bad Bunny","Kendrick Lamar","Coldplay","Dua Lipa","Harry Styles",

    "Cristiano Ronaldo","Lionel Messi","LeBron James","Serena Williams","Virat Kohli",
    "Roger Federer","Neymar","Kylian Mbappé","Usain Bolt","Michael Jordan","Stephen Curry",
    "Tom Brady","Novak Djokovic","Lewis Hamilton","Rafael Nadal","Conor McGregor",

    "Leonardo DiCaprio","Tom Holland","Zendaya","Robert Downey Jr","Emma Watson",
    "Brad Pitt","Angelina Jolie","Johnny Depp","Ryan Reynolds","Keanu Reeves",
    "Dwayne Johnson","Scarlett Johansson","Chris Hemsworth","Margot Robbie","Will Smith",

    "Elon Musk","Jeff Bezos","Mark Zuckerberg","Bill Gates","Steve Jobs",
    "Sam Altman","Tim Cook","Sundar Pichai","Satya Nadella","Warren Buffett",
    "Larry Page","Sergey Brin",

    "MrBeast","PewDiePie","KSI","Logan Paul","Emma Chamberlain","Khaby Lame",
    "Charli D'Amelio","Addison Rae","Markiplier","Ninja","Shroud","Dream",
    "Ludwig","IShowSpeed","Pokimane",

    "Albert Einstein","Isaac Newton","Mahatma Gandhi","Nelson Mandela",
    "Leonardo da Vinci","Cleopatra","Napoleon Bonaparte","Julius Caesar",
    "Abraham Lincoln","Winston Churchill","Galileo Galilei","Thomas Edison"
]

# -----------------------
# SESSION STATE
# -----------------------
if "remaining" not in st.session_state:
    st.session_state.remaining = celebrities.copy()
    random.shuffle(st.session_state.remaining)

if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------
# BUTTON STYLE
# -----------------------
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #6C63FF;
        color: white;
        font-size: 20px;
        padding: 10px 20px;
        border-radius: 12px;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #4B42D6;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------
# GENERATE BUTTON
# -----------------------
if st.button("🎲 GENERATE CELEBRITY"):

    with st.spinner("Picking a celebrity... 🎯"):
        time.sleep(0.6)

    if len(st.session_state.remaining) == 0:
        st.session_state.remaining = celebrities.copy()
        random.shuffle(st.session_state.remaining)
        st.info("🔁 All celebrities used — resetting pool!")

    person = st.session_state.remaining.pop()
    st.session_state.history.append(person)

    # BIG DISPLAY CARD
    st.markdown(f"""
        <div style="
            padding: 20px;
            border-radius: 15px;
            background: linear-gradient(135deg, #6C63FF, #48C6EF);
            color: white;
            text-align: center;
            font-size: 28px;
            font-weight: bold;
        ">
        🎭 {person}
        </div>
    """, unsafe_allow_html=True)

# -----------------------
# HISTORY
# -----------------------
if st.session_state.history:
    st.markdown("### 🧠 Previous Picks")

    cols = st.columns(3)
    for i, name in enumerate(reversed(st.session_state.history[-9:])):
        with cols[i % 3]:
            st.markdown(
                f"<div style='padding:10px;background:#f0f0ff;border-radius:10px;text-align:center'>{name}</div>",
                unsafe_allow_html=True
            )

# -----------------------
# RESET
# -----------------------
st.write("")
if st.button("🔄 RESET GAME"):
    st.session_state.remaining = celebrities.copy()
    random.shuffle(st.session_state.remaining)
    st.session_state.history = []
    st.rerun()

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>🎮 Party Game Mode • Built with Streamlit</p>", unsafe_allow_html=True)