class Paginated(object):
    def __init__(self, paged_data):
        self.page = int(paged_data['page'])
        self.pages = int(paged_data['total_pages'])
        self.items = paged_data['results']

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2, right_current=2, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or (self.page - left_current - 1 < num < self.page + right_current) \
                    or num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
