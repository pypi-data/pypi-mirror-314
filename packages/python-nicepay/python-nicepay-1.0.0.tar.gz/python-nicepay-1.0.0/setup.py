from setuptools import setup, find_packages


setup(
    name='python-nicepay',
    version='1.0.0',
    packages=find_packages(),
    description='This is the Official Python API client / library for NICEPAY Payment API',
    long_description_content_type='text/markdown',
    author='Harfa Thandila',
    author_email='harfa.thandila@nicepay.co.id',
    url='https://github.com/nicepay-dev/python-nicepay',
    license='',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'pycryptodome',
        'requests',
    ],

)
