from setuptools import setup
import os
import sys

os.system("pip install pylib3")
try:
    import pylib3
except ImportError as err:
    sys.exit(err)

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


with open("README.md") as ifile:
    long_description = ifile.read()

package_name = 'linode_mgmt'
setup(
    name=package_name,
    version=pylib3.get_version(
        caller=__file__,
        version_file='LINODE-MGMT_VERSION',
    ),
    include_package_data=True,
    packages=[package_name],
    install_requires=get_required_packages(),
    scripts=[
        f"{package_name}/scripts/linode-mgmt"
    ],
    data_files=[(os.path.join('docs', package_name), ['README.md'])],
    url='',
    author='Shlomi Ben-David',
    author_email='shlomi.ben.david@gmail.com',
    description='Linode management python package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
