"""
Setup script for CCC - Claude Code Coordinator
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

# Read requirements
requirements = [
    "mcp>=1.0.0",
    "click>=8.0",
    "pydantic>=2.0",
    "python-dotenv>=1.0",
    "asyncio",
    "gitpython>=3.1",
]

setup(
    name="casewise-coordination",
    version="0.1.0",
    author="natethegreatMD",
    author_email="natethegreatMD@users.noreply.github.com",
    description="Claude Code Coordinator - Orchestrate multiple Claude sessions for complex development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/natethegreatMD/casewise-claude-coordination-mcp",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ccc=casewise_coordination.cli:main",
            "ccc-server=casewise_coordination.server.ccc_server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "casewise_coordination": ["templates/*.json", "config/*.json"],
    },
    project_urls={
        "Bug Reports": "https://github.com/natethegreatMD/casewise-claude-coordination-mcp/issues",
        "Source": "https://github.com/natethegreatMD/casewise-claude-coordination-mcp",
    },
)