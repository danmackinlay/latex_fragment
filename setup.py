from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(
      name='latex_fragment',
      version='0.0.1',
      description=u"Skeleton of a Python package",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Dan MacKinlay",
      author_email='dan@livingthing.org',
      url='https://github.com/danmackinlay/latex_fragment',
      license='MIT',
      packages=['latex_fragment'],
      scripts=[],
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'test': ['pytest'],
      },
)
