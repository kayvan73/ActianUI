whoami
#i dont know why but psql loses access to Desktop and files whenever i restart 
sudo -s <<word
echo ----------------------------------------
echo ----------------------------------------
whoami
echo starting scripts
echo ----------------------------------------
su - psql
python3 ./psql_api/PSQL_http_api.py
word
chromium-browser ./javascriptUI/index.html
