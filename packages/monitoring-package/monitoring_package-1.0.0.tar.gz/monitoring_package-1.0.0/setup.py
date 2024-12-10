from setuptools import setup, find_packages

setup(
    name="monitoring_package",
    version="1.0.0",
    description="A monitoring package with agent and server components",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/monitoring_package",  # Your project's URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "psutil",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "monitor-agent=monitoring_agent.agent:main",
            "monitor-server=monitoring_server.server:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
