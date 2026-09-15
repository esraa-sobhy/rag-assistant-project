import os

import requests
from dotenv import load_dotenv


load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")

if not API_BASE_URL:
    raise ValueError("API_BASE_URL not found in .env")


def ask_question(question: str) -> dict:
    response = requests.post(
        f"{API_BASE_URL}/query",
        json={"question": question},
        timeout=60,
    )

    response.raise_for_status()

    return response.json()