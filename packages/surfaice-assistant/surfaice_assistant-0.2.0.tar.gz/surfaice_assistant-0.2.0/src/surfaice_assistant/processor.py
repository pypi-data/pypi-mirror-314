import asyncio
import httpx
from typing import IO

from openai import AsyncOpenAI
from openai.types.beta import Assistant, Thread
from openai.types.beta.threads import Message, Run


class AssistantProcessor:
    """
    AssistantProcessor class for managing interactions with OpenAI's Assistant API.

    This class provides methods to create messages, start runs, and execute function calls
    using the OpenAI Assistant API.

    Attributes:
        client (AsyncOpenAI): An instance of the AsyncOpenAI client for API interactions.
        function_registry (dict): A dictionary mapping function names to their implementations.

    Args:
        function_registry (dict): A dictionary of functions that can be called by the assistant.

    """

    def __init__(self, function_registry: dict | None = None, is_remote: bool = False,
                 remote_backend_url: str | None = None):
        self.client = AsyncOpenAI()
        if function_registry is None:
            self.function_registry = {}
        else:
            self.function_registry = function_registry
        self.is_remote = is_remote
        if is_remote and remote_backend_url is None:
            raise ValueError("remote_backend_url is required when is_remote is True")
        self.remote_backend_url = remote_backend_url

    async def start_run(self, thread_id: str, assistant_id: str) -> Run | None:
        """
        Start a new run for the specified thread and assistant.

        This method initiates a new run, which represents an execution of the assistant
        on the current thread. It continuously checks the run status and handles any
        required actions until the run is completed.

        Args:
            thread_id (str): The ID of the thread to start the run on.
            assistant_id (str): The ID of the assistant to use for the run.

        Returns:
            Run | None: The completed Run object if successful, None if an error occurs.

        Raises:
            Exception: If there's an error starting or processing the run.
        """
        try:
            run = await self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id
            )
            # Проверка статуса обработки
            while run.status != "completed":
                run = await self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

                if run.status == "requires_action":
                    tool_calls = run.required_action.submit_tool_outputs.tool_calls
                    await self.submit_tool_outputs(run, thread_id, tool_calls)

                await asyncio.sleep(1)

            return run
        except Exception as e:
            print(f"Error starting run: {e}")
            return None

    async def create_message(self, thread_id: str, assistant_id: str, content: str) -> Message | None:
        """
        Create a new message in the specified thread and start a run with the assistant.

        This method creates a new user message in the given thread and then initiates
        a run with the specified assistant. It handles any exceptions that may occur
        during this process.

        Args:
            thread_id (str): The ID of the thread to create the message in.
            assistant_id (str): The ID of the assistant to use for the run.
            content (str): The content of the message to be created.

        Returns:
            Message | None: The created Message object if successful, None if an error occurs.

        Raises:
            Exception: If there's an error creating the message or starting the run.
        """
        try:
            message = await self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=content
            )
            await self.start_run(thread_id, assistant_id)
            return message
        except Exception as e:
            print(f"Error creating message: {e}")
            return None

    async def execute_function_call(self, thread: Thread, function_name: str, arguments: dict):
        """
        Execute a function call based on the provided function name and arguments.

        This method checks if the requested function exists in the function registry.
        If the function is not found, it returns an error message.

        Args:
            thread (Thread): The thread object associated with the function call.
            function_name (str): The name of the function to be executed.
            arguments (dict): A dictionary of arguments to be passed to the function.

        Returns:
            str: An error message or function result.

        Note:
            This is part of the error handling before attempting to execute the function.
            The actual function execution is handled in the subsequent code.
        """
        if function_name not in self.function_registry:
            return f"Function '{function_name}' not found in the function registry"

        function = self.function_registry[function_name]

        try:
            # Execute the function with the provided arguments
            result = await function(thread=thread, **arguments)
            return result
        except Exception as e:
            return f"Error executing function '{function_name}': {str(e)}"

    async def execute_remote_function_call(self, thread: Thread, function_name: str, arguments: dict):
        """
        Execute a remote function call based on the provided function name and arguments.

        This method sends a request to a remote backend to execute the function.

        Args:
            thread (Thread): The thread object associated with the function call.
            function_name (str): The name of the function to be executed.
            arguments (dict): A dictionary of arguments to be passed to the function.

        Returns:
            str: The response from the remote backend or an error message.
        """
        try:

            async with httpx.AsyncClient() as client:
                payload = {
                    "function_name": function_name,
                    "arguments": arguments,
                    "thread_id": thread.id
                }
                response = await client.post(
                    f"{self.remote_backend_url}/execute-function",
                    json=payload
                )
                if response.status_code == 200:
                    remote_response = response.json()["result"]
                    return remote_response
                return f"Remote backend returned status code {response.status_code}"
        except Exception as e:
            return f"Error executing remote function '{function_name}': {str(e)}"

    async def submit_tool_outputs(self, run: Run, thread: Thread, tool_calls: list) -> Run:
        """
        Initialize an empty list to store tool outputs.

        This list will be populated with the results of function calls
        made in response to the assistant's tool calls. Each output
        will be a dictionary containing the tool call ID and the
        function's response.

        Returns:
            list: An empty list that will be filled with tool outputs.
        """
        tool_outputs = []
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = tool_call.function.arguments
            function_id = tool_call.id
            if self.is_remote:
                function_response = await self.execute_remote_function_call(thread, function_name, arguments)
            else:
                function_response = await self.execute_function_call(thread, function_name, arguments)
            tool_outputs.append(
                {
                    "tool_call_id": function_id,
                    "output": str(function_response),
                }
            )

        run = await self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
        )

        return run

    async def get_assistant_response(self, thread_id: str, max_retries: int = 3) -> Message | None:
        """
        Attempt to retrieve the assistant's response from the thread.

        This method will retry up to `max_retries` times if no assistant message is found.
        It introduces a delay between retries to allow time for the assistant to respond.

        Args:
            thread_id (str): The ID of the thread to retrieve messages from.
            max_retries (int, optional): The maximum number of retry attempts. Defaults to 3.

        Returns:
            Message | None: The latest message from the assistant if found, otherwise None.

        Raises:
            Exception: If unable to retrieve the assistant's response after all retry attempts.
        """
        retries = 0
        while retries < max_retries:
            try:
                messages = await self.client.beta.threads.messages.list(thread_id=thread_id)
                print(messages)
                if messages.data:
                    # Get the latest message from the assistant
                    assistant_message = next((msg for msg in messages.data if msg.role == "assistant"), None)
                    if assistant_message:
                        return assistant_message
                # If no assistant message found, wait and retry
                await asyncio.sleep(2)
                retries += 1
            except Exception as e:
                print(f"Error getting assistant response (attempt {retries + 1}): {e}")
                retries += 1
                if retries < max_retries:
                    await asyncio.sleep(2)

        # If all retries are exhausted, raise an error
        raise Exception(f"Failed to get assistant response after {max_retries} attempts")

    async def get_or_create_thread(self, thread_id: str | None = None) -> Thread | None:
        """
        Get an existing thread or create a new one.

        This method attempts to retrieve an existing thread using the provided thread_id.
        If no thread_id is provided, it creates a new thread.

        Args:
            thread_id (str | None): The ID of the thread to retrieve. If None, a new thread is created.

        Returns:
            Thread | None: The retrieved or newly created Thread object, or None if an error occurs.

        Raises:
            Exception: Any exception that occurs during thread retrieval or creation is caught
                       and logged, returning None in such cases.
        """
        try:
            if thread_id is None:
                # Create a new thread if no thread_id is provided
                return await self.client.beta.threads.create()
            # Try to retrieve the existing thread
            return await self.client.beta.threads.retrieve(thread_id=thread_id)
        except Exception as e:
            print(f"Error in get_or_create_thread: {e}")
            return None

    async def check_file_search_tool(self, assistant: Assistant) -> Assistant:
        """
        Check if the file_search tool is present in the assistant's tools.

        This method initializes a boolean flag to track whether the file_search
        tool is found among the assistant's tools. The flag is set to False
        initially and will be updated in the subsequent loop if the tool is found.

        Returns:
            bool: False initially, to be updated in the following code.
        """
        found = False
        for tool in assistant.tools:
            if tool.type == "file_search":
                found = True

        if not found:
            new_vector_id = self.client.beta.vector_stores.create(file_ids=[])

            if not assistant.tool_resources:
                tool_resources = {"file_search": {"vector_store_ids": [new_vector_id]}}
            else:
                tool_resources = assistant.tool_resources.to_dict().update(
                    {"file_search": {"vector_store_ids": [new_vector_id]}}
                )
            assistant = await self.client.beta.assistants.update(
                assistant.id,
                tools=assistant.tools + [{"type": "file_search"}],  # noqa # type: ignore
                tool_resources=tool_resources,  # type: ignore
            )
        return assistant

    async def upload_document_from_bytes(self, file_in_bytes: IO[bytes]) -> str:
        """
        Upload a document from bytes to the OpenAI API.

        This method takes a file-like object containing bytes and uploads it to the OpenAI API
        for use with assistants.

        Args:
            file_in_bytes (IO[bytes]): A file-like object containing the bytes of the document to upload.

        Returns:
            str: The ID of the uploaded file.

        Raises:
            Any exceptions raised by the OpenAI API during file upload will be propagated.
        """
        file = await self.client.files.create(file=file_in_bytes, purpose="assistants")
        return file.id
