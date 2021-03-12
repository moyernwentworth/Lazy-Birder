#Read-me 

## what this will walk you through 
- createing two GCP storage buckets
- createing a MYSQL instance and database
- Automatically ingesting and migrating database
	- in the future processing it as well
- Setting up the Raspbery-Pi

# Step-1: set-up (disregard if connecting to existing project)
- Create 2 google cloud storage buckets, called input and processed
	- pick on time zone
- Create a MYSQL instance  
	- pick same time zone
- Create 2 python 3.7 google cloud functions (we'll fill later)
	- trigger one on upload to input bucket
	- trigger one on upload to processed bucket

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
	- reflect that in files

# Step-3: Setting-up Functions
- Add the google functions with the respective requirements into functions we created earlier 
	- process-image is trigger: upload to the input bucket
	- create-sql trigger: process-bucket upload
- write in sensative variables 
- Add the service account key file for you project 
	- after createing the addcout ad a json key file and copy it with the same name
	
# Step-4: checking in 
- After running watch4motion.py on the Raspbery-Pi you should start seeing:
	- images in the process-bucket
	- MYSQL entrees that link the the process-bucket image
	
# Step-5: issues
- contact me:
	- moyern@wit.edu

