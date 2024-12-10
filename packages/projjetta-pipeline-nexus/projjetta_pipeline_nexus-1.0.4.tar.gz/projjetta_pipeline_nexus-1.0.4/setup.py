import setuptools

from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="projjetta-pipeline-nexus", # Replace with your own username
    version="1.0.4",
    author="Projjetta - Carlos Valdir Bortolotti",
    author_email="carlos@projjetta.com",
    description="Pipelines para integração de dados",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bortolottic/nexus-integration.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12.3',
    install_requires=[
        'asttokens==2.4.1',
        'certifi==2024.8.30',
        'charset-normalizer==3.3.2',
        'colorama==0.4.6',
        'comm==0.2.2',
        'Cython==3.0.11',
        'debugpy==1.8.6',
        'decorator==5.1.1',
        'executing==2.1.0',
        'greenlet==3.1.1',
        'idna==3.10',
        'ipykernel==6.29.5',
        'ipython==8.28.0',
        'jedi==0.19.1',
        'jupyter_client==8.6.3',
        'jupyter_core==5.7.2',
        'matplotlib-inline==0.1.7',
        'nest-asyncio==1.6.0',
        'packaging==24.1',
        'parso==0.8.4',
        'platformdirs==4.3.6',
        'prompt_toolkit==3.0.48',
        'psutil==6.0.0',
        'psycopg2==2.9.9',
        'pure_eval==0.2.3',
        'Pygments==2.18.0',
        'python-dateutil==2.9.0.post0',
        'python-env==1.0.0',
        'pyzmq==26.2.0',
        'requests==2.32.3',
        'setuptools==75.1.0',
        'setuptools-cythonize==1.0.7',
        'six==1.16.0',
        'SQLAlchemy==2.0.35',
        'stack-data==0.6.3',
        'tornado==6.4.1',
        'traitlets==5.14.3',
        'typing_extensions==4.12.2',
        'urllib3==2.2.3',
        'wcwidth==0.2.13',
        'wheel==0.44.0'],  # Adicionando as dependências aqui
)
