# Lazy Birder
This project was created by two undergraduate computer science students for a senior project class. The overarching goal is to have users learn more about the birds in their backyard. Lazy Birder is a unique application consisting of a connected network of hardware and software components which classifies birds, by species, that visit your home. This process is initialized when a bird comes to your bird feeder, specifically one that is suction-cupped to a window in your home. While gathering seed, a Raspberry Pi computer detects motion and takes a picture of the bird. This image is then sent to a Google Cloud instance where it is classified using a Keras-based machine-learning model and YOLO object detection. Upon classification, this image and associated metadata is sent to a locally-hosted Django website. Here, a post is created for the appropriate user which consists of the image, date, and species name. Users can view the birds that have recently visited their feeder, as well as learn what kind of seed each species likes the most. The result is a robust application which consists of multiple efficient and effective parts which can classify twenty bird species with an eighty-percent accuracy.


## Website Setup
This process will eventually be replaced by a startup script, but for now here are instructions.

You can run this site locally on your local computer, or run it locally on the raspberry pi that is taking the images.

The first thing you want to do is to create a virtual environment with our project's dependicies. `cd` into the directory in which you cloned this repo. Then run

`python -m venv env` or `python3 -m venv venv`

This will create a virtual environment folder named `venv`, that directory will be used to control package versions and python version. On *nix systems, run 

`source venv/bin/activate`

or on windows

`.\venv\Scripts\Activate.ps1`

After this command you should see a small `(venv)` pop up on the terminal line indicating you are in the virtual
environment. Once in the environment run the following:

`pip install -r requirements.txt`

make sure you add the path to that .txt file if need be. This will install all necessities to the virtual environemnt so the website will be good to go. From here we need to target that `manage.py` file, the one directly within the `Lazy-Birder` folder. So run 

`python path/to/manage.py runserver`

and now the site is locally served on port 8000. Open up a web browser to try it out. Crtl + C will stop serving the site and `deactivate` will stop the virtual environment. 

You will also have to update the `views.py` file located within the `dashbird` app. 
Here you will have to change the `json_credentials_path` to lead to your copy of the gcp key file.
You will also have to alter the `destination_file_name` and `old_file_name` to point to the `new` and `old` 
folder you create within `Lazy-Birder/lazy_birder/media/USERNAME` folder. 

Now upon refresh at localhost:8000/bird-posts/ you should see your bird posts!
## Adding Additional Bird Species to the Model

We initially pass the images through a YOLO object detection model that is housed within the google cloud instance. This shouldn't have to be altered, but if you want to do any tweaking, that is where it exists. As far as the bird species themselves we currently support the following 20 for classification:

1. Black-Capped Chickadee
2. Nothern Cardinal
3. Crow
4. American Goldfinch
5. Baltimore Oriole
6. Chipping Sparrow
7. Common Grackle
8. Common Starling
9. Dark-eyed Junco
10. Downy Woodpecker
11. Eastern Bluebird
12. Gary Catbird
13. House Finch
14. House Sparrow
15. Mourning Dove
16. Northern Flicker
17. Purple Finch
18. Red-Headed Woodpecker
19. Red-winged Blackbird
20. Titmouse

The model itself can be viewed in Google Collab [here](https://colab.research.google.com/drive/100PuqHGiwl6Ii7cHvhAnM17dI2dNnx1r?usp=sharing) and the associated h5 file is [here](https://drive.google.com/file/d/1-4lc0EVuAF9CMc5Md6LHbXyVVVXaQ3YK/view?usp=sharing). If you want to add additional species, the process is rather simple. Simply gather 200 images of the desired species and place them in a folder in Google Drive. Split them accordingly (140-60) just like the commented block at the top of the collab notebook. Next you add the species name to the catgeory list and change the last model.add method so that the first paramter is the number of species seen here:
`model.add(layers.Dense(NUMBER_OF_SPECIES_HERE, name="out", activation='softmax'))`. Make sure you change filepaths accordingly as well and then you will attain an h5 file that can be plugged into the appropiate google cloud function.

## Contributors
Wil - eddyw@wit.edu

Nick - moyern@wit.edu

Feel free to get involved, leave comments, or ask questions!