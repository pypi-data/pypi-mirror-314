from setuptools import setup, find_packages

setup(
    name='PyDataMesh',
    version='1.0.0',
    author='Vishnu Devarajan',
    author_email='vishnuprakash@live.com',
    description='A Python-based library implementing data mesh concepts.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vpdeva/PyDataMesh',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pandas>=1.0.0',
    ],
    include_package_data=True,
)