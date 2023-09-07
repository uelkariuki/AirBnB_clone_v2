#!/usr/bin/env bash
# Bash script that sets up my web servers for the deployment of web_static

# check if Nginx is installed
if ! [ -x "$(command -v nginx)" ]; then
  sudo apt-get update
  sudo apt-get install -y nginx
fi

# create /data/ folder if it does not already exist
if [ ! -d "/data/" ]; then
  sudo mkdir /data/
fi

# Create the folder /data/web_static/ if it doesn’t already exist
if [ ! -d "/data/web_static/" ]; then
sudo mkdir /data/web_static/
fi

# Create the folder /data/web_static/releases/ if it doesn’t already exist
if [ ! -d "/data/web_static/releases/" ]; then
sudo mkdir /data/web_static/releases/
fi

# Create the folder /data/web_static/shared/ if it doesn’t already exist
if [ ! -d "/data/web_static/shared/" ]; then
sudo mkdir /data/web_static/shared/
fi

# Create the folder /data/web_static/releases/test/ if it doesn’t already exist
if [ ! -d "/data/web_static/releases/test/" ]; then
sudo mkdir /data/web_static/releases/test/
fi

# Create a fake HTML file /data/web_static/releases/test/index.html
# (with simple content, to test your Nginx configuration)

sudo mkdir -p /data/web_static/releases/test/

cat > /data/web_static/releases/test/index.html <<EOL
<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    School
  </body>
</html>
EOL

# sudo chown -R www-data:www-data /data/web_static/releases/

# Create a symbolic link /data/web_static/current linked to the
# /data/web_static/releases/test/ folder. If the symbolic link already exists,
# it should be deleted and recreated every time the script is ran.
ln -sf /data/web_static/releases/test /data/web_static/current
sudo rm -rf /data/web_static/releases/test/test
# Give ownership of the /data/ folder to the ubuntu user AND group (you can assume this user and group exist).
# This should be recursive; everything inside should be created/owned by this user/group.
sudo chown -R ubuntu:ubuntu /data/

sudo sed -i '/^\tlocation \/ {/i \\tlocation \/hbnb_static\/ {\n\t\talias \/data\/web_static\/current\/;\n\t}\n' /etc/nginx/sites-available/default

exit 0
