"""
NeuroPrompt - Intelligent Prompt Compression for LLMs
Copyright (c) 2024 Tejas Chopra. All rights reserved.

Core package providing basic prompt compression functionality.
For evaluation features, install with: pip install neuroprompt[eval]
"""

from .compressor import NeuroPromptCompress
import nltk
import ssl

__version__ = "0.1.2"
__author__ = "Tejas Chopra"
__email__ = "chopratejas@gmail.com"

# Core exports
__all__ = ["NeuroPromptCompress"]

# Check for eval support
try:
    from neuroprompt_eval import NeuroPromptCompressWithEval
    __all__.append("NeuroPromptCompressWithEval")
    HAS_EVAL = True
except ImportError:
    HAS_EVAL = False

def has_eval_support() -> bool:
    """Check if evaluation features are available."""
    return HAS_EVAL

def get_version() -> str:
    """Get the current version of NeuroPrompt."""
    return __version__

def _setup_nltk():
    """Setup NLTK data and handle SSL certificate issues if any."""
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    # Only download what's absolutely necessary for core functionality
    # For example, if you only need punkt for sentence tokenization:
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

# Run setup when the package is imported
_setup_nltk()