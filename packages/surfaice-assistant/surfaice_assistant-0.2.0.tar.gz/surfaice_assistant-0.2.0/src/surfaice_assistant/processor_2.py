from typing import Any, Literal, Type, Union

from openai.types.beta import Thread
from openai.types.beta.threads import Run

from .abstract_provider import AssistantInterface
from .abstract_provider.assistant import (
    AssistantCreateResponse,
    AssistantGetResponse,
    AssistantMessageGetResponse,
    AssistantUpdateResponse,
    InferResponse,
    MessageCreateResponse,
    RunCreateResponse,
    ThreadClearResponse,
    ThreadGetResponse,
    ThreadMessagesGetResponse,
    ToolOutputsSubmitResponse,
)
from .implementations.openai_provider import OpenAIAssistantImpl

OPENAI = "openai"


# Registry of available assistant processor implementations.
# When adding a new assistant implementation, make sure to register it here with its provider name.
#
# Current implementations:
#   - "openai": OpenAI Assistant API implementation
processor_implementations: dict[str, Union[Type[AssistantInterface], Any]] = {
    OPENAI: OpenAIAssistantImpl,
}


def get_assistant_processor(provider: str, **kwargs):
    """Get the appropriate assistant processor implementation based on the config.

    Args:
        provider: The provider name to get implementation for.
        **kwargs: Additional arguments to pass to the implementation.

    Returns:
        An instance of the appropriate AssistantInterface implementation.

    Raises:
        KeyError: If the requested provider is not implemented.
    """
    if provider not in processor_implementations:
        raise KeyError(
            f"AssistanProcessor for Provider: {provider} is not implemented."
        )
    return processor_implementations[provider](**kwargs)


