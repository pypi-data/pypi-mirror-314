from setuptools import setup, find_packages

setup(
    name='IndovinaLaParola',
    version='1.1.2',
    description='Un gioco semplice di indovina la parola',
    author='Gasa industries',
    packages=find_packages(),
    python_requires='>=3.6',  
    install_requires=[
        'setuptools',  
    ],
    entry_points={
        'console_scripts': [
            'indovina_la_parola = IndovinaLaParola:giocoindovina_la_parola',
        ],
    },
)
