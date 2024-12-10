from setuptools import setup

setup(
    name='carnotpy',
    version='0.6.0',
    author='Carnot Innovations',
    description='Carnot Connection as a Python Package',
    long_description='Carnot Connection as a Python Package',
    py_modules=['carnotpy'],
    install_requires=[
        'pandas',
        'requests',
        'python-dateutil',
    ],
)
