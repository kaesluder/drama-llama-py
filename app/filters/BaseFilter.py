from copy import deepcopy


class BaseFilter:
    """Base filter class for developing other filters. This one doesn't do
    anything beyond adding a standard message to an item.
    """

    def __init__(self, id, tag, message="", explanation="", field_list=None, **kwargs):
        """Create a BaseFilter with some starting properties.

        Args:
            id (str): Unique identifier for this filter.
            tag (str): A human-readable tag added to items.
            message (str, optional): A longer message used in some views. Use this to report numeric results. Defaults to "".
            explanation (str, optional): A longer message describing what the filter results mean. Defaults to "".
            field_list (_type_, optional): List of string indexes for fields to be filtered on. Defaults to ['description'].
        """
        self.id = id
        self.tag = tag
        self.message = message
        self.explanation = explanation
        self.type = "BaseFilter"
        self.extras = kwargs

        if field_list:
            self.field_list = field_list
        else:
            self.field_list = ["summary"]

    def add_report_to_item(self, item, result):
        """Add a standardized report dict to item. Call within
        analyze to attach results to the item.

        Args:
            item (dict): Dict representing full item.
            result (truthy/falsy): Result of the analysis.
        """

        report = dict(id=self.id, result=result, message=self.message, tag=self.tag)

        if "filter_results" in item:
            item["filter_results"].append(report)
        else:
            item["filter_results"] = [report]

    def analyze(self, item):
        """Analyze an item and append a report to item.filter_results. Returns item.
        Subclasses should rewrite this function. Base class reports True.

        Args:
            item (dict): Dict containing item data.
        """

        self.add_report_to_item(item, True)
        return item

    def export_config(self):
        config = dict(
            id=self.id,
            tag=self.tag,
            message=self.message,
            explanation=self.explanation,
            type=self.type,
        )

        if self.extras:
            config.update(self.extras)

        return config


if __name__ == "__main__":
    filter_a = BaseFilter("hello", "yes")
    test_output = filter_a.analyze({})
    config_output = filter_a.export_config()
    print(test_output)
    print(config_output)
    filter_b = BaseFilter(**config_output)
    print(filter_b.id)
