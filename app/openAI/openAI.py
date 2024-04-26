from openai import OpenAI
from utils.settings import Settings

settings = Settings()

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

def summarize_text(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        # model="gpt-4-turbo", 
        messages = [
            {"role": "system", "content": "You are tasked with summarizing the user's text into concise bullet points. Please ensure that each point is clearly numbered, for example: 1. [Summary Point], 2. [Summary Point], etc. The objective is to condense the article's main ideas into an easily understandable format."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()