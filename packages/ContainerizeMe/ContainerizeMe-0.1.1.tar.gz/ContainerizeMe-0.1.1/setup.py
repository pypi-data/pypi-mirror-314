from setuptools import setup, find_packages

setup(
    name="ContainerizeMe",
    version="0.1.1",
    description="A Python package to optimize Dockerfiles and container images.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="amit",
    author_email="amitpotdar31@gmail.com",
    url="https://github.com/cyberdevil8/ContainerizeMe",
    packages=find_packages(),
    install_requires=[
        "docker",  
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
