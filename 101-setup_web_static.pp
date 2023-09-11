# Redo the task #0 but by using Puppet

$nginx_config = "server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html;
    add_header X-Served-By ${hostname};
    server_name uelkariuki.tech;

    location /hbnb_static {
        alias /data/web_static/current/;
    }
    location /data/web_static/current/ {
        alias /data/web_static/current/;
    }
    location /redirect_me {
         return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }
    error_page 404 /404.html;
    location /404 {
        internal;
    }

}"
# check if nginx is installed
package { 'nginx':
  ensure => 'present',
  provider => 'apt'
} ->

# create directories
file { ['/data/', '/data/web_static/', '/data/web_static/releases/', '/data/web_static/shared/', '/data/web_static/releases/test/']:
  ensure => 'directory',
} ->

# create a html file
file { '/data/web_static/releases/test/index.html':
  ensure => 'present',
  content => "<!DOCTYPE html>\n<html>\n<head>\n</head>\n<body>\nSchool\n</body>\n</html>"
} ->

# create symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test/',
} ->

exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

file { '/var/www':
  ensure => 'directory'
} ->

file { '/var/www/html/index.html':
  ensure => 'present',
  content => "Holberton School \n"
} ->

file { '/var/www/html/404.html':
  ensure => 'present',
  content => "Ceci n'est pas une page\n"
} ->

file { '/etc/nginx/sites-available/default':
  ensure => 'present',
  content =>  $nginx_config
} ->

exec { 'nginx restart':
  path => '/etc/init.d/'
}
