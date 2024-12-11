# author     : Hadi Cahyadi
# email      : cumulus13@gmail.com
# description: Snarl python lib, Send SNP/3.1 messages. (Snarl)
# created in 37 minutes :)
# -*- coding: UTF-8 -*-

import io
from setuptools import setup, find_packages

# Read the README file
with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

version = {}
with open("__version__.py") as fp:
    exec(fp.read(), version)

version = version['version']

setup(
    name="pysnarl",
    version=version,
    url="https://github.com/cumulus13/snarl",
    project_urls={
        "Documentation": "https://github.com/cumulus13/snarl",
        "Code": "https://github.com/cumulus13/snarl",
    },
    license="GPL",
    author="Hadi Cahyadi LD",
    author_email="cumulus13@gmail.com",
    maintainer="cumulus13 Team",
    maintainer_email="cumulus13@gmail.com",
    description="Snarl python lib, Send SNP/3.1 messages. (Snarl)",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'argparse',
        'rich',
        'configset',
        'ctraceback'
    ],
    entry_points={
        "console_scripts": [
            "snarl = pysnarl.__main__:usage",
            "pysnarl = pysnarl.__main__:usage",
        ]
    },
    data_files=['__version__.py', 'README.md', 'LICENSE.md'],
    license_files=["LICENSE.md"],    
    include_package_data=True,
    python_requires=">=3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: GNU General Public License (GPL)', 
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
