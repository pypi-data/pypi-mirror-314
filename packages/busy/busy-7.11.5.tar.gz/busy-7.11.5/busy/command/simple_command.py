from busy.command import CollectionCommand

# Like base but with the tags


class SimpleCommand(CollectionCommand):

    name = "simple"

    @CollectionCommand.wrap
    def execute(self):
        return self.output_items(lambda i: i.simple)
