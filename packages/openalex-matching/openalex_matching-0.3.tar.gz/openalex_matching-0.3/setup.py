from setuptools import setup, find_packages

setup(
    name= "openalex_matching",  
    version = "0.3",  
    author="Bryan Yuk", 
    author_email= "dzg5cg@virginia.edu",  
    license = "MIT",
    long_description= open('README.md').read(),
    long_description_content_type='text/markdown', 
    url="https://github.com/byuk729/openalex_matching",  
    packages=find_packages(),  
    install_requires=[
        "requests",  
        "pandas",
        "tqdm",
        "fuzzywuzzy",
        "nicknames"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",  
        "License :: OSI Approved :: MIT License",  
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis"
    ],
    python_requires='>=3.8',  # Minimum Python version required
)