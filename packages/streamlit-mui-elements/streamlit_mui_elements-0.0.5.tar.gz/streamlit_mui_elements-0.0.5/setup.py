import setuptools

# Read the content of your README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="streamlit-mui-elements",
    version="0.0.5",
    author="Tom Jose",
    author_email="tomj0311@gmail.com",
    description="A Streamlit component for Material-UI elements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/streamlit-mui-elements",  # Update with your repository URL
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",  # Set to Apache 2.0
        "Operating System :: OS Independent",
    ],
    license="Apache 2.0",  # Specify the license explicitly
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
    extras_require={
        "devel": [
            "wheel",
        ]
    }
)
