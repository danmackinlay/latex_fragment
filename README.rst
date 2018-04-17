latex_fragment
===============================

You are writing your code using jupyter_ or pweave_,
but your colleague freaks out because it's not using 
*that one special latex thing that we totally need or it's not real science*.
(Let's say it's ``\algorithmic``, say, because this problem is alrady solved for 
mathematical markup thanks to MathJax_ and Katex_.)

No problem.

.. code:: python

    import latex_fragment
    latex_fragment.LatexFragment(r'$x=y$')

This will render just fine, using your sytem LaTeX.

.. image:: screenshot.png

Fancier:

.. code:: python

    import latex_fragment
    latex_fragment.LatexFragment(r'''
    \usepackage{algorithmicx}
    \usepackage{algpseudocode}
    \begin{algorithm}
    \caption{Euclid’s algorithm}\label{euclid}
    \begin{algorithmic}[1]
    \Procedure{Euclid}{$a,b$}\Comment{The g.c.d. of a and b}
        \State $r\gets a\bmod b$
        \While{$r\not=0$}\Comment{We have the answer if r is 0}
            \State $a\gets b$
            \State $b\gets r$
            \State $r\gets a\bmod b$
        \EndWhile\label{euclidendwhile}
        \State \textbf{return} $b$\Comment{The gcd is b}
    \EndProcedure
    \end{algorithmic}
    \end{algorithm}
    ''')

.. image:: algo.png

.. _mathjax: https://www.mathjax.org/
.. _katex: https://github.com/Khan/KaTeX
.. _jupyter: https://jupyter.org/
.. _pweave: http://mpastell.com/pweave/