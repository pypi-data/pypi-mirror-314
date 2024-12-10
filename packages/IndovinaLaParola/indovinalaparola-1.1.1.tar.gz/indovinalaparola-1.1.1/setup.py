from setuptools import setup, find_packages

setup(
    name='IndovinaLaParola',
    version='1.1.1',
    description='Un gioco semplice di indovina la parola',
    author='Gasa industries',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'indovina_la_parola = IndovinaLaParola:giocoindovina_la_parola',
        ],
    },
)
