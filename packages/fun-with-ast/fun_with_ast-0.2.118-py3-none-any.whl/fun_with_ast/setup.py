from setuptools import find_packages, setup
setup(
    name='funwithast',
    packages=find_packages(),
    version='0.1.1',
    description='A package for manipulating AST trees (Python 3.10)',
    author='Shai Rubin',
    license='Apache',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.2.1'],
    test_suite='tests',
)