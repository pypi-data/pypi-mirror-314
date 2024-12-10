from setuptools import setup, find_packages

setup(
    name='remdex',
    version='0.39',
    description='Fast and lightweight federated learning framework',
    packages=find_packages(), 
    install_requires=[
        'cloudpickle',
        'numpy'
    ],
    license='MIT'
)


