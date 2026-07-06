"""Opt-in live-LLM smoke tests. Marked `requires_lm_studio`: conftest skips the
whole file automatically when no AI endpoint answers, so the default suite is
green with the GPU box off."""
import pytest

from app import ai

pytestmark = pytest.mark.requires_lm_studio


def test_chat_round_trip():
    reply = ai._chat([
        {"role": "system", "content": "You reply with exactly one word."},
        {"role": "user", "content": "Say OK."},
    ])
    assert isinstance(reply, str) and reply.strip()
