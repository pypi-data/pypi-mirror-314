from typing import Any

import aisuite as ai

CLIENT = ai.Client()


def chat(
    message: str,
    model: str = "openai:gpt-4o",
    llm_options: dict[str, Any] | None = None,
) -> str:
    if not llm_options:
        llm_options = {}

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": message,
        },
    ]

    response = CLIENT.chat.completions.create(
        model=model,
        messages=messages,
        **llm_options,
    )

    return response.choices[0].message.content
