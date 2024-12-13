import re

from juriscraper.opinions.united_states.federal_appellate import cadc


class Site(cadc.Site):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://www.cadc.uscourts.gov/internet/judgments.nsf/uscadcjudgments.xml"
        self.court_id = self.__module__

    def _get_case_names(self):
        return [
            e.split(", ", 1)[1]
            for e in self.html.xpath("//item/description/text()")
        ]

    def _get_docket_numbers(self):
        return [
            re.search(r"\d{2}-\d+", e).group(0)
            for e in self.html.xpath("//item/title/text()")
        ]

    def _get_precedential_statuses(self):
        return ["Unpublished" for _ in range(0, len(self.case_names))]
