from __future__ import annotations

import asyncio
import random

from ..typing import Type, List, CreateResult, Messages, AsyncResult
from .types import BaseProvider, BaseRetryProvider, ProviderType
from .. import debug
from ..errors import RetryProviderError, RetryNoProviderError

DEFAULT_TIMEOUT = 60

class IterListProvider(BaseRetryProvider):
    def __init__(
        self,
        providers: List[Type[BaseProvider]],
        shuffle: bool = True
    ) -> None:
        """
        Initialize the BaseRetryProvider.
        Args:
            providers (List[Type[BaseProvider]]): List of providers to use.
            shuffle (bool): Whether to shuffle the providers list.
            single_provider_retry (bool): Whether to retry a single provider if it fails.
            max_retries (int): Maximum number of retries for a single provider.
        """
        self.providers = providers
        self.shuffle = shuffle
        self.working = True
        self.last_provider: Type[BaseProvider] = None

    def create_completion(
        self,
        model: str,
        messages: Messages,
        stream: bool = False,
        **kwargs,
    ) -> CreateResult:
        """
        Create a completion using available providers, with an option to stream the response.
        Args:
            model (str): The model to be used for completion.
            messages (Messages): The messages to be used for generating completion.
            stream (bool, optional): Flag to indicate if the response should be streamed. Defaults to False.
        Yields:
            CreateResult: Tokens or results from the completion.
        Raises:
            Exception: Any exception encountered during the completion process.
        """
        exceptions = {}
        started: bool = False

        for provider in self.get_providers(stream):
            self.last_provider = provider
            debug.log(f"Using {provider.__name__} provider")
            try:
                for chunk in provider.create_completion(model, messages, stream, **kwargs):
                    if chunk:
                        yield chunk
                        started = True
                if started:
                    return
            except Exception as e:
                exceptions[provider.__name__] = e
                if debug.logging:
                    print(f"{provider.__name__}: {e.__class__.__name__}: {e}")
                if started:
                    raise e

        raise_exceptions(exceptions)

    async def create_async(
        self,
        model: str,
        messages: Messages,
        **kwargs,
    ) -> str:
        """
        Asynchronously create a completion using available providers.
        Args:
            model (str): The model to be used for completion.
            messages (Messages): The messages to be used for generating completion.
        Returns:
            str: The result of the asynchronous completion.
        Raises:
            Exception: Any exception encountered during the asynchronous completion process.
        """
        exceptions = {}

        for provider in self.get_providers(False):
            self.last_provider = provider
            debug.log(f"Using {provider.__name__} provider")
            try:
                chunk = await asyncio.wait_for(
                    provider.create_async(model, messages, **kwargs),
                    timeout=kwargs.get("timeout", DEFAULT_TIMEOUT),
                )
                if chunk:
                    return chunk
            except Exception as e:
                exceptions[provider.__name__] = e
                if debug.logging:
                    print(f"{provider.__name__}: {e.__class__.__name__}: {e}")

        raise_exceptions(exceptions)

    def get_providers(self, stream: bool) -> list[ProviderType]:
        providers = [p for p in self.providers if p.supports_stream] if stream else self.providers
        if self.shuffle:
            random.shuffle(providers)
        return providers

    async def create_async_generator(
        self,
        model: str,
        messages: Messages,
        stream: bool = True,
        **kwargs
    ) -> AsyncResult:
        exceptions = {}
        started: bool = False

        for provider in self.get_providers(stream):
            self.last_provider = provider
            debug.log(f"Using {provider.__name__} provider")
            try:
                if not stream:
                    chunk = await asyncio.wait_for(
                        provider.create_async(model, messages, **kwargs),
                        timeout=kwargs.get("timeout", DEFAULT_TIMEOUT),
                    )
                    if chunk:
                        yield chunk
                        started = True
                elif hasattr(provider, "create_async_generator"):
                    async for chunk in provider.create_async_generator(model, messages, stream=stream, **kwargs):
                        if chunk:
                            yield chunk
                            started = True
                else:
                    for token in provider.create_completion(model, messages, stream, **kwargs):
                        yield token
                        started = True
                if started:
                    return
            except Exception as e:
                exceptions[provider.__name__] = e
                debug.log(f"{provider.__name__}: {e.__class__.__name__}: {e}")
                if started:
                    raise e

        raise_exceptions(exceptions)

