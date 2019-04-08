from setuptools import setup
import os

packages = []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)


# TODO
# Change every instance of `your_library_name` to the name of your library.
# Change `author`
# Change `author_email`
# Change `url`
# Change the PyPI classifiers: https://pypi.org/pypi?%3Aaction=list_classifiers


# Probably should be changed, __init__.py is no longer required for Python 3
for dirpath, dirnames, filenames in os.walk('storinopt'):
    # Ignore dirnames that start with '.'
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


setup(
    name='storinopt',
    version="0.1",
    packages=packages,
    author="Carlos Gaete",
    author_email="cdgaete@gmail.com",
    license=open('LICENSE').read(),
    # Only if you have non-python data (CSV, etc.). Might need to change the directory name as well.
    # package_data={'your_name_here': package_files(os.path.join('your_library_name', 'data'))},
    entry_points = {
        'console_scripts': [
            'storinopt-cli = storinopt.bin.rename_me_cli:main',
        ]
    },
    install_requires=[
        'appdirs',
        'docopt',
        'pyomo',
        'pandas',
    ],
    url="https://github.com/cdgaete/StoInOpt",
    long_description=open('README.md').read(),
    description='Estimation of the electricity consumption of storage options in a determined power market',
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)
