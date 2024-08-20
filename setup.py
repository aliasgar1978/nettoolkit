import setuptools
from nettoolkit import version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nettoolkit",
    # version="1.7.2",
    version=version(),
    author="ALIASGAR - ALI",
    author_email="aholo2000@gmail.com",
    description="Tool Set for Networking Geeks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alias1978/nettoolkit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=['pandas', 'openpyxl', 'PySimpleGUI==4.60.5', 'numpy',
        'xlrd', 'jinja2', 'paramiko', 'netmiko', 'ntc-templates', 'pyyaml', 'attrs',
        # 'pywin32',                    ## Windows specific library, need to do manually...
    ],
    package_data={
        'nettoolkit.nettoolkit.forms':  ['cable_n_connectors.xlsx', ],
    },
)
