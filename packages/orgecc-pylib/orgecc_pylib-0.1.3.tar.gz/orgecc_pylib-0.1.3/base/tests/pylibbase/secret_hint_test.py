import hashlib
import pytest

from base.pylibbase import secret_hint

secret = 'ABCDEFGHIJKLMNOPQ'
secret_hash = hashlib.sha256(secret.encode()).hexdigest()


def test_empty_secret():
    assert secret_hint('') == '<!!! EMPTY SECRET !!!>'


def expected_output(a, b):
    return f'<{secret_hash} ({a}[...]{b}) Len: {len(secret)}>'


@pytest.mark.parametrize("reveal, pre, post, msg", [
    (8, 'AB', 'PQ', 'At most 1/8 even if more is requested'),
    (4, 'AB', 'PQ', 'At most 4'),
    (3, 'A', 'Q', 'At most 3'),
    (2, 'A', 'Q', 'At most 2'),
])
def test_reveal_sizes(reveal, pre, post, msg):
    assert secret_hint(secret, reveal) == expected_output(pre, post), msg


def test_reveal_1():
    assert secret_hint(secret, 1) == expected_output('', '').replace('[', '').replace(']', ''), 'Only ellipsis'
