# Flask Playground

- [Flask Tutorial](http://flask.pocoo.org/docs/1.0/tutorial/)

## Prerequisite

- Python 3.7 with `pyenv`
- Pipenv

## Initialize `pipenv` and `flask`

```
$ pipenv --python 3.7
$ pipenv install flask
```

Furthermore we can add the following useful packages for development.

```
$ pipenv install -d pytest black pylint --pre
```

The `black` package has only pre-release version. For this reason the `--pre` option should be used.

## Links

- [Pyenv](https://github.com/pyenv/pyenv)
- [Pipenv](https://docs.pipenv.org/en/latest/)
- [Flask](http://flask.pocoo.org/)
- [Pytest](https://docs.pytest.org/en/latest/)
- [Black](https://black.readthedocs.io/en/stable/)
- [Pylint](https://www.pylint.org/)
