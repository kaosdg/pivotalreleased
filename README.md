pivotalmakerelease
==================

Using Pivotal Tracker and need to generate Release Notes? Try this script for a charm..

The concept behind this Python script is to read Pivotal Tracker stories for completion and extrapolate Releases. Share
these release notes with the client.

Original python script generously shared by Houssam (Sam) Kawtharani at PT's GetSatisfaction forum:
http://community.pivotaltracker.com/pivotal/topics/release_notes_generation
under a "Release Notes Generation" thread.


##Usage
```
usage: pivotalmakerelease [-h] [-c CONFIG] [-o OFILE] [-f FORMAT]
                          [--no-footer]
                          project

Create release notes for a given Pivotal Tracker Project

positional arguments:
  project               The Project ID that you want to create release notes
                        for.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        The configuration file to use [pivotal.config by
                        default]
  -o OFILE, --ofile OFILE
                        The output file to write to [stdout by default]
  -f FORMAT, --format FORMAT
                        The output format you wish to use.
  --no-footer           Whether or not to include the footer
```


##Sample output
```pivotalmakerelease.py xxxxxx -f github```
# Project Details
### Redacted Project Title!

## Iteration Details
#### Iteration Number : 10
#### Iteration Start  : Monday, February 17 2014
#### Iteration Finish : Monday, February 24 2014
#### Team Strength    : 1
#### Number of Stories: 72
#### Iteration Points : 15

### BUGS
+ [[#xxxxxx]](http://www.pivotaltracker.com/story/show/xxxxxx) - Can not get past loading screen with no connection, no warning pop ups.. etc, 
Even after recconecting to a network, its still stuck at loading screen


### FEATURES
+ [[#xxxxxx]](http://www.pivotaltracker.com/story/show/xxxxxx) - iPhone: Implement the Rewards screen
+ [[#xxxxxx]](http://www.pivotaltracker.com/story/show/xxxxxx) - iPad: Implement the Rewards screen
+ [[#xxxxxx]](http://www.pivotaltracker.com/story/show/xxxxxx) - Integrate SessionM 
+ [[#xxxxxx]](http://www.pivotaltracker.com/story/show/xxxxxx) - Handling intermittent or unreliable internet connections
+ [[#xxxxxx]](http://www.pivotaltracker.com/story/show/xxxxxx) - Videos: Age Gating
+ [[#xxxxxx]](http://www.pivotaltracker.com/story/show/xxxxxx) - iPad: Implement the Privacy Policy screen
+ [[#xxxxxx]](http://www.pivotaltracker.com/story/show/xxxxxx) - iPhone: Implement the Privacy Policy screen
+ [[#xxxxxx]](http://www.pivotaltracker.com/story/show/xxxxxx) - iPad:  Implement the Terms & Conditions screen
+ [[#xxxxxx]](http://www.pivotaltracker.com/story/show/xxxxxx) - iPhone: Implement the Terms & Conditions screen
+ [[#xxxxxx]](http://www.pivotaltracker.com/story/show/xxxxxx) - iPad: Add support to display blog
+ [[#xxxxxx]](http://www.pivotaltracker.com/story/show/xxxxxx) - Add spinner to Gallery loading


### CHORES
+ [[#xxxxxx]](http://www.pivotaltracker.com/story/show/xxxxxx) - Move resources to assets manager

---
###### Release notes Generated by [pivotalmakerelease](https://github.com/kaosdg/pivotalreleased)

## Updates
Updated to use the latest Pivotal JSON API, added some options and config, and output in Github MD format