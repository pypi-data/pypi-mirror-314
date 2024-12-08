import pathlib
import re
import setuptools


setuptools.setup(
    name='arrange',
    version='1.0.0',
    description='',
    url='http://github.com/danijar/arrange',
    long_description_content_type='text/markdown',
    packages=['arrange'],
    install_requires=['imageio', 'Pillow', 'numpy'],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
