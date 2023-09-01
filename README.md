# VisualTango VisionUpdate

## Description
The aim of this project was to improve the VisualTango software and to add a computer vision dimension. Briefly, the aim of this software is to allow people to make tango choregraphy easily. 
We modified some movement to make them more realistic, and added some tools to make it easier to edit choreography. We also added some code that allow to detect the movement of a dancer, and to calculate the angle between the articulation of the dancer. We also modified the project so the app can be deployed on the web, and people can save and load choreography, and edit them. Classifying the movements to be able to enter them in the app would have been good but we did not succeed.
We have also added a modelisation option that allows you to see the dance of the video made by a person.

If you want to see the original version of VisualTango :

https://github.com/rabbit0v0/Visual-Tango-WebGL

## Installation
Pull the repo, create a virtualenv and activate it, then just enter the following line:
$ pip install -r requirements.txt
You will have all the requirements to run the project on a falsk development server.
If you want to deploy it on Heroku, just push it to your remote branch.

## Usage
If you want to see an example of what it can allow to do here is one : [LINK]

## Roadmap

It may be worthwhile to explore alternative methods for classifying landmark positions in body poses or angles of articulations. We encountered challenges in achieving this classification.
Regarding deployment, we opted for Heroku. To this end, adjust configuration files like the Procfile or requirements.txt as you modify the project.
Since Heroku is not convenient for large file uploads, we attempted to integrate an external storage service, specifically Cloudinary. This integration remains unfinished, necessitating the addition of API management.
This will enable the Celery worker to access user-uploaded videos and process them.

Outlined below are the steps to take:

    Upload the video from the client to Cloudinary.
    Download the video from Cloudinary to the Celery worker.
    Process the video.
    Return the result to the server.

It will allow the modelisation to work, and if the classification is improved, it will also work.


## Project status
Development has been STOPPED.
