from abc import ABC, abstractmethod
from collections import namedtuple
from typing import Any, Literal, Optional, Union

from openai.types.beta import Assistant, Thread
from openai.types.beta.threads import Message, Run
from pydantic import BaseModel


class AssistantCreateResponse(BaseModel):
    """Response model for assistant creation."""

    success: bool
    assistant: Optional[Union[Assistant, Any]] = None
    error: Optional[str] = None


class AssistantGetResponse(BaseModel):
    """Response model for getting an assistant."""

    success: bool
    assistant: Optional[Union[Assistant, Any]] = None
    error: Optional[str] = None


class AssistantUpdateResponse(BaseModel):
    """Response model for updating an assistant."""

    success: bool
    assistant: Optional[Union[Assistant, Any]] = None
    error: Optional[str] = None


class ThreadGetResponse(BaseModel):
    """Response model for getting a thread."""

    success: bool
    thread: Optional[Union[Thread, Any]] = None
    error: Optional[str] = None


class MessageCreateResponse(BaseModel):
    """Response model for creating a message."""

    success: bool
    message: Optional[Union[Message, Any]] = None
    error: Optional[str] = None


class ThreadMessagesGetResponse(BaseModel):
    """Response model for getting thread messages."""

    success: bool
    messages: list[Union[Message, Any]]
    error: Optional[str] = None


class AssistantMessageGetResponse(BaseModel):
    """Response model for getting assistant message."""

    success: bool
    message: Optional[Union[Message, Any]] = None
    error: Optional[str] = None


class ThreadClearResponse(BaseModel):
    """Response model for clearing thread messages."""

    success: bool
    error: Optional[str] = None


class RunCreateResponse(BaseModel):
    """Response model for creating a run."""

    success: bool
    run: Optional[Union[Run, Any]] = None
    error: Optional[str] = None


class ToolOutputsSubmitResponse(BaseModel):
    """Response model for submitting tool outputs."""

    success: bool
    run: Optional[Union[Run, Any]] = None
    error: Optional[str] = None


class InferResponse(BaseModel):
    """Response model for inference."""

    success: bool
    message: str
    error: Optional[str] = None


FunctionDefinition = namedtuple("FunctionDefinition", ["schema", "callable"])


class AssistantInterface(ABC):
    """Interface for assistant processor implementations."""

    @abstractmethod
    async def create_assistant(
        self,
        name: str,
        description: str,
        instructions: str,
        model: str,
        tools: list[dict],
        max_retries: int = 5,
    ) -> AssistantCreateResponse:
        """Creates an external assistant with the specified parameters.

        Args:
            name: The name of the assistant.
            description: A description of the assistant's purpose.
            instructions: Detailed instructions for the assistant's behavior.
            model: The model identifier to use (e.g. "gpt-3.5-turbo").
            tools: List of tool configurations for the assistant.
            max_retries: Maximum number of retry attempts.

        Returns:
            AssistantCreateResponse containing success status, assistant object if successful,
            and error message if failed.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    async def update_assistant(
        self,
        assistant_id: str,
        max_retries: int = 5,
        **update_params,
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
        pass

    @abstractmethod
    async def create_thread(self, **kwargs) -> ThreadGetResponse:
        """Create a new thread.

        Returns:
            ThreadGetResponse containing success status, thread object if successful,
            and error message if failed.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass
