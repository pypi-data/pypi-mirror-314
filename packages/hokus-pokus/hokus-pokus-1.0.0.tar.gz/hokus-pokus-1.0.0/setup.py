from setuptools import setup, find_packages

setup(
    name='hokus-pokus',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'transformers>=4.0.0',  # Model dependencies
        'torch>=1.8.0',         # PyTorch for model inference
        'click',                 # For the command-line interface
    ],
    entry_points={
        'console_scripts': [
            'hokus-pokus=hokus_pokus.hokus_pokus:main',  # Entry point to run your CLI
        ],
    },
    description='Your magical CLI for generating text spells and performing tasks.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/hokus-pokus',  # Your project repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
