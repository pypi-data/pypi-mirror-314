from setuptools import setup, find_packages

setup(
    name='desktop_by_harmless',  
    version='0.1.0',  
    description='Un package Python pour importer les fichiers de votre ordinateur ',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  
    author='Moi',
    author_email='tunelaurapas@gmail.com',
    url='https://github.com/MaxLinkerluabug/desktop', 
    packages=find_packages(),  
    install_requires=[  
        'numpy',
        'requests',
    ],
    classifiers=[  
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  
)
