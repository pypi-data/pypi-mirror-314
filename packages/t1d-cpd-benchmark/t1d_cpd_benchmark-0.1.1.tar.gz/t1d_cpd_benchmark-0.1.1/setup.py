from setuptools import setup, find_packages
import os
import shutil
import urllib.request
import zipfile
from setuptools.command.develop import develop
from setuptools.command.install import install
import sys


def download_and_extract_data():
    # URL of GitHub release zip file
    url = "https://github.com/Blood-Glucose-Control/t1d-change-point-detection-benchmark/archive/refs/tags/v0.1.0.zip"

    # Get the package installation directory
    if 'develop' in sys.argv:
        # For development installs, use current directory
        package_dir = os.path.abspath('t1d_cpd_benchmark')
    else:
        # For regular installs, use site-packages directory
        import t1d_cpd_benchmark
        package_dir = os.path.dirname(t1d_cpd_benchmark.__file__)

    zip_path = os.path.join(package_dir, 'temp.zip')
    try:
        print("Downloading data files...")
        urllib.request.urlretrieve(url, zip_path)

        print("Extracting data files...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Extract to a temporary directory first
            temp_dir = os.path.join(package_dir, 'temp_extract')
            os.makedirs(temp_dir, exist_ok=True)
            zip_ref.extractall(temp_dir)

            source_data_dir = os.path.join(
                temp_dir, 't1d-change-point-detection-benchmark-0.1.0', 't1d_cpd_benchmark', 'data')

            data_dir = os.path.join(package_dir, 'data')
            if os.path.exists(data_dir):
                shutil.rmtree(data_dir)

            shutil.move(source_data_dir, package_dir)
            shutil.rmtree(temp_dir)

        # Clean up
        os.remove(zip_path)
        print("Data files successfully downloaded and extracted!")
    except Exception as e:
        print(f"Error downloading data: {e}")
        raise


class PostDevelopCommand(develop):
    def run(self):
        download_and_extract_data()
        develop.run(self)


class PostInstallCommand(install):
    def run(self):
        download_and_extract_data()
        install.run(self)


setup(
    name="t1d_cpd_benchmark",
    version="0.1.1",
    description="An open source benchmark for semi-supervised change point detection of type 1 diabetic meals from continuous glucose monitor time series data. Originally created to present to PyData Global 2024 in association with sktime and skchange.",
    url="https://github.com/Blood-Glucose-Control/t1d-change-point-detection-benchmark",
    packages=find_packages(),
    license="MIT",
    author="Christopher Risi",
    author_email="christopher.risi@uwaterloo.ca",
    include_package_data=True,
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    install_requires=[
        "numpy>=1.25.0",
        "pandas>=2.0.3",
    ],
)
