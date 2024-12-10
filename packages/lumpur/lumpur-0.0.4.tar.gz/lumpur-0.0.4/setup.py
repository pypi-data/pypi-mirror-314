from setuptools import setup, find_packages

setup(
    name='lumpur',
    version='0.0.4',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "numpy>=1.26.4",      # Specify minimum version,
        "matplotlib>=3.8.4",
        "pandas>=2.2.2",
    ],
    tests_require=[
        'unittest',
    ],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            # If you have any console scripts, specify them here
        ],
    },
    url='https://github.com/dudung/lumpur',
    license='MIT',
    author='Sparisoma Viridi',
    author_email='dudung@gmail.com',
    description='learn to use methods for processing unclear response',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
