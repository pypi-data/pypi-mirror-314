from setuptools import setup, find_packages

VERSION = '0.1'
DESCRIPTION = 'Visualizer for SBMLDiagrams'
LONG_DESCRIPTION = 'Visualizes flux in an Antimony model through arrow size and color'

setup(
    name='SBVisualizer',
    version=VERSION,
    author='Priyanka Talur', 
    author_email='ptalur@uw.edu',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(include=['SBVisualizer', 'SBVisualizer.*']),
    install_requires=[
        'tellurium',
        'SBMLDiagrams',
        # Add other dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
