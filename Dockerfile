FROM python:3-slim

RUN mkdir /home/app
RUN useradd -d /home/app app
RUN chown app: /home/app
WORKDIR /home/app
USER app

ENV FLASK_APP=flaskr
ENV FLASK_ENV=production
ENV FLASKR_DATABASE_URI=/home/app/db
# ENV FLASKR_SECRET_KEY=

# Database can be stored an external volume
VOLUME /home/app/db

ENV PATH=/home/app/.local/bin:${PATH}

COPY requirements.txt ./requirements.txt
RUN pip install --user -r requirements.txt

COPY ./dist ./dist
RUN pip install --user ./dist/*

EXPOSE 8080

RUN flask init-db-prod
CMD ["waitress-serve", "--call", "flaskr:create_app"]