from setuptools import setup, find_packages

setup(
    name="openai_chat_api_wrapper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai==1.57.0",
    ],
    include_package_data=True,
    license = "Apache-2.0",
    author="Doriav Isakov",
    classifiers=[
        "Typing :: Typed",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License"
    ],
    python_requires=">=3.8",
)
