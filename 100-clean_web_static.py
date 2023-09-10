#!/usr/bin/python3

"""
Write a Fabric script (based on the file 2-do_deploy_web_static.py)
that creates and distributes an archive to your web servers,
using the function deploy:
"""

from fabric.api import run, env, run, put, sudo, local
from datetime import datetime
import os
from imported_pack_web_static import do_pack
from imported_do_deploy_web_static import do_deploy
""" Importing the required modules """

env.hosts = ["34.202.164.69", "100.25.41.114"]


def deploy():
    """
    Function that creates and distributes an archive to your web servers
    """
    created_archive = os.getenv('created_archive', None)
    if created_archive is None:
        created_archive = do_pack()
        os.environ['created_archive'] = created_archive
        return False

    return do_deploy(created_archive)


"""
Fabric script (based on the file 3-deploy_web_static.py) that deletes
out-of-date archives, using the function do_clean:
"""


def do_clean(number=0):
    """
    Function that deletes out-of-date archives
    Args:
    number: is the number of the archives, including the most recent, to keep.
    """

    number = int(number)
    # keep at least one version if the number is less than 1

    if number < 1:
        number = 1

    # Add 1 to exclude the most recent version
    number = number + 1

    # Delete old versions  in versions folder
    local(f'ls -1t versions | tail -n +{number} | xargs rm -f --')

    run(f'ls -1t /data/web_static/releases | tail -n +{number}\
        | xargs rm -f --')
