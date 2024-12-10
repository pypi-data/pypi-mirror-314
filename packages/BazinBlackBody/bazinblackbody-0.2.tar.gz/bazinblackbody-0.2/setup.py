from setuptools import setup, find_packages
import os

moduleDirectory = os.path.dirname(os.path.realpath(__file__))
exec(open(moduleDirectory + "/bazinBlackBody/__version__.py").read())


def readme():
    with open(moduleDirectory + '/README.md') as f:
        return f.read()


setup(
    name="BazinBlackBody",
    description='Fitting multiband lightcurves with a Bazin-Blackbody surface',
    long_description=readme(),
    long_description_content_type="text/markdown",
    version=__version__,
    author='RoyDavidWilliams',
    author_email='roydavidwilliams@gmail.com',
    license='MIT',
    url='https://github.com/RoyWilliams/bazinBlackBody',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
          'numpy',
          'scipy',
          'matplotlib',
      ],
    classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Utilities',
    ],
    python_requires='>=3.6',
)
