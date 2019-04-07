# Flask Playground

- [Flask Tutorial](http://flask.pocoo.org/docs/1.0/tutorial/)

## Prerequisite

- Python 3.7 with `pyenv` 

```bash
# Mac Mojave hack
$ CFLAGS="-I$(xcrun --show-sdk-path)/usr/include" pyenv install 3.7.3
$ pyenv global 3.7.3

# Check installation 
$ pyenv versions
$ python --version
```

- Pipenv

```bash
$ pip install pipenv
```

## Run this project

```bash
$ git clone git@github.com:zoltan-nz/flask-playground.git
$ cd flask-playground
$ pipenv install
$ FLASK_APP=flaskr FLASK_ENV=development FLASK_DEBUG=1 flask run
```

## Development

Test:

```bash
$ pytest --cov=./flaskr
```

Lint:

```bash
$ pylint **/*.py
```

Format:

```bash
$ black **/*.py
```

## Initialize `pipenv` and `flask`

```
$ pipenv --python 3.7
$ pipenv install flask
```

Furthermore we can add the following useful packages for development.

```
$ pipenv install -d pytest black pylint pylint-flask tox tox-pipenv coverage pytest-cov --pre
```

The `black` package has only pre-release version. For this reason the `--pre` option should be used.

## Links

- [Pyenv](https://github.com/pyenv/pyenv)
- [Pipenv](https://docs.pipenv.org/en/latest/)
- [Flask](http://flask.pocoo.org/)
- [Pytest](https://docs.pytest.org/en/latest/)
- [Black](https://black.readthedocs.io/en/stable/)
- [Pylint](https://www.pylint.org/)