class RetryProvider(IterListProvider):
    def __init__(
        self,
        providers: List[Type[BaseProvider]],
        shuffle: bool = True,
        single_provider_retry: bool = False,
        max_retries: int = 3,
    ) -> None:
        """
        Initialize the BaseRetryProvider.
        Args:
            providers (List[Type[BaseProvider]]): List of providers to use.
            shuffle (bool): Whether to shuffle the providers list.
            single_provider_retry (bool): Whether to retry a single provider if it fails.
            max_retries (int): Maximum number of retries for a single provider.
        """
        super().__init__(providers, shuffle)
        self.single_provider_retry = single_provider_retry
        self.max_retries = max_retries

    def create_completion(
        self,
        model: str,
        messages: Messages,
        stream: bool = False,
        **kwargs,
    ) -> CreateResult:
        """
        Create a completion using available providers, with an option to stream the response.
        Args:
            model (str): The model to be used for completion.
            messages (Messages): The messages to be used for generating completion.
            stream (bool, optional): Flag to indicate if the response should be streamed. Defaults to False.
        Yields:
            CreateResult: Tokens or results from the completion.
        Raises:
            Exception: Any exception encountered during the completion process.
        """
        if self.single_provider_retry:
            exceptions = {}
            started: bool = False
            provider = self.providers[0]
            self.last_provider = provider
            for attempt in range(self.max_retries):
                try:
                    if debug.logging:
                        print(f"Using {provider.__name__} provider (attempt {attempt + 1})")
                    for token in provider.create_completion(model, messages, stream, **kwargs):
                        yield token
                        started = True
                    if started:
                        return
                except Exception as e:
                    exceptions[provider.__name__] = e
                    if debug.logging:
                        print(f"{provider.__name__}: {e.__class__.__name__}: {e}")
                    if started:
                        raise e
            raise_exceptions(exceptions)
        else:
            yield from super().create_completion(model, messages, stream, **kwargs)

    async def create_async(
        self,
        model: str,
        messages: Messages,
        **kwargs,
    ) -> str:
        """
        Asynchronously create a completion using available providers.
        Args:
            model (str): The model to be used for completion.
            messages (Messages): The messages to be used for generating completion.
        Returns:
            str: The result of the asynchronous completion.
        Raises:
            Exception: Any exception encountered during the asynchronous completion process.
        """
        exceptions = {}

        if self.single_provider_retry:
            provider = self.providers[0]
            self.last_provider = provider
            for attempt in range(self.max_retries):
                try:
                    if debug.logging:
                        print(f"Using {provider.__name__} provider (attempt {attempt + 1})")
                    return await asyncio.wait_for(
                        provider.create_async(model, messages, **kwargs),
                        timeout=kwargs.get("timeout", 60),
                    )
                except Exception as e:
                    exceptions[provider.__name__] = e
                    if debug.logging:
                        print(f"{provider.__name__}: {e.__class__.__name__}: {e}")
            raise_exceptions(exceptions)
        else:
            return await super().create_async(model, messages, **kwargs)

    async def create_async_generator(
        self,
        model: str,
        messages: Messages,
        stream: bool = True,
        **kwargs
    ) -> AsyncResult:
        exceptions = {}
        started = False

        if self.single_provider_retry:
            provider = self.providers[0]
            self.last_provider = provider
            for attempt in range(self.max_retries):
                try:
                    debug.log(f"Using {provider.__name__} provider (attempt {attempt + 1})")
                    if not stream:
                        chunk = await asyncio.wait_for(
                            provider.create_async(model, messages, **kwargs),
                            timeout=kwargs.get("timeout", DEFAULT_TIMEOUT),
                        )
                        if chunk:
                            yield chunk
                            started = True
                    elif hasattr(provider, "create_async_generator"):
                        async for chunk in provider.create_async_generator(model, messages, stream=stream, **kwargs):
                            if chunk:
                                yield chunk
                                started = True
                    else:
                        for token in provider.create_completion(model, messages, stream, **kwargs):
                            yield token
                            started = True
                    if started:
                        return
                except Exception as e:
                    exceptions[provider.__name__] = e
                    if debug.logging:
                        print(f"{provider.__name__}: {e.__class__.__name__}: {e}")
            raise_exceptions(exceptions)
        else:
            async for chunk in super().create_async_generator(model, messages, stream, **kwargs):
                yield chunk

def raise_exceptions(exceptions: dict) -> None:
    """
    Raise a combined exception if any occurred during retries.

    Raises:
        RetryProviderError: If any provider encountered an exception.
        RetryNoProviderError: If no provider is found.
    """
    if exceptions:
        raise RetryProviderError("RetryProvider failed:\n" + "\n".join([
            f"{p}: {exception.__class__.__name__}: {exception}" for p, exception in exceptions.items()
        ]))

    raise RetryNoProviderError("No provider found")