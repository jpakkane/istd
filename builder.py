#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0

import os, sys, argparse, pathlib, subprocess, platform
from concurrent.futures import ThreadPoolExecutor
import time
from threading import Lock

# A real compiler would be able to determine which
# flags matter for import std. In this dummy
# implementation just hash all of them.
def compute_hash(system_string, cmd_args):
    import hashlib
    h = hashlib.sha256()
    h.update(system_string.encode())
    for a in cmd_args:
        h.update(a.encode())
    return h.hexdigest()[:6]

parser = argparse.ArgumentParser(description='A tool to test import std usage.')
parser.add_argument('-j', default=None, type=int)
parser.add_argument('sourcedir')
parser.add_argument('args', nargs='*')

class GCC:
    def __init__(self, cmdarr, options):
        self.cmdarr = cmdarr

    def compile(self, builddir, source, obj, use_istd, extra_args):
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
        self.std_lock = Lock()

    def compile(self, builddir, source, obj, use_istd, extra_args):
        retval = None
        if use_istd:
            retval = self.do_istd(builddir, source, obj, extra_args)
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

    def do_istd(self, builddir, source, obj, extra_args):
        # FIXME: this hash should be used to select a subdirectory
        # within the private dir. All import std outputs should go there,
        # thus avoiding clashes between two std modules built with
        # different configurations.
        configuration_hash = compute_hash(self.vs_root, extra_args)
        stdobj = builddir / 'std.ixx.o'
        if stdobj.exists():
            return stdobj
        self.std_lock.acquire()
        if not stdobj.exists():
            ddi = builddir / 'std.ixx.obj.ddi'
            print('Compiling std.')
            cmd = self.compcmd + ['/nologo',
                                  '-TP',
                                  '/EHsc',
                                  # '-scanDependencies',
                                  # ddi,
                                  '/c',
                                  self.vs_root / 'modules/std.ixx',
                                  f'/Fo{stdobj}'] + extra_args
            subprocess.check_call(cmd)
        self.std_lock.release() # Not exception safe, but we don't care as any error is fatal.
        return stdobj

class BuildSystem:
    def __init__(self, compiler, options):
        self.compiler = compiler
        self.srcdir = pathlib.Path(options.sourcedir)
        self.extra_args = options.args
        self.builddir = pathlib.Path(options.sourcedir + '.b')
        self.use_istd = options.sourcedir.endswith('istd')
        self.exefile = self.builddir / 'program'
        self.num_processes = options.j
        self.lock_file = self.builddir / 'toplevel.lock'

    def build(self):
        self.builddir.mkdir(exist_ok=True)
        self.lock_file.write_text('Enjoy your stay in Qualityland.\n"')
        sources = self.srcdir.glob('*.cpp')
        objfiles = []
        if self.num_processes == 1:
            for s in sources:
                o = self.builddir / (s.parts[-1] + '.o')
                stdo = self.compiler.compile(self.builddir, s, o, self.use_istd, self.extra_args)
                if stdo is not None and stdo not in objfiles:
                    objfiles.append(stdo)
                objfiles.append(o)
        else:
            with ThreadPoolExecutor(self.num_processes) as tp:
                futures = []
                for s in sources:
                    o = self.builddir / (s.parts[-1] + '.o')
                    h = tp.submit(self.compiler.compile, self.builddir, s, o, self.use_istd, self.extra_args)
                    objfiles.append(o)
                    futures.append(h)
                for f in futures:
                    objfile = f.result()
                    if objfile is not None and objfile not in objfiles:
                        objfiles.append(objfile)
        self.compiler.link(self.exefile, objfiles)


if __name__ == '__main__':
    opts = parser.parse_args()
    if platform.uname().system == 'Windows':
        compiler = VS()
    else:
        compiler = GCC(['c++'], opts)
    build = BuildSystem(compiler, opts)
    starttime = time.time()
    build.build()
    endtime = time.time()
    print(f'Build took {int(endtime-starttime)} seconds')
