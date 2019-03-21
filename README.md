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

### requirements.txt

Add any python libraries which are requirements for your library to be used

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

We recommend building documentation using [sphinx](http://www.sphinx-doc.org/en/master/), and hosting documentation on [Github pages](https://pages.github.com/) or [read the docs](https://readthedocs.org/). Github pages is easier to configure, while read the docs will build automatically with each pushed commit.

To start the documentation structure, first install `sphinx` using conda or pip. Then change to the `docs` directory, and run `sphinx-quickstart`. We suggest the following **non-default** configuration values (otherwise the default is fine):

* autodoc: automatically insert docstrings from modules (y/n): `y`
* mathjax: include math, rendered in the browser by MathJax (y/n): `y`
* githubpages: create .nojekyll file to publish the document on GitHub pages (y/n): `y` if using Github pages

Note that the default format for writing code is [RestructuredText](http://docutils.sourceforge.net/rst.html), which is different than markdown (what is used in Github, and this readme). You can use [markdown with sphinx](https://www.sphinx-doc.org/en/master/usage/markdown.html).

There are other options for documenting code; the two most popular being [Asciidoctor](https://asciidoctor.org/) and [MkDocs](https://www.mkdocs.org/).

## Testing

Writing good tests is a learned art. People also have strong opinions on what makes good tests! Read some tutorials, learn about fixtures, try things out. Write unit tests, write integration tests, try TDD or BDD. Some tests are better than no tests, but no tests may be better than bad tests. 100% coverage is a journey, not a destination.

## Code quality checks

We strongly recommend using [pytest](https://docs.pytest.org/en/latest/) for testing. It is installable via conda or pip.

### pylama

[pylama](https://github.com/klen/pylama) is a collection of code quality checks which is easy to use. Just install via conda or pip, and then run `pylama <your_library_name>`. You can also run pylama on your tests with `pytest --pylama`.

## Continuous integration (CI)

The services listed here should already have permission to work with BONSAMURAIS repositories. If you are working on you own account, you will have to give permission for each service to read from GitHub. Don't worry, it is pretty simple, and there are normally good instructions.

CI testing requires that you have already written tests.

### Coveralls

Log in to https://coveralls.io/ with your GitHub account. Click on `Add Repos`, find your repository, and click on the slider button.

### Travis (Linux and MacOs)

Edit the file `.travis.yml`, and change following:

* `<add your conda dependencies here>`: Change this is a list of your conda dependencies, separated by spaces
* `<add any other dependencies not available in conda here>`: Change this to a list of dependencies not in conda, or delete this line
* `<your_library_name>`: Change as in `setup.py`

Edit the file `ci/requirements-travis.txt`, and copy everything from `requirements.txt` (but leave the testing libraries).

Log in using your GitHub account, and add the repository you want to test. Travis will now run on every pushed commit, and send coverage information to coveralls.

### Appveyor (Windows)

Edit the file `.appveyor.yml`, and change following:

* `<add your conda dependencies here>`: Change this is a list of your conda dependencies, separated by spaces
* `<add any other dependencies not available in conda here>`: Change this to a list of dependencies not in conda, or delete this line

Log in using your GitHub account, and add the repository you want to test. Then, click on settings, and change the `Custom configuration .yml file name` to `.appveyor.yml`. Appveyor will now run on every pushed commit.
