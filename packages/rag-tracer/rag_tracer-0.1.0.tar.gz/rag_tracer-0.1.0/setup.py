from setuptools import setup, find_packages

setup(
    name='rag_tracer',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    description='A Python SDK for sending RAG trace node data',
    author='XiaoTeng',
    author_email='sunxiaoteng001@ke.com',
    url='https://livein-dev.coding.net/p/rag_workflow/d/RAG-workflow/git',
)
