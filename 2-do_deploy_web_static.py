#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that
distributes an archive to your web servers, using the function do_deploy:
"""

from fabric.api import run, env, run, put, sudo, local
from fabric.contrib import files
import os.path
""" Importing the required modules"""

env.hosts = ["34.202.164.69", "100.25.41.114"]


def do_deploy(archive_path):
    """ Function to help distributes an archive to the web servers"""

    if os.path.isfile(archive_path) is False:
        return False

    # Uncompress the archive to the folder /data/web_static/releases/
    # <archive filename without extension> on the web server
    archive_filename = archive_path.split("/")[-1]
    archive_name = archive_filename.split(".")[0]
    # Upload the archive to the /tmp/ directory of the web server

    path_archive_name = f'/data/web_static/releases/{archive_name}'
    if put(archive_path, f'/tmp/{archive_filename}').failed is True:
        return False
    # if run(f'sudo rm -rf /data/web_static/releases/\
    # {archive_name}/').failed is True:
    # return False
    if run(f'mkdir -p {path_archive_name}').failed is True:
        return False
    if run(f'tar -xzf /tmp/{archive_filename} -C {path_archive_name}/').failed is True:
        return False
    # Delete the archive from the web server
    if run(f'sudo rm /tmp/{archive_filename}').failed is True:
        return False

    if files.exists(path_archive_name) is False:
        if run(f'mv {path_archive_name}/web_static/* {path_archive_name}/').failed is True:
            return False

    if run(f'sudo rm -rf {path_archive_name}/web_static').failed is True:
        return False
    # Delete the symbolic link /data/web_static/current from the web server
    if run(f'sudo rm -rf /data/web_static/current').failed is True:
        return False

    # Create a new the symbolic link /data/web_static/current on the
    # web server linked to the new version of your code (/data/web_static/
    # releases/<archive filename without extension>)

    if run(f'sudo ln -s {path_archive_name}/ /data/web_static/current').failed is True:
        return False

    print("New version deployed!")
    # Returns True if all operations have been done correctly,
    # otherwise returns False
    return True
