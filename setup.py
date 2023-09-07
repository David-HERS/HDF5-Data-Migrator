from setuptools import setup

setup(
    name='hdf5migrator',
    version='0.1',
    description='Recursively searches through folders for .dat files and images, converting them into groups and datasets within an HDF5 file',
    author='David Ulises Herrera Serna et al.',
    author_email='davidhs1698@gmail.com',
    packages=['hdf5migrator'],
    install_requires=[
        'numpy',
        'h5py',
        'pillow',
    ],
)
