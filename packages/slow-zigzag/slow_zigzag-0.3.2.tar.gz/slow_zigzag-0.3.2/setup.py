from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
# from Cython.Build import cythonize

from build import build


setup(
    include_package_data=True,
    name='slow_zigzag',
    version='0.3.2',
    description='Zig Zag indicator',
    url='https://github.com/pakchu/zigzag',
    author=['hjkim17', 'pakchu'],
    packages=find_packages(),
    package_data={'zigzag': ['*.py'],
                  'zigzag_cython': ['*.py', '*.pyx', '*.pxd']},
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=[
        'numpy',
        'pandas',
    ],
    python_requires='>=3.9',
    long_description=open('README.md').read(),
    ext_modules=build(),
    cmdclass={"build_ext": build_ext},
)