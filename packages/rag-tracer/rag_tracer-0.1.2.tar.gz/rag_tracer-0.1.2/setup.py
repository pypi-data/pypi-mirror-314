from setuptools import setup, find_packages

setup(
    name='rag_tracer',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'requests',
        'apache-skywalking'
    ],
    description='A Python SDK for sending RAG trace node data',
    author='XiaoTeng',
    author_email='sunxiaoteng925@163.com',
    url='https://livein-dev.coding.net/p/rag_workflow/d/RAG-workflow/git',
)
