#!/bin/bash

projectroot="${PWD%/*}"
docker run --rm -it -p 80:80 -p 9000:9000 -v $projectroot:/opt/StackAnnotator comp9323/stackannotator 
#/bin/bash -c 'cd /opt/StackAnnotator; exec /bin/bash' 
