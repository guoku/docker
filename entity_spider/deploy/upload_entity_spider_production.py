#!/usr/bin/env python


import ConfigParser
import os

from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.project import rsync_project

Config = ConfigParser.ConfigParser()
Config.read('config_production.ini')

root_dir = os.path.join(os.getcwd(), '..')

env.hosts = ['10.0.2.49']

env.user = Config.get('global', 'user')


env.local_root = os.path.join(root_dir, Config.get('local', 'project_dir'))
env.project_root = Config.get('server', 'project_dir')



@parallel
def upload_code():
    rsync_project(
            remote_dir = env.project_root,
            local_dir = env.local_root,
            delete = True,
            extra_opts = "--password-file='guoku.pass' ",
            exclude=['.git/*', 'images/*','*.jpg']
        )


def upload():
    execute(upload_code)


