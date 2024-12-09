import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Ethan Smith",
    author_email="98723285+ethansmith2000@users.noreply.github.com",
    name='fsdp_optimizers',
    license='Apache',
    description='supporting pytorch FSDP for optimizers',
    version='0.0.1',
    long_description=README,
    url='https://github.com/ethansmith2000/fsdp_optimizers',
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
    long_description_content_type="text/markdown",
    install_requires=['torch', 'numpy'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)