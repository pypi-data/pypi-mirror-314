from setuptools import setup, find_packages

setup(
    name='easyarduino',  # Name of your package
    version='0.1',  # Initial version of the package
    description='A simple and easy-to-use Arduino control library using PyFirmata',
    author='AKM Korishee Apurbo',  # Your name or the name of your organization
    author_email='bandinvisible8@gmail.com',  # Your email
    url='https://github.com/IMApurbo/easyarduino',  # Link to your repository or website
    packages=find_packages(),  # Automatically finds all packages in the directory
    install_requires=[  # List the dependencies required by your package
        'pyfirmata',
        'pyserial',  # pyserial is required for serial communication
    ],
    classifiers=[  # Optional classifiers to help others find your package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum required Python version
)
