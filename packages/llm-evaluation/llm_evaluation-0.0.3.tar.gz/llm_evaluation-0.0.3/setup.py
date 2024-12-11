from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'LLM Evaluation Package'
LONG_DESCRIPTION = 'A package that allows to evaluate LLM work.'

# Setting up
setup(
    name="llm-evaluation",
    version=VERSION,
    author="Maks Lupey",
    author_email="<maxrty234@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['langfuse', 'openai', 'langchain_openai', 'langchain', 'rapidfuzz', 'scikit-learn',
                      'llama-index-llms-openai-like'],
    keywords=['python', 'llm', 'evaluation', 'llm evaluation'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)