import os
import time
import openai
from typing import BinaryIO

import requests
from requests import Response

# API_KEY = os.getenv("aeed0c99f1c6dc558890ea34857b9533")
BASE_URL = "https://api.elevenlabs.io"
openai.api_key = "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"

def _get_id_from_name(response: Response, name: str) -> str:
    id_to_name = {
        item.get("name"): item.get("voice_id") for item in response.json()["voices"]
    }

    return id_to_name[name]


def _save_binary_to_mp3(content: BinaryIO, filename: str) -> None:
    with open(filename, "wb") as mp3_file:
        mp3_file.write(content)


def list_available_names() -> list[str]:
    voices_response = requests.get(
        f"{BASE_URL}/v1/voices", params={"xi-api-key": API_KEY}, timeout=5
    )
    return [item.get("name") for item in voices_response.json()["voices"]]


def convert_text_to_mp3(message: str, voice_name: str, mp3_filename: str) -> None:

    voices_response = requests.get(
        f"{BASE_URL}/v1/voices", params={"xi-api-key": API_KEY}, timeout=5
    )

    voice_id = _get_id_from_name(response=voices_response, name=voice_name)

    payload = {
        "text": message,
        "voice_settings": {"stability": 0.75, "similarity_boost": 0.75},
    }

    text_to_speech_response = requests.post(
        f"{BASE_URL}/v1/text-to-speech/{voice_id}/stream",
        params={"voice_id": voice_id, "xi-api-key": API_KEY},
        json=payload,
        timeout=5,
    )

    while text_to_speech_response.status_code != 200:
        time.sleep(5)
        print("Trying again, the API maybe busy...")
        text_to_speech_response = requests.post(
            f"{BASE_URL}/v1/text-to-speech/{voice_id}/stream",
            params={"voice_id": voice_id, "xi-api-key": API_KEY},
            json=payload,
            timeout=5,
        )

    _save_binary_to_mp3(content=text_to_speech_response.content, filename=mp3_filename)