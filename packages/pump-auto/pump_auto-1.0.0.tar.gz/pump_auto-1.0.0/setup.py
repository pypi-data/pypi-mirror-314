from setuptools import setup, find_packages

setup(
    name="pump_auto",  # The name of your package on PyPI  
    version="1.0.0",   # Version of your package
    author="Your Name",
    author_email="your_email@example.com",
    description="A brief description of auto_pump package",
    #long_description=open("README.md").read(),  # Optional: Read from README.md
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/auto_pump",  # Optional: Link to your repo
    packages=find_packages(),  # Automatically includes the inner auto_pump folder
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify the minimum Python version
    install_requires=[],  # List dependencies if required
)
