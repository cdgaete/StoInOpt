# python-skeleton

Skeleton for Python projects that meet BONSAI guidelines.

Under development, follows the following:

* https://github.com/pyscaffold/pyscaffold
* https://docs.python-guide.org/writing/structure/
* https://github.com/modocache/pyhoe

## Getting started

The first step is to choose your library name. You should check [pypi](https://pypi.org/) to make sure your name is still available! Names should be lower case, and use underscores (`_`), not hyphens (`-`).

## License

The default license is 3-clause BSD. You need to insert your name(s) in the `LICENSE` file.

## Basic setup

Rename the directory `your_library_name` to the *exact* name of your library.

### Update `setup.py`

* Change every instance of `your_library_name` to the name of your library.
* Change `author`, `author_email`, `url`, and the PyPI [classifiers](https://pypi.org/pypi?%3Aaction=list_classifiers).

## Executable

There is a skeleton executable using [docopt](http://docopt.org/) in `your_library_name/bin`.

If you want to have a command line program that you can call from a terminal, you will need to do the following:

* Rename the file `your_library_name/bin/rename_me_cli.py`
* Change the `entry_points` section in `setup.py` to match the new directory and file names

Otherwise, do the following:

* Delete the `bin` directory
* Remove `docopt` from `requirements.txt`
* Delete the `entry_points` section from `setup.py`.

## Documentation

We recommend building documentation using [sphinx](), and hosting documentation on [Github pages](http://www.sphinx-doc.org/en/master/) or [read the docs](https://readthedocs.org/). Github pages is easier to configure, while read the docs will build automatically with each pushed commit.

To start the documentation structure, first install `sphinx` using conda or pip. Then change to the `docs` directory, and run `sphinx-quickstart`. We suggest the following **non-default** configuration values (otherwise the default is fine):

* autodoc: automatically insert docstrings from modules (y/n): `y`
* mathjax: include math, rendered in the browser by MathJax (y/n): `y`
* githubpages: create .nojekyll file to publish the document on GitHub pages (y/n): `y` if using Github pages
