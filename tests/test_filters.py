import pytest
import app.parsers.rss as rss
import app.filters.BaseFilter

EXAMPLE_FEED = "rss2sample.xml"


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
