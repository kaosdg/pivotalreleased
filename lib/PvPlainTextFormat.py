from PvFormat import PvFormat
from datetime import datetime
from cStringIO import StringIO


class PvPlainTextFormat(PvFormat):
    def format_project_details(self, project):
        file_pointer = StringIO()
        file_pointer.write('%s\n' % project.get('header'))
        file_pointer.write('-' * len(project.get('header')))
        file_pointer.write('\n')
        file_pointer.write('Project Name: %s\n' % project.get('name'))

        if project.get('description'):
            file_pointer.write('-' * len(project.get('description')))
            file_pointer.write('\n')
            file_pointer.write('%s\n' % project.get('description'))

        project_details = file_pointer.getvalue()
        file_pointer.close()

        return project_details

    def format_iteration_details(self, iteration):
        file_pointer = StringIO()

        stories = iteration.get('stories')

        start_date = datetime.strptime(iteration.get('start'), "%Y-%m-%dT%H:%M:%SZ")
        end_date = datetime.strptime(iteration.get('finish'), "%Y-%m-%dT%H:%M:%SZ")

        file_pointer.write("%s\n" % iteration.get('header'))
        file_pointer.write('-' * len(iteration.get('header')))
        file_pointer.write('\n')
        file_pointer.write("Iteration Number : %s\n" % iteration.get('number'))
        file_pointer.write("Iteration Start  : %s\n" % start_date.strftime('%A, %B %d %Y'))
        file_pointer.write("Iteration Finish : %s\n" % end_date.strftime('%A, %B %d %Y'))
        file_pointer.write("Team Strength    : %s\n" % iteration.get('team_strength'))
        file_pointer.write("Number of Stories: %s\n" % len(stories))
        file_pointer.write("Iteration Points : %s\n" % PvFormat.get_iteration_points(stories))

        iteration_details = file_pointer.getvalue()
        file_pointer.close()
        return iteration_details

    def format_story_details(self, story_type):
        file_pointer = StringIO()
        story_header = "%sS" % story_type.upper()
        file_pointer.write("%s\n" % story_header)
        file_pointer.write('-' * len(story_header))
        file_pointer.write('\n')
        story_details = file_pointer.getvalue()
        file_pointer.close()
        return story_details

    def format_bug(self, bug):
        return self.format_story(bug)

    def format_chore(self, chore):
        return self.format_story(chore)

    def format_feature(self, feature):
        return self.format_story(feature)

    def format_story(self, story):
        return "[#%s] %s (%s) \n" % (story.get('id'), story.get('name'), story.get('url'))

    @classmethod
    def footer(cls):
        file_pointer = StringIO()
        file_pointer.write("Release notes Generated by pivotalmakerelease (https://github.com/kaosdg/pivotalreleased)")
        file_pointer.write("\n")
        footer = file_pointer.getvalue()
        file_pointer.close()
        return footer