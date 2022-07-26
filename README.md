# DeepLodocus 

<img width="700" height="350" src="https://github.com/madmaxpython/DeepLodocus/blob/Master/Docs/Logos/dldc-WHITE-repository-open-graph-template.png">
 
DeepLodocus is a software in development from the Flores Lab (McGill University, Montreal).

It aims to extract behavioral data using output data from [DeepLabCut](http://www.mousemotorlab.org/deeplabcut) (.csv files for now).

## How it works:
After training a dedicated DeepLabCut model and tracking one or more animal(s), you will be able to define your regions of interest - namely the Zones - in which the total number of entries, time spent and locomotor activity will be calculated for each animal.<br/>
This basic functions can be applicated to numerous daily behavioural test as Elevated Plus Maze, Dark-Light Box, Conditioned Place Preference, and many others!

### Step One: Select analysis parameters:
<img width="470" height="300" src="https://github.com/madmaxpython/DeepLodocus/blob/Master/Docs/Images/GUI_screenshot.png">
At this step, you can define some parameters like measurement(s) you are interested in, the name of your zone(s) as well as some spec of your videos.

### Step Two: Define the zones:
<img width="470" height="250" src="https://github.com/madmaxpython/DeepLodocus/blob/Master/Docs/Images/AreaSelection_screenshot.png">
Here, you define your Zones. In this exemple, only two square zones are defined, but these can be of any polygonal shape and any number.

### Step Three: Run the analysis & Get the output:
<img width="300" height="130" src="https://github.com/madmaxpython/DeepLodocus/blob/Master/Docs/Images/Output_screenshot.png">
Finally, you get your results in a tabular file as well as in the terminal.

## List of the few scripts available for now, with a short description:
- main.py : main script that you will execute to run your analysis
- GUI_DLDC.py : in development GUI version of DeepLodocus.
- utils.py : contains every functions used by the main.py script to extract the time and number of entries in zones defined.
- calibvideo.py : allows you to define zones of interest. Save the coordinate of these zones in the 'zone.txt' file.
- ToSplit.py : splits a csv containing data of multiple animals in separated single-animal csv.


## What we need : 
### config.yaml

<img width="250" height="400" src="https://github.com/madmaxpython/DeepLodocus/blob/Master/Docs/Images/LabelRequirements.png">

- The colored point represent the required labels to be tracked on DeepLabCut, with their name (case-sensitive)<br/>
- The red lines represent the skeleton of the animal<br/>
- Individual name : Mouse 1<br/>

You can find an exemple of the config.yaml that we used to train our model [here](https://github.com/madmaxpython/DeepLodocus/blob/Master/Docs/config.yaml).

### Video name
Each video name needs to follow the same template: [cagenumber]_[animalID].mp4

This format is important and will alllows to define zones of interest only once for each cage, and thus to identify which animal passed in which cage.

_To make it clearer, here is an example:_

_In my experiment, I had 20 mice and 4 skinner boxes (1 to 4). Let's imagine that I made 5 rotations of 4 mice (one animal in each box), I would have:_
- _4 videos names starting with 1__[animalID].mp4,
- _4 videos names starting with 2__[animalID].mp4,
- _4 videos names starting with 3__[animalID].mp4,
- _4 videos names starting with 4__[animalID].mp4,


