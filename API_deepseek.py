from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
deepseek_api_key = os.getenv('deepseek_api_key')

client = AsyncOpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")


async def make_responce(messages_from_uniq_user):
    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages=messages_from_uniq_user,
        stream=False
    )
    return response
