from setuptools import setup, find_packages

setup(
    name='2024-ass2-ErbaFiore-DevOps',
    version='1.0',
    setup_requires=["wheel"],
    description='Assignment2 DevOps',
    author='GruppoErbaFiore',
    author_email='l.erba6@campus.unimib.it',
    packages=find_packages(),
    install_requires=[
        'pymongo',
        'pytest', 
        'prospector',
        'bandit',
        'mkdocs',
        'twine',
    ],
)
