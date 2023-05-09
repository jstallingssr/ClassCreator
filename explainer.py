import os
from functools import partial

import openai



openai.api_key = "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"

def send_app(question: str, app: str, difficulty: str) -> dict:
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"App: {app}, Difficulty: {difficulty}"},
            {"role": "user", "content": question},
        ],
    )


def retrieve_ai_answer(response: dict) -> str:
    return response["choices"][0]["message"]["content"]


def get_code_info(question: str, code: str, app: str, difficulty: str) -> str:
    resp = send_app(question=f"{question}\n\n{code}", app=app, difficulty=difficulty)
    return retrieve_ai_answer(resp)


retrieve_code_language = partial(
    get_code_info,
    question="Tell me what the user selected?",
)

