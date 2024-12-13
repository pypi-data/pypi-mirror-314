from setuptools import find_packages, setup

VERSION = '1.4.2'

with open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

setup(
    name='mylib-ual',
    version=VERSION,
    author='hellok',
    author_email='iz1241@163.com',
    description='A web tip of Django',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    keywords='mylib',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[

    ],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ],
)