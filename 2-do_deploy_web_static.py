#!/usr/bin/python3
"""
Fabric Script to distribute an archive to web servers
"""


from fabric.api import env, put, run
from os.path import exists
from datetime import datetime

env.host = ['3.85.1.161', '100.26.178.134']
env.user = 'ubuntu'
env.key_file = '~/.ssh/school'

def do_deploy(archive_path):
    """
    Distribute an archive to web servers
    """
    if not exists(archive_path):
        return False

    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_file = "web_static_{}.tgz".format(timestamp)

        put(archive_path, "/tmp/{}".format(archive_file))
        run("mkdir -p /data/web_static/releases/{}/".format(archive_file[:-4]))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
                .format(archive_file, archive_file[:-4]))
        run("rm /tmp/{}".format(archive_file))
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/"
                .format(archive_file[:-4], archive_file[:-4]))
        run("rm -rf /data/web_static/releases/{}/web_static".format(archive_file[:-4]))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
                .format(archive_file[:-4]))
        return True
    except Exception:
        return False
