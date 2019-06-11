FROM zoltannz/python-with-gcloud

RUN mkdir /home/app
RUN useradd -d /home/app app
RUN chown app: /home/app
WORKDIR /home/app
USER app

ENV PATH=/home/app/.local/bin:$PATH

ENV CI_PROJECT_DIR=/home/app
ENV PIP_CACHE_DIR=$CI_PROJECT_DIR/.cache/pip
ENV PIPENV_CACHE_DIR=$CI_PROJECT_DIR/.cache/pipenv
ENV PIPENV_VENV_IN_PROJECT=1
ENV LANG="en_NZ.UTF-8"
ENV LC_ALL="en_NZ.UTF-8"
ENV FLASK_APP=flaskr
ENV FLASK_ENV=production
ENV DEBUG=0

RUN pip install --user pipenv

COPY . .

# Tasks
RUN pipenv run setup
RUN pipenv run lint
RUN pipenv run test
RUN pipenv run cov-report
USER root