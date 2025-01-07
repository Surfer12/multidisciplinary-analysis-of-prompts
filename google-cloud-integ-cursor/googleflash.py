# First install and authenticate (run these in terminal):
# pip install --upgrade google-generativeai
# gcloud auth application-default login

import google.generativeai as genai
from google.generativeai import types
import base64

def generate():
    client = genai.Client(
        vertexai=True,
        project="snappy-run-446701-f0",
        location="us-central1"
    )

    model = "gemini-2.0-flash-thinking-exp-1219"
    contents = [
        types.Content(
            role="user",
            parts=[]
        )
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=2,
        top_p=0.95,
        max_output_tokens=8192,
        response_modalities=["TEXT"],
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="OFF"
            )
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk, end="")

generate()
