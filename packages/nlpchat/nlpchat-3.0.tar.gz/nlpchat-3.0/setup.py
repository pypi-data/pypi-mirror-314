from setuptools import setup, find_packages

setup(
    name='nlpchat',
    version='3.0',
    description='A package to simplify chatbot creation using NLP.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='AKM Korishee Apurbo',
    author_email='bandinvisible8@gmail.com',
    url='https://github.com/IMApurbo/nlpchat',
    packages=find_packages(),
    install_requires=[
        'sentence-transformers',
        'scikit-learn',
        'numpy',
        'pickle-mixin',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
