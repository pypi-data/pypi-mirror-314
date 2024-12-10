from setuptools import setup, find_packages

setup(
    name="levelpychat",                        # Name of your package on PyPI
    version="1.1.0",                     # Version of your package
    description="A sample Python module using Tkinter and Pygame",  # Short description
    long_description=open("README.md").read(),  # Read from README for detailed description
    long_description_content_type="text/markdown",  # Content type for README
    author="Oluwaseun Inioluwa Adeleye",                  # Your name
    author_email="SeunTechLTD@gmail.com",  # Your email
    url="https://hydiy123.github.io/Levelpychat/",  # Optional: Link to your project's homepage
    license="MIT",                       # License type (e.g., MIT, Apache 2.0)
    packages=find_packages(),            # Automatically find all packages
    requires=["pygame"],         # List of dependencies
    python_requires=">=3.6",             # Minimum Python version
    classifiers=[                        # Optional: Metadata for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",

    ],
    package_data={
        "levelpychat": ["sounds/*.wav"],  # Includes all .wav files in the sounds/ directory
    },
)
