from setuptools import setup, find_packages

setup(
    name="a5py",
    version="0.1.2",
    packages=find_packages(),
    description='a5 hydrometeorologic database management system',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author='Juan F. Bianchi',
    author_email='jbianchi@ina.gob.ar',
    url='https://github.com/jbianchi81/a5_client',
    python_requires=">=3.10",
    install_requires=[
        "requests",
        # "gdal",
        "numpy",
        "psycopg2",
        "sqlalchemy",
        "geoalchemy2",
        "rasterio",
        "shapely"
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'a5py=a5py.a5py_cli:main',
            'a5py_config=a5py.config:run',
        ],
    },
)

