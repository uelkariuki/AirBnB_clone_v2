#!/usr/bin/python3
"""
Write a Fabric script (based on the file 2-do_deploy_web_static.py)
that creates and distributes an archive to your web servers,
using the function deploy:
"""

from fabric.api import run, env, run, put, sudo, local
from datetime import datetime
from imported_pack_web_static import do_pack
from imported_do_deploy_web_static import do_deploy
""" Importing the required modules """

env.hosts = ["34.202.164.69", "100.25.41.114"]


def deploy():
    """
    Function that creates and distributes an archive to your web servers
    """

    created_archive = do_pack()

    if created_archive is None:
        return False

    return do_deploy(created_archive)
