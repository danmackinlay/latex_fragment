"""
pdflatex "standalone" rendering

based on https://github.com/johnjosephhorton/texscrap/blob/master/texscrap.py
and
https://gist.github.com/ahwillia/ce9a842f122757518c65d0bd545f28c1#file-equations-tex-L2
"""

from shutil import copy2 as copy
from tempfile import NamedTemporaryFile
import hashlib
import os
import os.path
import re
import subprocess
import sys
import tempfile

def call(*args, **kwargs):
    """execute a subprocess, return
    a tuple of the stdout and the stderr of the call.
    
    >>>call(['echo', 'hello world'])
    ('hello world\n', '')
    """
    with NamedTemporaryFile() as outfile, NamedTemporaryFile() as errfile:
        outfilename = outfile.name
        errfilename = errfile.name
        proc = subprocess.Popen(
            *args, stdout=outfile, stderr=errfile, **kwargs)
        proc.wait()
        with open(outfilename, 'r+b') as outfile:
            out = outfile.read()
        with open(errfilename, 'r+b') as errfile:
            err = errfile.read()
        return out, err


def as_standalone_document(extra_packages, body):
    """ Returns latex_string prepared as a LaTeX document """
    return r"""\documentclass[preview]{{standalone}}
    \usepackage{{amsmath}}
    \usepackage{{amsfonts}}
    \usepackage{{amssymb}}
    \usepackage[active]{{preview}}
    {extra_packages}
    \begin{{document}}
    \\pagestyle{{empty}}
    \begin{{preview}}
    {body}
    \end{{preview}}
    \end{{document}}""".format(
        extra_packages=extra_packages,
        body=body
    )


def hashed(content):
    """context_hash"""
    output = hashlib.md5()
    output.update(self.content)
    return output.hexdigest()


def temp_filepath(suffix=''):
    """ Return the name of a temporarily created file. Don't forget to delete it. """
    f = NamedTemporaryFile(suffix=suffix, delete=False)
    f.close()
    return f.name


def remove_if_exists(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


def extra_packages_body(latex_string):
    packages, body = [], []
    for line in latex_string.split('\n'):
        if line.startswith('\\usepackage'):
            packages.append(line)
        else:
            body.append(line)
    return '\n'.join(packages), '\n'.join(body)


def as_png(latex_string, dest='./', dpi=150):

    with NamedTemporaryFile(
            suffix='.tex',
            delete=False
            ) as tempfile:
        tempfilename = tempfile.name
        tempfile.write(
            as_standalone_document(
                *extra_packages_body(
                    latex_string
                )
            )
        )
        tempfile.close()
        subprocess.call(['pdflatex', '-interaction=nonstopmode', tempfilename])

    tempfiledir = os.path.dirname(tempfilename)

    # crop pdf, convert to png
    stderr, stdout = call([
        'pdfcrop',
        '{}.pdf'.format(tempfilename),
        '{}.pdf'.format(outfile)
    ])
    print(stderr, stdout)
    stderr, stdout = call([
        'convert',
        '-density',
        str(dpi),
        '{}.pdf'.format(outfile),
        '{}.png'.format(outfile)
    ])
    print(stderr, stdout)
    with open('{}.png'.format(outfile), 'r') as h:
        png = h.read()

    remove_if_exists(tmp_name + '.tex')
    remove_if_exists(tmp_name + '.pdf')
    remove_if_exists(tmp_name + '.log')
    remove_if_exists(tmp_name + '.aux')
    return png
    
