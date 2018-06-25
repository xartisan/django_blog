class Page:

    def __init__(self, number, num_pages, num_show_pages=5):
        self.number = number
        self.num_pages = num_pages
        self.num_show_pages = num_show_pages
        self.has_right_most = False
        self.has_left_most = False
        self.has_left = False
        self.has_right = False
        self.has_left_most_ellipsis = False
        self.has_right_most_ellipsis = False

        self._process()

    def _process(self):
        start = self.number - self.num_show_pages // 2
        end = self.number + self.num_show_pages // 2
        if start < 1:
            start = 1
            end = start + self.num_show_pages - 1
            if end > self.num_pages:
                end = self.num_pages
        elif end > self.num_pages:
            end = self.num_pages
            start = end - self.num_show_pages + 1
            if start < 1:
                start = 1
        if end < self.num_pages:
            self.has_right_most = True
            if end < self.num_pages - 1:
                self.has_right_most_ellipsis = True
        if start > 1:
            self.has_left_most = True
            if start > 2:
                self.has_left_most_ellipsis = True
        if self.number < self.num_pages:
            self.has_right = True
        if self.number > 1:
            self.has_left = True
        self.page_range = range(start, end + 1)


def page(i, num_pages):
    num_show_pages = 5
    start = i - num_show_pages // 2
    end = i + num_show_pages // 2

    if start < 1:
        start = 1
        end = start + num_show_pages - 1
        if end > num_pages:
            end = num_pages
    elif end > num_pages:
        end = num_pages
        start = end - num_show_pages + 1
        if start < 1:
            start = 1

    has_right_most = False
    has_left_most = False
    has_left = False
    has_right = False
    has_left_most_ellipsis = False
    has_right_most_ellipsis = False
    if end < num_pages:
        has_right_most = True
        if end < num_pages - 1:
            has_right_most_ellipsis = True
    if start > 1:
        has_left_most = True
        if start > 2:
            has_left_most_ellipsis = True
    if i < num_pages:
        has_right = True
    if i > 1:
        has_left = True
    rv = {
        'has_left': has_left,
        'has_right': has_right,
        'has_left_most': has_left_most,
        'has_left_most_ellipsis': has_left_most_ellipsis,
        'has_right_most_ellipsis': has_right_most_ellipsis,
        'has_right_most': has_right_most,
        'page_range': range(start, end + 1)
    }
    return rv
