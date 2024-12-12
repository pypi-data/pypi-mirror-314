# AWMT_BasicPythonPackage
Template for creating PyPI hosted python packages

This repo is intended to be used as a template for new AWMT python projects 

## Build Tools
Poetry was selected based on this article suggesting it has the best support and is most widely adopted:

https://www.pyopensci.org/python-package-guide/package-structure-code/python-package-build-tools.html

Repo structure has been adopted from Poetry docs here:

https://python-poetry.org/docs/basic-usage/#project-setup

Poetry can be installed as documented here:

https://python-poetry.org/docs/#installation

## Unit tests
Pytest has been chosen for unit testing based on its scalability and flexability for different applications - see here for more: https://builtin.com/data-science/pytest-vs-unittest

pytest can be installed using

```
pip install pytest
```

## Uploading to PyPI
Install twine using

```
pip install twine
```

Run the command

```
poetry build
```

Test upload to PyPI

```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```


Test install from PyPI

```
pip install -i https://test.pypi.org/simple/ AWMT_BasicPythonPackage
```

Full Upload to PyPI

```
twine upload dist/*
```

View Project

```
https://pypi.org/project/<package_name>
```

Full install

```
pip install <package_name>
```


