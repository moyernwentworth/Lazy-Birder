#Read-me 

## what this will walk you through 
- createing two GCP storage buckets
- createing a MYSQL instance and database
- Automatically ingesting and migrating database
	- in the future processing it as well
- Setting up the Raspbery-Pi

# Step-1: set-up (disregard if connecting to existing project)
- Create 3 google cloud storage buckets, called input, pre-process and processed
	- pick on time zone
- Create 2 python 3.7 google cloud functions (we'll fill later)
	- trigger one on upload to input bucket
	- trigger one on upload to pre-processed bucket

# Step-2: Setting-up Raspbery-Pi
- Wire in components and attach camera 
	- have to enable SSH and camera module in rasp.config
- Boot up latest version of Raspbery-Pi OS
- Set-up wifi
	- SSH into Raspbery-Pi
	- (optional) create a shared or network folder
- create a dir called scripts ('home/pi/scripts')
	- add the two script from the Raspbery-Pi folder 
	- change variable to reflect project
- You will have to update some components depending on several things
	- most-likey
		- Python
		- google
			- this will let you know which pip to use with the script
- you must authenticate you Raspbery-Pi by getting and storing a key file 
	- reflect that path in files
- Create an empty Dir "mkdir website"
	- Initialize git hub in that folder
	- clone this project and switch branch ```git checkout Postautomation``` to the PostAutomation branch
	- Follow that branches read me to set up the website 
	- After setting up the site on your raspberry pi you will need to run it differently and make one edit in your settings.py 
	- to run on local network from pi ```python manage.py runserver 0.0.0.0:8000```
		- to connect go to raspberyIP:8000 (or if you use a different port connect to that port)
		- you will see an error regarding allowed hosts
	- Edit settings.py in website, in ALLOWEDHOSTS = [] add 'raspberyIP'
	- Edit website paths for keys and file locations in views.py  

# Step-3: Setting-up Functions
- Add the google functions with the respective requirements into functions we created earlier 
	- process-image is trigger: upload to the input bucket
	- bird-detect: pre-process bucket upload
- write in sensative variables and add path to the needed files (you can place in any bucket and reference) 
- Add the service account key file for you project 
	- after createing the addcout ad a json key file and copy it with the same name
	
# Step-4: checking in 
- After running watch4motion.py on the Raspbery-Pi you should start seeing:
	- images in the process-bucket
	- MYSQL entrees that link the the process-bucket image
	
# Step-5: issues
- contact me:
	- moyern@wit.edu

# Step-6: run 24/7 (optional: set up crons)
- run watch4motion.py and website code 24/7 
- ssh into raspbery pi type "crontab -l"
	- should see no jobs
- now type "crontab -e"
	- enter the following lines
	- ```0 6 * * * /usr/bin/python3 /home/pi/scripts/watch4Motion.py >> ~/cron.log 2>&1```
	- ```* * * * * /usr/bin/env bash -c 'cd /home/pi/website/Lazy-Birder/lazy_birder && source /home/pi/website/env/bin/activate && ./manage.py runserver 0.0.0.0:8000' >> ~/run.log 2>&1```
- Explanation
	- cron jobs are jobs you tell it to do at a specific time
	- the first line we add starts our watch4motion.py script at 6 in the morning (script should exit at 8pm) and prints any errors to cron.log
	- second cron enables the bash env shell so we can use commands, from here you source the venv you set up in Postautomation and run the server on the local host at port 8000
