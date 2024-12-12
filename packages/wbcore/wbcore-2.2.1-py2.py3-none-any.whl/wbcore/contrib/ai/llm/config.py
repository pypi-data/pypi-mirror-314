from typing import TYPE_CHECKING, Any, Callable, Generic, TypeVar

from celery import shared_task
from django.db import models
from django.db.models.signals import ModelSignal
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from ..exceptions import APIStatusErrors
from .utils import construct_prompt, run_llm

if TYPE_CHECKING:
    from pydantic import BaseModel


@shared_task(
    autoretry_for=tuple(APIStatusErrors),
    retry_backoff=10,
    max_retries=5,  # retry i5 times maximum
    default_retry_delay=30,  # retry in 30s
    retry_jitter=False,
)
def invoke_as_task(
    instance,
    prompt: str,
    chat_model: type[BaseChatModel],
    chat_model_name: str,
    max_tokens: int,
    model_field: str | None,
    output_model: "type[BaseModel] | None",
    llm_kwargs: dict[str, Any],
):
    result = run_llm(prompt, instance, output_model, chat_model, chat_model_name, max_tokens, **llm_kwargs)
    if model_field is not None:
        setattr(instance, model_field, result)

    if output_model is not None:
        for field, value in result.items():
            setattr(instance, field, value)
    return instance


T = TypeVar("T", bound=models.Model)


add_llm_prompt = ModelSignal()


class LLMConfig(Generic[T]):
    def __init__(
        self,
        key: str,
        prompt: Callable | str,
        field: str | None = None,
        output_model: "type[BaseModel] | None" = None,
        on_save: bool = True,
        on_condition: Callable | bool | None = None,
        chat_model: type[BaseChatModel] = ChatOpenAI,
        chat_model_name: str = "gpt-4o-mini",
        max_tokens: int = 16000,
        **kwargs
    ):
        self.key = key
        self.on_save = on_save
        self.field = field
        self.on_condition = on_condition
        self.prompt = prompt
        self.output_model = output_model
        self.chat_model = chat_model
        self.chat_model_name = chat_model_name
        self.max_tokens = max_tokens
        self.kwargs = kwargs

    def check_condition(self, instance: T) -> bool:
        if self.on_condition is None:
            return True
        if callable(self.on_condition):
            return self.on_condition(instance)
        return bool(self.on_condition)

    def get_prompt(self, instance: T):
        prompt = construct_prompt(instance, self.prompt)
        for _, response in add_llm_prompt.send(sender=instance.__class__, instance=instance, key=self.key):
            prompt.extend(response)

        return prompt

    def schedule(self, instance: T, initial: bool = True):
        prompt = self.get_prompt(instance)
        args = []
        if initial:
            args.append(instance)
        args.extend(
            [
                prompt,
                self.chat_model,
                self.chat_model_name,
                self.max_tokens,
                self.field,
                self.output_model,
                self.kwargs,
            ]
        )
        return invoke_as_task.s(*args)

    def invoke(self, instance: T):
        self.schedule(instance)()
