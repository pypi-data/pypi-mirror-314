from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='chartfactor',
    version='5.1.23',
    description='Integrates ChartFactor with Jupyter Notebooks',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/Aktiun/chartfactor-py',
    author='Aktiun',
    author_email='juan.dominguez@aktiun.com',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.19.5',
        'pandas',
        'pandasql>=0.7.3',
        'pygeohash==1.2.0',
        'jsonschema>=3.2.0',
        'colorama>=0.4.4',
        'importlib-resources>=5.4.0',
        'tzlocal~=4.1',
        'chartfactor-jlab-ext==5.1.23',
    ],
    include_package_data=True,
    keywords=['aktiun', 'jupyter', 'jupyterhub', 'jupyterlab', 'chartfactor-py'],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
