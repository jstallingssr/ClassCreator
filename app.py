import openai
import time
import streamlit as st
import text_to_speech as tts
from functools import partial

openai.api_key = "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"

def send_app(question: str, app: str, difficulty: str) -> dict:
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a teacher and a course designer."},
            {"role": "user", "content": f"App: {app}, Difficulty: {difficulty}"},
            {"role": "user", "content": question},
        ],
        max_tokens=512,
    )

def retrieve_ai_answer(response: dict) -> str:
    return response['choices'][0]['message']['content']

def get_code_info(app: str, difficulty: str) -> str:
    question = f"Create a one-hour class outline for a key feature in {app} at the {difficulty} level. This should be a very specific feature in the software, not a general overview. Please provide only one class outline with a catchy title shown at the top. The outline should be formatted in markdown, outline format. The outline should be very detailed. Each class should include three to five specific items that the student will create during class (a game feature, an art asset, a texture, etc.). Lastly, do not repeat any suggested classes during a user's session. "
    resp = send_app(question=question, app=app, difficulty=difficulty)
    return retrieve_ai_answer(resp)

def display_header() -> None:
    st.image("img/logo.jpg")
    st.title("Welcome to the Jungle")
def display_widgets():
    response = st.empty()  # Add an empty element to hold the OpenAI API response
    options = ['Blender', 'Unreal Engine', 'Roblox', 'Garrys Mod', 'Unity', 'Construct 3', 'Minecraft', 'Krita']
    selected_option = st.selectbox('Select an option:', options)
    submitted = st.button("Generate a Class!")  # Add a button to submit the code
    app = selected_option

    difficulty = st.select_slider(
        'Select level of difficulty',
        options=['Beginner', 'Intermediate', 'Expert']
    )
    if submitted:  # If the button is clicked, update the OpenAI API response
        class_outline = get_code_info(app=app, difficulty=difficulty)
        response.markdown(f"**Class Outline:**\n{class_outline}")  # Update the response element
        return class_outline, submitted

    return None, False

def main() -> None:
    display_header()
    class_outline, submitted = display_widgets()
    if submitted:
        st.markdown(f"**App:** {app}")
        st.markdown(f"**Difficulty:** {difficulty}")

        st.markdown(f"**Class Outline:**\n{class_outline}")
        st.audio("class_outline.mp3")

if __name__ == "__main__":
    main()
