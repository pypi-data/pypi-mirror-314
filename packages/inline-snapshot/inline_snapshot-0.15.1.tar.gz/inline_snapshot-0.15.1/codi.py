from inline_snapshot import snapshot, Is

# snapshots inside snapshots
def test_a():
    assert get_schema() == snapshot(
        [
            {
                "name": "var_1",
                "type": snapshot("int") if version < 2 else snapshot("string"),
            }
        ]
    )


# runtime values inside snapshots
def test_b():
    for c in "abc":
        assert [c, "correct"] == snapshot([Is(c), "correct"])
