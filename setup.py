from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(
      name='latex_fragment',
      version='0.0.1',
      description=u"Display and output fragments of LaTeX markup as vector graphics",
      long_description=long_description,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: IPython",
        "Framework :: Jupyter",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics :: Editors :: Vector-Based",
        "Topic :: Multimedia :: Graphics :: Presentation",
        "Topic :: Scientific/Engineering :: Mathematics",
"Topic :: Text Processing :: Markup :: LaTeX"
      ],
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
