from setuptools import setup, find_packages

setup(
    name='MidBrain',
    version='1.2.3',
    packages=find_packages(),
    install_requires=[
        "openai",
        "colorama>=0.4.6",
        'transformers>=4.0.0',  
        'torch>=1.8.0',         
        'click',                 
    ],
    entry_points={
        'console_scripts': [
            'midbrain=MidBrain.MidBrain:main', 
        ],
    },
    description='Your magical CLI for generating text spells and performing tasks.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Harshit Kulkarni',
    author_email='harshitkulkarni22@gmail.com',
    url='https://github.com/harshitkulkarni22/hokus-pokus',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
