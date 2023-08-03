# Teenwork Readme

### Local Build
You can just run `python manage.py runserver 0.0.0.0:80` for running on 80 port or `python manage.py runserver` for running on 8000 port

### Docker build
The best practice is using production mode (below)
- build docker image (production) `docker-compose build` or `docker-compose -f docker-compose.yml build`
- start docker container (production) `docker-compose up` or `docker-compose -f docker-compose.yml up`
- execute commands in container `docker-compose exec [service-name] [command]`, for example: `docker-compose exec server python manage.py createsuperuser`

[Dockerization resource - backend](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)
[Dockerization resource - frontend](https://mherman.org/blog/dockerizing-a-react-app/)