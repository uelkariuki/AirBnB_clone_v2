#!/usr/bin/python3
"""
 Fabric script that generates a .tgz archive from the contents of the
 web_static folder of your AirBnB Clone repo, using the function do_pack.
"""

from fabric.api import local
from datetime import datetime
""" Importing the required modules"""


def do_pack():
    """ Function to help to generate the archive"""

    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    hour = now.strftime("%H")
    minute = now.strftime("%M")
    second = now.strftime("%S")

    local("mkdir -p versions")

    archive_name = f"versions/web_static_{year}{month}{day}{hour}\
{minute}{second}.tgz"
    # capture the result
    result = local(f"tar -czvf {archive_name} web_static", capture=True)

    if result.failed:
        return None
    else:
        return archive_name
