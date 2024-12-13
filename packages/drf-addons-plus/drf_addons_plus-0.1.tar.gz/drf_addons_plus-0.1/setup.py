from setuptools import setup, find_packages

setup(
    name='drf_addons_plus',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'djangorestframework>=3.0'
    ],
    author='José Gabriel Gruber',
    author_email='development@jgabrielgruber.dev',
    description='This project provides some extra functionalities to be used with Django REST Framework',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/JGabrielGruber/drf-addons-plus',
    license='AGPL-3.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)