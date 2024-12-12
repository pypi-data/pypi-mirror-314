from setuptools import setup, find_packages


setup(
    name='mosaik-api-v3',
    version='3.0.13',
    author='mosaik development team',
    author_email='mosaik@offis.de',
    description='Python implementation of the mosaik API version 3.',
    long_description='\n\n'.join(
        open(f, 'rb').read().decode('utf-8')
        for f in ['README.rst', 'CHANGES.txt', 'AUTHORS.txt']),
    long_description_content_type='text/x-rst',
    url='https://mosaik.offis.de',
    install_requires=[
        'docopt>=0.6.1',
        'loguru>=0.6.0',
        'typing-extensions>=4.4.0',
    ],
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    package_data= {
        'mosaik_api_v3': ['py.typed'],
    },
    entry_points={
        'console_scripts': [
            'pyexamplemas = example_mas.mosaik:main',
            'pyexamplesim = example_sim.mosaik:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
