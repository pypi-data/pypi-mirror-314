from setuptools import setup, find_packages

CURRENT_VERSION = '0.6'

setup(
    name='PyWrikeAssist',
    version=CURRENT_VERSION,
    packages=['PyWrikeAssist'],
    description='A Python package to make API calls to Wrike',
    author='Ambareen-Jawaheer',
    author_email='ambareenjawaheer@gmail.com',
    url='https://github.com/axirestech/PyWrikeAssist',
    download_url='https://github.com/axirestech/PyWrikeAssist/archive/refs/tags/v%s.tar.gz' % CURRENT_VERSION,
    keywords=['api', 'gateway', 'wrike', 'http', 'REST'],
    install_requires=[
        'requests>=2.0',
        'openpyxl>=3.0',
        'beautifulsoup4>=4.9',
        'pandas>=1.0',
        'Flask>=2.0',
        'PyWrike>=1.86'
    ],
    #use_2to3=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: Free For Home Use",
        "Operating System :: OS Independent",
    ],
)
