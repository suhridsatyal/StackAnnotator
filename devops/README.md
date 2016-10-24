Deployment
-------------------------
Execute the following steps:

 - `docker pull ubuntu:16.04`
 - `cd devops; make`
 - `./deploy.sh`

To change settings (e.g. Access Tokens), enter the container's teminal with
following command:

`docker exec -i -t stackannotator /bin/bash`

For troubleshooting, check `Dockerfile`


Development Environment
-----------------------

**Pre-requisite**: The host needs to have essential libraries like `git` and `docker`.


**Setup**

 - `docker pull ubuntu:16.04`
 - `docker build -t comp9323/stackannotator .` 
 - `cd devops; make`
 - `./run-dev.sh`


**General Information**

 - Git repository on your host is mounted on the container at `/opt/StackAnnotator`.
 - Container exposes port 80 and 9000, these are mapped to host ports
   80 and 9000 respectively


Development Workflow
=====================

- Start the container

- Change code on your host.
  Use your keys to twitter, google, and stackoverflow in django and backbone
  setting files.

- Put the following line in `/etc/hosts`
  `127.0.1.1	stackannotator.com www.stackannotator.com`
  Then visit `stackannotator.com`.

- To work with django development server,
  run `stack_annotator/run_dev` inside container. Make sure that
  nginx service is stopped. 

- If you want to work on the front-end independently, go to
  `stack_annotator/assets` on your host, and execute `grunt serve`.
  If you want to serve frontend from the container, execute 
  `make` in `stack_annotator/assets` inside the container.
