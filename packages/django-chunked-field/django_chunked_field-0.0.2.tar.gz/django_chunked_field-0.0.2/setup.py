import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-chunked-field',
    version='0.0.2',
    description='A Django app providing a ChunkedTextField for storing large text data in chunks.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='berkayeren',
    author_email='berkay-eren@hotmail.com',
    url='https://github.com/berkayeren/django-chunked-field',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'Django>=3.2',
    ],
)
