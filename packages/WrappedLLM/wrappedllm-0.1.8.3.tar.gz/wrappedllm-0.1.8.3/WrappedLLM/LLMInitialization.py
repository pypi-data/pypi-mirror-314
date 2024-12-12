from openai import OpenAI
import anthropic
import google.generativeai as genai

class Initialize:
    """
    This class provides methods for initializing and managing instances of various large language models (LLMs), including ChatGPT, Claude, and Gemini.
    
    The `Initialize` class has the following class methods:
    
    - `init_chatgpt(cls, api_key)`: Initializes the ChatGPT LLM instance using the provided API key. It tests the API key by making a simple API call.
    - `init_claude(cls, api_key)`: Initializes the Claude LLM instance using the provided API key. It tests the API key by making a simple API call.
    - `init_gemini(cls, api_key)`: Initializes the Gemini LLM instance using the provided API key. It configures the safety settings and tests the API key by making a simple API call.
    - `init_all(cls, chatgpt_api_key, claude_api_key, gemini_api_key, chatgpt_model="gpt-4o-mini-2024-07-18bo", claude_model="claude-2", gemini_model="gemini-1.5-flash-latest")`: Initializes all three LLM instances using the provided API keys and model names.
    - `get_chatgpt(cls)`, `get_claude(cls)`, and `get_gemini(cls)`: Provide access to the initialized instances of the respective LLMs.
    """
 
    chatgpt = None
    claude = None
    gemini = None

    @classmethod
    def init_chatgpt(cls, api_key):
        if not api_key:
            raise ValueError("ChatGPT API key is required")
        try:
            cls.chatgpt = OpenAI(api_key=api_key)
            # Test the API key by making a simple API call
            cls.chatgpt.chat.completions.create(model="gpt-4o-mini-2024-07-18", messages=[{"role": "user", "content": "Test"}])
        except Exception as e:
            raise ValueError(f"Invalid ChatGPT API key: {str(e)}")

    @classmethod
    def init_claude(cls, api_key):
        if not api_key:
            raise ValueError("Claude API key is required")
        try:
            cls.claude = anthropic.Anthropic(api_key=api_key)
            # Test the API key by making a simple API call
            cls.claude.completions.create(model="claude-2", prompt="Human: Test\n\nAssistant:", max_tokens_to_sample=1)
        except Exception as e:
            raise ValueError(f"Invalid Claude API key: {str(e)}")

    @classmethod
    def init_gemini(cls, api_key):
        if not api_key:
            raise ValueError("Gemini API key is required")
        try:
            
            safety_settings = [
                                {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
                                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                            ]
            
            genai.configure(api_key=api_key)
            cls.gemini = genai.GenerativeModel("gemini-1.5-flash-latest",safety_settings)
            
            # Test the API key by making a simple API call
            cls.gemini.generate_content("Test")
        
        except Exception as e:
            raise ValueError(f"Invalid Gemini API key: {str(e)}")

    @classmethod
    def init_all(cls, chatgpt_api_key, claude_api_key, gemini_api_key, chatgpt_model="gpt-4o-mini-2024-07-18", claude_model="claude-2", gemini_model="gemini-1.5-flash-latest"):
        cls.init_chatgpt(chatgpt_api_key, chatgpt_model)
        cls.init_claude(claude_api_key, claude_model)
        cls.init_gemini(gemini_api_key, gemini_model)

    @classmethod
    def get_chatgpt(cls):
        """
        Returns the initialized ChatGPT instance.
        
        Raises:
            RuntimeError: If the ChatGPT instance has not been initialized.
        
        Returns:
            OpenAI: The initialized ChatGPT instance.
        """
                
        if cls.chatgpt is None:
            raise RuntimeError("ChatGPT is not initialized. Please initialize it before calling Output.GPT()!")
        return cls.chatgpt

    @classmethod
    def get_claude(cls):
        """
        Returns the initialized Claude instance.
        
        Raises:
            RuntimeError: If the Claude instance has not been initialized.
        
        Returns:
            Anthropic: The initialized Claude instance.
        """
                
        if cls.claude is None:
            raise RuntimeError("Claude is not initialized. Please initialize it before calling Output.Claude()!")
        return cls.claude

    @classmethod
    def get_gemini(cls):
        """
        Returns the initialized Gemini client instance.
        
        Raises:
            RuntimeError: If the Gemini client instance has not been initialized.
        
        Returns:
            GenerativeModel: The initialized Gemini client instance.
        """
                
        if cls.gemini is None:
            raise RuntimeError("Gemini client is not initialized. Please initialize it before calling Output.Gemini()!")
        return cls.gemini

    @classmethod
    def is_chatgpt_initialized(cls) -> bool:
        """
        Returns whether the ChatGPT instance has been initialized.
        
        Returns:
            bool: True if the ChatGPT instance has been initialized, False otherwise.
        """
                
        return cls.chatgpt is not None

    @classmethod
    def is_claude_initialized(cls) -> bool:
        """
        Returns whether the Claude instance has been initialized.
        
        Returns:
            bool: True if the Claude instance has been initialized, False otherwise.
        """
                
        return cls.claude is not None

    @classmethod
    def is_gemini_initialized(cls) -> bool:
        """
        Returns whether the Gemini client instance has been initialized.
        
        Returns:
            bool: True if the Gemini client instance has been initialized, False otherwise.
        """
                
        return cls.gemini is not None
    
    @classmethod
    def are_all_llms_initialized(cls):
        return cls.is_chatgpt_initialized() and cls.is_claude_initialized() and cls.is_gemini_initialized()