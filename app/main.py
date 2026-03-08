import argparse
import os
import json
import asyncio
from typing import cast

from openai import OpenAI
from openai._utils import assert_signatures_in_sync
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionMessageToolCall, ChatCompletionToolParam

import app.tools
from app.helpers.discovery import load_tools
from app.helpers.executor import ToolExecutor
from app.helpers.registry import TOOL_REGISTRY


API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")


def tools_for_llm() -> list[ChatCompletionToolParam]:
    return [tool.schema 
        for tool in TOOL_REGISTRY.values()
    ]

async def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    load_tools(app.tools)

    executor = ToolExecutor()

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    messages: list[ChatCompletionMessageParam] = [{"role": "user", "content": args.p}]

    while True:
        response = client.chat.completions.create(
            model="anthropic/claude-haiku-4.5",
            messages=messages,
            tools=tools_for_llm()
        )

        msg = response.choices[0].message

        if not msg.tool_calls:
            print(msg.content)
            break

        messages.append(msg)

        for call in msg.tool_calls:
            if call.type != "function":
                continue

            name = call.function.name
            args_dict = json.loads(call.function.arguments or "{}")
            result = await executor.execute(name, args_dict)

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result),
            })

if __name__ == "__main__":
    asyncio.run(main())
