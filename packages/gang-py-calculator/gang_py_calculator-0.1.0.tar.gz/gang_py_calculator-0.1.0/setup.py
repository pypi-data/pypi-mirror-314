from setuptools import setup, find_packages

setup(
    name='gang_py_calculator',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='gang',
    author_email='gangadriyarraballi@example.com',
    description='A simple calculator package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)