from setuptools import setup, find_packages

setup(
    name="neuroprompt",
    version="0.1.3",
    packages=find_packages(include=['neuroprompt', 'neuroprompt.*']),
    install_requires=[
        "openai>=1.0.0",
        "llmlingua>=0.1.0",
        "tiktoken>=0.5.0",
        "nltk==3.8.1"
    ],
    extras_require={
        'eval': [
            "torch>=2.0.0",
            "numpy>=1.24.0",
            "rouge-score>=0.1.2",
            "transformers>=4.0.0",
            "scikit-learn>=1.0.0"
        ]
    },
    python_requires=">=3.8",
)