#!/bin/bash
echo CLEANUP..
git reset --hard
git pull
cd ..
sudo chown ubuntu:www-data . -R
sudo chmod +x . -R
sudo service tmdt restart
echo DONE
