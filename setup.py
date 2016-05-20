from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='pyunc',
    version='0.0.1',
    packages=['pyunc'],
    zip_safe=True,
    author='Jon Stutters',
    author_email='j.stutters@ucl.ac.uk',
    description='Classes for reading UNC format MRI files',
    long_description=readme(),
    url='https://github.com/jstutters/pyunc',
    install_requires=[
        "numpy",
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    license='MIT',
    classifiers=[
    ]
)
