from .LLMInitialization import Initialize as ini
from .LLMModels import LLM_MODELS, get_info
from typing import List, Dict, Tuple, Union, Optional, Any
from pydantic import BaseModel
from dataclasses import dataclass

import os
import imghdr
import base64
from pathlib import Path

def process_image(image_data: Union[str, os.PathLike, Tuple[Union[str, os.PathLike], str]]) -> Dict:
    """
    Processes an image provided as a file path, file-like object, or base64-encoded string.
    
    Args:
        image_data: Can be:
            - A file path (str or PathLike)
            - A base64-encoded string (str)
            - A tuple of (image_source, detail_level)
            
    Returns:
        Dict containing processed image data with format:
        {
            "type": "image_url",
            "image_url": {
                "url": "data:image/{format};base64,{content}",
                "detail": detail_level
            }
        }
    """
    image_path = image_data[0] if isinstance(image_data, tuple) else image_data
    detail = image_data[1] if isinstance(image_data, tuple) else "auto"
    
    # Handle file paths
    if isinstance(image_path, (str, os.PathLike)) and not _is_base64(image_path):
        image_path = Path(image_path)
        if not image_path.exists():
            raise ValueError(f"Image file does not exist: {image_path}")
            
        img_format = imghdr.what(image_path)
        if img_format not in ['png', 'jpeg', 'jpg']:
            raise ValueError("Image must be PNG, JPEG, or JPG format")
            
        with open(image_path, "rb") as img_file:
            image_content = base64.b64encode(img_file.read()).decode('utf-8')
    
    # Handle base64 strings
    elif isinstance(image_path, str):
        try:
            # Detect if string already includes data URI scheme
            if image_path.startswith('data:image/'):
                # Extract format and content from data URI
                header, content = image_path.split(',', 1)
                img_format = header.split('/')[1].split(';')[0]
                image_content = content
            else:
                # Verify and decode base64 string
                base64.b64decode(image_path)
                image_content = image_path
                img_format = 'png'  # Default format for raw base64 strings
                
        except Exception as e:
            raise ValueError(f"Invalid base64 string provided for image: {str(e)}")
    
    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/{img_format};base64,{image_content}",
            "detail": detail
        }
    }

def _is_base64(s: str) -> bool:
    """Helper function to check if a string is base64 encoded"""
    try:
        if isinstance(s, str):
            # Check if it's a data URI
            if s.startswith('data:image/'):
                return True
            # Check if it's a raw base64 string
            base64.b64decode(s)
            return True
    except:
        return False
    return False

@dataclass
class TokenUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cached_tokens: Optional[int] = None
    non_cached_tokens: Optional[int] = None
    reasoning_tokens: Optional[int] = None

@dataclass
class CostBreakdown:
    input_cost: float
    output_cost: float
    total_cost: float
    cached_cost: Optional[float] = None
    non_cached_cost: Optional[float] = None

class GPTResponse:
    def __init__(self, content: Any, token_usage: TokenUsage, cost_breakdown: CostBreakdown):
        self.content = content
        self.token_usage = token_usage
        self.cost_breakdown = cost_breakdown

    @property
    def total_tokens(self) -> int:
        return self.token_usage.total_tokens

    @property
    def total_cost(self) -> float:
        return self.cost_breakdown.total_cost

    def __str__(self) -> str:
        
        if isinstance(self.content, str):
            return f"GPTResponse(content={self.content[:50]}..., total_tokens={self.total_tokens}, total_cost=${self.total_cost:.6f})"

        else:
            return f"GPTResponse(content=OutputObject..., total_tokens={self.total_tokens}, total_cost=${self.total_cost:.6f})"

    def __repr__(self) -> str:
        return self.__str__()

    def detailed_summary(self) -> str:
        cached_tokens = str(self.token_usage.cached_tokens) if self.token_usage.cached_tokens is not None else "N/A"
        non_cached_tokens = str(self.token_usage.non_cached_tokens) if self.token_usage.non_cached_tokens is not None else "N/A"
        reasoning_tokens = str(self.token_usage.reasoning_tokens) if self.token_usage.reasoning_tokens is not None else "N/A"
        cached_cost = f"${self.cost_breakdown.cached_cost:.6f}" if self.cost_breakdown.cached_cost is not None else "N/A"
        non_cached_cost = f"${self.cost_breakdown.non_cached_cost:.6f}" if self.cost_breakdown.non_cached_cost is not None else "N/A"
        return f"""
GPT Response Summary:
---------------------

Token Usage:
  Prompt tokens:     {self.token_usage.prompt_tokens}
  Completion tokens: {self.token_usage.completion_tokens}
  Total tokens:      {self.token_usage.total_tokens}
  Cached tokens:     {cached_tokens}
  Non-cached tokens: {non_cached_tokens}
  Reasoning tokens:  {reasoning_tokens}
  
Cost Breakdown:
  Input cost:        ${self.cost_breakdown.input_cost:.6f}
  Output cost:       ${self.cost_breakdown.output_cost:.6f}
  Total cost:        ${self.cost_breakdown.total_cost:.6f}
  Cached cost:       {cached_cost}
  Non-cached cost:   {non_cached_cost}
"""

