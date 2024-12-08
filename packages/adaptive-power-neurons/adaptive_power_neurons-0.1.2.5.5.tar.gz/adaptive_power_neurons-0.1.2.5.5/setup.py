from setuptools import setup, find_packages

setup(
    # Basic metadata
    name='adaptive_power_neurons',  # Name of the package
    version='0.1.2.5.5',  # Version of the package (ensure this is updated on each release)
    author='Dedeep Vasireddy',  # Your name or organization
    author_email='vasireddydedeep@gmail.com',  # Your email
    description='A neural network model using adaptive power neurons for regression and classification',
    long_description=open('README.md').read(),  # The long description from your README.md
    long_description_content_type='text/markdown',  # The content type of the long description (markdown here)
    url='https://github.com/Dedeep007/adaptive-power-neurons',  # Your package's URL (replace with your repo link)
    project_urls={
        'Documentation': 'https://github.com/Dedeep007/adaptive-power-neurons/wiki',  # Optional: add links for documentation
        'Source': 'https://github.com/Dedeep007/adaptive-power-neurons',  # Optional: link to source code
    },

    # Python version compatibility
    python_requires='>=3.6',  # Python version that your package supports

    # List of packages to include in the distribution
    packages=find_packages(),  # Finds all packages in the current directory

    # Dependencies (these will be installed automatically when your package is installed)
    install_requires=[
        'numpy>=1.18.5',  # Example: if your package requires numpy
        'scikit-learn>=0.23.1',  # Example: if your package uses scikit-learn
    ],

    # Additional files to include (e.g., data, configuration files)
    include_package_data=True,
    package_data={
        '': ['data/*.csv'],  # Example: include CSV files from the data directory
    },

    # Optional: Testing dependencies
    extras_require={
        'dev': [
            'pytest>=5.4',  # Example: testing framework
            'sphinx>=3.0',  # Example: for documentation generation
        ],
    },

    # Classifiers for PyPI (help users find your package)
    classifiers=[
        'Development Status :: 3 - Alpha',  # This can change as your package matures
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',  # Update for specific versions you support
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',  # Assuming you're using MIT license
    ],

    # Optional: Keywords for your package to help users discover it
    keywords='neural network, regression, adaptive power neurons, machine learning',

    # Optional: Entry points for command-line interfaces (CLI)
    entry_points={
        'console_scripts': [
            'adaptive-power-neurons-cli=adaptive_power_neurons.cli:main',  # Example CLI entry point
        ],
    },
)
