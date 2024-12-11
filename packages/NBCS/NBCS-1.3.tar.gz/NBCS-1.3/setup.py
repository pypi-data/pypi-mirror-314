from setuptools import setup, find_packages

# Open the README.md file and use it as the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='NBCS',
    version='1.3',
    description='Python package that implements an adaptive classification and regression system using simplicial complexes. The package provides a novel approach to handling both binary and multi-class classification problems, as well as regression tasks, by adaptively creating a simplicial decomposition of the feature space.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Amit Ronen',
    author_email='erankfmn@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'scikit-learn'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
