import logging


class FilterList:
    """
    This class starts with a full list of items. And then we remove items based on index query options.
    The final results can be retrieved using the filtered_list method.
    """
    def __init__(self, master_list):
        self.logger = logging.getLogger(__name__)
        self.filtered_list = master_list

    def intersect(self, filtered_list):
        filtered_set = set(filtered_list)
        new_list = []
        for val in self.filtered_list:
            if val in filtered_set:
                new_list.append(val)
        self.filtered_list = new_list
