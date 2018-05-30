from importlib import reload
from . import render_latex


class LatexFragment:
    def __init__(self, body=""):
        self._body = body

    def _repr_latex_(self, fragment=True):
        if fragment:
            # A possibly syntactically-incorrect document fragment,
            # suitable for pweave or pandoc
            return render_latex.extra_packages_body(
                self._body
            )[1]
        else:
            # document fragment with preamble correct for standalone rendering
            return render_latex.latex_as_standalone_document(self._body)

    def _repr_png_(self, **kwargs):
        return render_latex.latex_as_png(self._body, **kwargs)

    def _repr_pdf_(self, **kwargs):
        return render_latex.latex_as_pdf(self._body,  **kwargs)

    def _repr_svg_(self, **kwargs):
        return render_latex.latex_as_svg(self._body, **kwargs)

    def _repr_html_(self, **kwargs):
        """
        We need to define this, otherwise LaTeX is rendered in preference to PNG,
        which doesn't work for non-math.
        """
        return render_latex.latex_as_html(self._body, **kwargs)

    def _repr_markdown_(self, **kwargs):
        """
        Probably we want to pass through raw latex so that it can be
        post-processed.
        """
        return self._repr_latex_(fragment=True, **kwargs)
