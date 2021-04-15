# Lazy Birder
This project was created by two undergraduate computer science students for a senior project class. The overarching goal is to have users learn more about the birds in their backyard. Lazy Birder is a unique application consisting of a connected network of hardware and software components which classifies birds, by species, that visit your home. This process is initialized when a bird comes to your bird feeder, specifically one that is suction-cupped to a window in your home. While gathering seed, a Raspberry Pi computer detects motion and takes a picture of the bird. This image is then sent to a Google Cloud instance where it is classified using a Keras-based machine-learning model. Upon classification, this image and associated metadata is sent to a locally-hosted Django website. Here, a post is created for the appropriate user which consists of the image, date, and species name. Users can view the birds that have recently visited their feeder, as well as learn what kind of seed each species likes the most. The result is a robust application which consists of multiple efficient and effective parts which can classify twenty bird species with an eighty-percent accuracy.


## Website Setup
This process will eventually be replaced by a startup script, but for now here are instructions.

The first thing you want to do is to create a virtual environment with our project's dependicies. `cd` into the directory in which you cloned this repo. The run

`python -m venv env` or `python3 -m venv venv`

This will create a virtual environment folder named `venv`, in that directory that will be used to
control package versions and python version. On *nix systems, run 

`source venv/bin/activate`

or on windows

`.\venv\Scripts\Activate.ps1`

if windows yells at you come find me, have to run a command in poweshell in admin mode if you're feeling independent, run a quick google search. Once this env is fired up you'll see '(env)' on the command line next to your prompt. Good job. Next run the ol'

`pip install -r requirements.txt`

make sure you add path to that .txt file if need be. This will install all necessities to the virtual environemnt so the website will be good to go (Django rn and its package dependicies). From here we need to target that highest level `manage.py` file, the one directly within the `Udemy-Project folder`. So run 

`python manage.py runserver`

and now the site is locally served on port 8000. Open up chrome to try it out. Open the `urls.py` file in `dashbird` directory and add the first argument in each list item to get to a new page. If you have any questions come find me. Crtl + C will stop serving the site and `deactivate` will stop the virtual environment. 

Password reset stuff
you must enter the email that is currently logged in in order to send the change email 
you must also go into your google settings and allow less secure app access in order to send
probably best to turn that off after

Images go in new folder, get moved to old

## Adding Additional Bird Species to the Model