from setuptools import setup, find_packages

setup(
    name='destinelab_test',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'lxml',
        'PyJWT',
    ],
)
