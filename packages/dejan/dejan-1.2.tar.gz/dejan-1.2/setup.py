from setuptools import setup, find_packages

setup(
    name="dejan",
    version="1.2",
    description="Machine learning utilities by DEJAN.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="DEJAN",
    author_email="enquiries@dejanmarketing.com",
    url="https://github.com/dejanmarketing/dejan",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
        "pandas",
        "transformers",
        "torch",
        "click",
    ],
    entry_points={
        'console_scripts': [
            'dejan=dejan.cli:cli',
        ],
    },
    include_package_data=True,
)
