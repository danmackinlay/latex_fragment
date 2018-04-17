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
from pathlib import Path
import base64


def as_image_data_uri_elem(data, alt=""):
    return (
        '''
        <img
            style=""
            src="data:image/png;base64,{data}"
            alt={alt}
        />
        '''
    ).format(
        data=''.join(base64.encodebytes(data).decode().split('\n')),
        alt=alt
    )

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
        return out, err, proc.returncode


def as_standalone_document(extra_packages, body):
    """ Returns latex_string prepared as a LaTeX document """
    return r"""\documentclass[preview]{{standalone}}
    \usepackage{{amsmath}}
    \usepackage{{amsfonts}}
    \usepackage{{amssymb}}
    \usepackage[active]{{preview}}
    {extra_packages}
    \begin{{document}}
    \pagestyle{{empty}}
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
        os.remove(str(filename))
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
            ) as temp_tex_file:
        temp_tex_path = Path(temp_tex_file.name)
        extra_packages, body = extra_packages_body(
            latex_string
        )
        temp_tex_file.write(
            as_standalone_document(
                extra_packages, body
            ).encode()
        )
        temp_tex_file.close()
        cwd = str(os.path.dirname(temp_tex_path))

        cmd = [
            'pdflatex',
            '-interaction=nonstopmode',
            '-halt-on-error',
            str(temp_tex_path),
        ]
        stderr, stdout, returncode = call(cmd, cwd=cwd)
        if returncode>0:
            raise ChildProcessError(
                "`{!r}` failed with return code {}:\n{}\n{}\n ".format(
                    cmd,
                    returncode,
                    stderr.decode(),
                    stdout.decode()
                )
            )

        cmd = [
            'convert',
            '-density',
            str(dpi),
            str(temp_tex_path.with_suffix('.pdf')),
            str(temp_tex_path.with_suffix('.png'))
        ]

        stderr, stdout, returncode = call(cmd, cwd=cwd)
        if returncode>0:
            raise ChildProcessError(
                "`{!r}` failed with return code {}:\n{}\n{}\n ".format(
                    cmd,
                    returncode,
                    stderr.decode(),
                    stdout.decode()
                )
            )
        with open(str(temp_tex_path.with_suffix('.png')), 'rb') as h:
            png = h.read()

        remove_if_exists(temp_tex_path.with_suffix('.pdf'))
        remove_if_exists(temp_tex_path.with_suffix('.png'))
        remove_if_exists(temp_tex_path.with_suffix('.log'))
        remove_if_exists(temp_tex_path.with_suffix('.aux'))
        return png


def as_pdf(latex_string):
    pass


def as_svg(latex_string):
    pass


def as_html(latex_string):
    img_bytes = as_png(latex_string)
    return as_image_data_uri_elem(img_bytes, latex_string)
