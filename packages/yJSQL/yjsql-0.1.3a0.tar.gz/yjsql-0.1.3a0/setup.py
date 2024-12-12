from setuptools import setup, find_packages
setup(
    name='yJSQL',
    version='0.1.3a',
    author='Giorgio Loggia',
    author_email='yungestdev@gmail.com',
    description='JSQL is a lightweight database system that stores data in a JSON file with SQL-like operations. It allows creating tables, inserting, querying, updating, and deleting data, and supports transactions with rollback and commit. JSQL enforces constraints such as unique keys and foreign keys, making it easy to manage structured data in JSON.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)