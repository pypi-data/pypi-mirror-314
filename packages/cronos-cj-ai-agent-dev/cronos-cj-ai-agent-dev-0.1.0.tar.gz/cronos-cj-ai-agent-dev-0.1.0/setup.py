from setuptools import setup, find_packages

setup(
    name='cronos-cj-ai-agent-dev',
    version='0.1.0',
    author='CJ',
    author_email='jing.chen@cronoslabs.org',
    description='Cronos AI Agent Development',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cryptocj/cronos-ai-agent-dev',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        "cachetools==5.5.0",
        "cohere==5.13.3",
        "crypto_com_ai_agent_client==1.0.5",
        "fastapi==0.115.6",
        "openai==1.57.1",
        "pyairtable==3.0.0",
        "pydantic==2.10.3",
        "python-dotenv==1.0.1",
        "python-telegram-bot==21.9",
        "requests==2.32.3",
        "setuptools==65.5.0",
        "tabulate==0.9.0",
        "tenacity==9.0.0",
        "uvicorn==0.32.1",
        "web3==7.6.0",
        "web3_input_decoder==0.1.13"
    ],
)