from four_k_search_engine_nosrednakram.FilterList import FilterList
from four_k_search_engine_nosrednakram.IndexListCompare import IndexListCompare
import logging


class FilterSet:
    """
    This is possible because we keep track of the index of the master list while we do our filtering.

    Given a list of dictionaries it will apply the filters one at a time and return the filtered
    down list.

        * Field is the dictionary Key
        * value is the value the filter compares with
        * include it True to include or False to Exclude records based on the filter value.


    filters = [{
                    "field": "Gender",
                    "value": "Female",
                    "include": True
              },
              {
                    "field": "Profession",
                    "value": "Auror",
                    "include": True
              }]


    The results attribute is a sublist of the master list after having been filtered.
    """

    def __init__(self, master_index, master_list, filters):
        self.logger = logging.getLogger(__name__)
        self.results = []
        #
        # Starting a With our list so we can filter it down
        #

        fl = FilterList(master_index)

        #
        # Now we filter our master index lists down
        #

        for row in filters:
            fl.intersect(IndexListCompare(master=master_list, list_filter=row).results)

        for idx in fl.filtered_list:
            self.results.append(master_list[idx])
