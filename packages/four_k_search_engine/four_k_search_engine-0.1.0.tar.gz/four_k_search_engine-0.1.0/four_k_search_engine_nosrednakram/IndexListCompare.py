import logging


class IndexListCompare:
    """
    We process a list and built a result set base on if the filter criteria is met. It supports both contains and
    doesn't contain using equal or not equal methods. The results are stored as an attribute.
    """
    def __init__(self, master, list_filter):
        self.logger = logging.getLogger(__name__)
        self._list = master
        self._filter = list_filter
        self.results = []
        if list_filter['include']  == True:
            self.equal()
        else:
            self.not_equal()

    def equal(self):
        for idx, row in enumerate(self._list):
            try:
                if row[self._filter['field']] == self._filter['value']:
                    self.results.append(idx)
            except:
                pass

    def not_equal(self):
        for idx, row in enumerate(self._list):
            try:
                if row[self._filter['field']] != self._filter['value']:
                    self.results.append(idx)
            except:
                pass

