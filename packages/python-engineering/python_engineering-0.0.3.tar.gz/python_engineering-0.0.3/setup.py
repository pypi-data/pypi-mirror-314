from setuptools import setup, find_packages
import multiprocessing

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='python-engineering',
      version='0.0.3',
      description='python-engineering, the ultimate engineering function library',
      long_description=readme(),
      url='https://github.com/snakesonabrain/python-engineering',
      download_url='https://github.com/snakesonabrain/python-engineering/archive/master.zip',
      keywords=['engineering', 'geotechnical', 'mechanical'],
      author='Bruno Stuyts',
      author_email='bruno@pro-found.be',
      license='Creative Commons BY-SA 4.0',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],)