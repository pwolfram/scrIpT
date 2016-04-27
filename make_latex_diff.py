#!/usr/bin/env python
"""
Script to obtain and build latex difference for a file under git version
control with output to pdf.

Phillip J. Wolfram
04/27/2016
"""
import os.path
import shlex
import subprocess as sp

def rmtrash(afile):
    if os.path.isfile(afile):
        from send2trash import send2trash
        # pip -v install git+ssh://git@github.com/hsoft/send2trash
        send2trash(afile)

def highlight_output(txt):
    print '================================================================================'
    print txt
    print '================================================================================'

def redirect_cmd_to_file(cmd, outfile):
    highlight_output('Running command: \n' + cmd + ' > ' + outfile)
    assert not os.path.isfile(outfile), 'File ' + outfile + ' already exists!'
    with open(outfile, 'w') as ofile:
        sp.call(shlex.split(cmd), stdout=ofile)

def run_cmd(cmd):
    highlight_output('Running command: \n' + cmd)
    try:
        proc = sp.check_output(shlex.split(cmd), stderr=sp.STDOUT)
    except sp.CalledProcessError:
        # There was an error - command exited with non-zero code
        print proc

def make_diff_pdf(githash, afile, basefile, difffile):

    # get previous file based on hash
    cmd = 'git show ' + githash + ':' + afile
    redirect_cmd_to_file(cmd, basefile)

    # get latex diff'd file
    cmd = 'latexdiff --append-context2cmd="abstract" ' + basefile + ' ' + afile
    redirect_cmd_to_file(cmd, difffile)

    # make pdf from file
    cmd = 'pdflatex ' + difffile
    run_cmd(cmd)
    highlight_output('Built pdf for latex difference: ' + difffile.replace('tex', 'pdf'))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-l", "--githash", dest="githash",
            help="git hash from log for difference")
    parser.add_argument("-f", "--file", dest="afile",
            help="latex file that should be differenced")
    parser.add_argument("-b", "--basefile", dest="basefile", default='base.tex',
            help="Filename for hashed file retrieved from repo")
    parser.add_argument("-o", "--outfile", dest="outfile", default='diff.tex',
            help="Name of file to save result from 'latexdiff'")
    parser.add_argument("-c", "--clean", dest='clean', action='store_true',
            help="Overwrite existing basefile and outfiles," \
                    + "defaults of base.texi and diff.tex")
    parser.set_defaults(clean=False)

    args = parser.parse_args()

    if args.githash is None:
        parser.error('Must specify githash')
    if args.afile is None:
        parser.error('Must file for comparison')
    if args.clean:
        rmtrash(args.basefile)
        rmtrash(args.outfile)

    make_diff_pdf(args.githash, args.afile, args.basefile, args.outfile)

# vim: foldmethod=marker ai ts=4 sts=4 et sw=4 ft=python
