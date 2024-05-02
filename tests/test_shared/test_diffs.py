from graph.shared.diffs import Change, hdiff


def test_hdiff() -> None:
    (*abcca,) = "abcca"
    (*BACC,) = "BACC"

    expected = [
        Change.deleted("a"),
        Change.constant("b", "B"),
        Change.inserted("A"),
        Change.constant("c", "C"),
        Change.constant("c", "C"),
        Change.deleted("a"),
    ]

    assert hdiff(abcca, BACC, str.lower, str.lower) == expected
