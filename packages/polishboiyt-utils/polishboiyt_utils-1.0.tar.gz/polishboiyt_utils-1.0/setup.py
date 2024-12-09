from setuptools import find_packages, setup

setup(
    name="polishboiyt-utils",
    version="1.0",
    description="Tools for people (like me) to make their lives easier.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="PolishBoiYT",
    author_email="polishboiyt@gmail.com",
    url="https://github.com/PolishBoiYT/polishboiyt-utils",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
