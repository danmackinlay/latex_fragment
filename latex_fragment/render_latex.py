"""
pdflatex "standalone" rendering

based on https://github.com/johnjosephhorton/texscrap/blob/master/texscrap.py
and
https://gist.github.com/ahwillia/ce9a842f122757518c65d0bd545f28c1#file-equations-tex-L2

There is a bit of wasteful creation and deletion of files here,
but I briefly thought I could do everything with pipes,
before I discovered PDFs need random access.
"""

from tempfile import NamedTemporaryFile
import os
import os.path
from subprocess import run, PIPE
from pathlib import Path
import base64


def verbose_run(cmd, **kwargs):
    """
    we always want to include stdout in the errors,
    which the default `check=True` does not.
    So we self-check.
    """
    proc = run(
        cmd,
        stdout=PIPE,
        stderr=PIPE,
        check=False,
        **kwargs)
    if proc.returncode > 0:
        raise ChildProcessError(
            "`{!r}` failed with return code {}:\n{}\n{}\n ".format(
                cmd,
                proc.returncode,
                proc.stderr.decode(),
                proc.stdout.decode()
            )
        )
    return proc


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


def as_standalone_document(latex_string):
    """ Returns latex_string prepared as a LaTeX document """
    extra_packages, body = extra_packages_body(
        latex_string
    )
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


def remove_if_exists(filename):
    try:
        os.remove(str(filename))
    except OSError:
        pass


def extra_packages_body(latex_string):
    packages, body = [], []
    for line in latex_string.split('\n'):
        if line.strip().startswith(r'\usepackage'):
            packages.append(line)
        else:
            body.append(line)
    return '\n'.join(packages), '\n'.join(body)


def as_png(latex_string, dest='./', dpi=150):
    """
    pdf is not a streaming format and must happen on FS.
    """
    pdf = as_pdf(latex_string)
    with NamedTemporaryFile(suffix='.pdf', mode="w+b") as temp_pdf_handle:
        temp_pdf_path = Path(temp_pdf_handle.name)
        temp_pdf_handle.write(pdf)
        temp_pdf_handle.seek(0)
        cmd = [
            'convert', '-density',
            str(dpi),
            str(temp_pdf_path),
            str('png:-')
        ]
        proc = verbose_run(
            cmd,
            bufsize=int(1e8),
        )
        return proc.stdout


def as_pdf(latex_string):
    """
    latex is temp file heavy and must happen on the FS
    """
    with NamedTemporaryFile(suffix='.tex', delete=False) as temp_tex_file:
        temp_tex_path = Path(temp_tex_file.name)
        temp_tex_file.write(as_standalone_document(latex_string).encode())
        temp_tex_file.close()
        cwd = str(temp_tex_path.parent)

        cmd = [
            'pdflatex',
            '-interaction=nonstopmode',
            '-halt-on-error',
            str(temp_tex_path),
        ]
        verbose_run(
            cmd,
            cwd=cwd,
            bufsize=int(1e8))

    with open(str(temp_tex_path.with_suffix('.pdf')), 'rb') as h:
        pdf = h.read()

    # there could be more files than this, but hopefully the OS will clean them up?
    remove_if_exists(temp_tex_path.with_suffix('.pdf'))
    remove_if_exists(temp_tex_path.with_suffix('.log'))
    remove_if_exists(temp_tex_path.with_suffix('.aux'))
    return pdf


def as_svg(latex_string, converter='pdf2svg'):
    pdf = as_pdf(latex_string)
    with NamedTemporaryFile(suffix='.pdf', mode="w+b") as temp_pdf_handle, \
            NamedTemporaryFile(suffix='.svg', delete=False) as temp_svg_handle:
        temp_pdf_path = Path(temp_pdf_handle.name)
        temp_pdf_handle.write(pdf)
        temp_pdf_handle.seek(0)
        if converter == 'pdf2svg':
            cmd = ['pdf2svg', str(temp_pdf_path), temp_svg_handle.name]
        else:
            cmd = [
                'inkscape',
                '--without-gui',
                '--file={}'.format(str(temp_pdf_path)),
                '--export-plain-svg={}'.format(temp_svg_handle.name)]

        proc = verbose_run(
            cmd,
        )
    with open(temp_svg_handle.name, 'r') as h:
        svg = h.read()
    remove_if_exists(temp_svg_handle.name)
    return svg


def as_html(latex_string):
    img_bytes = as_png(latex_string)
    return as_image_data_uri_elem(img_bytes, latex_string)
