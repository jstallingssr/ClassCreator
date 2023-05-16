from typing import NamedTuple
import streamlit as st
import openai
from functools import partial
from time import time

# Set up OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set up Streamlit
st.set_page_config(
    page_title="Class Creator Thing-a-ma-jig!",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "# This is a header. This is an *extremely* cool app!",
    },
)

# NamedTuple for ChatResponse
class ChatResponse(NamedTuple):
    content: str

# Function to send a request to the OpenAI API
def send_app(app: str, difficulty: str) -> ChatResponse:
    prompt = f"Generate a class outline for {app} at {difficulty} level."  # Update this as per your needs
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=150)
    return ChatResponse(response.choices[0].text.strip())

# Function to retrieve AI answer
def retrieve_ai_answer(app: str, difficulty: str) -> str:
    return send_app(app, difficulty).content.strip()

get_code_info = partial(retrieve_ai_answer)

# Caching the AI response
@st.cache(show_spinner=False)
def get_cached_code_info(app: str, difficulty: str, unique_id: float) -> str:
    return get_code_info(app=app, difficulty=difficulty)

# CSS Style
with open("style.css") as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

# Function to display widgets and generate class outline
def display_widgets() -> tuple:
    st.image("img/lblChoose.png")

    options = [
        "Blender",
        "Unreal Engine",
        "Microsoft Excel",
        "Roblox",
        "Godot",
        "Ableton Live",
        "Godot",
        "BandLab",
        "Unity",
        "Construct 3",
        "Minecraft",
        "Krita",
    ]
    app = st.selectbox("Select:", options)
    # Uncomment the line below if you have a function to display header
    # display_header(app)

    st.image("img/Diff.png")
    difficulty = st.select_slider(
        "Select:", options=["Beginner", "Intermediate", "Advanced", "Expert"]
    )

    class_outline = None  # Initialize class_outline with None
    unique_id = None  # Initialize unique_id with None

    if st.button("Generate a Class!"):
        unique_id = time()  # Generate a new unique identifier
        with st.spinner(text="Creating a class, hang tight! This can take up to 30 seconds..."):
            class_outline = get_cached_code_info(
                app=app, difficulty=difficulty, unique_id=unique_id
            )
            st.markdown(f"**Class Outline:**\n{class_outline}")

        return class_outline, app, difficulty
    return None, None, None  # Return None values if button is not pressed

# Main function
def main() -> None:
    st.markdown(
        "The **Class Creator Thing-a-ma-jig!** is an innovative educational tool that leverages artificial intelligence to create lesson plans for a wide array of software applications. Choose from a curated list of programs, including Blender, Unreal Engine, Unity, and more."
    )

    st.markdown(
        "Each class can be comfortably completed within a 45-60 minute time frame, and the difficulty level can be customized to match your student's skill, ranging from Beginner to Expert."
    )

    st.markdown(
        "Whether you are teaching a one-off class or looking for fresh ideas for your existing students, create unique and comprehensive class outlines with just a few clicks using the Class Creator Thing-a-ma-jig!"
    )

    class_outline, app, difficulty = display_widgets()

    if class_outline is not None:
        st.markdown(f"**App:** {app}")
        st.markdown(f"**Difficulty:** {difficulty}")

        if st.button("New Class"):
            # If "New Class" is clicked, clear the cache and stop the app
            st.caching.clear_cache()
            #st.experimental_rerun()

if __name__ == "__main__":
    main()

