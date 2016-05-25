#!/bin/bash

python3 tests/crosstag_api_tests.py

while true; do
echo "Do you want to continue to deploy to docker? y/n"
read answer

if [ "$answer" == "y" ]; then
   break
elif [ "$answer" == "n" ]; then
  echo "Exiting bash script!"
  exit
else
  echo "Could not read the input, try again!"
fi
done

echo "Logging in to docker cloud!"
echo -n "Enter username for docker: "
read username

echo -n "Enter password for docker: "
stty -echo
read password
stty echo

# Login to docker
repo="crosstag/crosstag"
tag="latest"
version="1.2"
sudo docker login -u="$username" -p="$password"
sudo docker build -f Dockerfile -t "$repo:$version" .
sudo docker tag "$repo:$version" "$repo:$tag"
sudo docker push "$repo"
echo "Deployment finished"
