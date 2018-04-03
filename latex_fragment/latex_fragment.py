from importlib import reload
import render_latex
render_latex = reload(render_latex)

class LatexFragment:
    def __init__(self, preamble="", content=""):
        self._preamble = preamble
        self._content = content

    def _repr_latex_(self):
        return self._preamble + self._content

    def _repr_png_(self):
        return render_latex.as_png(
            self._preamble,
            self.context
        )
