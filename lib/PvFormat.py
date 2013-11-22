class PvFormat(object):
    valid_formats = ['github', 'plaintext']

    def format_project_details(self, project):
        raise NotImplementedError("Subclasses must implement this")

    def format_iteration_details(self, iteration):
        raise NotImplementedError("Subclasses must implement this")

    def format_story_details(self, story_type):
        raise NotImplementedError("Subclasses must implement this")

    def format_story(self, story):
        raise NotImplementedError("Subclasses must implement this")

    def format_bug(self, bug):
        raise NotImplementedError("Subclasses must implement this")

    def format_chore(self):
        raise NotImplementedError("Subclasses must implement this")

    def format_feature(self):
        raise NotImplementedError("Subclasses must implement this")

    @classmethod
    def get_iteration_points(cls, stories):
        iteration_points = 0
        for story in stories:
            if story.get('story_type') == "feature":
                iteration_points += int(story.get('estimate'))

        return iteration_points

    @classmethod
    def format_footer(cls, footer):
        raise NotImplementedError("Subclasses must implement this")