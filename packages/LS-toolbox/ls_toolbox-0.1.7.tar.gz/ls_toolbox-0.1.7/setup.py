from setuptools import setup, find_packages

setup(
    name='LS_toolbox',
    version='0.1.7',
    author='Marc Gardegaront',
    author_email='marc.gardegaront@univ-eiffel.fr',
    description='Toolboxes for working with LS-Dyna and LS-Prepost through python.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'numpy-stl',
    ],
    include_package_data=True,
    package_data={'': ['Example/*']},  # Include the example folder in the package
)