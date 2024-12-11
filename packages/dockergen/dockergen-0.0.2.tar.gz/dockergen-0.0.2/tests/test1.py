
import sys
from dockergen import Gen, Mount

from typing import List

g = Gen()
g.from_('nvidia/cuda:11.1-devel-ubuntu20.04', platform='linux/amd64')
g.label(maintainer='Example User <foo@example.com>')
g.run(['apt-get update -yq', 'apt-get install wget gcc'])
g.run(['cp /opt/foo.txt foo.txt'], mount=Mount(from_='build1', source='/build', target='/opt'))
g.run(['cp /opt/foo.txt foo.txt'], mount=[
    Mount(from_='build1', source='/build', target='/opt'),
    Mount(from_='build1', source='/build2', target='/opt2')])

g.write(sys.stdout)
