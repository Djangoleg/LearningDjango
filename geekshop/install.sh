#!/bin/bash
base_python_interpreter=""
project_domain=""
project_path=`pwd`

read -p "Python interpreter: " base_python_interpreter
read -p "Your domain without protocol (for example, google.com): " project_domain
`$base_python_interpreter -m venv env`
source env/bin/activate
pip install -U pip
pip install -r requirements.txt

sed -i "s~dbms_template_path~$project_path~g" nginx/site.conf systemd/gunicorn.service
sed -i "s~dbms_template_domain~$project_domain~g" nginx/site.conf src/config/settings.py

# Check and create dirs.
nginx_dir="/etc/nginx/sites-enabled/";
if ! [[ -d $nginx_dir ]]
then
  sudo mkdir $nginx_dir
fi

system_dir="/etc/systemd/system/";
if ! [[ -d $system_dir ]]
then
  sudo mkdir $system_dir
fi

sudo ln -s $project_path/nginx/site.conf $nginx_dir
sudo ln -s $project_path/systemd/gunicorn.service $system_dir

sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo service nginx restart
