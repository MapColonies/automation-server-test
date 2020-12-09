#!/bin/bash
#[ ! -d "docker_images" ] && echo "Creating new output directory for docker images" && [ mkdir "docker_images" ]

if [ -d "docker_images" ]
then
    echo "Directory docker_images exist and result will be saved to directory."
else
    echo "Creating new Directory docker_images, and result will be saved to directory."
    mkdir -p "docker_images"

fi

VERSION=$(python setup.py --version | sed 's/+/./g')
echo VERSION:$VERSION
docker build --no-cache -t automation-test:$VERSION --build-arg VERSION=$VERSION .
docker tag automation-test:$VERSION automation-test:latest

echo automation-test:$VERSION > ./docker_images/generated_dockers.txt
