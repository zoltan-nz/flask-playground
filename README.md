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
$ PIPENV_VENV_IN_PROJECT=1 pipenv run setup
$ pipenv run init-db-dev
$ pipenv run server-watch
```

## Development

Test:

```bash
$ pytest
```

Test with watch:

```
$ pipenv run test-watch
```

Lint:

```bash
$ pylint --load-plugins pylint_flask flaskr test
```

Format:

```bash
$ black **/*.py
```

## DX (Development Experience)

```
$ pipenv run test-watch
$ DEBUG=1 pipenv run app-watch
```

## Initialize `pipenv` and `flask`

```
$ pipenv --python 3.7
$ pipenv install flask
```

Furthermore we can add the following useful packages for development.

```
$ pipenv install -d pytest black pylint pylint-flask coverage pytest-cov pytest-testmon pytest-watch --pre
```

The `black` package has only pre-release version. For this reason the `--pre` option should be used.

## Configuration files

- `pylintrc`
- `setup.cfg`

## Add dotenv support

```
$ pipenv install python-dotenv
```

## Links

- [Pyenv](https://github.com/pyenv/pyenv)
- [Pipenv](https://docs.pipenv.org/en/latest/)
- [Flask](http://flask.pocoo.org/)
- [Pytest](https://docs.pytest.org/en/latest/)
- [Black](https://black.readthedocs.io/en/stable/)
- [Pylint](https://www.pylint.org/)
- [Flask extensions](https://nickjanetakis.com/blog/15-useful-flask-extensions-and-libraries-that-i-use-in-every-project)
- [Flask with MongoDB Tutorial](https://medium.com/@riken.mehta/full-stack-tutorial-flask-react-docker-420da3543c91)

## Heroku deployment notes

Building production package:

```
python setup.py bdist_wheel
```

It is required that `FLASK_APP=flaskr` environment variable being setup. Afterward the following CLI script can be run.

```
$ heroku run python3 -m flask init-db
```

## Run a Docker locally

0. Install Docker for Mac
1. Build the docker image: `flaskr:latest`.
2. Create a Volume for database. Volume name is `db`.
3. Initialize the database.
4. Run the image and attach the volume and bind a port.


```bash
$ pipenv run build-docker
$ docker volume create db
$ docker run -it -p 8080:8080 -v db:/home/app/db flaskr:latest flask init-db 
$ docker run -it -p 8080:8080 -v db:/home/app/db flaskr:latest
$ open http://localhost:8080
```

## Run Kubernetes locally (Instructions for Mac)

0. Install Docker for Mac.
1. Turn on Kubernetes support.
2. Check `kubectl` command availability.
3. Install `octant` for visibility.
4. Run deployment configuration.

```bash
$ brew install octant
$ octant
$ pipenv run deploy-kubernetes-local
$ open http://localhost:9090
```

## Gitlab CI notes

## Google Cloud Deployment notes

## Upgrading Python

When a new version of Python is installed (with `pyenv`) rebuild the virtual environment with running the following commands.

```bash
$ pipenv --rm
$ pipenv run setup
```
