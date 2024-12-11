import setuptools

setuptools.setup(
    name='TANWEE',
    version='0.1',
    author='TAN',
    description='A test library for demonstrating Python packaging',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)