class Output:
    """
    Provides methods for generating output from various large language models (LLMs).
    
    The `Output` class provides static methods for generating output from different LLM models, including GPT, Claude, and Gemini. Each method takes a prompt as input and returns the generated output.
    
    The `GPT` method uses the OpenAI GPT model to generate output, with options to specify the model, temperature, and maximum tokens. The `Claude` method uses the Anthropic Claude model, with similar options. The `Gemini` method uses the Gemini model, which does not have any additional options.
    
    All methods raise a `ValueError` if the provided model name is invalid or the temperature is out of the valid range.
    """
        
    @staticmethod
    def GPT(
        user_prompt, 
        system_prompt: Optional[str] = None, 
        model: str = "gpt-4o-mini-2024-07-18", 
        temperature: float = 0.15, 
        max_tokens: int = 1024, 
        response_format: Optional[BaseModel] = None, 
        output_option: str = 'cont_prt_det', 
        images: Optional[List[Union[str, os.PathLike, Tuple[Union[str, os.PathLike], str]]]] = None
    ):
        """
            Generates output using the OpenAI GPT language model.

            Args:
                user_prompt (str): The input prompt to generate output from.
                system_prompt (str, optional): The system prompt to provide context for the generation.
                model (str, optional): The name of the GPT model to use. Defaults to "gpt-4o-mini-2024-07-18".
                temperature (float, optional): The temperature value to use for generating output. Must be between 0 and 1. Defaults to 0.15.
                max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 1024.
                response_format (BaseModel, optional): The response format to use for the generated output.
                output_option (str, optional): The output option to use for the generated output. Defaults to 'cont_prt_det'.
                images (List[Union[str, os.PathLike, Tuple[Union[str, os.PathLike], str]]], optional): The images to include for generating output.

            Returns:
                GPTResponse: An object containing the generated output, token usage, and cost breakdown.

            Raises:
                ValueError: If the provided model name is invalid, the temperature is out of the valid range, or the output option is invalid.
        """

    
        chatgpt = ini.get_chatgpt()
        
        if model not in LLM_MODELS['openai'].values():
            raise ValueError(f"Invalid model name: {model}. Please use one of the following: {', '.join(LLM_MODELS['openai'].values())}")
        
        if not 0 <= temperature <= 1:
            raise ValueError("Temperature must be between 0 and 1")
        
        valid_out_opts = ['cont', 'cont_prt_det', 'cont_prt_min', 'cont_cost', 'cont_cost_prt_det', 'cont_cost_prt_min']
        if output_option not in valid_out_opts:
            raise ValueError(f"Invalid out_opt. Please choose from: {', '.join(valid_out_opts)}")
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        if images:
            # Only allow images for GPT-4 models
            if not any(model.startswith(prefix) for prefix in ["gpt-4o", "gpt-4-"]):
                raise ValueError("Image input is only supported for GPT-4 models")
            
            content = []
            
            # Process each image
            for image_data in images:
                content.append(process_image(image_data))
            
            content.append({
            "type": "text",
            "text": user_prompt
            })    
            
            messages.append({
            "role": "user",
            "content": content
            })

        else:
            messages.append({"role": "user", "content": user_prompt})
        
        completion_args = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }
        
        if response_format:
            completion_args["response_format"] = response_format
            response = chatgpt.beta.chat.completions.parse(**completion_args)
        else:
            response = chatgpt.chat.completions.create(**completion_args)
        print(response)
        content = response.choices[0].message.content if not response_format else response.choices[0].message.parsed
        
        if hasattr(response.usage.completion_tokens_details,"audio_tokens"):
            cached_tokens = response.usage.prompt_tokens_details.cached_tokens
            reasoning_tokens = response.usage.completion_tokens_details.reasoning_tokens
        else:
            try:
                cached_tokens = response.usage.prompt_tokens_details.cached_tokens if hasattr(response.usage, 'prompt_tokens_details') else None
                reasoning_tokens = response.usage.completion_tokens_details.reasoning_tokens if hasattr(response.usage, 'prompt_tokens_details') else None
            except:
                cached_tokens = response.usage.prompt_tokens_details.get('cached_tokens', 0) if hasattr(response.usage, 'prompt_tokens_details') else None 
                reasoning_tokens = response.usage.completion_tokens_details.get("reasoning_tokens", 0) if hasattr(response.usage, 'completion_tokens_details') else None
            # cached_tokens = response.usage.prompt_tokens_details.cached_tokens if hasattr(response.usage, 'prompt_tokens_details') else None
            # reasoning_tokens = response.usage.completion_tokens_details.reasoning_tokens if hasattr(response.usage, 'completion_tokens_details') else None
        
        token_usage = TokenUsage(
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
            cached_tokens=cached_tokens,
            non_cached_tokens=response.usage.prompt_tokens - cached_tokens,
            reasoning_tokens=reasoning_tokens
        )

        model_info = get_info("openai").get("openai").get(model)
        input_cost_rate = model_info["cost_per_1k_tokens"]["input"]
        output_cost_rate = model_info["cost_per_1k_tokens"]["output"]

        cached_cost = (token_usage.cached_tokens / 1000) * (input_cost_rate / 2) if token_usage.cached_tokens is not None else None
        non_cached_cost = (token_usage.non_cached_tokens / 1000) * input_cost_rate if token_usage.non_cached_tokens is not None else None
        input_cost = cached_cost + non_cached_cost
        output_cost = (token_usage.completion_tokens / 1000) * output_cost_rate
        total_cost = input_cost + output_cost

        cost_breakdown = CostBreakdown(
            input_cost=input_cost,
            output_cost=output_cost,
            total_cost=total_cost,
            cached_cost=cached_cost,
            non_cached_cost=non_cached_cost
        )

        gpt_response = GPTResponse(content, token_usage, cost_breakdown)
        
        if output_option == 'cont':
            return content
        
        if output_option in ['cont_cost_prt_det', 'cont_prt_det']:
            print(gpt_response.detailed_summary())
            return gpt_response
        
        elif output_option in ['cont_cost_prt_min']:
            print(f"\nTotal tokens: {gpt_response.total_tokens}")
            print(f"Total cost:   ${gpt_response.total_cost:.6f}")
            
        if output_option == 'cont_prt_min':
            print(f"\nTotal tokens: {gpt_response.total_tokens}")
            print(f"Total cost:   ${gpt_response.total_cost:.6f}")
            return content

        return gpt_response
        

    @staticmethod
    def Claude(user_prompt, system_prompt: Optional[str] = None, model: str = "claude-3-5-sonnet-20240620", temperature: float = 0, max_tokens: int = 2048):
        """
            Generates a response from the Anthropic Claude language model based on the provided user prompt and optional system prompt.
            
            Args:
                user_prompt (str): The prompt to be sent to the language model.
                system_prompt (Optional[str]): An optional system prompt to be used by the language model.
                model (str): The name of the language model to use. Must be one of the values in LLM_MODELS['anthropic'].
                temperature (float): The temperature parameter for the language model, which controls the randomness of the generated output. Must be between 0 and 1.
                max_tokens (int): The maximum number of tokens to generate in the response.
            
            Returns:
                str: The generated response from the language model.
        """   
        
        claude = ini.get_claude()
        
        if model not in LLM_MODELS['anthropic'].values():
            raise ValueError(f"Invalid model name: {model}. Please use one of the following: {', '.join(LLM_MODELS['anthropic'].values())}")
        
        if not 0 <= temperature <= 1:
            raise ValueError("Temperature must be between 0 and 1")
        
        message = claude.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt
                        }
                    ],
                }
            ],
        )
        return message.content[0].text
    
    @staticmethod
    def Gemini(prompt):
        gemini = ini.get_gemini()
        
        return gemini.generate_content(prompt)