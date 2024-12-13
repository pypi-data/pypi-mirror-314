from setuptools import setup, find_packages

setup(
    name='thermo_metaextractor',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],  # Add dependencies if needed
    description='A library for extracting table names and data sources from SQL queries.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your_email@example.com',
    url='https://github.com/your_username/thermo_metaextractor',  # Replace with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
