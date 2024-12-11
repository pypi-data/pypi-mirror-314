from busy.command import CollectionCommand
from busy.model.collection import Collection


class TagsCommand(CollectionCommand):

    name = 'tags'

    @CollectionCommand.wrap
    def execute(self):
        tags = set()
        for item in self.collection:
            tags |= item.tags
        return '\n'.join(sorted(tags))
