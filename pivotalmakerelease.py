#!/usr//bin/python
'''
Connects to Pivotal Tracker and generates the release notes for the current iteration
@author: Karl C.
'''
import urllib2
import sys

import json

import Config
import datetime
import argparse


'''
@param fp: The file pointer to use
@param story: Story DOM object
@param story_type: type of story {bug, chore, feature}  
'''


def printStories(fp, stories, storyType):
    validStoryTypes = ['feature', 'bug', 'chore']

    fp.write("%sS\n" % storyType.upper())
    fp.write("-" * (storyType.__len__() + 1))
    fp.write("\n")

    if storyType in validStoryTypes:
        for story in stories:
            s_type = story.get('story_type')
            if s_type == storyType:
                s_id = story.get('id')
                s_name = story.get('name')
                s_url = story.get('url')
                fp.write("+ [#%s](%s) - %s \n" % (s_id, s_url, s_name))


'''
Gets total iteration points 
@param stories: Stories DOM object 
@return total_points: total iteration points
'''


def getIterationPoints(stories):
    iter_points = 0

    for story in stories:
        s_type = story.get('story_type')

        if s_type == "feature":
            iter_points += int(story.get('estimate'))

    return iter_points


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project", help='The Project ID that you want to create release notes for.')
    parser.add_argument("-c", "--config", help="The configuration file to use [pivotal.config by default]")
    parser.add_argument("-o", "--ofile", help="The output file to write to [stdout by default]")
    args = parser.parse_args()

    configfile = 'pivotal.config'
    if args.config:
        configfile = args.config

    config = Config.Config(configfile)

    project_id = args.project
    if args.ofile:
        fp = open(args.ofile, 'w')
    else:
        fp = sys.stdout

    token = config.sectionmap("pivotal")['app_token']
    iterations_url = config.sectionmap("pivotal")['iteration_url'] % project_id
    project_url = config.sectionmap("pivotal")['project_url'] % project_id

    #project information
    proj_req = urllib2.Request(project_url, None, {'X-TrackerToken': token})

    try:
        proj_response = urllib2.urlopen(proj_req)
        project = json.loads(proj_response.read())
    except urllib2.HTTPError as err:
        sys.stderr.write("%s\n" % str(err))
        jsonErr = json.loads(err.read())
        sys.stderr.write("%s - %s\n" % (jsonErr.get('error'), jsonErr.get('general_problem')))
        sys.stderr.write("%s\n" % jsonErr.get('possible_fix'))
        sys.exit(2)

    fp.write('# PROJECT DETAILS\n')
    fp.write('## Project Name: %s\n' % project.get('name'))
    fp.write('###### %s\n' % project.get('description'))
    fp.write('\n\n')

    req = urllib2.Request(iterations_url, None, {'X-TrackerToken': token})
    response = urllib2.urlopen(req)

    iteration = json.loads(response.read())[0]

    stories = iteration.get('stories')

    startDate = datetime.datetime.strptime(iteration.get('start'), "%Y-%m-%dT%H:%M:%SZ")
    endDate = datetime.datetime.strptime(iteration.get('finish'), "%Y-%m-%dT%H:%M:%SZ")

    fp.write("ITERATION DETAILS\n")
    fp.write("=================\n")
    fp.write("#### Iteration Number : %s\n" % iteration.get('number'))
    fp.write("#### Iteration Start  : %s\n" % startDate.strftime('%A, %B %d %Y'))
    fp.write("#### Iteration Finish : %s\n" % endDate.strftime('%A, %B %d %Y'))
    fp.write("#### Team Strength    : %s\n" % iteration.get('team_strength'))
    fp.write("#### Number of Stories: %s\n" % len(stories))
    fp.write("#### Iteration Points : %s\n" % getIterationPoints(stories))
    fp.write("\n\n")

    #print Bugs
    printStories(fp, stories, "bug")
    fp.write("\n\n")

    #print Features
    printStories(fp, stories, "feature")
    fp.write("\n\n")

    #print Chores
    printStories(fp, stories, "chore")
    fp.write("\n\n")

    fp.close()

if __name__ == "__main__":
   main()