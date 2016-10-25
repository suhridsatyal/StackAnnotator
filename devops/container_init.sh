#!/bin/bash
etc/init.d/postgresql start


cd /opt/StackAnnotator/stack_annotator/ && \
   python manage.py migrate && \
   python manage.py collectstatic --noinput

cd /opt/StackAnnotator/stack_annotator/assets/ && \
   make

cd /opt/StackAnnotator/

service nginx start
supervisord

# Ensure that container does not exit
/bin/bash
