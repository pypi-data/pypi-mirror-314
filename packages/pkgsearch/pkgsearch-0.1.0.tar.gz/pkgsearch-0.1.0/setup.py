from setuptools import setup, find_packages

setup(
    name="pkgsearch",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "packaging",
        "pyperclip",
    ],
    entry_points={
        'console_scripts': [
            'pkgsearch=pkgsearch.psearch:main',
        ],
    },
    author="kanigten", 
    author_email="10207922+5bhuv4n35h@users.noreply.github.com",
    description="A package to search for versions of packages from various repositorie and list versions",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/5bhuv4n35h/pkgsearch",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
