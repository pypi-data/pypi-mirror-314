from setuptools import setup, find_packages

setup(
    name='ugen',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'torch',  
    ],
    author='Yougen',
    author_email='you@gen.com',
    description='More powerful than pytorch',
    url='https://github.com/ugen/ugen',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)