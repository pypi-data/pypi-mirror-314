from dataclasses import dataclass
from enum import Enum
from typing import Optional

from openai import OpenAI
from openai.types.chat import ChatCompletion


class Role(Enum):
    SYSTEM = "system"  # Specify the way the model answers
    USER = "user"  # User input
    ASSISTANT = "assistant"  # Assistant input


@dataclass
class ChatMessage:
    role: Role
    content: str

    def to_dict(self) -> dict[str, str]:
        return {"role": self.role.value, "content": self.content}


class OpenAIWrapper:
    __openai_client: OpenAI
    __model_name: str
    __prompts: list[ChatMessage]

    def __init__(
        self,
        model_name: str,
        *,
        bot_guidelines: Optional[str] = None,
        api_key: Optional[str] = None,
        organization: Optional[str] = None,
        project: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        self.__openai_client = OpenAI(
            api_key=api_key,
            organization=organization,
            project=project,
            base_url=base_url,
        )
        self.__model_name = model_name
        self.__prompts = []

        if bot_guidelines:
            self.__prompts.append(ChatMessage(Role.SYSTEM, bot_guidelines))

    @property
    def __raw_prompts(self) -> list[dict[str, str]]:
        return [prompt.to_dict() for prompt in self.__prompts]

    def __query_api(self, messages: list[dict[str, str]]) -> ChatCompletion:
        return self.__openai_client.chat.completions.create(
            model=self.__model_name,
            messages=messages,
        )

    def __add_user_message(self, content: str) -> None:
        self.__prompts.append(ChatMessage(Role.USER, content))

    def __add_assistant_message(self, content: str) -> None:
        self.__prompts.append(ChatMessage(Role.ASSISTANT, content))

    def ask(self, user_message: str) -> str:
        self.__add_user_message(user_message)

        chat_completion = self.__query_api(self.__raw_prompts)

        assistant_answer = chat_completion.choices[0].message.content

        self.__add_assistant_message(assistant_answer)

        return assistant_answer

    def add_user_input_without_ask(self, user_message: str) -> None:
        self.__add_user_message(user_message)

    def add_assistant_message_manually(self, assistant_message: str) -> None:
        self.__add_assistant_message(assistant_message)

    def ask_without_context(
        self, user_message: str, guidelines: Optional[str] = None
    ) -> str:
        messages = []
        if guidelines:
            messages.append(ChatMessage(Role.SYSTEM, guidelines).to_dict())
        messages.append(ChatMessage(Role.USER, user_message).to_dict())

        chat_completion = self.__query_api(messages)

        assistant_message = chat_completion.choices[0].message.content
        return assistant_message

    def clear_context(self) -> None:
        self.__prompts = self.__prompts[:1]

    def get_context(self) -> list[ChatMessage]:
        return self.__prompts

    def interactive_chat(self) -> None:
        while True:
            user_message = input("You: ")
            if user_message.lower() == "exit":
                break
            assistant_answer = self.ask(user_message)
            print(f"Assistant: {assistant_answer}")
