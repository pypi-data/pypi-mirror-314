from setuptools import setup, find_packages

setup(
    name='viturka',
    version='0.1.65',
    description='A client library for federated learning platform.',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    install_requires=[
        'numpy==1.24.3',
        'pandas',
        'fastFM',
        'scikit-learn',
        'scipy',
        'seaborn'
    ],
    python_requires='>=3.6'
)

