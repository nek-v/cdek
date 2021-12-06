import os
import re

from setuptools import setup, find_packages

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "README.md")) as f:
    long_description = f.read()

with open(os.path.join(HERE, "requirements.txt")) as f:
    requirements = f.read().split("\n")


def format_branch_name(name):
    pattern = re.compile("^(bugfix|feature)\/issue-([0-9]+)-\S+")
    match = pattern.search(name)
    if not match:
        return match.group(2)
    if name == "master":
        return name
    raise ValueError(f"Wrong branch name: {name}")


setup(
    name='cdek',
    author='nek',
    author_email='nek@srez.org',
    description='A library that simplifies the work with the API of the CDEK delivery service.',
    license="MIT",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=requirements,
    keywords='cdek api',
    extras_require={
        'dev': ['pylint', 'pytest']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=["setuptools-git-versioning"],
    version_config={
        "template": "{tag}",
        "dev_template": "{branch}.dev{ccount}",
        "dirty_template": "{branch}.dev{ccount}",
        "branch_formatter": format_branch_name,
        "starting_version": "0.0.1",
    },
    python_requires='>=3.3',
    include_package_data=True,
    zip_safe=False
)
