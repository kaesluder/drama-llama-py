import pytest
import app.parsers.rss as rss
import app.filters.BaseFilter
import app.filters.RegexFilter

EXAMPLE_FEED = "rss2sample.xml"
example_item = rss.parse_source(EXAMPLE_FEED)["entries"][0]
base_test_filter = app.filters.BaseFilter.BaseFilter("hello world", "Yes!!")
regex_test_filter = app.filters.RegexFilter.RegexFilter(
    "hello regex",
    "regexMatch",
    "regexMatch",
    "a test of regex filter",
    None,
    "regex",
    test_extra="foo",
)


def test_basefilter_appends_result():
    example_item = rss.parse_source(EXAMPLE_FEED)["entries"][0]
    test_filter = app.filters.BaseFilter.BaseFilter("hello world", "Yes!!")
    result_item = test_filter.analyze(example_item)

    assert len(result_item["filter_results"]) == 1


def test_basefilter_results_contain_expected_texts():
    example_item = rss.parse_source(EXAMPLE_FEED)["entries"][0]
    test_filter = app.filters.BaseFilter.BaseFilter("hello world", "Yes!!")
    result_item = test_filter.analyze(example_item)
    reports = result_item["filter_results"]
    assert reports[0]["id"] == "hello world"
    assert reports[0]["tag"] == "Yes!!"
    assert reports[0]["result"] == True


def test_basefilter_export_contains_required_fields():
    required_fields = ["id", "tag", "message", "explanation", "type"]
    exported = base_test_filter.export_config()
    for field in required_fields:
        assert field in exported


def test_regex_export_contains_required_fields():
    required_fields = [
        "id",
        "tag",
        "message",
        "explanation",
        "type",
        "regex",
        "test_extra",
    ]
    exported = regex_test_filter.export_config()
    for field in required_fields:
        assert field in exported


def test_regex_results_contain_expected_texts():
    example_item = rss.parse_source(EXAMPLE_FEED)["entries"][0]
    test_filter = app.filters.RegexFilter.RegexFilter(
        "hello regex", "Maybe!!", regex=r"and|of|or"
    )
    result_item = test_filter.analyze(example_item)
    reports = result_item["filter_results"]
    assert reports[0]["id"] == "hello regex"
    assert reports[0]["tag"] == "Maybe!!"
    assert reports[0]["result"] == True
    assert len(reports[0]["matches"]) >= 1


def test_regex_can_return_false():
    example_item = rss.parse_source(EXAMPLE_FEED)["entries"][0]
    test_filter = app.filters.RegexFilter.RegexFilter(
        "hello regex", "Definitely Not!!", regex=r"goobygoobysnack"
    )
    result_item = test_filter.analyze(example_item)
    reports = result_item["filter_results"]
    assert reports[0]["result"] == False
    assert reports[0]["matches"] is None
