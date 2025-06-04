import base64
import os
import requests
import json
from PIL import Image
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def analyze_image(image: Image.Image):
    """
    Uses OpenRouter GPT-4 Vision or Claude to analyze rooftop image.
    Returns estimated area, usable space, obstacles, panel recommendation.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Make sure it's in your .env file as OPENROUTER_API_KEY")

    # Save image temporarily
    image_path = "temp_image.jpg"
    image.save(image_path)

    # Convert image to base64
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    # Prompt
    prompt = (
        "You are a solar expert. Analyze this rooftop image and return:\n"
        "- Estimated rooftop area in square meters\n"
        "- Usable area excluding obstacles\n"
        "- Number of standard 1.6 m² solar panels that can fit\n"
        "- Mention if there are obstacles (like tanks or ACs)\n"
        "Respond only in JSON format like:\n"
        "{\"area_m2\": 123, \"usable_area_m2\": 87, \"panel_count\": 54, \"obstacles\": \"2 tanks on left\"}"
    )

    payload = {
        "model": "anthropic/claude-3-opus",  # or try another model from OpenRouter if this fails
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                ]
            }
        ],
        "max_tokens": 300 # reduce to avoid 402 token limit errors

    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        json=payload,
        headers=headers
    )

    if response.status_code != 200:
        raise Exception(f"OpenRouter API error: {response.status_code} - {response.text}")

    try:
        result_text = response.json()["choices"][0]["message"]["content"]
        # Try parsing safely
        result_data = json.loads(result_text.replace("'", "\""))  # Convert single quotes to double quotes
        return result_data
    except Exception as e:
        raise Exception(f"Failed to parse AI response. Got: {result_text}\nError: {e}")
