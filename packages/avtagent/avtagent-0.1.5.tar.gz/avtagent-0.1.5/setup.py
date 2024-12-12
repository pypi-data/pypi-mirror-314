from setuptools import setup, find_packages

setup(
    name='avtagent',  # Replace with your package’s name
    version='0.1.5',
    packages=find_packages(),
    install_requires=[
        "openai",
        "pyautogen"
    ],
    author='Harry Wang',  
    author_email='lajja.khakhkhar@avtinc.onmicrosoft.com',
    url='https://github.com/AvnetGIS/bcs-oco-agent-lib.git',
    description='A library for avt agent',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',

)
