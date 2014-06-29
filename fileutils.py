""" fileutils.py
    v1.5
    This module contains convenience functions for working with files and paths.

    Jaysen Naidoo : 2006.01.16
    released subject to GPL, except for functions by Michael Foord # Copyright Michael Foord 2004 (BSD)

    # Copyright (C) 2014  jaysen

    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program. If not, see <http://www.gnu.org/licenses/>.

"""

import os
import sys


# ---file edit functions---#000000#FFFFFF---------------------------------

def editfile(fname, func, keepbackups=True):
    """ Given a filename fname, and a function, editFunc
            performs editFunc on a list of lines from file fname
            and writes to file fname

            Returns 1 if succeeds, else 0
    """
    try:
        if not os.path.isfile(fname):
            writelines(fname, [''])
        renamefile(fname, fname + '.bak')
        flines = readlines(fname + '.bak')
        try:
            newlines = func(flines)
            if newlines is None:
                # TODO: check return type !!!!!
                print 'Error in editfile : the user-specified edit function MUST return a list of strings'
        except Exception, funcErr:
            print 'Error in editfile : the user-specified edit function %s failed \n' % func
            print '%s' % funcErr
            return 0
        writelines(fname, newlines)
        if not keepbackups:
            os.remove(fname + '.bak')
        return 1
    except Exception, editfileErr:
        print 'couldnt edit file %s' % fname
        print '%s' % editfileErr
        return 0


# ---word based functions---#000000#FFFFFF---------------------------------

def wordcount(file):
    """ read a file and count the words. return a dictionary of the words and frequencies"""
    handle = open(file)
    text = handle.read()
    handle.close()

    words = text.split()

    count = dict()
    for word in words:
        if word in count:
            count[word] += 1
        else:
            count[word] = 1
    return count


# ---file line based functions---#000000#FFFFFF---------------------------------


def getlinecount(fname):
    """ Returns number of lines in fname"""
    return len(readlines(fname))


def removelines(fname, L1, L2, bak=True):
    """deletes lines L1 to L2 from fname"""
    editfile(fname, lambda lines: lines[:L1] + lines[L2:], bak)


def addlinenums(fname):
    """ adds line numbers to textfile fname eg. '1. this is the first line' """
    def adnums(lines):
        i = 1
        out = []
        for li in lines:
            out.append('%s. %s' % (i, li))
            i += 1
        return out
    editfile(fname, adnums)


# ---Functions from pathutils---#00FF00#040404-----------------------------------

# ---Functions to read and write files in text and binary mode.---#000000#FFFFFF-

def readlines(filename, createifmissing=True):
    """Passed a filename, it reads it, and returns a list of lines. (Read in text mode)"""
    if os.path.exists(filename):
        filehandle = open(filename, 'r')
        outfile = filehandle.readlines()
        filehandle.close()
        return outfile
    elif createifmissing:
        filehandle = open(filename, 'w')
        filehandle.close()
        return []
    return None


def writelines(filename, infile, newline=False):
    """
    Given a filename and a list of lines it writes the file. (In text mode)
    If newline is True (default is False) it adds a newline to each line.
    Overwrites the existing file if the file exists.
    If the file does not exist, creates a new file.
    """
    filehandle = open(filename, 'w+')
    if newline:
        infile = [line + '\n' for line in infile]
    filehandle.writelines(infile)
    filehandle.close()


def readbinary(filename):
    """Given a filename, read a file in binary mode. It returns a single string."""
    filehandle = open(filename, 'rb')
    thisfile = filehandle.read()
    filehandle.close()
    return thisfile


def writebinary(filename, infile):
    """Given a filename and a string, write the file in binary mode. """
    filehandle = open(filename, 'wb')
    filehandle.write(infile)
    filehandle.close()


def readfile(filename):
    """Given a filename, read a file in text mode. It returns a single string."""
    filehandle = open(filename, 'r')
    outfile = filehandle.read()
    filehandle.close()
    return outfile


def writefile(filename, infile):
    """Given a filename and a string, write the file in text mode."""
    filehandle = open(filename, 'w+')
    filehandle.write(infile)
    filehandle.close()


def printfile(filename):
    """Given a filename print the contents"""
    for l in readlines(filename):
        print l,

# ---Copy, Move, Rename, Delete, Backup Functions---#000000#FFFFFF---------------


def renamefile(old, new, deleteExisting='safe'):
    """ renames file old to new
            Needs to be called with deleteexisting == 'unsafe' to rename if new filename already exists
    """
    if os.path.exists(new):
        if deleteExisting == 'unsafe':
            os.remove(new)
    os.rename(old, new)


def fullcopy(src, dst):
    """
    Copy file from src to dst.

    If the dst directory doesn't exist, we will attempt to create it using makedirs.
    """
    import shutil
    if not os.path.isdir(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))
    shutil.copy(src, dst)


def delete(filename):
    if os.path.exists(filename):
        os.remove(filename)


def backup(filename):
    import shutil
    bakfile = filename + '.bak'
    delete(bakfile)
    # os.rename(filename,bakfile)
    shutil.copy(filename, filename + '.bak')
    return bakfile


# ---Module Helper ---#000000#FFFFFF------------------------------------------------
def import_path(fullpath, strict=True):
    """
    Import a file from the full path. Allows you to import from anywhere,
    something __import__ does not do.

    If strict is True (the default), raise an ImportError if the module
    is found in the "wrong" directory.

    Taken from firedrop2_ by `Hans Nowak`_

    .. _firedrop2: http://www.voidspace.org.uk/python/firedrop2/
    .. _Hans Nowak: http://zephyrfalcon.org
    """
    path, filename = os.path.split(fullpath)
    filename, ext = os.path.splitext(filename)
    sys.path.insert(0, path)
    try:
        module = __import__(filename)
    except ImportError:
        del sys.path[0]
        raise
    del sys.path[0]
    #
    if strict:
        path = os.path.split(module.__file__)[0]
        # FIXME: doesn't *startswith* allow room for errors ?
        if not fullpath.startswith(path):
            raise ImportError, "Module '%s' found, but not in '%s'" % (
                    filename, fullpath)
    #
    return module


# ---main()---#FFFFFF#004080------------------------------------------------------
if __name__ == "__main__":

    f = './test.txt'
    tl = ['why god ,why',
          '++from tombo',
          '....',
          'whyyyyyyyyy   ....',
          'my name is sam',
          '++end of from tombo',
          ' ',
          '',
          '      stilll heeeeerrrreeee.....     '
          ]
    writelines(f, tl, True)
    addlinenums(f)

    printfile(f)
