from setuptools import setup, find_packages

setup(
    name="qq",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "rich>=13.7.0",
        "anthropic>=0.18.1"
    ],
    entry_points={
        'console_scripts': [
            'qq=quickquestion.qq:main',
        ],
    },
    author="Cristian Vyhmeister",
    author_email="cv@southbrucke.com",
    description="A CLI tool for getting quick command-line suggestions using any LLM potentially available",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://southbrucke.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Topic :: Utilities",
        "Topic :: System :: Shells",
        "Topic :: Terminals",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: End Users/Desktop"
    ],
    python_requires=">=3.6",
    license="Proprietary",
    license_files=("LICENSE",),
)