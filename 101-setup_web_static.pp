# Redo the task #0 but by using Puppet

# check if nginx is installed
exec { 'install nginx':
  command => '/usr/bin/apt-get update && /usr/bin/apt-get install -y nginx',
  unless => '/usr/bin/which nginx',
}

# create directories
file { ['/data/', '/data/web_static/', '/data/web_static/releases/', '/data/web_static/shared/', '/data/web_static/releases/test/']:
  ensure => 'directory',
  owner => 'ubuntu',
  group => 'ubuntu',

}

# create a html file
file { '/data/web_static/releases/test/index.html':
  ensure => 'present',
  content => "<!DOCTYPE html>\n<html>\n<head>\n</head>\n<body>\nSchool\n</body>\n</html>"
}

# create symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test/',
}

# update nginx config
exec { 'nginx_config_update':
  command => "/bin/sed -i '/^\tlocation / i\\n\\tlocation /hbnb_static/ {\\n\\t\\talias /data/web_static/current/;\\n\\t}\\n' /etc/nginx/sites-available/default",
}

# restart nginx service
service { 'nginx':
  ensure => 'running',
  enable => true,
  subscribe => Exec['nginx_config_update'],
}
