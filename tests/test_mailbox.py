import pytest

from grotten.enums import Kind
from grotten.models import Mailbox, Message


@pytest.fixture
def mailbox():
    return Mailbox()


def test_add(mailbox):
    mailbox.add(kind=Kind.GAME, title="A title", content="Some content")

    assert mailbox.messages == [
        Message(kind=Kind.GAME, title="A title", content="Some content")
    ]


def test_pop(mailbox):
    mailbox.add(kind=Kind.GAME, title="A title")
    assert len(mailbox) == 1

    messages = mailbox.pop()

    assert mailbox.messages == []
    assert messages == [Message(kind=Kind.GAME, title="A title")]
