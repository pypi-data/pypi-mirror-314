from setuptools import setup, find_packages

setup(
    name='xyl-client.py',  # Name of the package
    version='0.2.1',
    description='Client library to interact with the XYL Network',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='debxylen',
    author_email='priyanshudeb3@gmail.com',
    url='https://github.com/debxylen/xyl-client.py',  # GitHub or project URL
    packages=find_packages(),
    install_requires=["requests", "web3", "eth-typing", "eth-utils", "eth-account", "eth-rlp"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum required Python version
)
