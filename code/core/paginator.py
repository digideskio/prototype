import math


class Paginator(object):
    """
    Custom paginator to limit and page results
    """
    def __init__(self, meta_dict):
        self.skip = meta_dict.get('skip', 0)
        self.limit = meta_dict.get('limit', 1)
        # FIXME: We're capping at 5000 which is the FDA API limit
        self.total = min(meta_dict.get('total', 0), 5000)
        self.pages = int(math.ceil(float(self.total) / self.limit))

    def has_previous(self):
        return self.page() != 1

    def has_next(self):
        return self.page() != self.pages

    def page(self):
        return int(self.skip / self.limit) + 1

    def page_display(self):
        bottom_range = min(self.skip + 1, self.total)
        top_range = min(self.skip + self.limit, self.total)

        return "%s to %s of %s" % (bottom_range, top_range, self.total)

    def pagination_display(self):
        return list(page_range_short(self))

    def prev(self):
        return max(self.page() - 1, 1)

    def next(self):
        return min(self.page() + 1, self.pages)


def page_range_short(paginator):
    middle = 3
    for p in xrange(1, paginator.pages + 1):
        if p <= 3:
            yield p
        elif paginator.pages - p < 3:
            yield p
        elif abs(p - paginator.page()) < middle:
            yield p
        elif abs(p - paginator.page()) == middle:
            yield "..."
