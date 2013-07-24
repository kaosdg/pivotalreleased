'''
Connects to Pivotal Tracker and generates the release notes for the current iteration
@author: Sam K.
'''
import urllib2, sys
from xml.dom import minidom

'''
Prints all stories of a specific type in a formatted manner "[Pivotal Tracker-$ID] - $NAME
@param fp: The file pointer to use
@param story: Story DOM object
@param story_type: type of story {bug, chore, feature}  
'''    
def printStories(fp, story, storyType):
    validStoryTypes = ['feature', 'bug', 'chore']   #Valid story types
    
    if storyType in validStoryTypes:
        s_type = story.getElementsByTagName("story_type")[0].firstChild.data
        
        if s_type == storyType: 
            s_id = story.getElementsByTagName('id')[0].firstChild.data
            s_name = story.getElementsByTagName('name')[0].firstChild.data
            fp.write("[Pivotal Tracker ID-%s] - %s\n" % (s_id, s_name))
        else:
            return
        
        return
    else:
        print "Invalid story type."
        sys.exit(1)

'''
Gets total iteration points 
@param stories: Stories DOM object 
@return total_points: total iteration points
''' 
def getIterationPoints(stories):
    iter_points = 0 
    
    for story in stories:
        s_type = story.getElementsByTagName("story_type")[0].firstChild.data
        
        if s_type == "feature":
            iter_points += int(story.getElementsByTagName("estimate")[0].firstChild.data)

    return iter_points

###################################

PROJECT_ID = "130837"                           # Pivotal Tracker IOU Project ID
TOKEN = "d383366a2fef4c33cd842d0545d6cfca"      # Pivotal Tracker IOU Token

# API URL to get current iteration
#url = "https://www.pivotaltracker.com/services/v3/projects/%s/iterations/done?offset=-1" % PROJECT_ID 
url = "https://www.pivotaltracker.com/services/v3/projects/%s/iterations/current" % PROJECT_ID

req = urllib2.Request(url, None, {'X-TrackerToken': TOKEN})
response = urllib2.urlopen(req)
dom = minidom.parseString(response.read())

# Get current iteration and all stories under it
iteration = dom.getElementsByTagName('iteration')[0]
stories = iteration.getElementsByTagName('story')

fp = open('release-notes.txt','w')

fp.write("ITERATION DETAILS:\n")
fp.write("=================\n\n")
fp.write("Iteration Number: %s\n" % iteration.getElementsByTagName('number')[0].firstChild.data)
fp.write("Iteration Start: %s\n" % iteration.getElementsByTagName('start')[0].firstChild.data)
fp.write("Iteration Finish: %s\n" % iteration.getElementsByTagName('finish')[0].firstChild.data)
fp.write("Team Strength: %s\n" % iteration.getElementsByTagName('team_strength')[0].firstChild.data)
fp.write("Number of Stories: %s\n" % len(stories)) 
fp.write("Iteration Points: %s\n" % getIterationPoints(stories)) 
fp.write("\n\n")

#print Bugs
fp.write("BUGS:\n")
fp.write("======\n\n")
for story in stories:
    printStories(fp, story, "bug")
fp.write("\n\n")
        
#print Features
fp.write("FEATURES:\n")
fp.write("==========\n\n")
for story in stories:
    printStories(fp, story, "feature")
fp.write("\n\n")

#print Chores
fp.write("CHORES:\n")
fp.write("=======\n\n")
for story in stories:
    printStories(fp, story, "chore")
fp.write("\n\n")

fp.close()
