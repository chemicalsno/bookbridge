"""The listening book list takes each book's listening time from ABS, like the totals above it."""

from src.web_server import _abs_listening_book_list


def test_rows_use_abs_listening_time_and_progress_date():
    items = {"book-a": {"timeListening": 15733.4, "mediaMetadata": {
        "title": "My Struggle", "authors": [{"id": "1", "name": "Karl Ove Knausgaard"}]}}}
    progress = {"book-a": {"lastUpdate": 1792975595000}}

    assert _abs_listening_book_list(items, progress, {"book-a": "My Struggle"}) == [{
        "bookKey": "abs:book-a", "absId": "book-a", "isLinked": True,
        "title": "My Struggle", "author": "Karl Ove Knausgaard",
        "totalSeconds": 15733, "sessionCount": None, "avgSessionSeconds": None,
        "lastReadAt": 1792975595,
    }]


def test_items_without_listening_time_are_skipped():
    items = {"a": {"timeListening": 0, "mediaMetadata": {"title": "A"}}, "b": {"mediaMetadata": {"title": "B"}}}

    assert _abs_listening_book_list(items, {}, {}) == []


def test_item_outside_bookbridge_is_unlinked():
    (row,) = _abs_listening_book_list({"x": {"timeListening": 60, "mediaMetadata": {"title": "X"}}}, {}, {})

    assert row["isLinked"] is False
    assert row["title"] == "X"


def test_title_falls_back_to_bookbridge_then_unknown():
    items = {"a": {"timeListening": 60, "mediaMetadata": {}}, "b": {"timeListening": 60}}

    rows = {row["absId"]: row for row in _abs_listening_book_list(items, {}, {"a": "Dark Matter"})}

    assert rows["a"]["title"] == "Dark Matter"
    assert rows["b"]["title"] == "Unknown book"


def test_newest_first_and_undated_last():
    items = {key: {"timeListening": 60, "mediaMetadata": {"title": key}} for key in ("old", "new", "none")}
    progress = {"old": {"lastUpdate": 1_000_000}, "new": {"lastUpdate": 2_000_000}}

    assert [row["absId"] for row in _abs_listening_book_list(items, progress, {})] == ["new", "old", "none"]


def test_missing_progress_still_lists_books():
    (row,) = _abs_listening_book_list({"a": {"timeListening": 60, "mediaMetadata": {"title": "A"}}}, None, {})

    assert row["lastReadAt"] is None
