from setuptools import setup, find_packages

setup(
    name='Dhan_Tradehull',  # Replace with your project name
    version='3.0.0',    # Initial version
    description='A Dhan Codebase from TradeHull',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='TradeHull',
    author_email='contact.tradehull@gmail.com',
    url='https://github.com/TradeHull/Dhan_Tradehull',  # GitHub repo or project URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'dhanhq>=2.0.0',
        'mibian>=0.1.3',
        'numpy>=1.24.4',
        'pandas>=2.0.3',
        'pytz>=2024.1',
        'requests>=2.32.3',
    ]
    ,
)
