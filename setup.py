from setuptools import setup, find_packages
from pathlib import Path
import re

with open(Path(__file__).absolute().parent/"README.md", "r") as fh:
    long_description = fh.read()

with open(Path(__file__).absolute().parent/"requirements.txt") as f:
    requirements = f.read().splitlines()


def format_branch_name(name):
    pattern = re.compile("^(bugfix|feature)\/issue-([0-9]+)-\S+")
    match = pattern.search(name)
    if not match:
        return match.group(2)
    if name == "master":
        return name
    raise ValueError(f"Wrong branch name: {name}")


setup(name='cdek',
      author='nek',
      author_email='nek@srez.org',
      description='A library that simplifies the work with the API of the CDEK delivery service.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=find_packages(),
      install_requires=requirements,
      extras_require={
          'dev': ['pylint', 'pytest']
      },
      classifiers=[
          "Programming Language :: Python :: 3.5",
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
      python_requires='>=3.6')
