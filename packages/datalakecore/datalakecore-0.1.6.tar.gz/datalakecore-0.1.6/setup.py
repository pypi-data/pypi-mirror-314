from setuptools import setup, find_packages

setup(
    name='datalakecore',  # Replace with your package’s name
    version='0.1.6',
    packages=find_packages(),
    install_requires=[],
    author='Data Platform Team',  
    author_email='data.platform@sankhya.com.br',
    description='Biblioteca Core',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',

)