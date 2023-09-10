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

    # keep at least one version if the number is less than 1
    number = 1 if int(number) == 0 else int(number)

    present_archives = sorted(os.listdir("versions"))

    [present_archives.pop() for q in range(number)]

    with lcd("versions"):
        [local(f'rm ./{arch}') for arch in present_archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [arch for arch in archives if "web_static_" in arch]

        [archives.pop() for q in range(number)]

        [run(f'rm -rf ./{arch}') for arch in archives]
