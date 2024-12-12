# WrappedLLM

WrappedLLM is a Python package that provides a unified interface for interacting with multiple Large Language Models (LLMs) including ChatGPT, Claude, and Gemini.

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

## GPT Function with Pydantic Class Outputs

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

## Cost Estimation for OpenAI Models

WrappedLLM now offers an advanced cost estimation feature for OpenAI models, providing detailed insights into token usage and associated costs.

### Usage

```markdown
from WrappedLLM import Output

response = Output.GPT(
    "Explain the concept of recursion in programming.",
    model="gpt-4o-mini-2024-07-18",
    output_option="cont_cost_prt_det"
)

# Access the response content
print(response.content)

# View detailed cost and token usage summary
print(response.detailed_summary())

# Access specific metrics
print(f"Total tokens: {response.total_tokens}")
print(f"Estimated cost: ${response.total_cost:.6f}")
```

### Output Options

| Option                | Description                                         |
| --------------------- | --------------------------------------------------- |
| `cont`              | Returns only the content                            |
| `cont_prt_det`      | Returns content and prints detailed token/cost info |
| `cont_prt_min`      | Returns content and prints minimal token/cost info  |
| `cont_cost`         | Returns GPTResponse object with all details         |
| `cont_cost_prt_det` | Returns GPTResponse object and prints detailed info |
| `cont_cost_prt_min` | Returns GPTResponse object and prints minimal info  |

### GPTResponse Object

The `GPTResponse` object provides comprehensive information:

* `content`: The generated text
* `token_usage`: Detailed token usage statistics
* `cost_breakdown`: Estimated costs for input, output, and total

#### Detailed Summary Example

```yaml
GPT Response Summary:
---------------------

Token Usage:
  Prompt tokens:     50
  Completion tokens: 150
  Total tokens:      200
  Cached tokens:     10
  Non-cached tokens: 40
  Reasoning tokens:  100
  
Cost Breakdown:
  Input cost:        $0.000250
  Output cost:       $0.001500
  Total cost:        $0.001750
  Cached cost:       $0.000025
  Non-cached cost:   $0.000225
```

### Important Notes

* This feature is currently available only for OpenAI models.
* Costs are estimates based on the latest available pricing and may not reflect exact charges.
* Actual billing is determined by OpenAI and may vary.

By leveraging this feature, you can gain valuable insights into your API usage and optimize your implementation for both performance and cost-effectiveness.

## Image Upload with GPT-4 Vision

WrappedLLM provides powerful image analysis capabilities through OpenAI's GPT-4 Vision models, supporting both single and multiple image analysis with customizable detail levels.

### Detail Levels and Token Costs

The system supports three detail levels that affect both analysis quality and token consumption:

1. `low`

   - Fixed 85 tokens per image regardless of size
   - Image processed at 512px x 512px resolution
   - Faster response times
   - Ideal for basic object recognition and simple scenes
   - Cost-effective for bulk processing
2. `high`

   - Initial low-res pass (85 tokens)
   - Additional 170 tokens per 512px x 512px tile
   - Maximum input size: 2048 x 2048
   - Shortest side scaled to 768px
   - Ideal for text recognition and fine details
3. `auto` (default)

   - Automatically selects between low/high based on image size
   - Optimizes token usage and detail level
   - Recommended for general use

#### Token Cost Examples

1. 1024 x 1024 image with `high` detail:

   - No initial resize (under 2048 limit)
   - Scaled to 768 x 768
   - Requires 4 tiles of 512px
   - Total cost: (170 * 4) + 85 = 765 tokens
2. 2048 x 4096 image with `high` detail:

   - Scaled to 1024 x 2048
   - Further scaled to 768 x 1536
   - Requires 6 tiles of 512px
   - Total cost: (170 * 6) + 85 = 1105 tokens
3. Any size image with `low` detail:

   - Fixed cost of 85 tokens
   - Scaled to 512px x 512px

For detailed specifications, visit [OpenAI&#39;s Vision Guide](https://platform.openai.com/docs/guides/vision).

### Implementation Examples

#### Basic Single Image Analysis

```python
import os
from WrappedLLM import Output
from WrappedLLM.LLMModels import LLM_MODELS as models

openai_models = models['openai']
gpt4 = openai_models['gpt4']

image_path = os.path.join("path", "to", "image.jpg")
response = Output.GPT(
    "What's in this image?",
    images=[image_path],
    model=gpt4
)
print(response.content)
```

#### Cost-Optimized Multiple Image Analysis

```python
from WrappedLLM import Output
from pathlib import Path
from WrappedLLM.LLMModels import LLM_MODELS as models

# Define image paths and detail levels
images = [
     (Path("path/to/detailed_document.jpg"), "high"),    # Full detail for text
     (Path("path/to/simple_scene.jpg"), "low"),          # Basic detail sufficient
     Path("path/to/unknown_content.jpg"),                # Auto detail for uncertain content
]

openai_models = models['openai']
gpt4_omni = openai_models['gpt4_omni']

response = Output.GPT(
     "Analyze these images with attention to text in the first one",
     images=images,
     model=gpt4_omni
)

print(response.content)
```

### Advanced Base64 Implementation

```python
import base64
from pathlib import Path
from WrappedLLM.LLMModels import LLM_MODELS as models

# Single image with high detail
with open(Path("path/to/image.jpg"), "rb") as img_file:
    base64_image = base64.b64encode(img_file.read()).decode('utf-8')

# Multiple base64 images with different detail levels
images = [
    (base64_image, "high"),
    (another_base64_image, "low")
]

openai_models = models['openai']
gpt4_omni_mini = openai_models['gpt4_omni_mini']

response = Output.GPT(
    "Provide a detailed analysis of these images",
    images=images,
    model=gpt4_omni_mini
)

print(response.content)
```

### Supported Models for Image Upload

* GPT-4 Turbo (gpt-4-turbo-2024-04-09)
* GPT-4 Omni (gpt-4o-2024-08-06)
* GPT-4 Omni Mini(gpt-4o-mini-2024-07-18)

### Image Format Requirements

* Supported formats: PNG, JPG/JPEG
* Maximum file size: 20MB per image
* Recommended resolution: 512x512px to 2048x2048px
* Color space: RGB

### Input Format

* Path-like object pointing to an image file
* Base64 encoded image string

Note: Image analysis is only available with OpenAI's vision-capable models. When using image upload, ensure you're using one of the supported models listed above.

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
