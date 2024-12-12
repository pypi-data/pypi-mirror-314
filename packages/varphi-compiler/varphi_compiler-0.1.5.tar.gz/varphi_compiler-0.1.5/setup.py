from setuptools import setup, find_packages

setup(
    name="varphi_compiler",
    version="0.1.5",
    description="Compiler for the Varphi Programming Language.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Hassan El-Sheikha",
    author_email="hassan.elsheikha@utoronto.ca",
    url="https://github.com/hassanelsheikha/vpc",
    packages=find_packages(),
    install_requires=[
        "varphi_parsing_tools==0.0.4",
        "pyinstaller",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'vpc=varphi_compiler.vpc:main',
        ],
    },
    include_package_data=True,
)

