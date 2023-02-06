from . import BaseFilter
import re


class RegexFilter(BaseFilter.BaseFilter):
    def __init__(
        self, id, tag, message="", explanation="", field_list=None, regex=None, **kwargs
    ):

        super().__init__(id, tag, message, explanation, field_list)
        self.type = "RegexFilter"
        self.extras = kwargs
        self.regex = regex

    def add_report_to_item(self, item, result, matches):
        """Add a standardized report dict to item. Call within
        analyze to attach results to the item.

        Args:
            item (dict): Dict representing full item.
            result (truthy/falsy): Result of the analysis.
        """

        report = dict(
            id=self.id,
            result=result,
            matches=matches,
            message=self.message,
            tag=self.tag,
        )

        if "filter_results" in item:
            item["filter_results"].append(report)
        else:
            item["filter_results"] = [report]

    def analyze(self, item):

        results = []

        for field in self.field_list:
            results.extend(re.findall(self.regex, item.get(field, "")))

        if results:
            self.add_report_to_item(item, True, results)
        else:
            self.add_report_to_item(item, False, None)

        return item
