from setuptools import setup, find_packages

setup(
    name='serializers',
    version='1.0',
    author="Sosnin Arthur",
    author_email="artursosnin2001@gmail.com",
    packages=find_packages(),
    install_requires=['toml', 'PyYAML'],
    test_suite='unit_tests',
    entry_points={
        'console_scripts': [
            'serializers = utillit:main',            
        ]
    }
)