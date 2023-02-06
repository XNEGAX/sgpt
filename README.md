# sgpt
Sistema de gestion de proyectos de titulo

# RUN SERVER
docker-compose up --build


docker-compose run django_app python3 manage.py makemigrations
docker-compose run django_app python3 manage.py migrate
docker-compose run django_app python3 manage.py implementacion
