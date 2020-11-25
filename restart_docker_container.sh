echo "stopping all existing docker containers."
sudo docker stop $(sudo docker ps -a -q)

echo "removing all stopped docker containers."
sudo docker rm $(sudo docker ps -a -q)

echo "starting the mysql docker container."
sudo docker run -p 3306:3306 --name mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql

echo "wait 30 seconds to let the sql server start."
sleep 30

echo "creating database \"cs6400\" in docker container."
sudo docker exec -i $(sudo docker ps -a -q) /usr/bin/mysql -u root --password=123456 -e "CREATE DATABASE IF NOT EXISTS cs6400"

echo "restoring database from backup."
cat backup.sql | sudo docker exec -i $(sudo docker ps -a -q) /usr/bin/mysql -u root --password=123456 cs6400
