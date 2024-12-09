from setuptools import setup, find_packages
import sys
import os

# 读取版本号
version_file = os.path.join(os.path.dirname(__file__), 'wqdebug', '_version.py')
with open(version_file, 'r') as f:
    exec(f.read())

if sys.version_info[:2] < (3, 6):
    sys.exit("Python < 3.6 is not supported")

setup(
    name="wqdebug",
    version=__version__,
    author="deng.weiwei",
    author_email="deng.weiwei@wuqi-tech.com",
    description="Python module for wuqi debug",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    install_requires=["wqgdb", "requests"],
    packages=find_packages(),
    package_data={
        'wqdebug': [
            'tools.json',
            'gdbinit.py',
            'test/*.*',
        ],
    },
    include_package_data=True,
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'wqdebug=wqdebug.wqdebug:main',
        ],
    }
)
