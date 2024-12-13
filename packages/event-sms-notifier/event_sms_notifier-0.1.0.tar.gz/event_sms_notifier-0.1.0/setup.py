from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="event-sms-notifier",
    version="0.1.0",
    author=" Namugga Sharifah",
    author_email="sharifahnamugga3@gmail.com",  # Please update with your email
    description="A library for event notifications with SMS capabilities using Africa's Talking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "africastalking>=1.2.5",
        "requests>=2.28.0",
    ],
    keywords="event notification sms africa's talking period tracking reminder",
)
