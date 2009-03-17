#!/bin/bash

apt-get install git-core python-pylons python-mako
mkdir -p /usr/share/linkhome
cp -a resources/example-menu/* /usr/share/linkhome
cp -a linkhome /usr/lib
