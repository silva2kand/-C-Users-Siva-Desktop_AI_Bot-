from setuptools import setup, find_packages

setup(
    name="desktop-floating-bots",
    version="1.0.0",
    description="Desktop floating AI bots application",
    author="Silva2kand",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "openai>=1.3.0",
        "python-dotenv>=1.0.0",
        "pystray>=0.19.0",
        "Pillow>=10.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "flake8>=6.0.0",
            "black>=23.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "floating-bots=src.main:main",
        ]
    },
)