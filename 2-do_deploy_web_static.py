#!/usr/bin/python3
"""
Fabric Script to distribute an archive to web servers
"""


from fabric.api import env, put, run
from os.path import exists

env.host = ['3.85.1.161', '100.26.178.134']
env.user = 'ubuntu'

def do_deploy(archive_path):
    """
    Distribute an archive to web servers
    """
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split("/")[-1]
        ext_file = archive_name.split(".")[0]

        put(archive_path, "/tmp/{}".format(archive_name))
        run("mkdir -p /data/web_static/releases/{}/".format(ext_file))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
                .format(archive_name, ext_file))
        run("rm /tmp/{}".format(archive_name))
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/"
                .format(ext_file, ext_file))
        run("rm -rf /data/web_static/releases/{}/web_static".format(ext_file))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
                .format(ext_file))
        return True
    except Exception:
        return False
