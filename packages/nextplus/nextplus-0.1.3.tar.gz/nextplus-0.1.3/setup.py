from setuptools import setup, find_packages

version = '0.1.3'

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='nextplus',
    version=version,
    author='NPO Systems LTD',
    author_email='info@nextplus.io',
    description='A Python SDK for interacting with the Next Plus MES system',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=2.7',
    install_requires=[
        'requests>=2.25.1'
    ],
    keywords='nextplus mes api sdk',
    license='MIT',
    include_package_data=True,
    zip_safe=False
)

