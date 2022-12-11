# flask_weather


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

add city name first 


`curl --location --request POST 'http://localhost:5000/api/sub/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "city":"London"
}'`