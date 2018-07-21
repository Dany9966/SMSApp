sudo apt-get update
script_path=`dirname $0`
cd $script_path/../..
sudo apt-get install -y python python-dev python-pip rabbitmq-server
sudo -H pip install --upgrade pip
sudo -H pip install setuptools
sudo rabbitmqctl add_user stackrabbit Passw0rd
sudo rabbitmqctl set_permissions stackrabbit ".*" ".*" ".*"
sudo -H pip install -e .
