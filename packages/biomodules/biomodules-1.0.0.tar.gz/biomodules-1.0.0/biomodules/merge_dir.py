# -*- coding: utf-8 -*-
from pathlib import Path
from shutil import copyfileobj

from okmodule import Module


class MergeDir(Module):
    """
    合并文件夹：给定一个输入文件夹和一个输出文件，把该文件夹下的所有文件合并到该文件中
    indir: 输入文件夹
    outfile: 输出文件
    """
    def __init__(self, indir, outfile):
        if isinstance(indir, str):
            indir = Path(indir)
        self.indir = indir
        if isinstance(outfile, str):
            outfile = Path(outfile)
        self.outfile = outfile

    def main(self):
        with self.outfile.open('wb') as ofp:
            for infile in self.indir.iterdir():
                if not infile.is_file():
                    continue
                with open(infile, 'rb') as ifp:
                    copyfileobj(ifp, ofp)
