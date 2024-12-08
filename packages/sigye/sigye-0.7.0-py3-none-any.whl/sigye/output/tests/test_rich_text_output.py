from datetime import datetime, timedelta

from ...models import TimeEntry
from ..rich_text_output import RichTextOutput


def test_rich_text_output():
    now = datetime.now().astimezone()

    t1 = TimeEntry(start_time=now + timedelta(hours=-4), project="test-project", comment="hello")
    t2 = TimeEntry(
        start_time=now + timedelta(hours=-2, minutes=-30),
        end_time=now,
        project="test-project-2",
        comment="test2",
        tags=["testtag2"],
    )

    output = RichTextOutput()
    output.single_entry_output(t1)
    output.single_entry_output(t2)
    output.multiple_entries_output([t1, t2])

    # TODO: add assertions for the output
