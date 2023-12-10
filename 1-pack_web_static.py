#!/usr/bin/python3
"""
Fabric script that generates .tgz archive from the contents of the web_static
"""


from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Create compressed .tgz file from web_static folder 
    Returns:
        str: path to the created archive if successful, else None
    """
    time_format = "%Y%m%d%H%M%S"
    now = datetime.now()
    timestamp = now.strftime(time_format)
    archive_path = "versions/web_static_{}.tgz".format(timestamp)

    try:
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        return None
