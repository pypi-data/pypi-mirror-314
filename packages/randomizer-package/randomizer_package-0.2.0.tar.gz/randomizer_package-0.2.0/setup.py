from setuptools import setup, find_packages

setup(
    name='randomizer_package',
    version='0.2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[

    ],
    entry_points={
        'console_scripts': [
            'randomizer=randomizer.gui:main',  
        ],
    },
    author='Nblancs',
    author_email='noeljhumel.blanco@1.ustp.edu.ph',
    description='A randomizer gui application for generating random outputs.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/NBlancs/randomizer_nblancs', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)