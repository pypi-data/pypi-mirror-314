from .mistune.highlight import HighlightMixin
from .mistune.toc import TocMixin
from .mistune.media import MediaMixin
import mistune
try:
    HTMLRenderer = mistune.HTMLRenderer
except Exception:
    HTMLRenderer = mistune.Renderer


class WikiRenderer(TocMixin, HighlightMixin, MediaMixin, HTMLRenderer):
    def __init__(self, *args, **kwargs):
        # self.enable_math()
        self.reset_toc()
        super(WikiRenderer, self).__init__(*args, **kwargs)
