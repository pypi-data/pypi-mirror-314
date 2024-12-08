from setuptools import setup, find_packages

setup(
    name="lymt",
    version="0.1.1",
    description="Let Your Model Think",
    author="GreenScreen410",
    author_email="pauljjang410@gmail.com",
    maintainer="GreenScreen410",
    maintainer_email="pauljjang410@gmail.com",
    url="https://github.com/GreenScreen410/lymt",
    packages=find_packages(),
    package_data={"lymt": ["prompt/*"]},
    license="MIT",
    keywords=[
        "llm",
        "machine learning",
        "deep learning",
        "ai",
        "openai",
        "claude",
        "prompt",
        "chatgpt",
        "cot",
    ],
    install_requires=["openai>=1.56.0", "anthropic>=0.40.0", "ollama>=0.4.2"],
)
