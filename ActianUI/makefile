#define most important goal of the project
.DEFAULT_GOAL := RunScripts

#define vartiables - tho i dont really need this because i am not using the python command
PYTHON := python3.5

#create "target" nemed GrantPermission where dependencies are defined after : 
#and the "Recipe" or commands to execute are written in the tabbed lines below
#NOTE if you dont put the @, the recipe code will also print out
GrantPermissions: 
	@echo "======================================="
	@echo "======================================="
	@echo "Begin Build"
	@echo "======================================="
	@echo "======================================="
	@whoami
	@echo "granting permissions"
	@sudo chmod 777 /home/pi/Desktop
	@sudo chmod 777 /home/pi/Desktop/ActianUI/ActianUI/* #give psql user access to foo.jpg and to oldImages folder
	@sudo chmod +x ./home.py

	
RunScripts: GrantPermissions
	@echo "Running Scripts"
	@sh ./buildApp.sh
	#@su -l psql -c /home/pi/Desktop/ActianUI/ActianUI/home.py
	#@chromium-browser ./src/index.html
	#use the above live if you want to remove need for shell script



