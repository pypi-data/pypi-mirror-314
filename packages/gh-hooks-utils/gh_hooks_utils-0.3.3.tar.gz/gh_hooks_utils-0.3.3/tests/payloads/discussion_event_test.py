from gh_hooks_utils.payloads import DiscussionEvent
from gh_hooks_utils.payloads.discussions import DiscussionStateEnum

from .data.discussion.payloads import discussion_closed


def test_discussion_event_should_acceppt_closed_action():
    event = DiscussionEvent(**discussion_closed)

    assert event is not None
    assert event.discussion.state == DiscussionStateEnum.CLOSED
