#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0

import os, sys, argparse, pathlib, subprocess, platform
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description='A tool to test import std usage.')
parser.add_argument('sourcedir')
parser.add_argument('args', nargs='*')

class GCC:
    def __init__(self, cmdarr, options):
        self.cmdarr = cmdarr

    def compile(self, source, obj, use_istd, extra_args):
        if use_istd:
            sys.exit('Import std not supported for GCC yet.')
        cmd = self.cmdarr + ['-Wall', '-c', '-o', obj, source] + extra_args
        subprocess.check_call(cmd)

    def link(self, exename, objfiles):
        cmd = self.cmdarr + ['-o', exename] + objfiles
        subprocess.check_call(cmd)

class VS:
    def __init__(self):
        self.compcmd = ['cl']
        self.linkcmd = ['link']
        self.vs_root = pathlib.WindowsPath(r'C:\Program Files\Microsoft Visual Studio\2022\Preview\VC\Tools\MSVC\14.43.34604')

    def compile(self, source, obj, use_istd, extra_args):
        retval = None
        if use_istd:
            retval = self.do_istd(source, obj, extra_args)
            cmd = self.compcmd + ['/nologo',
                                  '/c',
                                  f'/Fo{obj}',
                                  '/EHsc',
                                  source] + extra_args
        else:
            cmd = self.compcmd + ['/nologo',
                                  '/c',
                                  f'/Fo{obj}',
                                  '/EHsc',
                                  source] + extra_args
        subprocess.check_call(cmd)
        return retval

    def link(self, exename, objfiles):
        exename = exename.with_suffix('.exe')
        cmd = self.linkcmd + ['/nologo',
                              f'/OUT:{exename}',
                              '/SUBSYSTEM:CONSOLE'] + objfiles
        subprocess.check_call(cmd)

    def do_istd(self, source, obj, extra_args):
        builddir = pathlib.WindowsPath(obj.parts[0])
        stdobj = builddir / 'std.ixx.o'
        if stdobj.exists():
            return stdobj
        ddi = builddir / 'std.ixx.obj.ddi'
        cmd = self.compcmd + ['/nologo',
                              '-TP',
                              '/EHsc',
#                              '-scanDependencies',
#                              ddi,
                              '/c',
                              self.vs_root / 'modules/std.ixx',
                              f'/Fo{stdobj}'] + extra_args
        subprocess.check_call(cmd)
        return stdobj

class BuildSystem:
    def __init__(self, compiler, options):
        self.compiler = compiler
        self.srcdir = pathlib.Path(options.sourcedir)
        self.extra_args = options.args
        self.builddir = pathlib.Path(options.sourcedir + '.b')
        self.use_istd = options.sourcedir.endswith('istd')
        self.exefile = self.builddir / 'program'
        self.num_processes = 1

    def build(self):
        self.builddir.mkdir(exist_ok=True)
        sources = self.srcdir.glob('*.cpp')
        objfiles = []
        if self.num_processes == 1:
            for s in sources:
                o = self.builddir / (s.parts[-1] + '.o')
                stdo = self.compiler.compile(s, o, self.use_istd, self.extra_args)
                if stdo is not None and stdo not in objfiles:
                    objfiles.append(stdo)
                objfiles.append(o)
        else:
            with ThreadPoolExecutor(self.num_processes) as tp:
                futures = []
                for s in sources:
                    o = self.builddir / (s.parts[-1] + '.o')
                    h = tp.submit(self.compiler.compile, s, o, self.use_istd, self.extra_args)
                    objfiles.append(o)
                    futures.append(h)
                for f in futures:
                    f.result()
        self.compiler.link(self.exefile, objfiles)


if __name__ == '__main__':
    opts = parser.parse_args()
    if platform.uname().system == 'Windows':
        compiler = VS()
    else:
        compiler = GCC(['c++'], opts)
    build = BuildSystem(compiler, opts)
    build.build()
