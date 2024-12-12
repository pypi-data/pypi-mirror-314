from setuptools import setup, find_packages
import os

# Get the path to the `package_version.txt` file
version_file = os.path.join(
    os.path.dirname(__file__), "v_installer", "package_version.txt"
)

# Read the version from the VERSION file
with open(version_file) as f:
    version = f.read().strip()

setup(
    name="v-installer",
    version=version,
    description="Install my app, not for all people",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Koi",
    author_email="your.email@example.com",
    url="http://gitea:8000/datlt4/fortifai_monitoring",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "install_v=v_installer.cli:install_v",
        ],
    },
    package_data={
        "v_installer": ["package_version.txt"],
    },
    install_requires=[
        "requests",
        "textual==0.89.1",
        "textual-dev==1.7.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
