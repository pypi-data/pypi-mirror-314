from inline_snapshot import snapshot
from inline_snapshot.extra import warns
from warnings import warn


def test_warns():
    with warns(
        snapshot([(11, "UserWarning: some problem")]), include_line=True
    ):
        warn("some problem")
