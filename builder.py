#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0

import os, sys, argparse, pathlib, subprocess

parser = argparse.ArgumentParser(description='A tool to test import std usage.')
parser.add_argument('sourcedir')
parser.add_argument('args', nargs='*')

class GCC:
    def __init__(self, cmdarr, options):
        self.cmdarr = cmdarr

    def compile(self, source, obj, extra_args):
        cmd = self.cmdarr + ['-Wall', '-c', '-o', obj, source] + extra_args
        subprocess.check_call(cmd)

    def link(self, exename, objfiles):
        cmd = self.cmdarr + ['-o', exename] + objfiles
        subprocess.check_call(cmd)

class BuildSystem:
    def __init__(self, compiler, options):
        self.compiler = compiler
        self.srcdir = pathlib.Path(options.sourcedir)
        self.extra_args = options.args
        self.builddir = pathlib.Path(options.sourcedir + '.b')
        self.use_istd = options.sourcedir.endswith('istd')
        self.exefile = self.builddir / 'program'

    def build(self):
        self.builddir.mkdir(exist_ok=True)
        sources = self.srcdir.glob('*.cpp')
        objfiles = []
        for s in sources:
            o = self.builddir / (s.parts[-1] + '.o')
            self.compiler.compile(s, o, self.extra_args)
            objfiles.append(o)
        self.compiler.link(self.exefile, objfiles)


if __name__ == '__main__':
    opts = parser.parse_args()
    compiler = GCC(['c++'], opts)
    build = BuildSystem(compiler, opts)
    build.build()

