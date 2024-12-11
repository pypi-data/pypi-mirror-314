from busy.command import CollectionCommand


class DescribeCommand(CollectionCommand):
    """Show just the description"""

    name = 'describe'

    @CollectionCommand.wrap
    def execute(self):
        return self.output_items(lambda i: i.description)
