from setuptools import setup, find_packages

setup(
    name='adaptive_power_neurons',  # Name of the package
    version='0.3.6',  # Corrected version number
    author='Dedeep Vasireddy',  # Your name or organization
    author_email='vasireddydedeep@gmail.com',  # Your email
    description='A neural network model using adaptive power neurons for regression and classification',
    long_description=open('README.md').read(),  # The long description from your README.md
    long_description_content_type='text/markdown',  # The content type of the long description (markdown here)
    url='https://github.com/Dedeep007/adaptive-power-neurons',  # Your package's URL
    project_urls={
        'Documentation': 'https://github.com/Dedeep007/adaptive-power-neurons/wiki',
        'Source': 'https://github.com/Dedeep007/adaptive-power-neurons',
    },

    python_requires='>=3.6',  # Python version that your package supports

    packages=find_packages(),  # Finds all packages in the current directory

    install_requires=[
        'numpy>=1.18.5',
        'scikit-learn>=0.23.1',
    ],

    include_package_data=True,
    package_data={
        '': ['data/*.csv'],
    },

    extras_require={
        'dev': [
            'pytest>=5.4',
            'sphinx>=3.0',
        ],
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],

    keywords='neural network, regression, adaptive power neurons, machine learning',

    entry_points={
        'console_scripts': [
            'adaptive-power-neurons-cli=adaptive_power_neurons.cli:main',
        ],
    },
)
