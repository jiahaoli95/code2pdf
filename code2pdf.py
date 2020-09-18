import os
import argparse
import shutil
from collections import OrderedDict


# main.tex content
MAIN_TEX = \
r"""
\documentclass[letterpaper]{article}

\usepackage[utf8]{inputenc}
\usepackage{multicol}
\usepackage[margin=0.8in]{geometry} % set margin
\usepackage{minted} % code formatting
\usepackage[colorlinks=true,linkcolor=red]{hyperref}
\usepackage{seqsplit} % wrap lines by character
\usepackage{listings} % used to include text file verbatim

\usemintedstyle{vs} % set minted style

\begin{document}
\setlength{\parindent}{0pt} % remove all indents

\begin{multicols}{2}

\subsubsection*{Directories}
\input{dir.tex}

\subsubsection*{Files}
\input{file.tex}

\input{code.tex}

\end{multicols}
\end{document}
"""


# escape some characters for latex
def escape(string):
    string = '\_'.join(string.split('_'))
    return string


# wrap the text with \seqsplit
def seqsplit(string):
    string = string.split('\n')
    for i in range(len(string)):
        if string[i]:
            string[i] = '\\seqsplit{%s}' % string[i]
    return '\n'.join(string)


# wrap the text with \textbf
def textbf(string):
    return '\\textbf{%s}' % string


def main(out_path, code_path, language):
    # make output dir and copy code into it
    os.mkdir(out_path)
    shutil.copytree(code_path, os.path.join(out_path, code_path.strip('/').split('/')[-1]))
    os.chdir(out_path) # change working directory
    code_path = code_path.strip('/').split('/')[-1]

    # parse code directory
    dirs = {}
    files = {}
    for root, _, fnames in os.walk(code_path):
        # skip if it is hidden dir
        if sum([x.startswith('.') for x in root.split('/')]) > 0: continue
        # get dir name
        dname = root.split('/')[-1]
        # get parent path
        parent = '/'.join(root.split('/')[:-1])
        # record directories
        entry = textbf(escape(dname)) + ' \\pageref{' + root + '} ' + seqsplit(escape(parent)) +  '/\n\n'
        dirs[root] = entry
        # record file names, eliminating hidden files
        files[root] = [x for x in fnames if not x.startswith('.')]

    # write dir.tex
    with open('dir.tex', 'w') as f:
        for x in sorted(dirs.keys()):
            f.write(dirs[x])

    # write file.tex
    with open('file.tex', 'w') as f:
        for path in sorted(files.keys()):
            f.write(textbf(escape(path.split('/')[-1])))
            f.write(' \\label{' + path + '}')
            f.write('\n\n')
            for filename in sorted(files[path]):
                f.write(seqsplit('~~' + escape(filename)) + ' \\pageref{' + os.path.join(path, filename) + '}\n\n')

    # write main.tex
    fullpaths = []
    for path in files:
        for filename in files[path]:
            fp = os.path.join(path, filename)
            fullpaths.append(fp)
    fullpaths.sort()
    with open('code.tex', 'w') as f:
        for fp in fullpaths:
            filename = fp.split('/')[-1]
            f.write('\\subsubsection*{%s}\n\\label{%s}\n\\inputminted[fontsize=\scriptsize, breaklines]{%s}{%s}\n' % (escape(filename), fp, language, fp))

    # write main.tex
    with open('main.tex', 'w') as f:
        f.write(MAIN_TEX)
    # shutil.copy2('../resources/main.tex', '.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='copy2pdf')
    parser.add_argument('outpath', help='Path of output')
    parser.add_argument('codepath', help='Path of code')
    parser.add_argument('language', help='Programming language, see https://www.overleaf.com/learn/latex/Code_Highlighting_with_minted for supported languages.')
    args = parser.parse_args()
    main(args.outpath, args.codepath, args.language)
