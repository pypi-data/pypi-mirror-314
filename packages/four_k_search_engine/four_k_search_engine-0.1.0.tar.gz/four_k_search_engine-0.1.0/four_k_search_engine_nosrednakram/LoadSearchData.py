import logging


class LoadSearchData:
    """
    Loads all options for specified fields form the data set into individual list for use on the front end. The lists
    are stored in a filter_options list which has a dictionary pair for each filed with name and list of possible
    values.
    """
    def __init__(self, master_list, filter_fields):
        self.logger = logging.getLogger(__name__)
        #
        # Contains a list of possibly options for each supplied key
        #
        self.filter_options = {}

        self.master_list = master_list
        self.logger.info(f"{self.master_list} loaded master list")
        #
        # We'll start every list with a list of index values. We'll
        # use this to limit our values to only those who meet
        # all filters.
        #

        self.master_index = []

        #
        # Gather Information for Filter List Values. As expecting a single page app by using in a dict we
        # can send all easily in response to a get request.
        #
        filter_options = {}
        for key in filter_fields:
            filter_options[key] = []


        # Parse all records and see if filtered value is unique. If so add to attribute of same name
        for idx, rec in enumerate(self.master_list):
            self.master_index.append(idx)
            for key in filter_fields:
                if key in rec:
                    if rec[key] not in filter_options[key]:
                        filter_options[key].append(rec[key])
        self.logger.info(f"master index: {self.master_index}")

        # We want sorted list data
        for key in filter_fields:
            filter_options[key] = sorted(filter_options[key])

        # Now we attach to the class.
        self.filter_options = filter_options
        self.logger.info(f"filter_options: {self.filter_options}")