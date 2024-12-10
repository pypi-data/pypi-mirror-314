from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="voice_gender_recognition",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A voice gender recognition package using machine learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/voice_gender_recognition",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pyaudio",
        "librosa",
        "numpy",
        "tensorflow",  # if you're using tensorflow
    ],
) 