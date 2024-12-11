import configparser
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
import warnings
from ollama import Client
from pathlib import Path


warnings.filterwarnings("ignore")

config = configparser.ConfigParser()
config.read(Path.cwd() / "config.ini", encoding="utf8")

MODEL_NAME = config["llm"]["MODEL_NAME"]
MODEL_ID = config["llm"]["MODEL_ID"]
TEMPERATURE = config["llm"]["TEMPERATURE"]
API_KEY = config["key"]["GOOGLE_API_KEY"]
OLLAMA_URL = config["llm"]["OLLAMA_URL"]


def load_model_llm():
    if MODEL_NAME == "gemini":
        generation_config = {
            "temperature": TEMPERATURE,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        genai.configure(api_key=API_KEY)
        return genai.GenerativeModel(
            model_name=MODEL_ID,
            generation_config=generation_config,
        )
    else:
        raise NotImplementedError(
            "The implementation for other types of LLMs are not ready yet!"
        )


def gen_llm_local(prompt):
    client = Client(host=OLLAMA_URL)
    llm = client.generate(
        model=MODEL_NAME,
        prompt=prompt,
    )
    return llm["response"]
