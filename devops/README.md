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
 - `cd devops; make`
 - `./run-dev.sh`


**General Information**

 - Git repository on your host is mounted on the container at `/opt/StackAnnotator`.
 - Container exposes port 80 and 9000, these are mapped to host ports
   8000 and 9000 respectively


Development Workflow
--------------------

- Start the container
- Change code in your machine
- Perform general deployment operations inside container
  e.g. `grunt build`
- Visit `0.0.0.0:8000` to access the application.
  If you want to work with django development server,
  run `python manage.py runserver_plus` and visit `0.0.0.0:9000`


Troubleshooting
---------------
- > `0.0.0.0:8000` cannot be accessed.
  >> Inside the container, execute `service nginx start; supervisorctl start uwsgi`


TODOS
-----
- Postgres setup
- Mechanism for db backup restoration
- Upload image to docker registry

