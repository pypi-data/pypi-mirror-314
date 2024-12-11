from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize
import subprocess

class CustomBuildCommand(build_ext):
    def run(self):
        subprocess.check_call(["python", "build.py"])
        super().run()

setup(
    include_package_data=True,
    name='slow_zigzag',
    version='0.2.4',
    description='Zig Zag indicator',
    url='https://github.com/pakchu/zigzag',
    author=['hjkim17', 'pakchu'],
    packages=find_packages(),
    package_data={'zigzag': ['*.py', '*.pyx', '*.pxd', '*.c']},
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=[
        'numpy',
        'pandas',
        'pandas-ta'
    ],
    python_requires='>=3.9',
    long_description=open('README.md').read(),
    ext_modules=cythonize("zigzag/core.pyx"),
    cmdclass={"build_ext": CustomBuildCommand},
)