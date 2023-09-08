#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that
distributes an archive to your web servers, using the function do_deploy:
"""

from fabric.api import run, env, run, put

env.hosts = ['34.202.164.69', '100.25.41.114']


def do_deploy(archive_path):
    """ Function to help distributes an archive to the web servers"""

    try:
        with open(archive_path, 'r') as f:
            pass
    except FileNotFoundError:
        return False

    # Upload the archive to the /tmp/ directory of the web server
    put(archive_path, '/tmp/')

    # Uncompress the archive to the folder /data/web_static/releases/
    # <archive filename without extension> on the web server

    archive_filename = archive_path.split('/')[-1]
    archive_name = archive_filename.split('.')[0]

    run(f'mkdir -p /data/web_static/releases/{archive_name}')
    run(f'tar -xzf /tmp/{archive_filename} -C\
/data/web_static/releases/{archive_name}')
    # Delete the archive from the web server
    run(f'rm /tmp/{archive_filename}')

    # Delete the symbolic link /data/web_static/current from the web server
    sudo(f'rm -rf /data/web_static/current')

    # Create a new the symbolic link /data/web_static/current on the
    # web server linked to the new version of your code (/data/web_static/
    # releases/<archive filename without extension>)

    sudo(f'ln -s /data/web_static/releases/{archive_name}\
 /data/web_static/current')

    # Returns True if all operations have been done correctly,
    # otherwise returns False
    return True
