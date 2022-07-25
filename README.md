# DeepLodocus 

<img width="700" height="350" src="https://github.com/madmaxpython/DeepLodocus/blob/Master/Logo/dldc-WHITE-repository-open-graph-template.png">
 
DeepLodocus is a software in development from the Flores Lab (McGill University, Montreal).

The aim of the software is too extract behavioral data using output data from [DeepLabCut](http://www.mousemotorlab.org/deeplabcut) (.csv files for now).

## How it works:
After training a dedicated DeepLabCut model, and tracked animal(s) the user will be able to define regions of interest - namely Zones - in which the total time spend and the number of entries in these zone, as well as the total locomotor activity will be calculated by DeepLodocus.<br/>
This basic functions can be applicated to numerous daily behavioural test as Elevated Plus Maze, Dark-Light Box, Conditioned Place Preference, and many others

## List of the few scripts available and a short description:
- main.py : main script 
- GUI_DLDC.py : in development GUI version of DeepLodocus
- utils.py : contains every function used by the main.py script in order to extract the time and number of entries in zones define by the user
- calibvideo.py : allows the user to define zone of interest of the video. Save the coordinate of this zone in the 'zone.txt' file
- ToSplit.py : split a csv containing data of multiple animal in separated single animal csv


## What we need : 
### config.yaml

<img width="300" height="400" src="https://github.com/madmaxpython/DeepLodocus/blob/Master/Logo/LabelRequirements.png">

The colored point represent the required label to be tracked on DeepLabCut<br/>
The red lines represent the skeleton of the animal<br/>
Individual name : Mouse 1<br/>

### Video name
Each video name needs to follow the same template: [cagenumber]_[animalID].mp4

This format will alllows to define zones of interest only once for each cage, and thus to identify which animal passed in which cage.

_To make it clearer, here is an example:_

_In my experiment, I have 20 mice and 4 skinner boxes (1 to 4). Let's imagine that I make 5 rotations of 4 mice (one animal in each box), I would have:_
- _4 videos names starting with 1__[animalID].mp4,
- _4 videos names starting with 2__[animalID].mp4,
- _4 videos names starting with 3__[animalID].mp4,
- _4 videos names starting with 4__[animalID].mp4,


