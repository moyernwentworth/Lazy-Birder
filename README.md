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
- Create 2 python 3.7 google cloud functions (we'll fill later) (4gb > of mem on creation)
	- trigger one on upload to input bucket
	- trigger one on upload to pre-processed bucket

# Step-2: Setting-up Raspbery-Pi
- Wire in components and attach camera 
	- have to enable SSH and camera module in rasp.config
	- wire PIR sensor to gpio 4 and 5v and ground
- Boot up latest version of Raspbery-Pi OS
- Set-up wifi
	- SSH into Raspbery-Pi
	- (optional) create a shared or network folder
- create a dir called scripts ('home/pi/scripts')
	- add the two script from the Raspbery-Pi folder 
	- change variables to reflect your project
- You will have to update some components depending on several things, errors will let you know what to pip install, working on requirements.txt for pi 
	- most-likey
		- Python
		- google
			- google-cloud-storage
- you must authenticate you Raspbery-Pi scripts by getting and storing a key.json file from the google console 
	- reflect that path in files
- Create an empty Dir ```mkdir website```
	- Initialize github in that folder
	- clone this project and switch the branch if not already on main ```git status``` then ```git checkout main``` to switch to the main branch
	- Follow that branches read me to set up the website 
	- After setting up the site on your raspberry pi you will need to run it differently and make one edit in your settings.py and several in views.py
	- Edit website paths for keys and file locations in views.py  
	- to run on local network from pi ```python manage.py runserver 0.0.0.0:8000```
		- to connect go to raspberyIP:8000 (or if you use a different port connect to that port)
		- you will see an error regarding allowed hosts
	- Edit settings.py in website, in ALLOWEDHOSTS = [] add 'raspberyIP'

# Step-3: Setting-up Functions
- Add the google functions with the respective requirements into functions we created earlier 
	- process-image triggered: upload to the output/processed bird bucket
	- bird-detect triggered: pre-process bucket upload
- write in sensative variables and add path to the needed files (you can place in any bucket and reference with gs://) 
- Add the service account key file for you project 
	- after createing the functions create a json key file and copy it with the same name into both projects to reference easily 
	
# Step-4: checking in 
- After running watch4motion.py on the Raspbery-Pi you should start seeing:
	- if the prints are commented out, you will see nothing
	- go to your input bucket to look at files, and you procceded-birds bucket to see if they classified 

# Step-5: run 24/7 (optional: set up crons) 
- run watch4motion.py and website code 24/7 
- ssh into raspbery pi type "crontab -l"
	- should see no jobs
- now type ```crontab -e```
	- enter the following lines
	- ```0 6 * * * /usr/bin/python3 /home/pi/scripts/watch4Motion.py >> ~/cron.log 2>&1```
	- ```* * * * * /usr/bin/env bash -c 'cd /home/pi/website/Lazy-Birder/lazy_birder && source /home/pi/website/Lazy-Birder/env/bin/activate && ./manage.py runserver 0.0.0.0:8000' >> ~/run.log 2>&1```
- Explanation
	- crons do not run prints correctly avoid them for anything other than trouble shooting
	- cron jobs are jobs you tell it to do at a specific time
	- the first line we add starts our watch4motion.py script at 6 in the morning (script should exit at 8pm) and prints any errors to cron.log
	- second cron enables the bash env shell so we can use commands, from here you source the venv you set up in Postautomation and run the server on the local host at port 8000 and prints errors to run.log

# Step-6: issues
- contact me:
	- moyern@wit.edu


