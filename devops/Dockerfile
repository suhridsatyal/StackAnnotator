FROM ubuntu:16.04


RUN apt-get update && apt-get install -y\
    sudo python python-dev python-pip build-essential python3-dev \
    postgresql postgresql-contrib libpq-dev \
    curl git-flow nginx tmux vim

RUN git clone https://github.com/suhridsatyal/StackAnnotator.git /opt/StackAnnotator 

RUN pip install --upgrade pip &&\
    pip install uwsgi &&\
    pip install -r /opt/StackAnnotator/devops/requirements.txt 

# Install npm dependencies
RUN curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash - 
RUN apt-get install -y nodejs  

RUN npm install -g bower grunt 
RUN cd /opt/StackAnnotator/stack_annotator/assets/ && \
    bower install --allow-root &&\ 
    npm install &&\
    grunt build &&\
    cd /opt/ 


# Create a PostgreSQL role named ``ubuntu`` with ``ubuntu`` as the password and
# then create a database `ubuntu` owned by the ``ubuntu`` role.
USER postgres
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER django WITH SUPERUSER PASSWORD 'django';" &&\
    createdb -O django django

USER root
RUN ln -sf /opt/StackAnnotator/devops/cmd_config/.vimrc ~/.vimrc

#Setup Nginx
RUN ln -sf /opt/StackAnnotator/devops/server_config/stackannotator_nginx.conf /etc/nginx/sites-enabled/default

# Setup uWSGI
RUN mkdir /etc/uwsgi &&\
    mkdir /etc/uwsgi/vassals &&\
    ln -sf /opt/StackAnnotator/devops/server_config/stackannotator_uwsgi.ini /etc/uwsgi/vassals/ &&\ 
    mkdir /var/log/uwsgi 

RUN pip install supervisor &&\
    ln -sf /opt/StackAnnotator/devops/server_config/supervisord.conf /etc/supervisord.conf

EXPOSE 80

CMD ["sudo service nginx start"]
CMD ["sudo supervisord"]
CMD ["/bin/bash"]
