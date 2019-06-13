FROM python:3-slim

RUN pip install --upgrade pip

RUN mkdir /home/app
RUN addgroup --gid 1024 app-group
RUN useradd --uid 1024 --gid 1024 --non-unique --comment "" --home-dir /home/app app
RUN chown 1024:1024 /home/app
RUN chmod 775 /home/app
RUN chmod g+s /home/app
WORKDIR /home/app
USER app

# Create a directory for the database and expose as a volume for persistence
RUN mkdir /home/app/db
RUN chown 1024:1024 /home/app/db
VOLUME /home/app/db

ARG flaskr_secret_key='rewrite this with docker run -e FLASKR_SECRET_KEY=realsecret'

ENV FLASK_APP=flaskr
ENV FLASK_ENV=production
ENV FLASKR_DATABASE_URI=/home/app/db/production.sqlite
ENV FLASKR_SECRET_KEY=$flaskr_secret_key

ENV PATH=/home/app/.local/bin:${PATH}

COPY requirements.txt ./requirements.txt
RUN pip install --user -r requirements.txt

COPY ./dist ./dist
RUN pip install --user ./dist/*

EXPOSE 8080

CMD ["waitress-serve", "--call", "flaskr:create_app"]