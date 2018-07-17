sudo apt-get install python python-dev python-pip rabbitmq-server
sudo -H pip install --upgrade pip
sudo -H pip install setuptools
sudo rabbitmqctl add_user stackrabbit Passw0rd
sudo rabbitmqctl set_permissions stackrabbit ".*" ".*" ".*"