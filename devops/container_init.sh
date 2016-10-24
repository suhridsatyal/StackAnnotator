#!/bin/bash
service nginx start
supervisord
etc/init.d/postgresql start

# Ensure that container does not exit
/bin/bash
