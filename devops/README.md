Docker container setup
----------------------

Test, Demo, or Production
-------------------------
`TODO`

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
--------------------

- Start the container

- Change code on your host

- Perform general deployment operations inside container
  e.g. `make`, `python manage.py collectstatic`

- Put the following line in `/etc/hosts`
  `127.0.1.1	stackannotator.com www.stackannotator.com`
  Then visit `stackannotator.com`.

- If you want to work with django development server,
  run `stack_annotator/run_dev` inside container. Make sure that
  nginx service is stopped. Using dev server is essential if you
  want to work with front-end independently on your host.

- If you want to work on the front-end independently, go to
  `stack_annotator/assets` on your host, and execute `grunt serve`.


Troubleshooting
---------------
1. Application at **`0.0.0.0:8000` cannot be accessed.**
     
    Inside the container, execute `supervisord` then `service nginx start`


TODOS
-----
- Postgres setup
- Mechanism for db backup restoration
- Upload image to docker registry

