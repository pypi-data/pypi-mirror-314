from setuptools import setup, find_packages

setup(
    name="fluss_api",
    version="0.1.7",
    packages= find_packages(),
    install_requires =[

    ],
    author="Njeru Ndegwa",
    author_email="njeru@fluss.io",
    description='A library to integrate the Fluss API into Home Assistant',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)