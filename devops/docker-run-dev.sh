#!/bin/bash

projectroot="${PWD%/*}"
docker run --rm -it -v $projectroot:/opt/StackAnnotator comp9323/stackannotator /bin/bash -c 'cd /opt/StackAnnotator; exec /bin/bash' 
