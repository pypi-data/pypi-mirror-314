import logging


class Search:
    """
    Dose a basic search for a substring. This returns all matches if multiple search filters sent. This is on
    purpose but can be changed by sending list in calling code one at a time and resending results list.
    """
    def __init__(self, search_list, search_request):
        self.logger = logging.getLogger(__name__)
        self.logger.info('Initializing Search')
        self.logger.info(f'Search request: {search_request}')
        self.results = []
        for rec in search_list:
            for srch in search_request:
                if srch['field'] in rec:
                    if srch['value'].lower() in rec[srch['field']].lower():
                        if rec not in self.results:
                            self.results.append(rec)
        self.logger.info('Search results: {}'.format(self.results))