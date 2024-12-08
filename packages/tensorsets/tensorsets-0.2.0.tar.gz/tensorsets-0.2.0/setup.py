import pathlib
import setuptools


setuptools.setup(
    name='tensorsets',
    version='0.2.0',
    description='Fast format for datasets.',
    url='http://github.com/danijar/tensorsets',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=['tensorsets'],
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
