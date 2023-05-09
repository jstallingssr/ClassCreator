from typing import NamedTuple
from functools import partial
import os
import openai
import streamlit as st
import text_to_speech as tts

openai.api_key = "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"

class ChatResponse(NamedTuple):
    content: str

def send_app(question: str, app: str, difficulty: str) -> ChatResponse:
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=f"App: {app}, Difficulty: {difficulty}\n\n{question}",
        max_tokens=512,
    )
    return ChatResponse(response.choices[0].text)

def retrieve_ai_answer(response: ChatResponse) -> str:
    return response.content.strip()

get_code_info = partial(send_app, 
                        question="Create a one-hour class outline for a key feature in {app} at the {difficulty} level. This should be a very specific feature in the software, not a general overview. Please provide only one class outline with a catchy title shown at the top. The outline should be formatted in markdown, outline format. The outline should be very detailed. Each class should include three to five specific items that the student will create during class (a game feature, an art asset, a texture, etc.). Lastly, do not repeat any suggested classes during a user's session.")

@st.cache(show_spinner=False, allow_output_mutation=True)
def get_cached_code_info(app: str, difficulty: str) -> str:
    return retrieve_ai_answer(get_code_info(app=app, difficulty=difficulty))

def display_header() -> None:
    st.image("img/logo.png")

def display_widgets() -> tuple:
    st.subheader('First, choose a software application from the list below:')
    response = st.empty()
    options = ['Blender', 'Unreal Engine', 'Roblox', 'BandLab', 'Unity', 'Construct 3', 'Minecraft', 'Krita']
    selected_option = st.selectbox('Select:', options)
    app = selected_option
    st.subheader('Next, select the level of difficulty for this class')
    difficulty = st.select_slider(
        'Next, select the level of difficulty for this class:',
        options=['Beginner', 'Intermediate', 'Advanced', 'Expert']
    )

    if st.button("Generate a Class!"):
        class_outline = get_cached_code_info(app=app, difficulty=difficulty)
        response.markdown(f"**Class Outline:**\n{class_outline}")
        return class_outline, app, difficulty

    return None, None, None

def main() -> None:
    display_header()
    class_outline, app, difficulty = display_widgets()
    if class_outline:
        st.markdown(f"**App:** {app}")
        st.markdown(f"**Difficulty:** {difficulty}")
        st.markdown(f"**Class Outline:**\n{class_outline}")

if __name__ == "__main__":
    main()
