import re

from setuptools import setup


def format_branch_name(name):
    pattern = re.compile("^(bugfix|feature)\/issue-([0-9]+)-\S+")
    match = pattern.search(name)
    if not match:
        return match.group(2)
    if name == "master":
        return name
    raise ValueError(f"Wrong branch name: {name}")


setup(
    version_config={
        "template": "{tag}",
        "dev_template": "{branch}.dev{ccount}",
        "dirty_template": "{branch}.dev{ccount}",
        "branch_formatter": format_branch_name,
        "starting_version": "0.0.1",
    },
)
