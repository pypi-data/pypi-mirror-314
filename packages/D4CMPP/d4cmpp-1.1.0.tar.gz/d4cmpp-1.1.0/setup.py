from setuptools import setup, find_packages

setup(
    name='D4CMPP',
    version='1.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'torch>=2',
        'dgl>=1',
        'tqdm',
        'pandas',
        'numpy',
        'matplotlib',
        'pyyaml',
        'rdkit',
        'scikit_learn',
        'prettytable'
    ],
    author="Park Jinyong",
    author_email="phillip1998@korea.ac.kr",
    description="Molecular property prediction based on Graph Convolution Network published by Deep4Chem",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/phillip1998/D4C_MPP",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)