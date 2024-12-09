from setuptools import setup, find_packages

setup(
    name="MMsuit",
    version="0.0.1",
    author="Your Name",
    author_email="your-email@example.com",
    description="A package for Michaelis-Menten enzyme kinetics analysis",
    url="https://github.com/yahiasuw/MMsuit",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "pandas",
        "dash",
        "Flask",
        "plotly",

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        "console_scripts": [
            "MMsuit=MMsuit:MMsuit",
        ],
    }
)


