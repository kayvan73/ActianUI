#!/bin/bash
whoami
path4=$(pwd)  #not sure why i have to do this outside of the sudo -s thing but
#if i dont then the variable will not save
#echo 'correct path is: '
#echo ${path4}
#echo '-------------------'
#i dont know why but psql loses access to Desktop and files whenever i restart 
sudo -s <<word
#echo $PATH
echo ----------------------------------------
echo ----------------------------------------
whoami
echo starting scripts
echo ----------------------------------------:
su - psql
cd ${path4}
pwd
${path4}/psql_api/PSQL_http_api.py &  #directly execute the python-psql api
#switching to psql user changes the direcotry, so I have to store the correct absolute path
#and then send it after user change

#also - note how i have to cd AND use absolute path. i cd otherwise the python script will be in wring folder and i run absolute otherwise i get error
word
chromium-browser ./javascriptUI/index.html
