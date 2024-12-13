from typing import Any, Callable

from langchain_core.language_models import BaseChatModel
from langchain_core.messages.base import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

type Prompt = str | list[BaseMessage] | BaseMessage


def construct_prompt(instance: Any, prompt: Prompt | Callable[[Any], Prompt]) -> Prompt:
    if isinstance(prompt, str):
        return prompt.format(instance)

    elif callable(prompt):
        return prompt(instance)

    return prompt


def run_llm(
    prompt: Prompt | Callable[[Any], Prompt],
    instance: Any | None = None,
    output_model: "type[BaseModel] | None" = None,
    chat_model: type[BaseChatModel] = ChatOpenAI,
    chat_model_name: str = "gpt-4o-mini",
    max_tokens: int = 16000,
    **kwargs,
) -> str | dict[str, Any]:
    model = chat_model(model=chat_model_name, max_tokens=max_tokens, **kwargs)  # type: ignore
    prompt = construct_prompt(instance, prompt)
    if output_model is None:
        result = model.invoke(prompt, **kwargs)  # type: ignore
        parser = StrOutputParser()
        return parser.invoke(result, **kwargs)

    structured_model = model.with_structured_output(output_model)
    result = structured_model.invoke(prompt)  # type: ignore

    output = dict()
    for field, value in result:
        output[field] = value

    return output
