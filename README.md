# flask_docker_ngiex


learning from this website
sudo docker-compose build
sudo docker-compose up
sudo docker-compose exec web python manage.py create_db
sudo docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev
\l
\dt
\q
sudo docker-compose exec web python manage.py seed_db
sudo docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev
select * from subscription;
\q