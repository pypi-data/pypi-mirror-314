from setuptools import setup, find_packages

setup(
    name='pg_index_insight',
    version='v1.5.0',
    author='Huseyin Demir,Mert Yavaşca',
    author_email='huseyin.d3r@gmail.com',
    description='A CLI tool for analyzing PostgreSQL index efficiency',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kylorend3r/pg_index_insight',  
    packages=find_packages(), 
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'click', 
        'psycopg2==2.9.9',
        'tabulate',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'pgindexinsight=pg_index_insight.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
