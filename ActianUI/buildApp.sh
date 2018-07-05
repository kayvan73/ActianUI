whoami
#i dont know why but psql loses access to Desktop and files whenever i restart 
sudo -s <<word
echo ----------------------------------------
echo ----------------------------------------
whoami
echo starting scripts
echo ----------------------------------------
su - psql
python3 /home/pi/Desktop/ActianUI/ActianUI/home.py &
word
chromium-browser ./src/index.html
