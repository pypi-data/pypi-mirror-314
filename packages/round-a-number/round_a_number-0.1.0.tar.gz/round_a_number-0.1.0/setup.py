from setuptools import setup, find_packages

setup(
    name='round_a_number',  # Name of the package
    version='0.1.0',
    packages=find_packages(include=['round_a_number']),
    install_requires=[
        # List any required dependencies
    ],
    author='Vivek',  
    author_email='x23324902@student.ncirl.ie',
    description='A library that rounds a given number to either upwards or downwards as mentioned',
    setup_requires=['pytest-runner'],
    tests_require=['pytest>=4.4.1'],
    test_suite='tests',
    python_requires='>=3.6',

)