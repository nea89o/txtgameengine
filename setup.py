from setuptools import setup, find_packages
import os
def o(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))
setup(
    name='txtgameengine',
    version='0.0.0',
    author='Rom',
    packages=find_packages(),
    install_requires=o('requirements.txt').readlines(),
    zip_safe=False,
    include_package_data=True,
)
