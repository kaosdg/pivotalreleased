#!/usr//bin/python
'''
Connects to Pivotal Tracker and generates the release notes for the current iteration
@author: Karl C.
'''
import urllib2
import sys
import json
import argparse
from cStringIO import StringIO

import Config
from lib.PvFormat import PvFormat
from lib.PvGithubFormat import PvGithubFormat
from lib.PvPlainTextFormat import PvPlainTextFormat


def collate_stories(stories, story_type):
    story_list = []
    valid_states = ['delivered', 'finished', 'accepted']

    for story in stories:
        s_type = story.get('story_type')
        s_state = story.get('current_state')
        if (s_type == story_type) and (s_state in valid_states):
            story_list.append(story)

    return story_list


def format_stories(pv_format, stories, story_type):
    formatted_stories = ''

    if stories and len(stories) > 0:
        file_pointer = StringIO()
        file_pointer.write(pv_format.format_story_details(story_type))
        for story in stories:
            if story_type == 'feature':
                formatted_story = pv_format.format_feature(story)
            elif story_type == 'bug':
                formatted_story = pv_format.format_bug(story)
            elif story_type == 'chore':
                formatted_story = pv_format.format_chore(story)

            file_pointer.write(formatted_story)
        formatted_stories = file_pointer.getvalue()
        file_pointer.close()
    return formatted_stories


class ValidFormats(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values in PvFormat.valid_formats:
            setattr(namespace, self.dest, values)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project", help='The Project ID that you want to create release notes for.')
    parser.add_argument("-c", "--config", help="The configuration file to use [pivotal.config by default]")
    parser.add_argument("-o", "--ofile", help="The output file to write to [stdout by default]")
    parser.add_argument("-f", "--format", help="The output format you wish to use.", action=ValidFormats)
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

    pv_format = PvPlainTextFormat()
    if args.format:
        if args.format == 'github':
            pv_format = PvGithubFormat()

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
        json_err = json.loads(err.read())
        sys.stderr.write("%s - %s\n" % (json_err.get('error'), json_err.get('general_problem')))
        sys.stderr.write("%s\n" % json_err.get('possible_fix'))
        sys.exit(2)

    project_header = config.sectionmap("output_details")['project_header']
    iteration_header = config.sectionmap("output_details")['iteration_header']

    project['header'] = project_header
    fp.write(pv_format.format_project_details(project))
    fp.write('\n')

    req = urllib2.Request(iterations_url, None, {'X-TrackerToken': token})
    response = urllib2.urlopen(req)

    iteration = json.loads(response.read())[0]

    stories = iteration.get('stories')

    iteration['header'] = iteration_header
    fp.write(pv_format.format_iteration_details(iteration))
    fp.write("\n")

    bugs = collate_stories(stories, "bug")
    features = collate_stories(stories, "feature")
    chores = collate_stories(stories, "chore")

    fp.write(format_stories(pv_format, bugs, "bug"))
    fp.write("\n\n")

    fp.write(format_stories(pv_format, features, "feature"))
    fp.write("\n\n")

    fp.write(format_stories(pv_format, chores, "chore"))
    fp.write("\n\n")

    fp.write("\n\n\n")
    fp.write(pv_format.footer())

    fp.close()

if __name__ == "__main__":
   main()