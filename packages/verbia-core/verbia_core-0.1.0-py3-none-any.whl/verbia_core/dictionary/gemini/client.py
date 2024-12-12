from __future__ import annotations

from os import environ

from verbia_core.error import VerbiaError


def get_client(api_key: str):
    import google.generativeai as genai

    if not api_key:
        api_key = environ.get("GEMINI_API_KEY")
    if not api_key:
        raise VerbiaError("GEMINI_API_KEY required.")
    model_name = environ.get("GEMINI_MODEL_NAME", "gemini-1.5-flash")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name=model_name)
