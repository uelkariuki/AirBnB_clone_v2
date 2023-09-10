#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that
distributes an archive to your web servers, using the function do_deploy:
"""

from fabric.api import run, env, run, put, sudo, local
import os.path
""" Importing the required modules"""

env.hosts = ["34.202.164.69", "100.25.41.114"]


def do_deploy(archive_path):
    """ Function to help distributes an archive to the web servers"""

    # check if the codde is running locally or on remote hosts
    local_running = os.getenv("runned_locally", None)
    if local_running is None:
        # code for running locally (before deployment to the remote hosts)

        if os.path.isfile(archive_path) is False:
            return False
        # set the runned_locally environment variable to prevent running
        # these commands again on remote hosts
        os.environ["runned_locally"] = "True"
    # Uncompress the archive to the folder /data/web_static/releases/
    # <archive filename without extension> on the web server
    archive_filename = os.path.basename(archive_path)
    archive_name = os.path.splitext(archive_filename)[0]

    # Upload the archive to the /tmp/ directory of the web server

    if put(archive_path, f'/tmp/{archive_filename}').failed is True:
        return False
    if run(f'rm -rf /data/web_static/releases/{archive_name}/').failed is True:
        return False
    if run(f'mkdir -p /data/web_static/releases/{archive_name}/')\
       .failed is True:
        return False
    if run(f'tar -xzf /tmp/{archive_filename} -C\
 /data/web_static/releases/{archive_name}/').failed is True:
        return False
    # Delete the archive from the web server
    if run(f'rm /tmp/{archive_filename}').failed is True:
        return False

    if run(f'mv /data/web_static/releases/{archive_name}/web_static/* '
           f'/data/web_static/releases/{archive_name}/').failed is True:
        return False

    if run(f'rm -rf /data/web_static/releases/{archive_name}/web_static/* ')\
       .failed is True:
        return False
    # Delete the symbolic link /data/web_static/current from the web server
    if run(f'rm -rf /data/web_static/current').failed is True:
        return False

    # Create a new the symbolic link /data/web_static/current on the
    # web server linked to the new version of your code (/data/web_static/
    # releases/<archive filename without extension>)

    if run(f'ln -s /data/web_static/releases/{archive_name}/\
 /data/web_static/current').failed is True:
        return False

    # Returns True if all operations have been done correctly,
    # otherwise returns False
    return True
