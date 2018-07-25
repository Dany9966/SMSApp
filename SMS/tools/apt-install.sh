#!/bin/sh
usage()
{
	echo "usage: apt-install.sh [-url URL] [-port PORT] [-vhost virtual_host] [-user User] [-password Password] [-time TimeInterval] [-cpu_used (true/false)] [-memory_used (true/false)]"
}

url='localhost'
port='5672'
vhost='/'
user='stackrabbit'
password='Passw0rd'
time_interval='7'
cpu_used="true"
memory_used="true"

# parameter handling

while [ "$1" != "" ] ; do
	case $1 in
		-url )				shift
							url=$1
							;;
		-port )				shift
							port=$1
							;;
		-vhost )			shift
							vhost=$1
							;;
		-user )				shift
							user=$1
							;;
		-password )			shift
							password=$1
							;;
		-time )				shift
							time_interval=$1
							;;
		-cpu_used )			shift
							cpu_used=$1
							;;
		-memory_used )		shift
							memory_used=$1
							;;
		-h | --help )		usage
							exit
							;;
		* )					usage
							exit 1
	esac
	shift
done

# conf file generation
sudo rm -rf $HOME/.local/SMS
mkdir $HOME/.local/SMS
SMS_dir=$HOME/.local/SMS
conf_path=$HOME/.local/SMS/SMS.conf
echo "" > $conf_path
echo "[db]" > $conf_path
echo "url = sqlite:///$SMS_dir/SMS.sqlite" >> $conf_path
echo "logging = false" >> $conf_path
echo "" >> $conf_path
echo "[amqp]" >> $conf_path
echo "url = $url" >> $conf_path
echo "port = $port" >> $conf_path
echo "vhost = $vhost" >> $conf_path
echo "user = $user" >> $conf_path
echo "password = $password" >> $conf_path
echo "" >> $conf_path
echo "[metrics]" >> $conf_path
echo "time_interval = $time_interval" >> $conf_path
echo "cpu_percentage_used = $cpu_used" >> $conf_path
echo "memory_used = $memory_used" >> $conf_path
echo "" >> $conf_path
echo "[log]" >> $conf_path
echo "debug = false" >> $conf_path
echo "console_log = false" >> $conf_path
echo "log_format = '[%(asctime)s] %(levelname)s - %(message)s'" >> $conf_path
echo "log_file = $SMS_dir/SMS.log" >> $conf_path

# installing dependencies first, then the application
# sudo apt-get update
script_path=`dirname $0`
cd $script_path/../..
# sudo apt-get install -y python python-dev python-pip rabbitmq-server screen
# sudo -H pip install --upgrade pip
# sudo -H pip install setuptools
sudo rabbitmqctl add_user $user $password
sudo rabbitmqctl set_permissions $user ".*" ".*" ".*"
sudo -H pip install .

# creating startup entry
# TODO

#running app
SMS_client --config-path $conf_path &