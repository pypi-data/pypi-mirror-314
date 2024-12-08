from __future__ import annotations

import json
import base64
import random

from ...typing import AsyncResult, Messages
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ...errors import ModelNotFoundError
from ...requests import StreamSession, raise_for_status
from ...image import ImageResponse

from .HuggingChat import HuggingChat

class HuggingFace(AsyncGeneratorProvider, ProviderModelMixin):
    url = "https://huggingface.co/chat"
    working = True
    supports_message_history = True
    default_model = HuggingChat.default_model
    default_image_model = "black-forest-labs/FLUX.1-dev"
    models = [*HuggingChat.models, default_image_model]
    image_models = [default_image_model]
    model_aliases = HuggingChat.model_aliases

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool = True,
        proxy: str = None,
        api_base: str = "https://api-inference.huggingface.co",
        api_key: str = None,
        max_new_tokens: int = 1024,
        temperature: float = 0.7,
        prompt: str = None,
        **kwargs
    ) -> AsyncResult:
        model = cls.get_model(model)
        headers = {
            'accept': '*/*',
            'accept-language': 'en',
            'cache-control': 'no-cache',
            'origin': 'https://huggingface.co',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://huggingface.co/chat/',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        }
        if api_key is not None:
            headers["Authorization"] = f"Bearer {api_key}"
        if model in cls.image_models:
            stream = False
            prompt = messages[-1]["content"] if prompt is None else prompt
            payload = {"inputs": prompt, "parameters": {"seed": random.randint(0, 2**32)}}
        else:
            params = {
                "return_full_text": False,
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                **kwargs
            }
            payload = {"inputs": format_prompt(messages), "parameters": params, "stream": stream}
        async with StreamSession(
            headers=headers,
            proxy=proxy,
            timeout=600
        ) as session:
            async with session.post(f"{api_base.rstrip('/')}/models/{model}", json=payload) as response:
                if response.status == 404:
                    raise ModelNotFoundError(f"Model is not supported: {model}")
                await raise_for_status(response)
                if stream:
                    first = True
                    async for line in response.iter_lines():
                        if line.startswith(b"data:"):
                            data = json.loads(line[5:])
                            if not data["token"]["special"]:
                                chunk = data["token"]["text"]
                                if first:
                                    first = False
                                    chunk = chunk.lstrip()
                                if chunk:
                                    yield chunk
                else:
                    if response.headers["content-type"].startswith("image/"):
                        base64_data = base64.b64encode(b"".join([chunk async for chunk in response.iter_content()]))
                        url = f"data:{response.headers['content-type']};base64,{base64_data.decode()}"
                        yield ImageResponse(url, prompt)
                    else:
                        yield (await response.json())[0]["generated_text"].strip()

def format_prompt(messages: Messages) -> str:
    system_messages = [message["content"] for message in messages if message["role"] == "system"]
    question = " ".join([messages[-1]["content"], *system_messages])
    history = "".join([
        f"<s>[INST]{messages[idx-1]['content']} [/INST] {message['content']}</s>"
        for idx, message in enumerate(messages)
        if message["role"] == "assistant"
    ])
    return f"{history}<s>[INST] {question} [/INST]"
