# Assistant Processor Guides

## **Warning**
The file `processor_2.py` is a temporary file used in the current branch and will be renamed to `processor.py`. Please be aware that any references to `processor_2.py` should be updated to `processor.py` once the renaming is complete.

## Installation
### Poetry Installation from Git

To install this package directly from Git using Poetry, add the following to your `pyproject.toml`:

```toml
[tool.poetry.dependencies]
surfaice-assistance = { git = "https://github.com/gdml/surfaice-assistant.git", branch = "feature/s42t207_add-ai-models-choice" }
```
or locally:

```toml
[tool.poetry.dependencies]
surfaice-assistant = { path = "path/to/surfaice-assistant"}
```

## Usage
### Basic Setup
```python
from surfaice_assistance.processor2 import AssistantProcessor   

class YourClass:
    ...

    @property
    def assistant_processor(self) -> AssistantProcessor:
        return AssistantProcessor(api_key=self.api_key, provider=self.provider.value)
    ...

    def create_assistant(self) -> AssistantCreateResponse:
        return self.assistant_processor.create_assistant(
            name="Your Assistant Name",
            description="Your Assistant Description",
            instructions="Your Assistant Instructions",
            model="gpt-4o",
            tools=list[dict],
        )   

    def get_assistant(self) -> AssistantGetResponse:
        return self.assistant_processor.get_assistant(
            assistant_id="your_assistant_id",
        )
    
    def update_assistant(self) -> AssistantUpdateResponse:
        return self.assistant_processor.update_assistant(
            assistant_id="your_assistant_id",
            name="Your Assistant Name",
            description="Your Assistant Description",
            instructions="Your Assistant Instructions",
            model="gpt-4o",
            tools=list[dict],
        )
    
    # ... other methods

```

## Adding a New Implementation

When adding a new assistant implementation to the system, follow these steps:

1. Create a new implementation class that inherits from `AssistantInterface`:
   - Create a new file in the `implementations/` directory
   - Implement all abstract methods from `AssistantInterface`
   - Follow the response models pattern using Pydantic models
   - Add import to `__all__` in `implementations/__init__.py`

2. Register the implementation in `processor_2.py`:
   ```python
   from implementations.your_provider import YourProviderImpl

   processor_implementations: dict[str, Union[Type[OpenAIAssistantImpl], Type[YourProviderImpl], Any]] = {
       OPENAI: OpenAIAssistantImpl,
       "your_provider": YourProviderImpl,  # Add your implementation here
   }
   ```

3. Define a constant for your provider name at the top of `processor_2.py`:
   ```python
   YOUR_PROVIDER = "your_provider"
   ```

4. Ensure your implementation:
   - Uses the standard response models from `abstract_provider.assistant`
   - Handles retries and error cases consistently
   - Includes proper logging
   - Has appropriate type hints
   - Follows the existing pattern for async methods

## Implementation Requirements

Your implementation class must:

1. Inherit from `AssistantInterface`
2. Implement all abstract methods defined in the interface
3. Use the standard response models:
   - AssistantCreateResponse
   - AssistantGetResponse
   - ThreadGetResponse
   - MessageCreateResponse
   - etc.

## Example Implementation Structure 
```python
from abstract_provider import AssistantInterface
from abstract_provider.assistant import (
    AssistantCreateResponse,
    AssistantGetResponse,
# ... other response models
)
class YourProviderImpl(AssistantInterface):
    def init(self, api_key: str) -> None:
    # Initialize your provider's client
        pass
    async def create_assistant(
        self,
        name: str,
        description: str,
        instructions: str,
        model: str,
        tools: list[dict],
        max_retries: int = 5,
        ) -> AssistantCreateResponse:
        pass
```
## Reference Implementation

See the OpenAI implementation (`implementations/openai_provider.py`) for a complete example of how to structure your implementation.

## Guidelines for Response Models   

- Use Pydantic models for response models
- Follow the response models pattern using Pydantic models
- Add the response models to the `implementations.your_provider` module
- Add the type of your models to unions in `abstract_provider.assistant` models
- Example:
    ```python
    from pydantic import BaseModel
    class YourResponseModel(BaseModel):
        # Define your model fields here
        success: bool   
        your_field: Optional[YourType] = None
        error: Optional[str] = None
    ```


