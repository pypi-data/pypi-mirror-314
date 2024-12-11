from setuptools import find_packages
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ipfabric_netbox",
    version="3.1.1",
    author="Solution Architecture",
    author_email="solution.architecture@ipfabric.io",
    description="NetBox plugin to sync IP Fabric data into NetBox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["ipfabric>=6.6.4", "netutils"],
    url="https://gitlab.com/ip-fabric/integrations/ipfabric-netbox-sync",
    project_urls={
        "Bug Tracker": "https://gitlab.com/ip-fabric/integrations/ipfabric-netbox-sync/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
