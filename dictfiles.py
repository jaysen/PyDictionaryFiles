""" dictfiles.py
    version 0.3

    Reads key/value pairs to and from being embedded within
    normal text files.
    Leaves all non key:value text alone / preserves comments and non key:value pairs.
    Processes multiple key:value formats.

    by Jaysen Naidoo
    2014.06.28

    ChangeLog:
    2014.06.28: v0.3 starts with fixes:
        - leaves comments and non key pairs alone.
        - only replaces a line if it contains a keypair and the value has changed
    2006.08.21: fixed update - to properly update the file when a keyword is changed

    TODO: Handle Key:Values in the following formats:
            - [key:value]
            - [key=value]
    TODO: handle multi-line key:value pairs (?)
    TODO: Allow the reading of multiple key:value formats

    TODO: change dictionary to component instead of parent (?)



    # Copyright (C) 2014 Jaysen

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
from UserDict import UserDict
import fileutils as fu


DEFAULTSEPERATOR = ':'


class FileDict(UserDict):

    """ A class that reads and writes dictionary key:values from text files
        Ignores & Preserves comments and non key:value pairs
    """

    filename = './test.txt'
    seperator = DEFAULTSEPERATOR
    raiseErrors = False

    def __init__(self, fname=None, sep=DEFAULTSEPERATOR):
        """ inits the class - by checking filename and reading in dict values
            arguments:
                fname = filename to work with
                sep         : (optional) the separator used in the file (default = ':')
                raiseErrors : (optional) whether or not to raise exceptions (default = False)
        """
        UserDict.__init__(self)
        self.filename = fname
        self.seperator = sep
        self.fileRead()

    def fileRead(self):
        """ reads from file into FileDict
            returns 1 if file exists - else returns 0
        """
        if os.path.exists(self.filename):
            for line in open(self.filename, 'r'):
                splitline = line.split(self.seperator)
                if len(splitline) > 1:
                    self.data[splitline[0].strip()] = splitline[1].strip()
            return 1
        # doesn't exist - so create empty file:
        else:
            f = open(self.filename, 'w')
            f.close()
        return 0

    def fileUpdate(self, keepbackups=True):
        """ updates the file with the contents of the dictionary
            Preserves comments and non key:value pairs

            returns 1 it if succeeds, otherwise 0
        """
        if os.path.exists(self.filename):
            fu.backup(self.filename)

        tempdict = self.data
        templines = []
        for line in fu.readlines(self.filename):
            templine = line
            splitline = templine.split(self.seperator)
            if len(splitline) > 1:
                tempkey = splitline[0].strip()
                tempval = splitline[1].strip()
                if tempkey in self.data:
                    if tempdict[tempkey] == tempval:
                        templines.append(line.strip())
                    else:
                        templines.append('%-20s : %s'.strip() % (tempkey, tempdict[tempkey]))
                    # del existing pairs from tempdict - so you dont repeat them when u append tempdict
                    del tempdict[tempkey]
            else:
                templines.append(line.strip())

        for k in sorted(tempdict.iterkeys()):
            templines.append('%-20s : %s'.strip() % (k, tempdict[k]))
        fu.writelines(self.filename, templines, True)
        if not keepbackups:
            fu.delete(self.filename + '.bak')
        # self.fileRead()

# -----------------------------------------------------------------------------
    def getValue(self, key, raw=False):
        """ Returns the value associated with the key
            Returns NULL if not found
            If Raw=true: get from file.
        """
        if key in self:
            return self.data[key]

    def printDict(self):
        for k, v in sorted(fd.iteritems()):
            print '%-20s : %s' % (k, v)

    def printDictFile(self):
        print("")
        if os.path.exists(self.filename):
            # log('print fd file contents:')
            for l in (fu.readlines(self.filename)):
                print l,


def log(string):
    """ debug/log output """
    print ("******    %s" % string)


if __name__ == "__main__":

    testfile = './test2.txt'
    # TEMP DEBUG - DELETE BEFORE:
    # fu.delete(testfile)

    fd = FileDict(testfile)
    fd.fileRead()

    try:
        if ('read-count' in fd.data.keys() and int(fd.data['read-count']) > 5):
            log("DELETING!!!")
            fu.delete(testfile)
            fd.data.clear()
    except:
        log("readcount failed!!!!!")

    if not os.path.exists(testfile):
        log("create a new dict file")
        newlines = ["TESTING DICTFILES.PY",
                    "- A Script to read and handle Key:Value Pairs embedded files with normal text",
                    "",
                    "read-count :0:fldsjfal",
                    "greetings friendly tester.",
                    "",
                    "c:0",
                    "DD:09",
                    "varA:1",
                    "testWord :       the WORD : a comment ... and another",
                    "and YET another comment",
                    "",
                    "then the END OF FREE TEXT!!!!!!!"]
        fu.writelines(testfile, newlines, True)
        fd.fileRead()

    # log("===================================")
    # log("print the dict file first time!")
    # fd.printDictFile()

    # log("read dict from the file")
    # fd.fileRead()

    log("===================================")
    log("Print the dictionary:")
    fd.printDict()

    log("===================================")
    log("Then change the dict in code ...")

    fd.data['testWord'] = 'the WORD'
    fd['testSentence'] = 'a whole SENTENCE'

    varA, varB = '1', '5'
    readcount = '0'
    try:
        varA = str(int(fd.data['varA']) + 1)
        varB = str(int(fd.data['varB']) + 5)
        readcount = str(int(fd.data['read-count']) + 1)
    except:
        pass
    finally:
        fd.data['varA'] = varA
        fd.data['varB'] = varB
        fd.data['read-count'] = readcount

    fd['DD'] = '10'
    fd['DE'] = '10'
    fd['DD'] = '11'

    # log("print the dictionary BEFORE update:")
    # fd.printDict()

    log("===================================")
    log('now update file from new fd.data:')
    fd.fileUpdate()

    log("print the dictionary AFTER update:")
    fd.printDict()

    print("")
    log('then reprint the FileDict file:')
    fd.printDictFile()
