import re
from busy.command import CollectionCommand, MultiCollectionCommand
from busy.error import BusyError
from busy.model.item import Item

from wizlib.parser import WizParser

FIELDS = ['num', r'^val:[a-z].*$', 'base', 'url', 'checkbox',
          'tags', 'elapsed', 'simple', 'listable', 'nodata',
          'state', r'^tag:[a-zA-Z][a-zA-Z0-9\-]*$']


class ViewCommand(MultiCollectionCommand):
    """Output items using specified fields. Designed to replace base, describe,
    simple, etc. Defaults to the top item. Outputs with space separation. Note
    that blank lines will appear for any entry with no value."""

    name = 'view'
    fields: str = 'base'
    unique: bool = False

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        parser.add_argument('--fields', '-f', default='base')
        parser.add_argument(
            '--unique', '-u', action='store_true',
            help='Performs a mildly fuzzy deduplication of output items')

    @CollectionCommand.wrap
    def execute(self):

        # Perform fuzz deduplication if requested

        if self.unique:
            items = []
            fuzzmatches = set()
            for index, item in reversed(self.selection):
                fuzzkey = item.fuzzkey
                if fuzzkey not in fuzzmatches:
                    items.append((index, item))
                    fuzzmatches.add(item.fuzzkey)
            items.reverse()
        else:
            items = self.selection

        # Check for unknown fields

        fields = self.fields.split(',')
        unknown_fields = [f for f in fields if
                          not any(re.match(p, f) for p in FIELDS)]
        if any(unknown_fields):
            raise BusyError(f"Unknown field(s) {','.join(unknown_fields)}")
        if 'num' in self.fields and not self.collection.sequence_number_ok:
            raise BusyError('Invalid field num for multi-state view')

        # Process the output

        cols = range(len(fields))
        widths = [1 for f in cols]
        rows = []
        for index, item in items:
            row = []
            for col in cols:
                field = fields[col]
                if field == 'num':
                    val = index + 1
                elif field.startswith('val:'):
                    key = field[4]
                    val = item.data_value(key)
                elif field.startswith('tag:'):
                    tag = field[4:]
                    val = tag if tag in item.tags else ''
                else:
                    val = getattr(item, field)
                val = str(val) if val is not None else ''
                widths[col] = max(widths[col], len(val))
                row.append(val)
            rows.append(row)
        return '\n'.join(' '.join(f"{r[c]:<{widths[c]}}"
                                  for c in cols).rstrip() for r in rows)