class AssistantProcessor(AssistantInterface):
    """Base class for processing assistant responses.

    This class serves as a blueprint for implementing various assistant processors.
    It defines common attributes and methods that all processors should implement.

    Attributes:
        processor (AssistantInterface): The underlying processor implementation.
    """
    def __init__(
        self,
        api_key: str,
        provider: str,
    ) -> None:
        """Initialize the AssistantProcessor.

        Args:
            api_key: The API key for the provider.
            provider: The provider name (e.g. "openai").
        """
        self.processor = get_assistant_processor(provider, api_key=api_key)

    def __getattr__(self, name: str):
        """Allow calling any method from the implementation class."""
        return getattr(self.processor, name)

    async def create_assistant(
        self,
        name: str,
        model: str,
        description: str | None = None,
        instructions: str | None = None,
        tools: list[dict[str, Any] | None] = [],
        max_retries: int = 5,
    ) -> AssistantCreateResponse:
        """Creates an external assistant with the specified parameters.

        Args:
            name: The name of the assistant.
            model: The model identifier to use (e.g. "gpt-3.5-turbo").
            description: A description of the assistant's purpose.
            instructions: Detailed instructions for the assistant's behavior.
            tools: List of tool configurations for the assistant.
            max_retries: Maximum number of retry attempts.

        Returns:
            AssistantCreateResponse containing success status, assistant object if successful,
            and error message if failed.
        """
        return await self.processor.create_assistant(
            name=name,
            model=model,
            description=description,
            instructions=instructions,
            tools=tools,
            max_retries=max_retries,
        )

    async def get_assistant(
        self,
        assistant_id: str,
        max_retries: int = 5,
    ) -> AssistantGetResponse:
        """Get an assistant by ID.

        Args:
            assistant_id: The ID of the assistant to retrieve.
            max_retries: Maximum number of retry attempts.

        Returns:
            AssistantGetResponse containing success status, assistant object if successful,
            and error message if failed.
        """
        return await self.processor.get_assistant(
            assistant_id=assistant_id,
            max_retries=max_retries,
        )

    async def update_assistant(
        self,
        assistant_id: str,
        max_retries: int = 5,
        **update_params: Any,
    ) -> AssistantUpdateResponse:
        """Updates an existing assistant with the specified parameters.

        Args:
            assistant_id: The ID of the assistant to update.
            max_retries: Maximum number of retry attempts.
            **update_params: Key-value pairs of parameters to update.

        Returns:
            AssistantUpdateResponse containing success status, updated assistant object if successful,
            and error message if failed.
        """
        return await self.processor.update_assistant(
            assistant_id=assistant_id,
            max_retries=max_retries,
            **update_params,
        )

    async def create_thread(self, **kwargs: Any) -> ThreadGetResponse:
        """Create a new thread.

        Returns:
            ThreadGetResponse containing success status, thread object if successful,
            and error message if failed.
        """
        return await self.processor.create_thread(**kwargs)

    async def get_thread(
        self,
        thread_id: str,
        max_retries: int = 5,
    ) -> ThreadGetResponse:
        """Get a thread by ID.

        Args:
            thread_id: The ID of the thread to retrieve.
            max_retries: Maximum number of retry attempts.

        Returns:
            ThreadGetResponse containing success status, thread object if successful,
            and error message if failed.
        """
        return await self.processor.get_thread(
            thread_id=thread_id,
            max_retries=max_retries,
        )

    async def create_message(
        self,
        thread_id: str,
        content: str,
        role: Literal["user", "assistant"] = "user",
    ) -> MessageCreateResponse:
        """Create a message in a thread.

        Args:
            thread_id: The ID of the thread to create the message in.
            content: The content of the message.
            role: The role of the message sender ("user" or "assistant").

        Returns:
            MessageCreateResponse containing success status, message object if successful,
            and error message if failed.
        """
        return await self.processor.create_message(
            thread_id=thread_id,
            content=content,
            role=role,
        )

    async def get_thread_messages(
        self,
        thread_id: str,
        max_retries: int = 5,
    ) -> ThreadMessagesGetResponse:
        """Get all messages from a thread.

        Args:
            thread_id: The ID of the thread to get messages from.
            max_retries: Maximum number of retry attempts.

        Returns:
            ThreadMessagesGetResponse containing success status, list of messages if successful,
            and error message if failed.
        """
        return await self.processor.get_thread_messages(
            thread_id=thread_id,
            max_retries=max_retries,
        )

    async def get_assistant_response(
        self,
        thread_id: str,
        max_retries: int = 5,
    ) -> AssistantMessageGetResponse:
        """Get the assistant's response from a thread.

        Args:
            thread_id: The ID of the thread to get the response from.
            max_retries: Maximum number of retry attempts.

        Returns:
            AssistantMessageGetResponse containing success status, message object if successful,
            and error message if failed.
        """
        return await self.processor.get_assistant_response(
            thread_id=thread_id,
            max_retries=max_retries,
        )

    async def clear_thread_messages(
        self,
        thread_id: str,
        max_retries: int = 5,
    ) -> ThreadClearResponse:
        """Delete all messages from a thread.

        Args:
            thread_id: The ID of the thread to clear messages from.
            max_retries: Maximum number of retry attempts.

        Returns:
            ThreadClearResponse containing success status and error message if failed.
        """
        return await self.processor.clear_thread_messages(
            thread_id=thread_id,
            max_retries=max_retries,
        )

    async def create_run(
        self,
        thread_id: str,
        assistant_id: str,
        max_retries: int = 5,
    ) -> RunCreateResponse:
        """Create a run for a thread.

        Args:
            thread_id: The ID of the thread to create the run in.
            assistant_id: The ID of the assistant to use for the run.
            max_retries: Maximum number of retry attempts.

        Returns:
            RunCreateResponse containing success status, run object if successful,
            and error message if failed.
        """
        return await self.processor.create_run(
            thread_id=thread_id,
            assistant_id=assistant_id,
            max_retries=max_retries,
        )

    async def submit_tool_outputs(
        self,
        run: Run,
        thread: Thread,
        tool_calls: list,
        max_retries: int = 5,
    ) -> ToolOutputsSubmitResponse:
        """Submit tool outputs for a run.

        Args:
            run: The run object containing tool calls.
            thread: The thread object where the run is executing.
            tool_calls: List of tool calls to process.
            max_retries: Maximum number of retry attempts.

        Returns:
            ToolOutputsSubmitResponse containing success status, updated run object if successful,
            and error message if failed.
        """
        return await self.processor.submit_tool_outputs(
            run=run,
            thread=thread,
            tool_calls=tool_calls,
            max_retries=max_retries,
        )

    async def infer(
        self,
        assistant_id: str,
        thread_id: str,
        message: str,
    ) -> InferResponse:
        """Complete cycle of interaction with assistant.

        Args:
            assistant_id: The ID of the assistant to use.
            thread_id: The ID of the thread for the interaction.
            message: The user message to send.

        Returns:
            InferResponse containing success status, assistant's response message if successful,
            and error message if failed.
        """
        return await self.processor.infer(
            assistant_id=assistant_id,
            thread_id=thread_id,
            message=message,
        )
