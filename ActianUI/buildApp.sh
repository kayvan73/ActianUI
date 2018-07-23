#!/bin/bash
whoami
path4=$(pwd)  #not sure why i have to do this outside of the sudo -s thing but
#if i dont then the variable will not save
echo 'correct path is: '
echo ${path4}
echo '-------------------'
#i dont know why but psql loses access to Desktop and files whenever i restart 
sudo -s <<word
echo $PATH
echo ----------------------------------------
echo ----------------------------------------
whoami
echo starting scripts
echo ----------------------------------------:
su - psql
cd ${path4}
pwd
./psql_api/PSQL_http_api.py
word
chromium-browser ./javascriptUI/index.html
