#!/usr/bin/python3

"""
Write a Fabric script (based on the file 2-do_deploy_web_static.py)
that creates and distributes an archive to your web servers,
using the function deploy:
"""

from fabric.api import run, env, run, put, sudo, local
from datetime import datetime
import re
import os
from imported_pack_web_static import do_pack
from imported_do_deploy_web_static import do_deploy
""" Importing the required modules"""

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

    number = 1 if number <= 1 else number
    path_Release = '/data/web_static/releases/'

    archive_left = os.getenv('archive_left', None)

    if archive_left is None:
        versions = [
                re.findall(r'\d+', version)[0] for version in
                os.listdir('./versions')]

        archive_left = '|'.join(sorted(versions)[-number:])

        os.environ['archive_left'] = archive_left

        local((
            "find {} -maxdepth 1 -name \"{}\" " +
            "-type d | grep -Ev \"{}\" | xargs rm -rf").format(
            path_Release, "web_static*", archive_left))

        local((
            "find versions -maxdepth 1 -name" +
            " \"{}\" -type f | grep -Ev \"{}\" | xargs rm -rf").format(
                "web_static*", archive_left))

    run((
        "find {} -maxdepth 1 -name \"{}\" " +
        "-type d | grep -Ev \"{}\" | xargs rm -rf").format(
        path_Release, "web_static*", archive_left))
