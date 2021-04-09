I'm using python 3.8.2, doesn't really matter what you're using. Just a heads up. If you're on a *nix system though consider getting `pyenv`, allows you to download versions from command line as opposed to going to python.org blah blah blah.

First thing is to clone this and then in the top directory run:

`python -m venv env`

This will create a virtual environment folder in that directory that will be used to
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