#!/bin/bash

apt-get install git-core python-pylons python-mako
mkdir -p /usr/share/linkhome
cp -a example-menu/* /usr/share/linkhome
