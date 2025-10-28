"""
Setup configuration for quant_trader package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quant_trader",
    version="0.1.0",
    author="Rayan & Guillaume",
    author_email="",
    description="AI-Powered Options Trading System using Reinforcement Learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ravanso/Trading",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scipy>=1.10.0",
        "matplotlib>=3.7.0",
        "scikit-learn>=1.3.0",
    ],
    extras_require={
        "rl": [
            "stable-baselines3>=2.0.0",
            "gymnasium>=0.29.0",
            "torch>=2.0.0",
        ],
        "options": [
            "py_vollib>=1.0.1",
            "QuantLib>=1.30",
        ],
        "brokers": [
            "ib_insync>=0.9.86",
            "alpaca-py>=0.14.0",
        ],
        "viz": [
            "plotly>=5.14.0",
            "streamlit>=1.25.0",
            "seaborn>=0.12.0",
        ],
        "dev": [
            "pytest>=7.4.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
            "jupyter>=1.0.0",
        ],
    },
)

