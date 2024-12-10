from setuptools import setup, find_packages

setup(
    name='validated_chat',
    version='0.0.2',
    description='A package to generate and validate chat responses with retry logic.',
    author='Eugene Evstafev',
    author_email='chigwel@gmail.com',
    packages=find_packages(),
    install_requires=[
        'ollama==0.4.4',
        'pydantic==2.10.3',
    ],
    python_requires='>=3.7',
)
