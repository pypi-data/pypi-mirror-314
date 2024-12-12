from setuptools import setup
import os
import sys


BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def get_required_packages():
    """
    Reads the requirements packages from requirement.txt file

    :return list of package names and versions (i.e ['requests==2.19.1'])
    """
    file_name = 'requirements.txt'
    file_path = os.path.join(BASE_PATH, file_name)
    if not os.path.exists(file_path):
        sys.exit(f"The '{file_name}' file is missing...")

    required_packages = open(file_path).readlines()
    return [package.rstrip() for package in required_packages]


setup(
    install_requires=get_required_packages()
)
