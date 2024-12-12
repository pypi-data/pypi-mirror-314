# LLM-Wrapper

LLM-Wrapper is a Python package that provides a unified interface for interacting with multiple Large Language Models (LLMs) including ChatGPT, Claude, and Gemini.

## Features

- Easy initialization of LLM clients
- Unified interface for generating outputs from different LLMs
- Support for multiple models within each LLM platform
- API key validation during initialization

## Installation

```bash
pip install WrappedLLM
```

## Usage

### Initializing LLMs

You can initialize LLMs individually or all at once:

```python
from WrappedLLM import Initialize

# Initialize ChatGPT
Initialize.init_chatgpt("your_openai_api_key")

# Initialize Claude
Initialize.init_claude("your_anthropic_api_key")

# Initialize Gemini
Initialize.init_gemini("your_gemini_api_key")

# Initialize all LLMs at once
Initialize.init_all(
    chatgpt_api_key="your_openai_api_key",
    claude_api_key="your_anthropic_api_key",
    gemini_api_key="your_gemini_api_key"
)
```

Note: During initialization, a few tokens are used to verify that the provided API key is correct.

### Checking LLM Initialization Status

You can now check whether specific LLMs or all LLMs have been initialized:

```markdown
from WrappedLLM import Initialize

# Check if ChatGPT is initialized
if Initialize.is_chatgpt_initialized():
    print("ChatGPT is ready to use")

# Check if Claude is initialized
if Initialize.is_claude_initialized():
    print("Claude is ready to use")

# Check if Gemini is initialized
if Initialize.is_gemini_initialized():
    print("Gemini is ready to use")

# Check if all LLMs are initialized
if Initialize.are_all_llms_initialized():
    print("All LLMs are ready to use")
else:
    print("Not all LLMs are initialized")
```

These methods return `True` if the respective LLM is initialized, and `False` otherwise. This allows you to easily manage the state of your LLM instances and handle cases where an LLM might not be initialized before use.

### Generating Output

```python
from WrappedLLM import Output

# Generate output using ChatGPT
gpt_response = Output.GPT("Tell me a joke about programming.")

# Generate output using Claude
claude_response = Output.Claude("Explain quantum computing in simple terms.")

# Generate output using Gemini
gemini_response = Output.Gemini("What are the benefits of renewable energy?")
```

### Customizing Model Parameters

You can customize model parameters when generating output:

```python
# Using a specific GPT model with custom temperature and max tokens
gpt_response = Output.GPT(
    "Summarize the history of artificial intelligence.",
    model="gpt-4o-mini-2024-07-18",
    temperature=0.7,
    max_tokens=2048
)

# Using a specific Claude model with custom temperature and max tokens
claude_response = Output.Claude(
    "Describe the process of photosynthesis.",
    model="claude-3-5-sonnet-20240620",
    temperature=0.5,
    max_tokens=1000
)
```

### New Feature: GPT Function with Pydantic Class Outputs

You can now use the GPT function to return Pydantic class outputs. This provides a structured way to handle responses from the LLM.

Example:

```python
from WrappedLLM import Initialize, Output
from pydantic import BaseModel

# Initialize the LLM
Initialize.init_chatgpt('your_api_key_here')

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

# Use the Output class to interact with the LLM
response = Output.GPT(
    "Alice and Bob are going to a science fair on Friday.",
    system_prompt="Extract the event information.",
    response_format=CalendarEvent
)
print(response)
```

In this example, we define a `CalendarEvent` Pydantic class and use it as the `response_format` in the GPT function call. This allows the LLM to structure its response according to the defined class.

## Available Models

You can get detailed information about available LLM models using the `get_info()` function:

```markdown
from WrappedLLM.LLMModels import get_llm_models_info

# Get info for all LLM providers
all_llm_info = get_info()

# Get info for a specific provider (e.g., OpenAI)
openai_llm_info = gets_info('openai')
```

This function returns a dictionary containing model information, including descriptions and image upload support(Not Implemented). You can optionally specify a provider ('openai', 'anthropic', or 'google') to get information for only that provider's models.

To get just the list of available models, you can use the `LLM_MODELS` dictionary:

```python
from WrappedLLM.LLMModels import LLM_MODELS as models

# OpenAI models
openai_models = models['openai']
gpt3_5 = openai_models['gpt3_5']
gpt4 = openai_models['gpt4']
gpt4_omni = openai_models['gpt4_omni']
gpt4_omni_mini = openai_models['gpt4_omni_mini']

# Anthropic models
anthropic_models = models['anthropic']
claude3_5_sonnet = anthropic_models['claude3_5_sonnet']
claude3_opus = anthropic_models['claude3_opus']
claude3_sonnet = anthropic_models['claude3_sonnet']
claude3_haiku = anthropic_models['claude3_haiku']

# Google models
google_models = models['google']
gemini1_5_flash = google_models['gemini1_5_flash']
```

You can use these model names when generating output. Here's an example using the GPT function:

```python
from WrappedLLM import Output

# Generate output using ChatGPT
gpt_response = Output.GPT("Tell me a joke about programming.", model=gpt3_5)

print(gpt_response)
```

This example demonstrates how to use the `gpt3_5` model name when calling the GPT function. The `model` parameter specifies which GPT model should be used for generating the response.

Note: The `get_llm_info()` function provides additional information about each model, including descriptions and image upload support. However, image upload functionality is not currently implemented in the WrappedLLM.

## Error Handling

The package includes error handling for invalid API keys, unsupported models, and incorrect parameter values. Make sure to handle these exceptions in your code.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

```vhdl

This README provides an overview of the LLM-Wrapper package, including installation  instructions, usage examples for initializing LLMs and generating output, and information about customizing model parameters. It also mentions the API key validation during initialization and how to access the list of available models.
```
