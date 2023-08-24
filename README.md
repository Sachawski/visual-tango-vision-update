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
If you want to se ean example of what it can allow to do here is one : [LINK]

## Roadmap
Maybe it would be interesting to find another way of classifying the landmarks positions of the bodypose or the angle of the articulations. We've struggled on making the classification.
For deployment, we've choose Heroku, so just modify the configuration files, such as Procfile or requirements.txt as you modify the project
As Heroku is not convenient for large file upload, we tried to add an external storage service, in this case Cloudinary. It is not finished, so we must add the management of this API.
It will allow the Celery worker to access the video uploaded by the user and to process it. 

Here is a list of things to do :

Upload the video from the client to Cloudinary. 
Download the video from Cloudinary to the celery worker.
Process the video.
Return the result to the server.

It will allow the modelisation to work, and if the classification is improved, it will also work.


## Project status
Development as STOPPED.
