Docker container setup
----------------------

The host needs to have essential libraries like
`git` and `docker`.

To install this app's docker container, first pull ubuntu image:
`docker pull ubuntu:16.04`

Then, build the application container:
`make`

Then, run `./docker-run.sh` to start a development container.
This script takes care of setting up the development environment.
It installs all essential libraries in container, and configures the
application to run.
The repository on your host will be mounted in docker. Therefore,
you can code in your host, and test it inside the container.
After running this command, you will be able access command line of
the container. Here, you will be able to use tmux.
