from .LLMInitialization import Initialize
from .LLMOutput import Output
from .LLMModels import get_info
import os

__all__ = ['Initialize', 'Output', 'get_info']

# You can add a version number if desired
__version__ = '0.1.5.3'

# In mypackage/__init__.py

def get_readme():
    """Return the content of the README.md file."""
    possible_locations = [
        os.path.join(os.path.dirname(__file__), 'README.md'),
        os.path.join(os.path.dirname(__file__), '..', 'README.md'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'README.md'),
    ]
    
    for location in possible_locations:
        if os.path.exists(location):
            with open(location, 'r', encoding='utf-8') as file:
                return file.read()
    
    return "README.md not found"

