import pathlib
import setuptools


def parse_reqs(filename):
  requirements = pathlib.Path(filename)
  requirements = requirements.read_text().split('\n')
  requirements = [x for x in requirements if x.strip()]
  return requirements


setuptools.setup(
    name='worldmodels',
    version='0.2.0',
    author='Danijar Hafner',
    author_email='mail@danijar.com',
    description='World models',
    url='http://github.com/danijar/worldmodels',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=parse_reqs('requirements.txt'),
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
