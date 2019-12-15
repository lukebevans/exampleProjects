from setuptools import setup, find_packages

setup(
    name='listS3Contents',
    version='0.0.1',

    description="list contents of S3 bucket",
    author='Luke Bevans',
    packages= find_packages(
        exclude=['tests']
    ),
    test_suite='tests',

    install_requires=[
        'boto3'
    ],
    tests_require=[
        'moto'
    ],

)
