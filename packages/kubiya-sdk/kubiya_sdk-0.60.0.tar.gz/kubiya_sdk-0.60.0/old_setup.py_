from setuptools import setup, find_packages

setup(
    name="kubiya_sdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "click",
        "jmespath",
        "PyYAML",
    ],
    entry_points={
        "console_scripts": [
            "kubiya=kubiya_sdk.main:cli",
        ],
    },
    author="Shaked Askayo",
    author_email="shaked@kubiya.ai",
    description="Kubiya SDK for workflow and tool management",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kubiyabot/sdk-py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
